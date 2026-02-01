"""
Core game entities for survival shooter.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import uuid


class EntityType(Enum):
    """Types of game entities."""
    PLAYER = "player"
    ENEMY = "enemy"
    PROJECTILE = "projectile"
    PICKUP = "pickup"
    ZONE = "zone"
    BUS = "bus"


@dataclass
class Vector2:
    """2D vector for position and movement."""
    x: float = 0.0
    y: float = 0.0
    
    def distance_to(self, other: 'Vector2') -> float:
        """Calculate distance to another vector."""
        import math
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def normalize(self) -> 'Vector2':
        """Return normalized vector."""
        import math
        length = math.sqrt(self.x ** 2 + self.y ** 2)
        if length > 0:
            return Vector2(self.x / length, self.y / length)
        return Vector2(0, 0)


@dataclass
class Player:
    """Player entity."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Player"
    player_class: str = "commando"  # mage, commando, dimension_runner, biotech_paladin
    
    # Transform
    position: Vector2 = field(default_factory=Vector2)
    rotation: float = 0.0  # Radians
    
    # Stats
    health: float = 100.0
    max_health: float = 100.0
    armor: float = 0.0
    damage_multiplier: float = 1.0
    speed_multiplier: float = 1.0
    
    # State
    is_alive: bool = True
    is_in_zone: bool = False
    respawn_timer: float = 0.0
    
    # Progression
    level: int = 1
    experience: int = 0
    currency: int = 0
    upgrades: Dict[str, int] = field(default_factory=dict)
    unlocked_skins: List[str] = field(default_factory=list)
    
    # Inventory
    equipped_weapon: Optional[str] = None
    equipped_skin: Optional[str] = None
    consumables: Dict[str, int] = field(default_factory=dict)
    
    # Squad
    squad_id: Optional[str] = None
    squad_role: str = "member"  # leader, member
    
    # Network
    session_id: Optional[str] = None
    last_input_time: float = 0.0


@dataclass
class Enemy:
    """Enemy entity."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    enemy_type: str = "basic"  # undead_warrior, zombie_horde, etc.
    
    # Transform
    position: Vector2 = field(default_factory=Vector2)
    rotation: float = 0.0
    
    # Stats
    health: float = 50.0
    max_health: float = 50.0
    damage: float = 10.0
    speed: float = 150.0
    
    # Behavior
    target_player_id: Optional[str] = None
    ai_state: str = "patrol"  # patrol, chase, attack, flee
    aggro_range: float = 500.0
    attack_range: float = 100.0
    
    # Rewards
    currency_drop: int = 10
    experience_drop: int = 25
    
    # Wave tracking
    wave_number: int = 1
    difficulty_scaling: float = 1.0


@dataclass
class Zone:
    """Hold zone entity."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Zone Alpha"
    theme: str = "fantasy"
    
    # Transform
    position: Vector2 = field(default_factory=Vector2)
    radius: float = 300.0
    
    # State
    is_active: bool = False
    players_in_zone: List[str] = field(default_factory=list)
    hold_progress: float = 0.0  # 0.0 to 1.0
    required_players: int = 1
    
    # Configuration
    difficulty_multiplier: float = 1.0
    enemy_spawn_rate: float = 1.0


@dataclass
class RescueBus:
    """Rescue bus entity."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Transform
    position: Vector2 = field(default_factory=Vector2)
    
    # State
    is_active: bool = False
    current_stop_zone_id: Optional[str] = None
    boarding_time_remaining: float = 0.0
    boarded_players: List[str] = field(default_factory=list)
    next_arrival_time: float = 120.0


@dataclass
class Projectile:
    """Projectile entity (bullets, spells, etc.)."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    projectile_type: str = "bullet"
    
    # Transform
    position: Vector2 = field(default_factory=Vector2)
    velocity: Vector2 = field(default_factory=Vector2)
    
    # Properties
    damage: float = 10.0
    speed: float = 800.0
    lifetime: float = 3.0
    owner_id: Optional[str] = None
    
    # Effects
    piercing: bool = False
    explosive: bool = False
    explosion_radius: float = 0.0


@dataclass
class GameState:
    """Overall game state."""
    # Collections
    players: Dict[str, Player] = field(default_factory=dict)
    enemies: Dict[str, Enemy] = field(default_factory=dict)
    zones: Dict[str, Zone] = field(default_factory=dict)
    projectiles: Dict[str, Projectile] = field(default_factory=dict)
    bus: Optional[RescueBus] = None
    
    # Wave management
    current_wave: int = 1
    wave_active: bool = False
    enemies_remaining: int = 0
    wave_start_time: float = 0.0
    
    # Zone control
    active_zone_id: Optional[str] = None
    zone_rotation_timer: float = 0.0
    
    # Time
    game_time: float = 0.0
    delta_time: float = 0.0
    
    # Match state
    match_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    match_started: bool = False
    match_ended: bool = False
    survivors: int = 0


@dataclass
class Squad:
    """Player squad/team."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Squad Alpha"
    leader_id: Optional[str] = None
    member_ids: List[str] = field(default_factory=list)
    
    # Stats
    total_kills: int = 0
    total_waves_survived: int = 0
    squad_level: int = 1
    
    # Matchmaking
    average_skill_rating: float = 1000.0
    in_queue: bool = False
