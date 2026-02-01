"""
Game systems that process components.
Systems contain the behavior logic for the game.
"""
from typing import List
import random
from app.engine import System, Entity
from app.components import (
    ResourceProducer, ResourceConverter, Particle, Transform,
    GameResources, Stats, Clickable, Achievement
)


class ResourceProductionSystem(System):
    """System that handles automatic resource generation."""
    
    def __init__(self, resources_entity: Entity):
        super().__init__()
        self.resources_entity = resources_entity
    
    def update(self, entities: List[Entity], delta_time: float) -> None:
        """Update resource production."""
        resources = self.resources_entity.get_component(GameResources)
        if not resources:
            return
        
        for entity in entities:
            producer = entity.get_component(ResourceProducer)
            if producer:
                amount = producer.production_rate * delta_time
                resources.add_resource(producer.resource_type, amount)


class ResourceConversionSystem(System):
    """System that handles resource conversion."""
    
    def __init__(self, resources_entity: Entity):
        super().__init__()
        self.resources_entity = resources_entity
    
    def update(self, entities: List[Entity], delta_time: float) -> None:
        """Update resource conversions."""
        resources = self.resources_entity.get_component(GameResources)
        if not resources:
            return
        
        for entity in entities:
            converter = entity.get_component(ResourceConverter)
            if converter and converter.enabled:
                # Check if we have enough input resource
                input_needed = converter.input_rate * delta_time
                if resources.can_afford(converter.input_type, input_needed):
                    # Perform conversion
                    resources.spend(converter.input_type, input_needed)
                    output_amount = converter.output_rate * delta_time * converter.efficiency * converter.level
                    resources.add_resource(converter.output_type, output_amount)


class ParticleSystem(System):
    """System that updates particle effects."""
    
    def __init__(self, world):
        super().__init__()
        self.world = world
    
    def update(self, entities: List[Entity], delta_time: float) -> None:
        """Update all particles."""
        for entity in entities:
            particle = entity.get_component(Particle)
            transform = entity.get_component(Transform)
            
            if particle and transform:
                # Update age
                particle.age += delta_time
                
                # Remove if expired
                if particle.age >= particle.lifetime:
                    self.world.remove_entity(entity)
                    continue
                
                # Update position
                transform.x += particle.velocity_x * delta_time
                transform.y += particle.velocity_y * delta_time
                
                # Fade effect
                if particle.fade:
                    fade_ratio = 1.0 - (particle.age / particle.lifetime)
                    particle.size = max(0, particle.size * fade_ratio)


class CooldownSystem(System):
    """System that handles cooldowns."""
    
    def update(self, entities: List[Entity], delta_time: float) -> None:
        """Update cooldowns."""
        for entity in entities:
            clickable = entity.get_component(Clickable)
            if clickable and clickable.cooldown > 0:
                clickable.cooldown = max(0, clickable.cooldown - delta_time)


class StatsTrackingSystem(System):
    """System that tracks game statistics."""
    
    def __init__(self, stats_entity: Entity, resources_entity: Entity):
        super().__init__()
        self.stats_entity = stats_entity
        self.resources_entity = resources_entity
    
    def update(self, entities: List[Entity], delta_time: float) -> None:
        """Update statistics."""
        stats = self.stats_entity.get_component(Stats)
        resources = self.resources_entity.get_component(GameResources)
        
        if not stats or not resources:
            return
        
        # Update play time
        stats.play_time += delta_time
        
        # Track highest resources
        stats.highest_energy = max(stats.highest_energy, resources.energy)
        stats.highest_crystals = max(stats.highest_crystals, resources.crystals)


class AchievementSystem(System):
    """System that checks and unlocks achievements."""
    
    def __init__(self, stats_entity: Entity, resources_entity: Entity, game_engine):
        super().__init__()
        self.stats_entity = stats_entity
        self.resources_entity = resources_entity
        self.game_engine = game_engine
    
    def update(self, entities: List[Entity], delta_time: float) -> None:
        """Check achievements."""
        stats = self.stats_entity.get_component(Stats)
        resources = self.resources_entity.get_component(GameResources)
        
        if not stats or not resources:
            return
        
        for entity in entities:
            achievement = entity.get_component(Achievement)
            if achievement and not achievement.unlocked:
                # Check if requirement is met
                unlocked = False
                
                if achievement.requirement_type == "resource_total":
                    # Check total earned (from stats)
                    if achievement.target == "energy":
                        unlocked = stats.total_energy_earned >= achievement.requirement_value
                    elif achievement.target == "crystals":
                        unlocked = stats.total_crystals_earned >= achievement.requirement_value
                
                elif achievement.requirement_type == "clicks":
                    unlocked = stats.total_clicks >= achievement.requirement_value
                
                elif achievement.requirement_type == "play_time":
                    unlocked = stats.play_time >= achievement.requirement_value
                
                if unlocked:
                    achievement.unlocked = True
                    stats.achievements_unlocked += 1
                    
                    # Apply reward
                    if achievement.reward_type == "multiplier":
                        if achievement.target == "energy":
                            resources.energy_multiplier *= achievement.reward_value
                        elif achievement.target == "global":
                            resources.global_multiplier *= achievement.reward_value
                    
                    # Emit event
                    self.game_engine.emit("achievement_unlocked", 
                                         name=achievement.name,
                                         description=achievement.description)


class DailyRewardSystem(System):
    """System for daily login rewards."""
    
    def __init__(self):
        super().__init__()
        self.last_reward_day = -1
        self.current_streak = 0
    
    def update(self, entities: List[Entity], delta_time: float) -> None:
        """Check for daily rewards (simplified)."""
        # In a real implementation, this would check actual dates
        pass
