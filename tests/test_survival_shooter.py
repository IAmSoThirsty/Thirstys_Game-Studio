"""
Unit tests for survival shooter core systems.
"""
import pytest
import asyncio
from app.survival_shooter.entities import (
    Player, Enemy, Zone, Vector2, GameState, Squad, RescueBus
)
from app.survival_shooter.config import GameConfig, PLAYER_CLASSES, ZONES
from app.survival_shooter.systems import WaveManager, ZoneManager
from app.survival_shooter.marketplace import Marketplace, ItemType


class TestVector2:
    """Test Vector2 math utilities."""
    
    def test_distance_calculation(self):
        """Test distance calculation between vectors."""
        v1 = Vector2(0, 0)
        v2 = Vector2(3, 4)
        assert v1.distance_to(v2) == 5.0
    
    def test_normalization(self):
        """Test vector normalization."""
        v = Vector2(3, 4)
        normalized = v.normalize()
        assert abs(normalized.x - 0.6) < 0.01
        assert abs(normalized.y - 0.8) < 0.01
    
    def test_zero_vector_normalization(self):
        """Test normalizing zero vector."""
        v = Vector2(0, 0)
        normalized = v.normalize()
        assert normalized.x == 0
        assert normalized.y == 0


class TestGameConfig:
    """Test game configuration."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = GameConfig()
        assert config.SERVER_PORT == 8765
        assert config.MAX_PLAYERS_PER_SQUAD == 4
        assert config.MAX_CONCURRENT_PLAYERS == 100
        assert config.TICK_RATE == 60
    
    def test_bundle_prices(self):
        """Test marketplace bundle prices."""
        config = GameConfig()
        assert config.BUNDLE_PRICES["premium_pack"] == 10.00
        assert config.BUNDLE_PRICES["starter_pack"] == 5.00
        assert config.BUNDLE_PRICES["coffee_boost"] == 1.99


class TestPlayerClasses:
    """Test player class configurations."""
    
    def test_all_classes_defined(self):
        """Test all 4 player classes are defined."""
        assert len(PLAYER_CLASSES) == 4
        assert "mage" in PLAYER_CLASSES
        assert "commando" in PLAYER_CLASSES
        assert "dimension_runner" in PLAYER_CLASSES
        assert "biotech_paladin" in PLAYER_CLASSES
    
    def test_mage_config(self):
        """Test Mage class configuration."""
        mage = PLAYER_CLASSES["mage"]
        assert mage.name == "Mage"
        assert mage.base_health == 80.0
        assert mage.base_damage == 15.0
        assert len(mage.abilities) == 4
        assert "fireball" in mage.abilities
    
    def test_commando_config(self):
        """Test Commando class configuration."""
        commando = PLAYER_CLASSES["commando"]
        assert commando.name == "Commando"
        assert commando.base_health == 120.0
        assert len(commando.abilities) == 4
    
    def test_upgrade_trees(self):
        """Test all classes have upgrade trees."""
        for class_name, class_config in PLAYER_CLASSES.items():
            assert len(class_config.upgrade_tree) >= 3


class TestZones:
    """Test zone configurations."""
    
    def test_zone_count(self):
        """Test correct number of zones."""
        assert len(ZONES) == 6
    
    def test_zone_themes(self):
        """Test zone themes are unique."""
        themes = [zone.theme for zone in ZONES]
        assert "fantasy" in themes
        assert "scifi" in themes
        assert "horror" in themes
        assert "mythic" in themes
        assert "alien" in themes
        assert "eldritch" in themes
    
    def test_difficulty_scaling(self):
        """Test zones have increasing difficulty."""
        difficulties = [zone.difficulty_multiplier for zone in ZONES]
        assert min(difficulties) == 1.0
        assert max(difficulties) == 1.5


class TestPlayer:
    """Test Player entity."""
    
    def test_player_creation(self):
        """Test creating a player."""
        player = Player(name="TestPlayer", player_class="commando")
        assert player.name == "TestPlayer"
        assert player.player_class == "commando"
        assert player.is_alive == True
        assert player.health == 100.0
    
    def test_player_with_class_stats(self):
        """Test player initialized with class stats."""
        config = PLAYER_CLASSES["mage"]
        player = Player(
            player_class="mage",
            max_health=config.base_health,
            health=config.base_health
        )
        assert player.max_health == 80.0
        assert player.health == 80.0
    
    def test_player_position(self):
        """Test player position."""
        player = Player()
        assert player.position.x == 0.0
        assert player.position.y == 0.0
        
        player.position = Vector2(100, 200)
        assert player.position.x == 100
        assert player.position.y == 200


class TestEnemy:
    """Test Enemy entity."""
    
    def test_enemy_creation(self):
        """Test creating an enemy."""
        enemy = Enemy(enemy_type="basic")
        assert enemy.enemy_type == "basic"
        assert enemy.health == 50.0
        assert enemy.ai_state == "patrol"
    
    def test_enemy_reward_drops(self):
        """Test enemy drops currency and XP."""
        enemy = Enemy(currency_drop=25, experience_drop=50)
        assert enemy.currency_drop == 25
        assert enemy.experience_drop == 50


class TestZoneEntity:
    """Test Zone entity."""
    
    def test_zone_creation(self):
        """Test creating a zone."""
        zone = Zone(name="Test Zone", theme="fantasy")
        assert zone.name == "Test Zone"
        assert zone.theme == "fantasy"
        assert zone.is_active == False
        assert zone.hold_progress == 0.0
    
    def test_zone_player_tracking(self):
        """Test zone tracks players."""
        zone = Zone()
        assert len(zone.players_in_zone) == 0
        
        zone.players_in_zone = ["player1", "player2"]
        assert len(zone.players_in_zone) == 2


class TestGameState:
    """Test GameState."""
    
    def test_game_state_initialization(self):
        """Test initializing game state."""
        state = GameState()
        assert len(state.players) == 0
        assert len(state.enemies) == 0
        assert len(state.zones) == 0
        assert state.current_wave == 1
        assert state.match_started == False
    
    def test_adding_players(self):
        """Test adding players to game state."""
        state = GameState()
        player = Player(name="Player1")
        state.players[player.id] = player
        
        assert len(state.players) == 1
        assert player.id in state.players


class TestWaveManager:
    """Test WaveManager system."""
    
    def test_wave_manager_initialization(self):
        """Test wave manager setup."""
        state = GameState()
        wave_mgr = WaveManager(state)
        
        assert wave_mgr.current_wave == 1
        assert wave_mgr.wave_active == False
        assert wave_mgr.base_enemy_count == 10
    
    def test_wave_start(self):
        """Test starting a wave."""
        state = GameState()
        
        # Create a zone
        zone = Zone(name="Test Zone", is_active=True)
        state.zones[zone.id] = zone
        state.active_zone_id = zone.id
        
        wave_mgr = WaveManager(state)
        wave_mgr.start_wave()
        
        assert wave_mgr.wave_active == True
        assert state.current_wave == 2
        assert state.enemies_remaining > 0
        assert len(state.enemies) > 0
    
    def test_enemy_scaling(self):
        """Test enemy difficulty scaling."""
        state = GameState()
        zone = Zone(is_active=True)
        state.zones[zone.id] = zone
        state.active_zone_id = zone.id
        
        wave_mgr = WaveManager(state)
        
        # Start wave 1
        wave_mgr.start_wave()
        wave_1_count = len(state.enemies)
        
        # Clear enemies and start wave 2
        state.enemies.clear()
        wave_mgr.complete_wave()
        wave_mgr.start_wave()
        wave_2_count = len(state.enemies)
        
        # Wave 2 should have more enemies
        assert wave_2_count > wave_1_count


class TestZoneManager:
    """Test ZoneManager system."""
    
    def test_zone_manager_initialization(self):
        """Test zone manager setup."""
        state = GameState()
        zone_mgr = ZoneManager(state)
        
        # Should create 6 zones
        assert len(state.zones) == 6
        
        # One zone should be active
        active_zones = [z for z in state.zones.values() if z.is_active]
        assert len(active_zones) == 1
    
    def test_zone_hold_progress(self):
        """Test zone hold progress calculation."""
        state = GameState()
        zone_mgr = ZoneManager(state)
        
        # Get active zone
        active_zone = [z for z in state.zones.values() if z.is_active][0]
        
        # Add player to zone
        player = Player(position=active_zone.position, is_alive=True)
        state.players[player.id] = player
        
        # Update for 1 second
        zone_mgr.update(1.0)
        
        # Progress should increase
        assert active_zone.hold_progress > 0


class TestMarketplace:
    """Test Marketplace system."""
    
    def test_marketplace_initialization(self):
        """Test marketplace has items."""
        marketplace = Marketplace()
        assert len(marketplace.items) > 0
    
    def test_get_item(self):
        """Test getting item by ID."""
        marketplace = Marketplace()
        item = marketplace.get_item("premium_pack_01")
        
        assert item is not None
        assert item.name == "Ultimate Warrior Pack"
        assert item.price == 10.00
    
    def test_get_available_items(self):
        """Test filtering by player level."""
        marketplace = Marketplace()
        
        # Level 0 player
        items_lvl0 = marketplace.get_available_items(player_level=0)
        
        # Level 10 player
        items_lvl10 = marketplace.get_available_items(player_level=10)
        
        # Higher level should have more items
        assert len(items_lvl10) >= len(items_lvl0)
    
    def test_get_items_by_type(self):
        """Test filtering by item type."""
        marketplace = Marketplace()
        
        bundles = marketplace.get_items_by_type(ItemType.BUNDLE, player_level=10)
        skins = marketplace.get_items_by_type(ItemType.CHARACTER_SKIN, player_level=10)
        
        assert len(bundles) > 0
        assert len(skins) > 0
        
        # Check all bundles are correct type
        for item in bundles:
            assert item.item_type == ItemType.BUNDLE
    
    def test_purchase_validation(self):
        """Test purchase validation."""
        marketplace = Marketplace()
        
        # Valid purchase
        success, msg = marketplace.purchase_item("coffee_boost_xp", player_level=1)
        assert success == True
        
        # Invalid - level too low
        success, msg = marketplace.purchase_item("skin_mage_archmage", player_level=1)
        assert success == False
        assert "Requires level" in msg


class TestSquad:
    """Test Squad entity."""
    
    def test_squad_creation(self):
        """Test creating a squad."""
        squad = Squad(name="Alpha Squad")
        assert squad.name == "Alpha Squad"
        assert len(squad.member_ids) == 0
        assert squad.squad_level == 1
    
    def test_squad_members(self):
        """Test adding members to squad."""
        squad = Squad()
        squad.member_ids = ["player1", "player2", "player3"]
        
        assert len(squad.member_ids) == 3


@pytest.mark.asyncio
async def test_async_game_loop():
    """Test async game loop can run."""
    from app.survival_shooter.server import GameServer
    
    server = GameServer()
    
    # Simulate one update
    await server._update(0.016)  # 16ms = 1/60 second
    
    assert server.game_state.game_time >= 0


def test_player_classes_balance():
    """Test player classes are balanced."""
    total_stats = {}
    
    for class_name, config in PLAYER_CLASSES.items():
        # Calculate total stat points
        total = config.base_health + config.base_damage + config.movement_speed
        total_stats[class_name] = total
    
    # Check variance isn't too high
    stats_list = list(total_stats.values())
    avg_stats = sum(stats_list) / len(stats_list)
    max_deviation = max(abs(s - avg_stats) for s in stats_list)
    
    # Max 20% deviation from average for balance
    assert max_deviation / avg_stats < 0.2


def test_marketplace_pricing():
    """Test marketplace has proper pricing tiers."""
    marketplace = Marketplace()
    
    premium_items = [i for i in marketplace.items.values() if i.price >= 10.00]
    starter_items = [i for i in marketplace.items.values() if 4.00 <= i.price < 10.00]
    coffee_items = [i for i in marketplace.items.values() if 1.50 <= i.price < 2.50]
    micro_items = [i for i in marketplace.items.values() if i.price < 1.00]
    
    # Should have items in each tier
    assert len(premium_items) > 0
    assert len(coffee_items) > 0
    assert len(micro_items) > 0
