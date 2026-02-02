"""
Advanced combat system for Blood-Thirsty.
Includes weapons, shooting mechanics, and damage calculations.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum
import time


class WeaponType(Enum):
    """Types of weapons."""
    ASSAULT_RIFLE = "assault_rifle"
    SHOTGUN = "shotgun"
    SNIPER_RIFLE = "sniper_rifle"
    ROCKET_LAUNCHER = "rocket_launcher"
    ENERGY_WEAPON = "energy_weapon"
    MAGIC_STAFF = "magic_staff"


class DamageType(Enum):
    """Types of damage."""
    PHYSICAL = "physical"
    ENERGY = "energy"
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    POISON = "poison"
    HOLY = "holy"
    VOID = "void"


@dataclass
class WeaponStats:
    """Weapon statistics."""
    name: str
    weapon_type: WeaponType
    damage: float
    damage_type: DamageType
    
    # Firing mechanics
    fire_rate: float  # Rounds per second
    magazine_size: int
    reload_time: float  # Seconds
    
    # Accuracy
    accuracy: float  # 0.0 to 1.0
    recoil: float  # Kick per shot
    
    # Range
    effective_range: float  # Effective damage range
    max_range: float  # Maximum range
    
    # Special
    penetration: int = 0  # Number of enemies penetrated
    explosive_radius: float = 0.0  # AOE damage radius
    projectile_speed: float = 1000.0  # Units per second (0 = hitscan)
    
    # Modifiers
    crit_chance: float = 0.10  # 10% base crit chance
    crit_multiplier: float = 2.0  # 2x damage on crit
    
    # Ammo
    ammo_per_shot: int = 1
    max_ammo: int = 300


@dataclass
class Weapon:
    """Active weapon instance."""
    stats: WeaponStats
    current_ammo: int = 0
    reserve_ammo: int = 0
    last_shot_time: float = 0.0
    is_reloading: bool = False
    reload_start_time: float = 0.0
    heat_level: float = 0.0  # For energy weapons
    
    def __post_init__(self):
        if self.current_ammo == 0:
            self.current_ammo = self.stats.magazine_size
        if self.reserve_ammo == 0:
            self.reserve_ammo = self.stats.max_ammo
    
    def can_shoot(self, current_time: float) -> bool:
        """Check if weapon can shoot."""
        if self.is_reloading:
            return False
        if self.current_ammo <= 0:
            return False
        
        # Check fire rate
        time_since_last_shot = current_time - self.last_shot_time
        min_time_between_shots = 1.0 / self.stats.fire_rate
        
        return time_since_last_shot >= min_time_between_shots
    
    def shoot(self, current_time: float) -> bool:
        """Attempt to shoot weapon."""
        if not self.can_shoot(current_time):
            return False
        
        self.current_ammo -= self.stats.ammo_per_shot
        self.last_shot_time = current_time
        self.heat_level = min(1.0, self.heat_level + 0.1)
        
        return True
    
    def reload(self, current_time: float):
        """Start reloading."""
        if self.is_reloading:
            return
        if self.current_ammo >= self.stats.magazine_size:
            return
        if self.reserve_ammo <= 0:
            return
        
        self.is_reloading = True
        self.reload_start_time = current_time
    
    def update(self, current_time: float, delta_time: float):
        """Update weapon state."""
        # Handle reload
        if self.is_reloading:
            if current_time - self.reload_start_time >= self.stats.reload_time:
                # Complete reload
                ammo_needed = self.stats.magazine_size - self.current_ammo
                ammo_to_reload = min(ammo_needed, self.reserve_ammo)
                
                self.current_ammo += ammo_to_reload
                self.reserve_ammo -= ammo_to_reload
                self.is_reloading = False
        
        # Cool down heat
        if self.heat_level > 0:
            self.heat_level = max(0, self.heat_level - delta_time * 0.5)


# Predefined weapons
WEAPONS = {
    # Assault Rifles
    "ar_basic": WeaponStats(
        name="M4 Assault Rifle",
        weapon_type=WeaponType.ASSAULT_RIFLE,
        damage=25.0,
        damage_type=DamageType.PHYSICAL,
        fire_rate=10.0,  # 10 rounds/sec
        magazine_size=30,
        reload_time=2.0,
        accuracy=0.85,
        recoil=0.1,
        effective_range=500.0,
        max_range=1000.0,
        projectile_speed=2000.0,
    ),
    
    "ar_advanced": WeaponStats(
        name="SCAR-H Heavy Rifle",
        weapon_type=WeaponType.ASSAULT_RIFLE,
        damage=35.0,
        damage_type=DamageType.PHYSICAL,
        fire_rate=7.0,
        magazine_size=25,
        reload_time=2.5,
        accuracy=0.90,
        recoil=0.15,
        effective_range=600.0,
        max_range=1200.0,
        projectile_speed=2500.0,
    ),
    
    # Shotguns
    "shotgun_pump": WeaponStats(
        name="Combat Shotgun",
        weapon_type=WeaponType.SHOTGUN,
        damage=80.0,  # Per pellet, multiple pellets
        damage_type=DamageType.PHYSICAL,
        fire_rate=1.0,
        magazine_size=8,
        reload_time=3.5,
        accuracy=0.60,  # Wide spread
        recoil=0.3,
        effective_range=150.0,
        max_range=300.0,
        projectile_speed=1000.0,
    ),
    
    "shotgun_auto": WeaponStats(
        name="AA-12 Auto Shotgun",
        weapon_type=WeaponType.SHOTGUN,
        damage=60.0,
        damage_type=DamageType.PHYSICAL,
        fire_rate=5.0,
        magazine_size=20,
        reload_time=4.0,
        accuracy=0.65,
        recoil=0.25,
        effective_range=180.0,
        max_range=350.0,
        projectile_speed=1200.0,
    ),
    
    # Sniper Rifles
    "sniper_bolt": WeaponStats(
        name="Bolt Action Sniper",
        weapon_type=WeaponType.SNIPER_RIFLE,
        damage=200.0,
        damage_type=DamageType.PHYSICAL,
        fire_rate=0.5,
        magazine_size=5,
        reload_time=3.0,
        accuracy=0.99,
        recoil=0.5,
        effective_range=2000.0,
        max_range=3000.0,
        projectile_speed=3000.0,
        penetration=2,
    ),
    
    "sniper_semi": WeaponStats(
        name="M110 Semi-Auto Sniper",
        weapon_type=WeaponType.SNIPER_RIFLE,
        damage=120.0,
        damage_type=DamageType.PHYSICAL,
        fire_rate=2.0,
        magazine_size=10,
        reload_time=2.5,
        accuracy=0.95,
        recoil=0.3,
        effective_range=1500.0,
        max_range=2500.0,
        projectile_speed=2800.0,
        penetration=1,
    ),
    
    # Rocket Launchers
    "rocket_basic": WeaponStats(
        name="RPG-7",
        weapon_type=WeaponType.ROCKET_LAUNCHER,
        damage=500.0,
        damage_type=DamageType.PHYSICAL,
        fire_rate=0.3,
        magazine_size=1,
        reload_time=4.0,
        accuracy=0.80,
        recoil=0.8,
        effective_range=800.0,
        max_range=1500.0,
        projectile_speed=300.0,
        explosive_radius=300.0,
    ),
    
    # Energy Weapons
    "energy_rifle": WeaponStats(
        name="Plasma Rifle",
        weapon_type=WeaponType.ENERGY_WEAPON,
        damage=40.0,
        damage_type=DamageType.ENERGY,
        fire_rate=8.0,
        magazine_size=50,
        reload_time=3.0,
        accuracy=0.92,
        recoil=0.05,
        effective_range=700.0,
        max_range=1500.0,
        projectile_speed=2000.0,
    ),
    
    "energy_cannon": WeaponStats(
        name="Laser Cannon",
        weapon_type=WeaponType.ENERGY_WEAPON,
        damage=150.0,
        damage_type=DamageType.ENERGY,
        fire_rate=1.5,
        magazine_size=10,
        reload_time=4.0,
        accuracy=0.98,
        recoil=0.2,
        effective_range=1200.0,
        max_range=2000.0,
        projectile_speed=0.0,  # Hitscan
        penetration=3,
    ),
    
    # Magic Staves
    "staff_fire": WeaponStats(
        name="Staff of Inferno",
        weapon_type=WeaponType.MAGIC_STAFF,
        damage=75.0,
        damage_type=DamageType.FIRE,
        fire_rate=3.0,
        magazine_size=20,
        reload_time=2.5,
        accuracy=0.88,
        recoil=0.0,
        effective_range=600.0,
        max_range=1000.0,
        projectile_speed=1500.0,
        explosive_radius=100.0,
    ),
    
    "staff_ice": WeaponStats(
        name="Staff of Frost",
        weapon_type=WeaponType.MAGIC_STAFF,
        damage=60.0,
        damage_type=DamageType.ICE,
        fire_rate=4.0,
        magazine_size=30,
        reload_time=2.0,
        accuracy=0.90,
        recoil=0.0,
        effective_range=500.0,
        max_range=800.0,
        projectile_speed=1200.0,
    ),
}


@dataclass
class CombatStats:
    """Combat statistics tracking."""
    shots_fired: int = 0
    shots_hit: int = 0
    critical_hits: int = 0
    damage_dealt: float = 0.0
    kills: int = 0
    headshots: int = 0
    
    def accuracy(self) -> float:
        """Calculate accuracy percentage."""
        if self.shots_fired == 0:
            return 0.0
        return (self.shots_hit / self.shots_fired) * 100.0
    
    def crit_rate(self) -> float:
        """Calculate crit rate percentage."""
        if self.shots_hit == 0:
            return 0.0
        return (self.critical_hits / self.shots_hit) * 100.0


class CombatManager:
    """Manages combat interactions."""
    
    def __init__(self):
        self.active_projectiles: List[Dict] = []
        self.damage_events: List[Dict] = []
    
    def calculate_damage(
        self, 
        weapon: Weapon, 
        distance: float,
        is_headshot: bool = False
    ) -> Dict:
        """Calculate damage for a shot."""
        import random
        
        base_damage = weapon.stats.damage
        
        # Distance falloff
        if distance > weapon.stats.effective_range:
            falloff = 1.0 - min(1.0, (distance - weapon.stats.effective_range) / 
                               (weapon.stats.max_range - weapon.stats.effective_range))
            base_damage *= falloff
        
        # Critical hit
        is_crit = random.random() < weapon.stats.crit_chance
        if is_crit:
            base_damage *= weapon.stats.crit_multiplier
        
        # Headshot multiplier
        if is_headshot:
            base_damage *= 2.0
        
        return {
            "damage": base_damage,
            "is_crit": is_crit,
            "is_headshot": is_headshot,
            "damage_type": weapon.stats.damage_type,
        }
    
    def apply_damage(
        self,
        target_id: str,
        damage_info: Dict,
        source_player_id: str
    ):
        """Record damage event."""
        self.damage_events.append({
            "target_id": target_id,
            "source_id": source_player_id,
            "damage": damage_info["damage"],
            "damage_type": damage_info["damage_type"],
            "is_crit": damage_info["is_crit"],
            "is_headshot": damage_info["is_headshot"],
            "timestamp": time.time(),
        })
