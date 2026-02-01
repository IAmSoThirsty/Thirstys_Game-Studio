"""
Tests for the game engine core components.
"""
import pytest
from app.engine import (
    Component, System, Entity, World, GameEngine, GameConfig, GameState
)


def test_entity_creation():
    """Test entity creation and component management."""
    entity = Entity("TestEntity")
    
    assert entity.name == "TestEntity"
    assert entity.active is True
    assert len(entity.components) == 0


def test_entity_components():
    """Test adding and retrieving components."""
    
    class TestComponent(Component):
        def __init__(self, value):
            self.value = value
    
    entity = Entity("Test")
    component = TestComponent(42)
    
    entity.add_component(component)
    
    assert entity.has_component(TestComponent)
    retrieved = entity.get_component(TestComponent)
    assert retrieved is not None
    assert retrieved.value == 42


def test_world_entity_management():
    """Test world entity creation and removal."""
    world = World()
    
    entity1 = world.create_entity("Entity1")
    entity2 = world.create_entity("Entity2")
    
    assert len(world.entities) == 2
    assert entity1 in world.entities
    assert entity2 in world.entities
    
    world.remove_entity(entity1)
    world.update(0.016)  # Trigger cleanup
    
    assert len(world.entities) == 1
    assert entity2 in world.entities


def test_world_find_entities():
    """Test finding entities by components."""
    
    class CompA(Component):
        pass
    
    class CompB(Component):
        pass
    
    world = World()
    
    e1 = world.create_entity("E1")
    e1.add_component(CompA())
    
    e2 = world.create_entity("E2")
    e2.add_component(CompA())
    e2.add_component(CompB())
    
    e3 = world.create_entity("E3")
    e3.add_component(CompB())
    
    # Find entities with CompA
    with_a = world.find_entities_with(CompA)
    assert len(with_a) == 2
    assert e1 in with_a
    assert e2 in with_a
    
    # Find entities with both CompA and CompB
    with_both = world.find_entities_with(CompA, CompB)
    assert len(with_both) == 1
    assert e2 in with_both


def test_system_update():
    """Test system processing entities."""
    
    class TestComponent(Component):
        def __init__(self):
            self.value = 0
    
    class TestSystem(System):
        def update(self, entities, delta_time):
            for entity in entities:
                comp = entity.get_component(TestComponent)
                if comp:
                    comp.value += 1
    
    world = World()
    system = TestSystem()
    world.add_system(system)
    
    e1 = world.create_entity("E1")
    e1.add_component(TestComponent())
    
    e2 = world.create_entity("E2")
    e2.add_component(TestComponent())
    
    # Update once
    world.update(0.016)
    
    assert e1.get_component(TestComponent).value == 1
    assert e2.get_component(TestComponent).value == 1
    
    # Update again
    world.update(0.016)
    
    assert e1.get_component(TestComponent).value == 2
    assert e2.get_component(TestComponent).value == 2


def test_game_engine_initialization():
    """Test game engine initialization."""
    config = GameConfig(target_fps=60)
    engine = GameEngine(config)
    
    assert engine.config.target_fps == 60
    assert engine.state == GameState.MENU
    assert engine.running is False
    assert engine.paused is False


def test_game_engine_entity_creation():
    """Test entity creation through engine."""
    engine = GameEngine()
    
    entity = engine.create_entity("TestEntity")
    
    assert entity.name == "TestEntity"
    assert entity in engine.world.entities


def test_game_engine_events():
    """Test event system."""
    engine = GameEngine()
    
    event_triggered = {"value": False, "data": None}
    
    def callback(**kwargs):
        event_triggered["value"] = True
        event_triggered["data"] = kwargs
    
    engine.subscribe("test_event", callback)
    engine.emit("test_event", test_data="hello")
    
    assert event_triggered["value"] is True
    assert event_triggered["data"]["test_data"] == "hello"


def test_game_engine_state_change():
    """Test game state changes."""
    engine = GameEngine()
    
    state_changed = {"old": None, "new": None}
    
    def on_state_change(old_state, new_state):
        state_changed["old"] = old_state
        state_changed["new"] = new_state
    
    engine.subscribe("state_changed", on_state_change)
    
    engine.change_state(GameState.PLAYING)
    
    assert engine.state == GameState.PLAYING
    assert state_changed["old"] == GameState.MENU
    assert state_changed["new"] == GameState.PLAYING


def test_game_engine_update():
    """Test game engine update loop."""
    
    class CounterComponent(Component):
        def __init__(self):
            self.count = 0
    
    class CounterSystem(System):
        def update(self, entities, delta_time):
            for entity in entities:
                comp = entity.get_component(CounterComponent)
                if comp:
                    comp.count += 1
    
    engine = GameEngine()
    engine.start()  # Initialize timing
    entity = engine.create_entity("Counter")
    entity.add_component(CounterComponent())
    engine.add_system(CounterSystem())
    
    # Update several times with actual time passing
    import time
    for _ in range(5):
        time.sleep(0.02)  # Sleep to simulate time passing
        engine.update()
    
    comp = entity.get_component(CounterComponent)
    assert comp.count > 0  # Should have updated at least once


def test_game_engine_pause():
    """Test pause functionality."""
    engine = GameEngine()
    
    pause_state = {"paused": None}
    
    def on_pause(paused):
        pause_state["paused"] = paused
    
    engine.subscribe("pause_toggled", on_pause)
    
    engine.toggle_pause()
    assert engine.paused is True
    assert pause_state["paused"] is True
    
    engine.toggle_pause()
    assert engine.paused is False
    assert pause_state["paused"] is False


def test_system_enable_disable():
    """Test enabling and disabling systems."""
    
    class TestComponent(Component):
        def __init__(self):
            self.value = 0
    
    class TestSystem(System):
        def update(self, entities, delta_time):
            for entity in entities:
                comp = entity.get_component(TestComponent)
                if comp:
                    comp.value += 1
    
    world = World()
    system = TestSystem()
    world.add_system(system)
    
    entity = world.create_entity("Test")
    entity.add_component(TestComponent())
    
    # Update with system enabled
    world.update(0.016)
    assert entity.get_component(TestComponent).value == 1
    
    # Disable system
    system.enabled = False
    world.update(0.016)
    assert entity.get_component(TestComponent).value == 1  # No change
    
    # Re-enable system
    system.enabled = True
    world.update(0.016)
    assert entity.get_component(TestComponent).value == 2
