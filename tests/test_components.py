"""
Tests for game components.
"""
import pytest
from app.components import (
    Transform, ResourceProducer, ResourceConverter, ClickGenerator,
    Upgrade, Achievement, Particle, Visual, Clickable, Stats, GameResources
)


def test_transform_component():
    """Test Transform component."""
    transform = Transform(x=100.0, y=200.0, scale=2.0)
    
    assert transform.x == 100.0
    assert transform.y == 200.0
    assert transform.scale == 2.0


def test_resource_producer():
    """Test ResourceProducer component."""
    producer = ResourceProducer(
        resource_type="energy",
        base_rate=10.0,
        multiplier=2.0,
        level=5,
        cost_base=100.0,
        cost_multiplier=1.15
    )
    
    # Test production rate calculation
    assert producer.production_rate == 10.0 * 2.0 * 5
    
    # Test upgrade cost calculation
    expected_cost = 100.0 * (1.15 ** 5)
    assert abs(producer.upgrade_cost - expected_cost) < 0.01


def test_resource_converter():
    """Test ResourceConverter component."""
    converter = ResourceConverter(
        input_type="energy",
        output_type="crystals",
        input_rate=100.0,
        output_rate=10.0,
        efficiency=1.5,
        level=2
    )
    
    # Test conversion rate
    expected_rate = (10.0 / 100.0) * 1.5 * 2
    assert converter.conversion_rate == expected_rate


def test_click_generator():
    """Test ClickGenerator component."""
    generator = ClickGenerator(
        resource_type="energy",
        amount=5.0,
        multiplier=3.0,
        critical_chance=0.2,
        critical_multiplier=2.5
    )
    
    assert generator.click_value == 5.0 * 3.0


def test_upgrade_component():
    """Test Upgrade component."""
    upgrade = Upgrade(
        name="Test Upgrade",
        description="Doubles production",
        cost=1000.0,
        resource_type="energy",
        purchased=False,
        effect_type="multiplier",
        effect_value=2.0
    )
    
    assert upgrade.name == "Test Upgrade"
    assert upgrade.purchased is False
    assert upgrade.effect_value == 2.0


def test_achievement_component():
    """Test Achievement component."""
    achievement = Achievement(
        name="First Steps",
        description="Earn 100 energy",
        requirement_type="resource_total",
        requirement_value=100.0,
        unlocked=False,
        reward_type="multiplier",
        reward_value=1.1
    )
    
    assert achievement.name == "First Steps"
    assert achievement.unlocked is False


def test_particle_component():
    """Test Particle component."""
    particle = Particle(
        lifetime=1.5,
        age=0.0,
        velocity_x=50.0,
        velocity_y=-30.0,
        color=(255, 128, 0),
        size=10.0,
        fade=True
    )
    
    assert particle.lifetime == 1.5
    assert particle.age == 0.0
    assert particle.velocity_x == 50.0


def test_visual_component():
    """Test Visual component."""
    visual = Visual(
        color=(255, 0, 0),
        size=50.0,
        shape="circle"
    )
    
    assert visual.color == (255, 0, 0)
    assert visual.shape == "circle"


def test_clickable_component():
    """Test Clickable component."""
    clickable = Clickable(
        radius=100.0,
        enabled=True,
        cooldown=0.0,
        cooldown_max=0.1
    )
    
    assert clickable.enabled is True
    assert clickable.radius == 100.0


def test_stats_component():
    """Test Stats component."""
    stats = Stats()
    
    assert stats.total_clicks == 0
    assert stats.total_energy_earned == 0.0
    assert stats.play_time == 0.0
    
    # Modify stats
    stats.total_clicks = 100
    stats.total_energy_earned = 5000.0
    
    # Test to_dict
    stats_dict = stats.to_dict()
    assert stats_dict["total_clicks"] == 100
    assert stats_dict["total_energy_earned"] == 5000.0


def test_game_resources_add():
    """Test adding resources."""
    resources = GameResources(
        energy=100.0,
        energy_multiplier=2.0,
        global_multiplier=1.5
    )
    
    resources.add_resource("energy", 10.0)
    
    # Should be 100 + (10 * 2.0 * 1.5) = 130
    assert resources.energy == 130.0


def test_game_resources_can_afford():
    """Test checking if resources can be afforded."""
    resources = GameResources(
        energy=100.0,
        crystals=50.0
    )
    
    assert resources.can_afford("energy", 50.0) is True
    assert resources.can_afford("energy", 150.0) is False
    assert resources.can_afford("crystals", 50.0) is True
    assert resources.can_afford("crystals", 51.0) is False


def test_game_resources_spend():
    """Test spending resources."""
    resources = GameResources(
        energy=100.0,
        crystals=50.0
    )
    
    # Successful spend
    result = resources.spend("energy", 30.0)
    assert result is True
    assert resources.energy == 70.0
    
    # Failed spend (insufficient resources)
    result = resources.spend("energy", 100.0)
    assert result is False
    assert resources.energy == 70.0  # Unchanged


def test_game_resources_get_resource():
    """Test getting resource amounts."""
    resources = GameResources(
        energy=123.45,
        crystals=67.89,
        essence=12.34
    )
    
    assert resources.get_resource("energy") == 123.45
    assert resources.get_resource("crystals") == 67.89
    assert resources.get_resource("essence") == 12.34
    assert resources.get_resource("unknown") == 0.0


def test_game_resources_multipliers():
    """Test resource multipliers."""
    resources = GameResources(
        energy=0.0,
        energy_multiplier=2.0,
        crystal_multiplier=3.0,
        global_multiplier=1.5
    )
    
    # Add energy (should use energy_multiplier and global_multiplier)
    resources.add_resource("energy", 10.0)
    assert resources.energy == 10.0 * 2.0 * 1.5
    
    # Add crystals
    resources.add_resource("crystals", 10.0)
    assert resources.crystals == 10.0 * 3.0 * 1.5


def test_resource_producer_leveling():
    """Test producer level progression."""
    producer = ResourceProducer(
        resource_type="energy",
        base_rate=1.0,
        level=1,
        cost_base=10.0,
        cost_multiplier=1.15
    )
    
    # Initial state
    assert producer.level == 1
    assert producer.production_rate == 1.0
    
    # Level up
    producer.level = 2
    assert producer.production_rate == 2.0
    
    # Cost should increase
    cost1 = 10.0 * (1.15 ** 2)
    assert abs(producer.upgrade_cost - cost1) < 0.01


def test_converter_efficiency():
    """Test converter efficiency scaling."""
    converter = ResourceConverter(
        input_type="energy",
        output_type="crystals",
        input_rate=100.0,
        output_rate=1.0,
        efficiency=1.0,
        level=1
    )
    
    base_rate = converter.conversion_rate
    
    # Double efficiency
    converter.efficiency = 2.0
    assert converter.conversion_rate == base_rate * 2.0
    
    # Level up
    converter.level = 2
    assert converter.conversion_rate == base_rate * 2.0 * 2.0
