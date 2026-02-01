"""
Core game engine with Entity Component System architecture.
Provides the foundation for a scalable, performant game.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Set, Type, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import time


class Component:
    """Base class for all components in the ECS system."""
    pass


class System(ABC):
    """Base class for all systems that process components."""
    
    def __init__(self):
        self.enabled = True
    
    @abstractmethod
    def update(self, entities: List['Entity'], delta_time: float) -> None:
        """Update all entities with required components."""
        pass


class Entity:
    """Entity in the ECS system. Just an ID with attached components."""
    
    _next_id = 0
    
    def __init__(self, name: str = ""):
        self.id = Entity._next_id
        Entity._next_id += 1
        self.name = name or f"Entity_{self.id}"
        self.components: Dict[Type[Component], Component] = {}
        self.active = True
    
    def add_component(self, component: Component) -> 'Entity':
        """Add a component to this entity."""
        self.components[type(component)] = component
        return self
    
    def get_component(self, component_type: Type[Component]) -> Optional[Component]:
        """Get a component of the specified type."""
        return self.components.get(component_type)
    
    def has_component(self, component_type: Type[Component]) -> bool:
        """Check if entity has a component of the specified type."""
        return component_type in self.components
    
    def remove_component(self, component_type: Type[Component]) -> None:
        """Remove a component from this entity."""
        self.components.pop(component_type, None)


class World:
    """Manages all entities and systems in the game."""
    
    def __init__(self):
        self.entities: List[Entity] = []
        self.systems: List[System] = []
        self._entities_to_remove: Set[int] = set()
    
    def create_entity(self, name: str = "") -> Entity:
        """Create and register a new entity."""
        entity = Entity(name)
        self.entities.append(entity)
        return entity
    
    def remove_entity(self, entity: Entity) -> None:
        """Mark entity for removal at end of frame."""
        self._entities_to_remove.add(entity.id)
    
    def add_system(self, system: System) -> None:
        """Register a system."""
        self.systems.append(system)
    
    def update(self, delta_time: float) -> None:
        """Update all systems."""
        # Update systems
        for system in self.systems:
            if system.enabled:
                system.update([e for e in self.entities if e.active], delta_time)
        
        # Remove marked entities
        if self._entities_to_remove:
            self.entities = [e for e in self.entities if e.id not in self._entities_to_remove]
            self._entities_to_remove.clear()
    
    def find_entities_with(self, *component_types: Type[Component]) -> List[Entity]:
        """Find all entities that have all specified components."""
        return [e for e in self.entities 
                if e.active and all(e.has_component(ct) for ct in component_types)]


class GameState(Enum):
    """Game states."""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


@dataclass
class GameConfig:
    """Configuration for the game."""
    target_fps: int = 60
    fixed_timestep: float = 1.0 / 60.0
    window_width: int = 1280
    window_height: int = 720
    title: str = "Thirsty's Game"
    max_frame_time: float = 0.25  # Prevent spiral of death


class GameEngine:
    """
    Core game engine with fixed timestep game loop.
    Manages the world, systems, and game state.
    """
    
    def __init__(self, config: GameConfig = None):
        self.config = config or GameConfig()
        self.world = World()
        self.state = GameState.MENU
        self.running = False
        self.paused = False
        
        # Time tracking
        self.current_time = time.time()
        self.accumulator = 0.0
        self.frame_count = 0
        self.fps = 0.0
        self.last_fps_update = time.time()
        
        # Event system
        self.event_listeners: Dict[str, List[callable]] = {}
    
    def subscribe(self, event_name: str, callback: callable) -> None:
        """Subscribe to an event."""
        if event_name not in self.event_listeners:
            self.event_listeners[event_name] = []
        self.event_listeners[event_name].append(callback)
    
    def emit(self, event_name: str, **kwargs) -> None:
        """Emit an event to all subscribers."""
        if event_name in self.event_listeners:
            for callback in self.event_listeners[event_name]:
                callback(**kwargs)
    
    def add_system(self, system: System) -> None:
        """Add a system to the world."""
        self.world.add_system(system)
    
    def create_entity(self, name: str = "") -> Entity:
        """Create a new entity in the world."""
        return self.world.create_entity(name)
    
    def update(self) -> None:
        """
        Update game logic with fixed timestep.
        Uses accumulator pattern to ensure consistent physics.
        """
        new_time = time.time()
        frame_time = new_time - self.current_time
        
        # Prevent spiral of death
        if frame_time > self.config.max_frame_time:
            frame_time = self.config.max_frame_time
        
        self.current_time = new_time
        self.accumulator += frame_time
        
        # Fixed timestep updates
        while self.accumulator >= self.config.fixed_timestep:
            if not self.paused:
                self.world.update(self.config.fixed_timestep)
                self.emit("update", delta_time=self.config.fixed_timestep)
            self.accumulator -= self.config.fixed_timestep
        
        # Update FPS counter
        self.frame_count += 1
        if new_time - self.last_fps_update >= 1.0:
            self.fps = self.frame_count
            self.frame_count = 0
            self.last_fps_update = new_time
    
    def change_state(self, new_state: GameState) -> None:
        """Change game state."""
        old_state = self.state
        self.state = new_state
        self.emit("state_changed", old_state=old_state, new_state=new_state)
    
    def start(self) -> None:
        """Start the game engine."""
        self.running = True
        self.current_time = time.time()
        self.emit("game_start")
    
    def stop(self) -> None:
        """Stop the game engine."""
        self.running = False
        self.emit("game_stop")
    
    def toggle_pause(self) -> None:
        """Toggle pause state."""
        self.paused = not self.paused
        self.emit("pause_toggled", paused=self.paused)
