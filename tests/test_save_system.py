"""
Tests for save/load system.
"""
import os
import pytest
import tempfile
import shutil
from app.save_system import SaveSystem, serialize_game_state, deserialize_game_state
from app.game import ThirstysGame


@pytest.fixture
def temp_save_dir():
    """Create a temporary directory for saves."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_save_system_initialization(temp_save_dir):
    """Test save system initialization."""
    save_system = SaveSystem(temp_save_dir)
    
    assert save_system.save_dir == temp_save_dir
    assert os.path.exists(temp_save_dir)


def test_save_and_load(temp_save_dir):
    """Test basic save and load functionality."""
    save_system = SaveSystem(temp_save_dir)
    
    # Test data
    test_data = {
        "player_name": "TestPlayer",
        "level": 42,
        "score": 1000
    }
    
    # Save
    result = save_system.save_game(test_data)
    assert result is True
    assert save_system.has_save()
    
    # Load
    loaded_data = save_system.load_game()
    assert loaded_data is not None
    assert loaded_data["player_name"] == "TestPlayer"
    assert loaded_data["level"] == 42
    assert loaded_data["score"] == 1000


def test_load_nonexistent_save(temp_save_dir):
    """Test loading when no save exists."""
    save_system = SaveSystem(temp_save_dir)
    
    loaded_data = save_system.load_game()
    assert loaded_data is None
    assert not save_system.has_save()


def test_delete_save(temp_save_dir):
    """Test deleting save file."""
    save_system = SaveSystem(temp_save_dir)
    
    # Create a save
    save_system.save_game({"test": "data"})
    assert save_system.has_save()
    
    # Delete it
    result = save_system.delete_save()
    assert result is True
    assert not save_system.has_save()


def test_serialize_game_state():
    """Test serializing game state."""
    game = ThirstysGame(headless=True)
    
    # Modify some values
    from app.components import GameResources
    resources = game.resources_entity.get_component(GameResources)
    resources.energy = 1234.5
    resources.crystals = 67.8
    
    # Serialize
    state = serialize_game_state(game)
    
    assert state is not None
    assert "resources" in state
    assert state["resources"]["energy"] == 1234.5
    assert state["resources"]["crystals"] == 67.8
    assert "stats" in state
    assert "producers" in state
    assert "converters" in state
    assert "upgrades" in state
    assert "achievements" in state


def test_deserialize_game_state():
    """Test deserializing game state."""
    game = ThirstysGame(headless=True)
    
    # Create state data
    state = {
        "resources": {
            "energy": 5000.0,
            "crystals": 200.0,
            "essence": 10.0,
            "prestige_points": 0,
            "energy_multiplier": 2.0,
            "crystal_multiplier": 1.5,
            "essence_multiplier": 1.0,
            "global_multiplier": 1.2,
        },
        "stats": {
            "total_clicks": 500,
            "total_energy_earned": 10000.0,
            "total_crystals_earned": 500.0,
            "total_essence_earned": 50.0,
            "play_time": 300.0,
            "highest_energy": 6000.0,
            "highest_crystals": 250.0,
            "upgrades_purchased": 3,
            "achievements_unlocked": 2,
        },
        "click_generator": {
            "amount": 1.0,
            "multiplier": 5.0,
            "critical_chance": 0.2,
            "critical_multiplier": 3.0,
        },
        "producers": [],
        "converters": [],
        "upgrades": [],
        "achievements": [],
    }
    
    # Deserialize
    result = deserialize_game_state(game, state)
    assert result is True
    
    # Verify resources
    from app.components import GameResources, Stats, ClickGenerator
    resources = game.resources_entity.get_component(GameResources)
    assert resources.energy == 5000.0
    assert resources.crystals == 200.0
    assert resources.essence == 10.0
    assert resources.energy_multiplier == 2.0
    
    # Verify stats
    stats = game.stats_entity.get_component(Stats)
    assert stats.total_clicks == 500
    assert stats.total_energy_earned == 10000.0
    assert stats.play_time == 300.0
    
    # Verify click generator
    click_gen = game.click_generator_entity.get_component(ClickGenerator)
    assert click_gen.multiplier == 5.0
    assert click_gen.critical_chance == 0.2


def test_round_trip_save_load():
    """Test complete save and load cycle."""
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create game and modify state
        game1 = ThirstysGame(headless=True)
        game1.save_system = SaveSystem(temp_dir)
        
        from app.components import GameResources, Stats
        resources = game1.resources_entity.get_component(GameResources)
        resources.energy = 9999.0
        resources.crystals = 888.0
        
        stats = game1.stats_entity.get_component(Stats)
        stats.total_clicks = 777
        stats.play_time = 600.0
        
        # Save
        game1.save_game()
        
        # Create new game instance
        game2 = ThirstysGame(headless=True)
        game2.save_system = SaveSystem(temp_dir)
        
        # Load saved state
        state = game2.save_system.load_game()
        deserialize_game_state(game2, state)
        
        # Verify state matches
        resources2 = game2.resources_entity.get_component(GameResources)
        assert resources2.energy == 9999.0
        assert resources2.crystals == 888.0
        
        stats2 = game2.stats_entity.get_component(Stats)
        assert stats2.total_clicks == 777
        assert stats2.play_time == 600.0
        
    finally:
        shutil.rmtree(temp_dir)


def test_save_producers_state():
    """Test saving and loading producer states."""
    game = ThirstysGame(headless=True)
    
    # Upgrade some producers
    from app.components import ResourceProducer
    if len(game.producer_entities) > 0:
        producer = game.producer_entities[0].get_component(ResourceProducer)
        producer.level = 10
        producer.multiplier = 3.0
    
    # Serialize
    state = serialize_game_state(game)
    
    # Create new game and deserialize
    game2 = ThirstysGame(headless=True)
    deserialize_game_state(game2, state)
    
    # Verify producer state
    if len(game2.producer_entities) > 0:
        producer2 = game2.producer_entities[0].get_component(ResourceProducer)
        assert producer2.level == 10
        assert producer2.multiplier == 3.0


def test_save_upgrades_state():
    """Test saving and loading upgrade purchases."""
    game = ThirstysGame(headless=True)
    
    # Purchase some upgrades
    from app.components import Upgrade
    if len(game.upgrade_entities) > 1:
        upgrade1 = game.upgrade_entities[0].get_component(Upgrade)
        upgrade1.purchased = True
        
        upgrade2 = game.upgrade_entities[1].get_component(Upgrade)
        upgrade2.purchased = True
    
    # Serialize
    state = serialize_game_state(game)
    
    # Create new game and deserialize
    game2 = ThirstysGame(headless=True)
    deserialize_game_state(game2, state)
    
    # Verify upgrade state
    if len(game2.upgrade_entities) > 1:
        upgrade1 = game2.upgrade_entities[0].get_component(Upgrade)
        assert upgrade1.purchased is True
        
        upgrade2 = game2.upgrade_entities[1].get_component(Upgrade)
        assert upgrade2.purchased is True


def test_save_achievements_state():
    """Test saving and loading achievement unlocks."""
    game = ThirstysGame(headless=True)
    
    # Unlock some achievements
    from app.components import Achievement
    if len(game.achievement_entities) > 0:
        achievement = game.achievement_entities[0].get_component(Achievement)
        achievement.unlocked = True
    
    # Serialize
    state = serialize_game_state(game)
    
    # Create new game and deserialize
    game2 = ThirstysGame(headless=True)
    deserialize_game_state(game2, state)
    
    # Verify achievement state
    if len(game2.achievement_entities) > 0:
        achievement2 = game2.achievement_entities[0].get_component(Achievement)
        assert achievement2.unlocked is True
