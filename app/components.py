"""
Game components for the ECS system.
Each component represents data without behavior.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from app.engine import Component


@dataclass
class Transform(Component):
    """Position and scale in 2D space."""
    x: float = 0.0
    y: float = 0.0
    scale: float = 1.0


@dataclass
class ResourceProducer(Component):
    """Produces a resource over time."""
    resource_type: str = "energy"
    base_rate: float = 1.0
    multiplier: float = 1.0
    level: int = 1
    cost_base: float = 10.0
    cost_multiplier: float = 1.15
    
    @property
    def production_rate(self) -> float:
        """Calculate total production rate."""
        return self.base_rate * self.multiplier * self.level
    
    @property
    def upgrade_cost(self) -> float:
        """Calculate cost to upgrade to next level."""
        return self.cost_base * (self.cost_multiplier ** self.level)


@dataclass
class ResourceConverter(Component):
    """Converts one resource to another."""
    input_type: str = "energy"
    output_type: str = "crystals"
    input_rate: float = 10.0
    output_rate: float = 1.0
    efficiency: float = 1.0
    level: int = 1
    enabled: bool = True
    
    @property
    def conversion_rate(self) -> float:
        """Calculate effective conversion rate."""
        return (self.output_rate / self.input_rate) * self.efficiency * self.level


@dataclass
class ClickGenerator(Component):
    """Generates resources on click."""
    resource_type: str = "energy"
    amount: float = 1.0
    multiplier: float = 1.0
    critical_chance: float = 0.1
    critical_multiplier: float = 2.0
    
    @property
    def click_value(self) -> float:
        """Calculate base click value."""
        return self.amount * self.multiplier


@dataclass
class Upgrade(Component):
    """An upgrade that can be purchased."""
    name: str = ""
    description: str = ""
    cost: float = 100.0
    resource_type: str = "energy"
    purchased: bool = False
    effect_type: str = "multiplier"  # multiplier, unlock, special
    effect_value: float = 2.0
    target: str = ""  # What this upgrade affects


@dataclass
class Achievement(Component):
    """An achievement that can be unlocked."""
    name: str = ""
    description: str = ""
    requirement_type: str = "resource_total"
    requirement_value: float = 1000.0
    unlocked: bool = False
    reward_type: str = "multiplier"
    reward_value: float = 1.1


@dataclass
class Particle(Component):
    """Visual particle effect."""
    lifetime: float = 1.0
    age: float = 0.0
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    color: tuple = (255, 255, 255)
    size: float = 5.0
    fade: bool = True


@dataclass
class Visual(Component):
    """Visual representation of an entity."""
    color: tuple = (255, 255, 255)
    size: float = 50.0
    shape: str = "circle"  # circle, rect, sprite
    sprite_path: Optional[str] = None
    animation_frame: int = 0


@dataclass
class Clickable(Component):
    """Makes an entity clickable."""
    radius: float = 50.0
    enabled: bool = True
    cooldown: float = 0.0
    cooldown_max: float = 0.0


@dataclass
class Stats(Component):
    """Game statistics tracker."""
    total_clicks: int = 0
    total_energy_earned: float = 0.0
    total_crystals_earned: float = 0.0
    total_essence_earned: float = 0.0
    play_time: float = 0.0
    highest_energy: float = 0.0
    highest_crystals: float = 0.0
    upgrades_purchased: int = 0
    achievements_unlocked: int = 0
    
    def to_dict(self) -> Dict:
        """Convert stats to dictionary."""
        return {
            "total_clicks": self.total_clicks,
            "total_energy_earned": self.total_energy_earned,
            "total_crystals_earned": self.total_crystals_earned,
            "total_essence_earned": self.total_essence_earned,
            "play_time": self.play_time,
            "highest_energy": self.highest_energy,
            "highest_crystals": self.highest_crystals,
            "upgrades_purchased": self.upgrades_purchased,
            "achievements_unlocked": self.achievements_unlocked,
        }


@dataclass
class GameResources(Component):
    """Main resource pool for the game."""
    energy: float = 0.0
    crystals: float = 0.0
    essence: float = 0.0
    prestige_points: int = 0
    
    # Multipliers
    energy_multiplier: float = 1.0
    crystal_multiplier: float = 1.0
    essence_multiplier: float = 1.0
    global_multiplier: float = 1.0
    
    def add_resource(self, resource_type: str, amount: float) -> None:
        """Add amount to specified resource."""
        if resource_type == "energy":
            self.energy += amount * self.energy_multiplier * self.global_multiplier
        elif resource_type == "crystals":
            self.crystals += amount * self.crystal_multiplier * self.global_multiplier
        elif resource_type == "essence":
            self.essence += amount * self.essence_multiplier * self.global_multiplier
    
    def can_afford(self, resource_type: str, amount: float) -> bool:
        """Check if player can afford the cost."""
        if resource_type == "energy":
            return self.energy >= amount
        elif resource_type == "crystals":
            return self.crystals >= amount
        elif resource_type == "essence":
            return self.essence >= amount
        return False
    
    def spend(self, resource_type: str, amount: float) -> bool:
        """Spend resources if available."""
        if not self.can_afford(resource_type, amount):
            return False
        
        if resource_type == "energy":
            self.energy -= amount
        elif resource_type == "crystals":
            self.crystals -= amount
        elif resource_type == "essence":
            self.essence -= amount
        
        return True
    
    def get_resource(self, resource_type: str) -> float:
        """Get current amount of resource."""
        if resource_type == "energy":
            return self.energy
        elif resource_type == "crystals":
            return self.crystals
        elif resource_type == "essence":
            return self.essence
        return 0.0
