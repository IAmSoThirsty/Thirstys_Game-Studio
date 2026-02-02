"""
Wave management system for spawning and controlling enemy waves.
"""
from typing import List, Dict, Optional
import random
import math

from .entities import Enemy, Vector2, GameState, Zone
from .config import ZONES


class WaveManager:
    """Manages wave-based enemy spawning and difficulty scaling."""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.current_wave = 1
        self.wave_active = False
        self.wave_cooldown = 30.0  # Seconds between waves
        self.wave_timer = 0.0
        
        # Difficulty scaling
        self.base_enemy_count = 10
        self.enemy_count_per_wave = 5
        self.base_enemy_health = 50.0
        self.health_scale_per_wave = 1.15
        
        # Enemy type distribution
        self.enemy_type_weights = {
            "basic": 0.5,
            "fast": 0.2,
            "tank": 0.15,
            "ranged": 0.15,
        }
    
    def update(self, delta_time: float):
        """Update wave state."""
        self.wave_timer += delta_time
        
        if not self.wave_active:
            # Check if it's time to start next wave
            if self.wave_timer >= self.wave_cooldown:
                self.start_wave()
        else:
            # Check if wave is complete
            if self.game_state.enemies_remaining <= 0:
                self.complete_wave()
    
    def start_wave(self):
        """Start a new wave."""
        self.current_wave += 1
        self.wave_active = True
        self.wave_timer = 0.0
        self.game_state.current_wave = self.current_wave
        self.game_state.wave_active = True
        
        # Calculate wave difficulty
        enemy_count = self.base_enemy_count + (self.current_wave * self.enemy_count_per_wave)
        difficulty_multiplier = 1.0 + (self.current_wave * 0.1)
        
        # Get active zone for spawning
        active_zone = self._get_active_zone()
        if not active_zone:
            return
        
        # Spawn enemies
        self._spawn_wave_enemies(enemy_count, difficulty_multiplier, active_zone)
        
        self.game_state.enemies_remaining = enemy_count
    
    def complete_wave(self):
        """Complete the current wave."""
        self.wave_active = False
        self.game_state.wave_active = False
        self.wave_timer = 0.0
        
        # Reward players
        self._reward_players()
    
    def _spawn_wave_enemies(self, count: int, difficulty: float, zone: Zone):
        """Spawn enemies for the wave."""
        for i in range(count):
            enemy_type = self._select_enemy_type()
            enemy = self._create_enemy(enemy_type, difficulty, zone)
            self.game_state.enemies[enemy.id] = enemy
    
    def _select_enemy_type(self) -> str:
        """Select enemy type based on wave and weights."""
        types = list(self.enemy_type_weights.keys())
        weights = list(self.enemy_type_weights.values())
        return random.choices(types, weights=weights, k=1)[0]
    
    def _create_enemy(self, enemy_type: str, difficulty: float, zone: Zone) -> Enemy:
        """Create an enemy entity."""
        # Base stats
        health = self.base_enemy_health * (self.health_scale_per_wave ** self.current_wave)
        
        # Type-specific modifications
        type_mods = {
            "basic": {"health": 1.0, "damage": 1.0, "speed": 1.0},
            "fast": {"health": 0.7, "damage": 0.8, "speed": 1.5},
            "tank": {"health": 2.0, "damage": 1.2, "speed": 0.6},
            "ranged": {"health": 0.8, "damage": 1.3, "speed": 0.9},
        }
        
        mods = type_mods.get(enemy_type, type_mods["basic"])
        
        # Spawn position (around zone perimeter)
        spawn_pos = self._get_spawn_position(zone)
        
        enemy = Enemy(
            enemy_type=enemy_type,
            position=spawn_pos,
            health=health * mods["health"] * difficulty,
            max_health=health * mods["health"] * difficulty,
            damage=10.0 * mods["damage"] * difficulty,
            speed=150.0 * mods["speed"],
            wave_number=self.current_wave,
            difficulty_scaling=difficulty,
            currency_drop=int(10 * difficulty),
            experience_drop=int(25 * difficulty),
        )
        
        return enemy
    
    def _get_spawn_position(self, zone: Zone) -> Vector2:
        """Get random spawn position around zone."""
        angle = random.uniform(0, 2 * math.pi)
        distance = zone.radius + random.uniform(200, 400)
        
        x = zone.position.x + math.cos(angle) * distance
        y = zone.position.y + math.sin(angle) * distance
        
        return Vector2(x, y)
    
    def _get_active_zone(self) -> Optional[Zone]:
        """Get the currently active zone."""
        if self.game_state.active_zone_id:
            return self.game_state.zones.get(self.game_state.active_zone_id)
        return None
    
    def _reward_players(self):
        """Reward all players for completing wave."""
        base_currency = 50
        base_experience = 100
        
        wave_bonus = self.current_wave * 10
        
        for player in self.game_state.players.values():
            if player.is_alive:
                player.currency += base_currency + wave_bonus
                player.experience += base_experience + wave_bonus


class ZoneManager:
    """Manages zone control and rotation."""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.rotation_interval = 120.0  # 2 minutes
        self.rotation_timer = 0.0
        self.hold_time_required = 60.0  # 1 minute
        
        # Initialize zones
        self._initialize_zones()
    
    def _initialize_zones(self):
        """Create zones from config."""
        for i, zone_config in enumerate(ZONES):
            # Distribute zones across map
            angle = (2 * math.pi * i) / len(ZONES)
            distance = 2000.0  # Distance from center
            
            x = math.cos(angle) * distance
            y = math.sin(angle) * distance
            
            zone = Zone(
                name=zone_config.name,
                theme=zone_config.theme,
                position=Vector2(x, y),
                radius=300.0,
                difficulty_multiplier=zone_config.difficulty_multiplier,
                enemy_spawn_rate=zone_config.difficulty_multiplier,
            )
            
            self.game_state.zones[zone.id] = zone
        
        # Activate first zone
        if self.game_state.zones:
            first_zone = list(self.game_state.zones.values())[0]
            self._activate_zone(first_zone.id)
    
    def update(self, delta_time: float):
        """Update zone state."""
        self.rotation_timer += delta_time
        
        # Get active zone
        active_zone = self._get_active_zone()
        if not active_zone:
            return
        
        # Update zone hold progress
        self._update_zone_progress(active_zone, delta_time)
        
        # Check for zone rotation
        if self.rotation_timer >= self.rotation_interval:
            self._rotate_zone()
    
    def _update_zone_progress(self, zone: Zone, delta_time: float):
        """Update hold progress for zone."""
        # Count players in zone
        players_in_zone = self._count_players_in_zone(zone)
        zone.players_in_zone = players_in_zone
        
        if len(players_in_zone) >= zone.required_players:
            # Progress increases when enough players are in zone
            progress_rate = 1.0 / self.hold_time_required
            zone.hold_progress = min(1.0, zone.hold_progress + (progress_rate * delta_time))
            
            # Update player states
            for player_id in players_in_zone:
                player = self.game_state.players.get(player_id)
                if player:
                    player.is_in_zone = True
        else:
            # Progress decreases when not enough players
            decay_rate = 0.5 / self.hold_time_required
            zone.hold_progress = max(0.0, zone.hold_progress - (decay_rate * delta_time))
            
            # Update all player states
            for player in self.game_state.players.values():
                if player.id not in players_in_zone:
                    player.is_in_zone = False
    
    def _count_players_in_zone(self, zone: Zone) -> List[str]:
        """Count alive players within zone radius."""
        players_in_zone = []
        
        for player in self.game_state.players.values():
            if not player.is_alive:
                continue
            
            distance = player.position.distance_to(zone.position)
            if distance <= zone.radius:
                players_in_zone.append(player.id)
        
        return players_in_zone
    
    def _rotate_zone(self):
        """Rotate to next zone."""
        self.rotation_timer = 0.0
        
        # Get all zone IDs
        zone_ids = list(self.game_state.zones.keys())
        if not zone_ids:
            return
        
        # Find current active zone index
        current_index = 0
        if self.game_state.active_zone_id:
            try:
                current_index = zone_ids.index(self.game_state.active_zone_id)
            except ValueError:
                pass
        
        # Move to next zone
        next_index = (current_index + 1) % len(zone_ids)
        next_zone_id = zone_ids[next_index]
        
        self._activate_zone(next_zone_id)
    
    def _activate_zone(self, zone_id: str):
        """Activate a specific zone."""
        # Deactivate all zones
        for zone in self.game_state.zones.values():
            zone.is_active = False
            zone.hold_progress = 0.0
        
        # Activate selected zone
        zone = self.game_state.zones.get(zone_id)
        if zone:
            zone.is_active = True
            self.game_state.active_zone_id = zone_id
    
    def _get_active_zone(self) -> Optional[Zone]:
        """Get currently active zone."""
        if self.game_state.active_zone_id:
            return self.game_state.zones.get(self.game_state.active_zone_id)
        return None
