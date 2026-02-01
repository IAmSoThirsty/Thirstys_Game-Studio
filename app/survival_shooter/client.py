"""
Client-side game with UI rendering and input handling.
Connects to game server for multiplayer functionality.
"""
import asyncio
import logging
from typing import Optional, Dict
import sys

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

from .entities import Player, Vector2
from .network import NetworkManager, NetworkMessage
from .config import GameConfig, PLAYER_CLASSES, ZONES


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GameClient:
    """
    Client-side game implementation with rendering and input handling.
    """
    
    def __init__(self, player_name: str = "Player", player_class: str = "commando"):
        self.config = GameConfig()
        self.player_name = player_name
        self.player_class = player_class
        
        # Network
        self.network = NetworkManager(is_server=False)
        self.connected = False
        self.player_id: Optional[str] = None
        
        # Local game state (client predictions)
        self.local_player: Optional[Player] = None
        self.players: Dict[str, Player] = {}
        self.enemies: Dict[str, Dict] = {}
        self.zones: Dict[str, Dict] = {}
        
        # UI state
        self.screen_width = 1280
        self.screen_height = 720
        self.camera_x = 0.0
        self.camera_y = 0.0
        
        # Input state
        self.keys_pressed = set()
        self.mouse_pos = (0, 0)
        self.mouse_buttons = (False, False, False)
        
        # Rendering
        if PYGAME_AVAILABLE:
            pygame.init()
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            pygame.display.set_caption("Thirsty's Survival Shooter")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 24)
            self.font_large = pygame.font.Font(None, 48)
        else:
            self.screen = None
        
        # Register handlers
        self._register_handlers()
        
        # Game state
        self.running = False
        self.target_fps = 60
    
    def _register_handlers(self):
        """Register network message handlers."""
        self.network.register_handler("welcome", self._handle_welcome)
        self.network.register_handler(NetworkMessage.GAME_STATE, self._handle_game_state)
        self.network.register_handler(NetworkMessage.PLAYER_STATE, self._handle_player_state)
        self.network.register_handler(NetworkMessage.ENEMY_SPAWN, self._handle_enemy_spawn)
        self.network.register_handler(NetworkMessage.ENEMY_DEATH, self._handle_enemy_death)
    
    async def connect(self, server_url: str = "ws://localhost:8765"):
        """Connect to game server."""
        logger.info(f"Connecting to server: {server_url}")
        
        try:
            await self.network.connect_client(server_url)
            self.connected = True
            
            # Send join request
            join_data = {
                "name": self.player_name,
                "class": self.player_class
            }
            message = NetworkMessage(NetworkMessage.PLAYER_JOIN, join_data)
            await self.network.send_to_server(message)
            
            logger.info("Connected to server")
        
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            self.connected = False
    
    async def _handle_welcome(self, client_id: str, data: Dict):
        """Handle welcome message from server."""
        self.player_id = data.get("player_id")
        logger.info(f"Received player ID: {self.player_id}")
        
        # Create local player
        class_config = PLAYER_CLASSES[self.player_class]
        self.local_player = Player(
            id=self.player_id,
            name=self.player_name,
            player_class=self.player_class,
            max_health=class_config.base_health,
            health=class_config.base_health,
        )
    
    async def _handle_game_state(self, client_id: str, data: Dict):
        """Handle game state update from server."""
        # Update game state (simplified)
        pass
    
    async def _handle_player_state(self, client_id: str, data: Dict):
        """Handle player state update."""
        pass
    
    async def _handle_enemy_spawn(self, client_id: str, data: Dict):
        """Handle enemy spawn."""
        enemy_id = data.get("enemy_id")
        if enemy_id:
            self.enemies[enemy_id] = data
    
    async def _handle_enemy_death(self, client_id: str, data: Dict):
        """Handle enemy death."""
        enemy_id = data.get("enemy_id")
        if enemy_id in self.enemies:
            del self.enemies[enemy_id]
    
    def run(self):
        """Run the game client."""
        if not PYGAME_AVAILABLE:
            logger.error("Pygame not available - cannot run client")
            return
        
        self.running = True
        
        # Create async loop for networking
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Main game loop
        while self.running:
            delta_time = self.clock.tick(self.target_fps) / 1000.0
            
            # Handle events
            self._handle_events()
            
            # Update
            self._update(delta_time)
            
            # Render
            self._render()
        
        pygame.quit()
    
    def _handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                
                # Quit on ESC
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_buttons = pygame.mouse.get_pressed()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_buttons = pygame.mouse.get_pressed()
        
        self.mouse_pos = pygame.mouse.get_pos()
    
    def _update(self, delta_time: float):
        """Update game state."""
        if not self.local_player or not self.connected:
            return
        
        # Process input and send to server
        direction = Vector2(0, 0)
        
        if pygame.K_w in self.keys_pressed or pygame.K_UP in self.keys_pressed:
            direction.y -= 1
        if pygame.K_s in self.keys_pressed or pygame.K_DOWN in self.keys_pressed:
            direction.y += 1
        if pygame.K_a in self.keys_pressed or pygame.K_LEFT in self.keys_pressed:
            direction.x -= 1
        if pygame.K_d in self.keys_pressed or pygame.K_RIGHT in self.keys_pressed:
            direction.x += 1
        
        # Normalize diagonal movement
        if direction.x != 0 or direction.y != 0:
            direction = direction.normalize()
            
            # Send input to server
            input_message = NetworkMessage(NetworkMessage.PLAYER_INPUT, {
                "type": "move",
                "direction": {"x": direction.x, "y": direction.y}
            })
            
            # Client prediction - update local position
            speed = self.config.PLAYER_SPEED
            self.local_player.position.x += direction.x * speed * delta_time
            self.local_player.position.y += direction.y * speed * delta_time
            
            # Update camera to follow player
            self.camera_x = self.local_player.position.x - self.screen_width / 2
            self.camera_y = self.local_player.position.y - self.screen_height / 2
        
        # Shooting
        if self.mouse_buttons[0]:  # Left click
            # Send shoot input
            pass
    
    def _render(self):
        """Render game."""
        # Clear screen
        self.screen.fill((20, 20, 30))
        
        if not self.local_player:
            # Show connecting screen
            text = self.font_large.render("Connecting to server...", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(text, text_rect)
        else:
            # Render game world
            self._render_world()
            self._render_ui()
        
        pygame.display.flip()
    
    def _render_world(self):
        """Render game world."""
        # Draw zones (simplified)
        for zone in ZONES:
            zone_x = 400 + ZONES.index(zone) * 100 - self.camera_x
            zone_y = 300 - self.camera_y
            
            pygame.draw.circle(self.screen, (100, 100, 150), (int(zone_x), int(zone_y)), 50, 2)
            
            zone_text = self.font.render(zone.name, True, (200, 200, 200))
            self.screen.blit(zone_text, (zone_x - 40, zone_y - 70))
        
        # Draw player
        if self.local_player:
            player_screen_x = self.screen_width // 2
            player_screen_y = self.screen_height // 2
            
            # Player circle
            pygame.draw.circle(self.screen, (50, 200, 50), (player_screen_x, player_screen_y), 20)
            
            # Player name
            name_text = self.font.render(self.local_player.name, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(player_screen_x, player_screen_y - 30))
            self.screen.blit(name_text, name_rect)
        
        # Draw enemies (simplified)
        for enemy_id, enemy_data in self.enemies.items():
            enemy_x = 500 - self.camera_x
            enemy_y = 300 - self.camera_y
            pygame.draw.circle(self.screen, (200, 50, 50), (int(enemy_x), int(enemy_y)), 15)
    
    def _render_ui(self):
        """Render UI overlay."""
        if not self.local_player:
            return
        
        # Health bar
        health_percent = self.local_player.health / self.local_player.max_health
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 10
        
        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (200, 50, 50), (bar_x, bar_y, int(bar_width * health_percent), bar_height))
        
        health_text = self.font.render(f"HP: {int(self.local_player.health)}/{int(self.local_player.max_health)}", True, (255, 255, 255))
        self.screen.blit(health_text, (bar_x + 5, bar_y + 2))
        
        # Class
        class_text = self.font.render(f"Class: {self.local_player.player_class.title()}", True, (255, 255, 255))
        self.screen.blit(class_text, (10, 40))
        
        # Controls
        controls = [
            "Controls:",
            "WASD/Arrows - Move",
            "Mouse - Aim",
            "Left Click - Shoot",
            "ESC - Quit"
        ]
        
        for i, control in enumerate(controls):
            text = self.font.render(control, True, (150, 150, 150))
            self.screen.blit(text, (10, self.screen_height - 120 + i * 20))
        
        # Position debug
        pos_text = self.font.render(f"Pos: ({int(self.local_player.position.x)}, {int(self.local_player.position.y)})", True, (150, 150, 150))
        self.screen.blit(pos_text, (self.screen_width - 200, 10))
        
        # FPS
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (150, 150, 150))
        self.screen.blit(fps_text, (self.screen_width - 200, 35))


def main():
    """Main entry point for client."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Survival Shooter Game Client")
    parser.add_argument("--name", type=str, default="Player", help="Player name")
    parser.add_argument("--class", type=str, dest="player_class", default="commando", 
                       choices=["mage", "commando", "dimension_runner", "biotech_paladin"],
                       help="Player class")
    parser.add_argument("--server", type=str, default="ws://localhost:8765", help="Server URL")
    
    args = parser.parse_args()
    
    client = GameClient(player_name=args.name, player_class=args.player_class)
    
    # Connect in background
    # In production, would properly integrate async networking with pygame
    # For now, showing the structure
    
    logger.info(f"Starting client as {args.name} ({args.player_class})")
    client.run()


if __name__ == "__main__":
    main()
