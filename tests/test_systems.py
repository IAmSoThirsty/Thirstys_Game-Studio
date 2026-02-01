"""
Tests for game systems.
"""
import pytest
from app.engine import Entity, World
from app.components import (
    ResourceProducer, ResourceConverter, Particle, Transform,
    GameResources, Stats, Clickable, Achievement
)
from app.systems import (
    ResourceProductionSystem, ResourceConversionSystem, ParticleSystem,
    CooldownSystem, StatsTrackingSystem, AchievementSystem
)


def test_resource_production_system():
    """Test ResourceProductionSystem."""
    world = World()
    
    # Create resources entity
    resources_entity = world.create_entity("Resources")
    resources_entity.add_component(GameResources(energy=0.0))
    
    # Create producer
    producer_entity = world.create_entity("Producer")
    producer_entity.add_component(ResourceProducer(
        resource_type="energy",
        base_rate=10.0,
        multiplier=2.0,
        level=3
    ))
    
    # Add system
    system = ResourceProductionSystem(resources_entity)
    world.add_system(system)
    
    # Update for 1 second
    world.update(1.0)
    
    resources = resources_entity.get_component(GameResources)
    
    # Should produce 10 * 2 * 3 * 1.0 = 60 energy per second (with multipliers)
    assert resources.energy > 0


def test_resource_conversion_system():
    """Test ResourceConversionSystem."""
    world = World()
    
    # Create resources entity with initial energy
    resources_entity = world.create_entity("Resources")
    resources_entity.add_component(GameResources(energy=1000.0, crystals=0.0))
    
    # Create converter
    converter_entity = world.create_entity("Converter")
    converter_entity.add_component(ResourceConverter(
        input_type="energy",
        output_type="crystals",
        input_rate=100.0,
        output_rate=10.0,
        efficiency=1.0,
        level=1,
        enabled=True
    ))
    
    # Add system
    system = ResourceConversionSystem(resources_entity)
    world.add_system(system)
    
    # Update for 1 second
    world.update(1.0)
    
    resources = resources_entity.get_component(GameResources)
    
    # Should have consumed some energy
    assert resources.energy < 1000.0
    
    # Should have produced some crystals
    assert resources.crystals > 0


def test_conversion_disabled():
    """Test that disabled converters don't convert."""
    world = World()
    
    resources_entity = world.create_entity("Resources")
    resources_entity.add_component(GameResources(energy=1000.0, crystals=0.0))
    
    converter_entity = world.create_entity("Converter")
    converter_entity.add_component(ResourceConverter(
        input_type="energy",
        output_type="crystals",
        input_rate=100.0,
        output_rate=10.0,
        enabled=False  # Disabled
    ))
    
    system = ResourceConversionSystem(resources_entity)
    world.add_system(system)
    
    world.update(1.0)
    
    resources = resources_entity.get_component(GameResources)
    
    # Should not have changed
    assert resources.energy == 1000.0
    assert resources.crystals == 0.0


def test_particle_system():
    """Test ParticleSystem."""
    world = World()
    
    # Create particle with short lifetime
    particle_entity = world.create_entity("Particle")
    particle_entity.add_component(Transform(x=100.0, y=100.0))
    particle_entity.add_component(Particle(
        lifetime=0.5,
        age=0.0,
        velocity_x=10.0,
        velocity_y=20.0
    ))
    
    system = ParticleSystem(world)
    world.add_system(system)
    
    # Update
    world.update(0.1)
    
    transform = particle_entity.get_component(Transform)
    particle = particle_entity.get_component(Particle)
    
    # Position should have changed
    assert transform.x > 100.0
    assert transform.y > 100.0
    
    # Age should have increased
    assert particle.age > 0
    
    # Update until expired
    world.update(0.5)
    
    # Particle should be removed
    assert particle_entity not in world.entities


def test_cooldown_system():
    """Test CooldownSystem."""
    world = World()
    
    entity = world.create_entity("Clickable")
    entity.add_component(Clickable(
        cooldown=1.0,
        cooldown_max=1.0
    ))
    
    system = CooldownSystem()
    world.add_system(system)
    
    # Update
    world.update(0.5)
    
    clickable = entity.get_component(Clickable)
    assert clickable.cooldown == 0.5
    
    # Update again
    world.update(0.6)
    
    # Should be at 0 (clamped)
    assert clickable.cooldown == 0.0


def test_stats_tracking_system():
    """Test StatsTrackingSystem."""
    world = World()
    
    resources_entity = world.create_entity("Resources")
    resources_entity.add_component(GameResources(
        energy=500.0,
        crystals=100.0
    ))
    
    stats_entity = world.create_entity("Stats")
    stats_entity.add_component(Stats(
        play_time=0.0,
        highest_energy=0.0,
        highest_crystals=0.0
    ))
    
    system = StatsTrackingSystem(stats_entity, resources_entity)
    world.add_system(system)
    
    # Update
    world.update(1.0)
    
    stats = stats_entity.get_component(Stats)
    
    # Play time should increase
    assert stats.play_time == 1.0
    
    # Highest resources should be recorded
    assert stats.highest_energy == 500.0
    assert stats.highest_crystals == 100.0


def test_achievement_system_resource_total():
    """Test AchievementSystem with resource total requirement."""
    from app.engine import GameEngine
    
    world = World()
    engine = GameEngine()
    
    resources_entity = world.create_entity("Resources")
    resources_entity.add_component(GameResources(energy=0.0))
    
    stats_entity = world.create_entity("Stats")
    stats_entity.add_component(Stats(
        total_energy_earned=150.0,
        achievements_unlocked=0
    ))
    
    achievement_entity = world.create_entity("Achievement")
    achievement = Achievement(
        name="Test Achievement",
        description="Earn 100 energy",
        requirement_type="resource_total",
        requirement_value=100.0,
        unlocked=False,
        reward_type="multiplier",
        reward_value=1.5
    )
    achievement.target = "energy"
    achievement_entity.add_component(achievement)
    
    system = AchievementSystem(stats_entity, resources_entity, engine)
    world.add_system(system)
    
    # Update
    world.update(0.016)
    
    # Achievement should be unlocked
    assert achievement.unlocked is True
    
    stats = stats_entity.get_component(Stats)
    assert stats.achievements_unlocked == 1
    
    # Multiplier should be applied
    resources = resources_entity.get_component(GameResources)
    assert resources.energy_multiplier == 1.5


def test_achievement_system_clicks():
    """Test AchievementSystem with clicks requirement."""
    from app.engine import GameEngine
    
    world = World()
    engine = GameEngine()
    
    resources_entity = world.create_entity("Resources")
    resources_entity.add_component(GameResources())
    
    stats_entity = world.create_entity("Stats")
    stats_entity.add_component(Stats(
        total_clicks=150,
        achievements_unlocked=0
    ))
    
    achievement_entity = world.create_entity("Achievement")
    achievement = Achievement(
        name="Clicker",
        description="Click 100 times",
        requirement_type="clicks",
        requirement_value=100.0,
        unlocked=False,
        reward_type="multiplier",
        reward_value=1.1
    )
    achievement.target = ""
    achievement_entity.add_component(achievement)
    
    system = AchievementSystem(stats_entity, resources_entity, engine)
    world.add_system(system)
    
    # Update
    world.update(0.016)
    
    # Achievement should be unlocked
    assert achievement.unlocked is True


def test_achievement_system_play_time():
    """Test AchievementSystem with play time requirement."""
    from app.engine import GameEngine
    
    world = World()
    engine = GameEngine()
    
    resources_entity = world.create_entity("Resources")
    resources_entity.add_component(GameResources())
    
    stats_entity = world.create_entity("Stats")
    stats_entity.add_component(Stats(
        play_time=350.0,
        achievements_unlocked=0
    ))
    
    achievement_entity = world.create_entity("Achievement")
    achievement = Achievement(
        name="Dedicated",
        description="Play for 300 seconds",
        requirement_type="play_time",
        requirement_value=300.0,
        unlocked=False,
        reward_type="multiplier",
        reward_value=1.2
    )
    achievement.target = ""
    achievement_entity.add_component(achievement)
    
    system = AchievementSystem(stats_entity, resources_entity, engine)
    world.add_system(system)
    
    # Update
    world.update(0.016)
    
    # Achievement should be unlocked
    assert achievement.unlocked is True


def test_multiple_producers():
    """Test multiple producers working together."""
    world = World()
    
    resources_entity = world.create_entity("Resources")
    resources_entity.add_component(GameResources(energy=0.0))
    
    # Create multiple producers
    for i in range(3):
        producer_entity = world.create_entity(f"Producer{i}")
        producer_entity.add_component(ResourceProducer(
            resource_type="energy",
            base_rate=10.0,
            level=1
        ))
    
    system = ResourceProductionSystem(resources_entity)
    world.add_system(system)
    
    # Update for 1 second
    world.update(1.0)
    
    resources = resources_entity.get_component(GameResources)
    
    # All producers should contribute
    assert resources.energy > 25.0  # 3 producers * 10 rate


def test_system_order():
    """Test that systems execute in order."""
    world = World()
    
    execution_order = []
    
    class System1(ResourceProductionSystem):
        def update(self, entities, delta_time):
            execution_order.append(1)
            super().update(entities, delta_time)
    
    class System2(CooldownSystem):
        def update(self, entities, delta_time):
            execution_order.append(2)
            super().update(entities, delta_time)
    
    resources_entity = world.create_entity("Resources")
    resources_entity.add_component(GameResources())
    
    world.add_system(System1(resources_entity))
    world.add_system(System2())
    
    world.update(0.016)
    
    assert execution_order == [1, 2]
