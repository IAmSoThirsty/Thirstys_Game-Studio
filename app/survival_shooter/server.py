"""
Main game server implementation.
Server-authoritative game state with real-time updates to clients.
"""
import asyncio
import logging
from typing import Dict, Optional
from dataclasses import asdict

from .entities import GameState, Player, Squad, Vector2
from .systems import WaveManager, ZoneManager
from .network import NetworkManager, NetworkMessage, MatchmakingManager
from .config import GameConfig, PLAYER_CLASSES


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GameServer:
    """
    Main game server managing game state and player connections.
    Implements server-authoritative architecture for cheat prevention.
    """
    
    def __init__(self, config: Optional[GameConfig] = None):
        self.config = config or GameConfig()
        self.game_state = GameState()
        
        # Managers
        self.network = NetworkManager(is_server=True)
        self.wave_manager = WaveManager(self.game_state)
        self.zone_manager = ZoneManager(self.game_state)
        self.matchmaking = MatchmakingManager()
        
        # Player sessions
        self.player_sessions: Dict[str, str] = {}  # session_id -> player_id
        self.squads: Dict[str, Squad] = {}
        
        # Server state
        self.running = False
        self.tick_rate = self.config.TICK_RATE
        self.tick_duration = 1.0 / self.tick_rate
        
        # Register network handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register network message handlers."""
        self.network.register_handler(
            NetworkMessage.PLAYER_JOIN, 
            self._handle_player_join
        )
        self.network.register_handler(
            NetworkMessage.PLAYER_LEAVE,
            self._handle_player_leave
        )
        self.network.register_handler(
            NetworkMessage.PLAYER_INPUT,
            self._handle_player_input
        )
    
    async def start(self, host: str = "0.0.0.0", port: int = 8765):
        """Start the game server."""
        logger.info(f"Starting game server on {host}:{port}")
        
        # Start network server
        await self.network.start_server(host, port)
        
        # Start game loop
        self.running = True
        await self._game_loop()
    
    async def stop(self):
        """Stop the game server."""
        logger.info("Stopping game server")
        self.running = False
    
    async def _game_loop(self):
        """Main server game loop running at fixed tick rate."""
        last_time = asyncio.get_event_loop().time()
        
        while self.running:
            current_time = asyncio.get_event_loop().time()
            delta_time = current_time - last_time
            last_time = current_time
            
            # Update game state
            await self._update(delta_time)
            
            # Broadcast state to clients
            await self._broadcast_state()
            
            # Sleep to maintain tick rate
            sleep_time = max(0, self.tick_duration - (asyncio.get_event_loop().time() - current_time))
            await asyncio.sleep(sleep_time)
    
    async def _update(self, delta_time: float):
        """Update all game systems."""
        self.game_state.delta_time = delta_time
        self.game_state.game_time += delta_time
        
        # Update managers
        self.wave_manager.update(delta_time)
        self.zone_manager.update(delta_time)
        
        # Update player states
        for player in self.game_state.players.values():
            if not player.is_alive and player.respawn_timer > 0:
                player.respawn_timer -= delta_time
                if player.respawn_timer <= 0:
                    await self._respawn_player(player.id)
        
        # Update AI (simplified)
        await self._update_enemy_ai(delta_time)
        
        # Update projectiles
        await self._update_projectiles(delta_time)
    
    async def _update_enemy_ai(self, delta_time: float):
        """Update enemy AI behaviors."""
        for enemy in list(self.game_state.enemies.values()):
            # Find nearest player
            nearest_player = self._find_nearest_player(enemy.position)
            
            if nearest_player:
                distance = enemy.position.distance_to(nearest_player.position)
                
                if distance <= enemy.aggro_range:
                    enemy.target_player_id = nearest_player.id
                    enemy.ai_state = "chase"
                    
                    # Move towards player
                    direction = Vector2(
                        nearest_player.position.x - enemy.position.x,
                        nearest_player.position.y - enemy.position.y
                    ).normalize()
                    
                    enemy.position.x += direction.x * enemy.speed * delta_time
                    enemy.position.y += direction.y * enemy.speed * delta_time
                    
                    # Attack if in range
                    if distance <= enemy.attack_range:
                        enemy.ai_state = "attack"
                        await self._enemy_attack(enemy, nearest_player)
    
    async def _update_projectiles(self, delta_time: float):
        """Update projectile positions and collisions."""
        for projectile in list(self.game_state.projectiles.values()):
            # Update position
            projectile.position.x += projectile.velocity.x * delta_time
            projectile.position.y += projectile.velocity.y * delta_time
            
            # Update lifetime
            projectile.lifetime -= delta_time
            if projectile.lifetime <= 0:
                del self.game_state.projectiles[projectile.id]
                continue
            
            # Check collisions with enemies
            for enemy in list(self.game_state.enemies.values()):
                distance = projectile.position.distance_to(enemy.position)
                if distance < 30.0:  # Hit radius
                    await self._damage_enemy(enemy.id, projectile.damage)
                    
                    if not projectile.piercing:
                        del self.game_state.projectiles[projectile.id]
                    break
    
    async def _enemy_attack(self, enemy, player: Player):
        """Enemy attacks player."""
        # Simple attack cooldown (would be more sophisticated in production)
        damage = enemy.damage
        
        player.health -= damage
        
        if player.health <= 0:
            player.is_alive = False
            player.respawn_timer = self.config.RESPAWN_TIME
            
            # Notify clients
            message = NetworkMessage(NetworkMessage.DAMAGE_DEALT, {
                "target_type": "player",
                "target_id": player.id,
                "damage": damage,
                "is_death": True
            })
            await self.network.broadcast(message)
    
    async def _damage_enemy(self, enemy_id: str, damage: float):
        """Apply damage to enemy."""
        enemy = self.game_state.enemies.get(enemy_id)
        if not enemy:
            return
        
        enemy.health -= damage
        
        if enemy.health <= 0:
            # Enemy died
            await self._enemy_died(enemy)
    
    async def _enemy_died(self, enemy):
        """Handle enemy death."""
        # Remove from game state
        if enemy.id in self.game_state.enemies:
            del self.game_state.enemies[enemy.id]
        
        self.game_state.enemies_remaining -= 1
        
        # Reward player who had it as target
        # (In full implementation, track damage dealers)
        
        # Notify clients
        message = NetworkMessage(NetworkMessage.ENEMY_DEATH, {
            "enemy_id": enemy.id,
            "currency_drop": enemy.currency_drop,
            "experience_drop": enemy.experience_drop
        })
        await self.network.broadcast(message)
    
    async def _respawn_player(self, player_id: str):
        """Respawn a player."""
        player = self.game_state.players.get(player_id)
        if not player:
            return
        
        player.is_alive = True
        player.health = player.max_health
        
        # Spawn at active zone
        active_zone = self.zone_manager._get_active_zone()
        if active_zone:
            player.position = Vector2(active_zone.position.x, active_zone.position.y)
        
        # Notify clients
        message = NetworkMessage(NetworkMessage.PLAYER_RESPAWN, {
            "player_id": player_id,
            "position": {"x": player.position.x, "y": player.position.y}
        })
        await self.network.broadcast(message)
    
    def _find_nearest_player(self, position: Vector2) -> Optional[Player]:
        """Find nearest alive player to position."""
        nearest = None
        min_distance = float('inf')
        
        for player in self.game_state.players.values():
            if not player.is_alive:
                continue
            
            distance = position.distance_to(player.position)
            if distance < min_distance:
                min_distance = distance
                nearest = player
        
        return nearest
    
    async def _broadcast_state(self):
        """Broadcast game state to all clients."""
        # In production, use delta compression and only send changes
        # For now, send simplified state
        
        state_data = {
            "game_time": self.game_state.game_time,
            "current_wave": self.game_state.current_wave,
            "wave_active": self.game_state.wave_active,
            "player_count": len(self.game_state.players),
            "enemy_count": len(self.game_state.enemies),
            "active_zone_id": self.game_state.active_zone_id,
        }
        
        message = NetworkMessage(NetworkMessage.GAME_STATE, state_data)
        await self.network.broadcast(message)
    
    async def _handle_player_join(self, session_id: str, data: Dict):
        """Handle player joining."""
        player_name = data.get("name", f"Player{len(self.game_state.players) + 1}")
        player_class = data.get("class", "commando")
        
        # Validate player class
        if player_class not in PLAYER_CLASSES:
            player_class = "commando"
        
        class_config = PLAYER_CLASSES[player_class]
        
        # Create player
        player = Player(
            name=player_name,
            player_class=player_class,
            max_health=class_config.base_health,
            health=class_config.base_health,
            session_id=session_id,
        )
        
        # Add to game state
        self.game_state.players[player.id] = player
        self.player_sessions[session_id] = player.id
        
        logger.info(f"Player {player_name} ({player_class}) joined: {player.id}")
        
        # Send welcome message
        welcome_data = {
            "player_id": player.id,
            "game_state": "active",
            "config": {
                "tick_rate": self.tick_rate,
                "zone_count": len(self.game_state.zones),
            }
        }
        
        message = NetworkMessage("welcome", welcome_data)
        await self.network.send_to_client(session_id, message)
    
    async def _handle_player_leave(self, session_id: str, data: Dict):
        """Handle player leaving."""
        player_id = self.player_sessions.get(session_id)
        if not player_id:
            return
        
        player = self.game_state.players.get(player_id)
        if player:
            logger.info(f"Player {player.name} left: {player_id}")
            del self.game_state.players[player_id]
        
        if session_id in self.player_sessions:
            del self.player_sessions[session_id]
    
    async def _handle_player_input(self, session_id: str, data: Dict):
        """Handle player input."""
        player_id = self.player_sessions.get(session_id)
        if not player_id:
            return
        
        player = self.game_state.players.get(player_id)
        if not player or not player.is_alive:
            return
        
        # Process input (movement, shooting, abilities)
        input_type = data.get("type")
        
        if input_type == "move":
            # Update player position
            direction = data.get("direction", {"x": 0, "y": 0})
            speed = self.config.PLAYER_SPEED * player.speed_multiplier
            
            player.position.x += direction["x"] * speed * self.game_state.delta_time
            player.position.y += direction["y"] * speed * self.game_state.delta_time
        
        elif input_type == "shoot":
            # Create projectile
            # (Simplified - would validate, add cooldowns, etc.)
            pass
        
        elif input_type == "ability":
            # Use ability
            # (Would implement ability system)
            pass


async def main():
    """Main entry point for game server."""
    config = GameConfig()
    server = GameServer(config)
    
    try:
        await server.start(host="0.0.0.0", port=config.SERVER_PORT)
    except KeyboardInterrupt:
        logger.info("Server interrupted")
    finally:
        await server.stop()


if __name__ == "__main__":
    asyncio.run(main())
