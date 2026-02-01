"""
Game configuration and constants.
"""
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class GameConfig:
    """Core game configuration."""
    # Server settings
    SERVER_PORT: int = 8765
    MAX_PLAYERS_PER_SQUAD: int = 4
    MAX_CONCURRENT_PLAYERS: int = 100
    TICK_RATE: int = 60  # Server ticks per second
    
    # Gameplay settings
    ZONE_HOLD_TIME: float = 60.0  # Seconds to hold zone
    BUS_ROTATION_INTERVAL: float = 120.0  # Seconds between bus arrivals
    WAVE_INTERVAL: float = 30.0  # Seconds between waves
    
    # Map settings
    MAP_SIZE: Tuple[int, int] = (10000, 10000)  # World units
    ZONE_COUNT: int = 6
    
    # Player settings
    PLAYER_SPEED: float = 300.0  # Units per second
    PLAYER_HEALTH: float = 100.0
    RESPAWN_TIME: float = 5.0
    
    # Economy
    BUNDLE_PRICES: Dict[str, float] = None
    
    def __post_init__(self):
        if self.BUNDLE_PRICES is None:
            self.BUNDLE_PRICES = {
                "premium_pack": 10.00,
                "starter_pack": 5.00,
                "coffee_boost": 1.99,
                "micro_boost": 0.99,
            }


@dataclass
class ZoneConfig:
    """Configuration for themed zones."""
    name: str
    theme: str  # fantasy, scifi, horror, mythic, alien, eldritch
    difficulty_multiplier: float
    enemy_types: List[str]
    environment_hazards: List[str]


# Predefined zones
ZONES = [
    ZoneConfig(
        name="Ruined Citadel",
        theme="fantasy",
        difficulty_multiplier=1.0,
        enemy_types=["undead_warrior", "skeleton_archer", "necromancer"],
        environment_hazards=["cursed_ground", "falling_debris"]
    ),
    ZoneConfig(
        name="Abandoned Labs",
        theme="scifi",
        difficulty_multiplier=1.2,
        enemy_types=["mutant_soldier", "cyber_drone", "rogue_ai"],
        environment_hazards=["toxic_gas", "electrical_hazard"]
    ),
    ZoneConfig(
        name="Haunted Township",
        theme="horror",
        difficulty_multiplier=1.1,
        enemy_types=["zombie_horde", "possessed_civilian", "wraith"],
        environment_hazards=["fog_of_madness", "blood_pools"]
    ),
    ZoneConfig(
        name="Mythic Forest",
        theme="mythic",
        difficulty_multiplier=1.3,
        enemy_types=["corrupted_treant", "shadow_beast", "ancient_guardian"],
        environment_hazards=["entangling_roots", "spirit_wisps"]
    ),
    ZoneConfig(
        name="Alien Wasteland",
        theme="alien",
        difficulty_multiplier=1.4,
        enemy_types=["xenomorph_swarm", "alien_brute", "mind_controller"],
        environment_hazards=["acid_pools", "gravity_anomaly"]
    ),
    ZoneConfig(
        name="Eldritch Demiplane",
        theme="eldritch",
        difficulty_multiplier=1.5,
        enemy_types=["cosmic_horror", "void_tentacle", "reality_warper"],
        environment_hazards=["sanity_drain", "dimensional_rift"]
    ),
]


# Player class configurations
@dataclass
class PlayerClassConfig:
    """Configuration for player classes."""
    name: str
    description: str
    base_health: float
    base_damage: float
    movement_speed: float
    abilities: List[str]
    upgrade_tree: Dict[str, Dict]


PLAYER_CLASSES = {
    "mage": PlayerClassConfig(
        name="Mage",
        description="Master of arcane arts with devastating elemental spells",
        base_health=80.0,
        base_damage=15.0,
        movement_speed=280.0,
        abilities=["fireball", "ice_nova", "lightning_chain", "arcane_shield"],
        upgrade_tree={
            "spell_power": {"max_level": 10, "cost_multiplier": 1.5},
            "mana_regen": {"max_level": 5, "cost_multiplier": 2.0},
            "elemental_mastery": {"max_level": 3, "cost_multiplier": 3.0},
        }
    ),
    "commando": PlayerClassConfig(
        name="Commando",
        description="Heavy weapons specialist with military-grade firepower",
        base_health=120.0,
        base_damage=12.0,
        movement_speed=260.0,
        abilities=["assault_rifle", "rocket_launcher", "tactical_grenade", "armor_plating"],
        upgrade_tree={
            "weapon_damage": {"max_level": 10, "cost_multiplier": 1.5},
            "armor": {"max_level": 5, "cost_multiplier": 2.0},
            "tactical_expertise": {"max_level": 3, "cost_multiplier": 3.0},
        }
    ),
    "dimension_runner": PlayerClassConfig(
        name="Dimension Runner",
        description="Teleporting assassin who strikes from impossible angles",
        base_health=90.0,
        base_damage=18.0,
        movement_speed=350.0,
        abilities=["blink_strike", "shadow_step", "phase_shift", "temporal_blade"],
        upgrade_tree={
            "mobility": {"max_level": 10, "cost_multiplier": 1.5},
            "critical_chance": {"max_level": 5, "cost_multiplier": 2.0},
            "dimensional_mastery": {"max_level": 3, "cost_multiplier": 3.0},
        }
    ),
    "biotech_paladin": PlayerClassConfig(
        name="Biotech Paladin",
        description="Holy warrior augmented with bio-tech healing abilities",
        base_health=110.0,
        base_damage=10.0,
        movement_speed=270.0,
        abilities=["healing_pulse", "divine_smite", "regeneration_field", "resurrection"],
        upgrade_tree={
            "healing_power": {"max_level": 10, "cost_multiplier": 1.5},
            "support_range": {"max_level": 5, "cost_multiplier": 2.0},
            "biotech_mastery": {"max_level": 3, "cost_multiplier": 3.0},
        }
    ),
}
