"""
Advanced ability system for Blood-Thirsty player classes.
Each class has 4 unique abilities with cooldowns and effects.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Callable, Dict
from enum import Enum
import time


class AbilityType(Enum):
    """Types of abilities."""
    OFFENSIVE = "offensive"
    DEFENSIVE = "defensive"
    UTILITY = "utility"
    SUPPORT = "support"
    ULTIMATE = "ultimate"


class TargetType(Enum):
    """Ability targeting types."""
    SELF = "self"
    ENEMY = "enemy"
    ALLY = "ally"
    GROUND = "ground"
    DIRECTION = "direction"
    AOE = "aoe"


@dataclass
class AbilityStats:
    """Ability statistics and configuration."""
    id: str
    name: str
    description: str
    ability_type: AbilityType
    target_type: TargetType
    
    # Resources
    cooldown: float  # Seconds
    mana_cost: int
    
    # Effects
    damage: float = 0.0
    healing: float = 0.0
    shield_amount: float = 0.0
    duration: float = 0.0  # Effect duration
    
    # Range/Area
    cast_range: float = 0.0
    aoe_radius: float = 0.0
    
    # Special
    charges: int = 1  # Number of charges
    charge_cooldown: float = 0.0  # Cooldown per charge
    cast_time: float = 0.0  # Channel time
    projectile_speed: float = 0.0  # 0 = instant
    
    # Status effects
    applies_burn: bool = False
    applies_freeze: bool = False
    applies_stun: bool = False
    applies_slow: float = 0.0  # Slow percentage
    
    # Modifiers
    damage_multiplier: float = 1.0
    crit_chance_bonus: float = 0.0


@dataclass
class Ability:
    """Active ability instance."""
    stats: AbilityStats
    current_cooldown: float = 0.0
    charges_available: int = 0
    is_casting: bool = False
    cast_start_time: float = 0.0
    
    def __post_init__(self):
        if self.charges_available == 0:
            self.charges_available = self.stats.charges
    
    def can_cast(self, current_mana: int) -> bool:
        """Check if ability can be cast."""
        if self.current_cooldown > 0:
            return False
        if self.charges_available <= 0:
            return False
        if current_mana < self.stats.mana_cost:
            return False
        if self.is_casting:
            return False
        return True
    
    def start_cast(self, current_time: float) -> bool:
        """Start casting ability."""
        if self.stats.cast_time > 0:
            self.is_casting = True
            self.cast_start_time = current_time
            return False  # Not ready yet
        return True  # Instant cast
    
    def complete_cast(self, current_time: float):
        """Complete ability cast."""
        self.charges_available -= 1
        self.is_casting = False
        
        if self.charges_available == 0:
            self.current_cooldown = self.stats.cooldown
        else:
            self.current_cooldown = self.stats.charge_cooldown
    
    def update(self, delta_time: float):
        """Update ability state."""
        if self.current_cooldown > 0:
            self.current_cooldown = max(0, self.current_cooldown - delta_time)
            
            # Restore charge
            if self.current_cooldown == 0 and self.charges_available < self.stats.charges:
                self.charges_available += 1
                if self.charges_available < self.stats.charges:
                    self.current_cooldown = self.stats.charge_cooldown


# Mage Abilities
MAGE_ABILITIES = {
    "fireball": AbilityStats(
        id="fireball",
        name="Fireball",
        description="Launch a blazing fireball that explodes on impact",
        ability_type=AbilityType.OFFENSIVE,
        target_type=TargetType.DIRECTION,
        cooldown=8.0,
        mana_cost=40,
        damage=150.0,
        cast_range=1000.0,
        aoe_radius=150.0,
        projectile_speed=800.0,
        applies_burn=True,
    ),
    
    "ice_nova": AbilityStats(
        id="ice_nova",
        name="Ice Nova",
        description="Freeze all enemies in a large radius",
        ability_type=AbilityType.OFFENSIVE,
        target_type=TargetType.AOE,
        cooldown=15.0,
        mana_cost=60,
        damage=80.0,
        aoe_radius=400.0,
        applies_freeze=True,
        duration=3.0,
    ),
    
    "lightning_chain": AbilityStats(
        id="lightning_chain",
        name="Lightning Chain",
        description="Strike an enemy with lightning that bounces to nearby targets",
        ability_type=AbilityType.OFFENSIVE,
        target_type=TargetType.ENEMY,
        cooldown=10.0,
        mana_cost=50,
        damage=120.0,
        cast_range=800.0,
        aoe_radius=300.0,  # Bounce range
    ),
    
    "arcane_shield": AbilityStats(
        id="arcane_shield",
        name="Arcane Shield",
        description="Create a protective shield that absorbs damage",
        ability_type=AbilityType.DEFENSIVE,
        target_type=TargetType.SELF,
        cooldown=20.0,
        mana_cost=30,
        shield_amount=200.0,
        duration=8.0,
    ),
}


# Commando Abilities
COMMANDO_ABILITIES = {
    "assault_rifle": AbilityStats(
        id="assault_rifle",
        name="Assault Mode",
        description="Increase fire rate and damage for a short duration",
        ability_type=AbilityType.OFFENSIVE,
        target_type=TargetType.SELF,
        cooldown=12.0,
        mana_cost=30,
        damage_multiplier=1.5,
        duration=6.0,
    ),
    
    "rocket_launcher": AbilityStats(
        id="rocket_launcher",
        name="Rocket Barrage",
        description="Fire explosive rockets in an area",
        ability_type=AbilityType.OFFENSIVE,
        target_type=TargetType.GROUND,
        cooldown=18.0,
        mana_cost=70,
        damage=250.0,
        cast_range=1500.0,
        aoe_radius=350.0,
        cast_time=1.0,
    ),
    
    "tactical_grenade": AbilityStats(
        id="tactical_grenade",
        name="Tactical Grenade",
        description="Throw a grenade that stuns and damages enemies",
        ability_type=AbilityType.OFFENSIVE,
        target_type=TargetType.GROUND,
        cooldown=10.0,
        mana_cost=40,
        damage=100.0,
        cast_range=800.0,
        aoe_radius=250.0,
        applies_stun=True,
        duration=2.0,
        charges=2,
        charge_cooldown=5.0,
    ),
    
    "armor_plating": AbilityStats(
        id="armor_plating",
        name="Armor Plating",
        description="Activate heavy armor reducing incoming damage",
        ability_type=AbilityType.DEFENSIVE,
        target_type=TargetType.SELF,
        cooldown=25.0,
        mana_cost=35,
        damage_multiplier=0.5,  # 50% damage reduction
        duration=10.0,
    ),
}


# Dimension Runner Abilities
DIMENSION_RUNNER_ABILITIES = {
    "blink_strike": AbilityStats(
        id="blink_strike",
        name="Blink Strike",
        description="Teleport to target and deal massive damage",
        ability_type=AbilityType.OFFENSIVE,
        target_type=TargetType.ENEMY,
        cooldown=8.0,
        mana_cost=45,
        damage=200.0,
        cast_range=1000.0,
        crit_chance_bonus=0.50,  # +50% crit chance
    ),
    
    "shadow_step": AbilityStats(
        id="shadow_step",
        name="Shadow Step",
        description="Become invisible and gain movement speed",
        ability_type=AbilityType.UTILITY,
        target_type=TargetType.SELF,
        cooldown=15.0,
        mana_cost=40,
        duration=5.0,
    ),
    
    "phase_shift": AbilityStats(
        id="phase_shift",
        name="Phase Shift",
        description="Dodge all incoming damage for a brief moment",
        ability_type=AbilityType.DEFENSIVE,
        target_type=TargetType.SELF,
        cooldown=12.0,
        mana_cost=25,
        duration=1.5,
        charges=2,
        charge_cooldown=6.0,
    ),
    
    "temporal_blade": AbilityStats(
        id="temporal_blade",
        name="Temporal Blade",
        description="Your next attack deals critical damage and rewinds time on kill",
        ability_type=AbilityType.OFFENSIVE,
        target_type=TargetType.SELF,
        cooldown=20.0,
        mana_cost=50,
        damage_multiplier=3.0,
        crit_chance_bonus=1.0,  # Guaranteed crit
    ),
}


# Biotech Paladin Abilities
BIOTECH_PALADIN_ABILITIES = {
    "healing_pulse": AbilityStats(
        id="healing_pulse",
        name="Healing Pulse",
        description="Heal yourself and nearby allies",
        ability_type=AbilityType.SUPPORT,
        target_type=TargetType.AOE,
        cooldown=10.0,
        mana_cost=40,
        healing=150.0,
        aoe_radius=400.0,
    ),
    
    "divine_smite": AbilityStats(
        id="divine_smite",
        name="Divine Smite",
        description="Strike down an enemy with holy power",
        ability_type=AbilityType.OFFENSIVE,
        target_type=TargetType.ENEMY,
        cooldown=8.0,
        mana_cost=35,
        damage=180.0,
        cast_range=600.0,
        cast_time=0.5,
    ),
    
    "regeneration_field": AbilityStats(
        id="regeneration_field",
        name="Regeneration Field",
        description="Create a field that heals allies over time",
        ability_type=AbilityType.SUPPORT,
        target_type=TargetType.GROUND,
        cooldown=25.0,
        mana_cost=60,
        healing=20.0,  # Per second
        cast_range=800.0,
        aoe_radius=500.0,
        duration=10.0,
    ),
    
    "resurrection": AbilityStats(
        id="resurrection",
        name="Resurrection",
        description="Revive a fallen teammate with full health",
        ability_type=AbilityType.SUPPORT,
        target_type=TargetType.ALLY,
        cooldown=120.0,  # 2 minute cooldown
        mana_cost=100,
        healing=999999.0,  # Full revive
        cast_range=300.0,
        cast_time=3.0,
    ),
}


# All abilities by class
CLASS_ABILITIES = {
    "mage": MAGE_ABILITIES,
    "commando": COMMANDO_ABILITIES,
    "dimension_runner": DIMENSION_RUNNER_ABILITIES,
    "biotech_paladin": BIOTECH_PALADIN_ABILITIES,
}


class AbilityManager:
    """Manages ability casting and effects."""
    
    def __init__(self):
        self.active_effects: List[Dict] = []
        self.ability_events: List[Dict] = []
    
    def cast_ability(
        self,
        player_id: str,
        ability: Ability,
        current_time: float,
        target_position: Optional[tuple] = None,
        target_id: Optional[str] = None
    ) -> bool:
        """Attempt to cast an ability."""
        if ability.stats.cast_time > 0:
            success = ability.start_cast(current_time)
            if not success:
                return False
        
        # Record ability event
        self.ability_events.append({
            "player_id": player_id,
            "ability_id": ability.stats.id,
            "target_position": target_position,
            "target_id": target_id,
            "timestamp": current_time,
        })
        
        ability.complete_cast(current_time)
        
        # Apply effects
        if ability.stats.duration > 0:
            self._apply_effect(player_id, ability, current_time)
        
        return True
    
    def _apply_effect(self, player_id: str, ability: Ability, current_time: float):
        """Apply lasting ability effect."""
        self.active_effects.append({
            "player_id": player_id,
            "ability_id": ability.stats.id,
            "start_time": current_time,
            "end_time": current_time + ability.stats.duration,
            "effect_data": {
                "damage": ability.stats.damage,
                "healing": ability.stats.healing,
                "shield": ability.stats.shield_amount,
                "multiplier": ability.stats.damage_multiplier,
            }
        })
    
    def update(self, current_time: float, delta_time: float):
        """Update active effects."""
        # Remove expired effects
        self.active_effects = [
            effect for effect in self.active_effects
            if effect["end_time"] > current_time
        ]
