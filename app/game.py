"""
Main game class with Pygame rendering.
Implements the addictive incremental game mechanics.
"""
import sys
import random
import math
from typing import Optional, Tuple
from dataclasses import dataclass

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Pygame not available. Running in headless mode.")

from app.engine import GameEngine, GameConfig, GameState, Entity
from app.components import (
    Transform, ResourceProducer, ResourceConverter, ClickGenerator,
    Upgrade, Achievement, Particle, Visual, Clickable, GameResources, Stats
)
from app.systems import (
    ResourceProductionSystem, ResourceConversionSystem, ParticleSystem,
    CooldownSystem, StatsTrackingSystem, AchievementSystem
)


@dataclass
class Theme:
    """Visual theme for the game."""
    primary: Tuple[int, int, int] = (26, 188, 156)  # Turquoise
    secondary: Tuple[int, int, int] = (52, 152, 219)  # Blue
    accent: Tuple[int, int, int] = (230, 126, 34)  # Orange
    background: Tuple[int, int, int] = (44, 62, 80)  # Dark blue-grey
    text: Tuple[int, int, int] = (236, 240, 241)  # Light grey
    success: Tuple[int, int, int] = (46, 204, 113)  # Green
    warning: Tuple[int, int, int] = (241, 196, 15)  # Yellow
    danger: Tuple[int, int, int] = (231, 76, 60)  # Red


class ThirstysGame:
    """
    Main game class implementing God-tier addictive mechanics.
    Features:
    - Incremental/idle gameplay
    - Multiple resource types with conversions
    - Click-based and passive generation
    - Achievement system
    - Upgrade tree
    - Beautiful visual effects
    """
    
    def __init__(self, headless: bool = False):
        """Initialize the game."""
        self.headless = headless or not PYGAME_AVAILABLE
        
        # Game configuration
        config = GameConfig(
            title="Thirsty's Game - Energy Empire",
            window_width=1280,
            window_height=720,
            target_fps=60
        )
        
        # Initialize engine
        self.engine = GameEngine(config)
        self.theme = Theme()
        
        # Pygame setup
        if not self.headless:
            pygame.init()
            self.screen = pygame.display.set_mode((config.window_width, config.window_height))
            pygame.display.set_caption(config.title)
            self.clock = pygame.time.Clock()
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)
        
        # Core entities
        self.resources_entity: Optional[Entity] = None
        self.stats_entity: Optional[Entity] = None
        self.click_generator_entity: Optional[Entity] = None
        
        # Entity lists for quick access
        self.producer_entities = []
        self.converter_entities = []
        self.upgrade_entities = []
        self.achievement_entities = []
        
        # UI state
        self.selected_tab = "main"  # main, upgrades, achievements, stats
        
        self._setup_game()
    
    def _setup_game(self):
        """Set up the game entities and systems."""
        # Create main resource pool
        self.resources_entity = self.engine.create_entity("Resources")
        self.resources_entity.add_component(GameResources(
            energy=10.0,
            crystals=0.0,
            essence=0.0
        ))
        
        # Create stats tracker
        self.stats_entity = self.engine.create_entity("Stats")
        self.stats_entity.add_component(Stats())
        
        # Create click generator
        self.click_generator_entity = self.engine.create_entity("ClickGenerator")
        self.click_generator_entity.add_component(ClickGenerator(
            resource_type="energy",
            amount=1.0,
            multiplier=1.0,
            critical_chance=0.1,
            critical_multiplier=2.0
        ))
        if not self.headless:
            self.click_generator_entity.add_component(Transform(x=640, y=360))
            self.click_generator_entity.add_component(Visual(
                color=self.theme.primary,
                size=100.0,
                shape="circle"
            ))
            self.click_generator_entity.add_component(Clickable(radius=100.0))
        
        # Create producers
        self._create_producer("Solar Panel", "energy", 1.0, 10.0, 100, 200)
        self._create_producer("Wind Turbine", "energy", 5.0, 50.0, 300, 250)
        self._create_producer("Fusion Reactor", "energy", 25.0, 500.0, 500, 300)
        self._create_producer("Crystal Mine", "crystals", 0.1, 1000.0, 700, 350)
        
        # Create converters
        self._create_converter("Energy Crystallizer", "energy", "crystals", 100.0, 1.0, 200, 400)
        self._create_converter("Crystal Refinery", "crystals", "essence", 10.0, 1.0, 400, 450)
        
        # Create upgrades
        self._create_upgrade("Click Power I", "Double click power", 100, "energy", "click_multiplier", 2.0)
        self._create_upgrade("Click Power II", "Triple click power", 500, "energy", "click_multiplier", 3.0)
        self._create_upgrade("Production Boost I", "2x all production", 1000, "energy", "production_multiplier", 2.0)
        self._create_upgrade("Efficiency I", "Converters 50% more efficient", 5000, "crystals", "efficiency", 1.5)
        self._create_upgrade("Critical Strike", "20% crit chance", 10000, "crystals", "critical_chance", 0.2)
        
        # Create achievements
        self._create_achievement("First Steps", "Earn 100 energy", "resource_total", 100.0, "energy", "multiplier", 1.1, "energy")
        self._create_achievement("Energy Baron", "Earn 10,000 energy", "resource_total", 10000.0, "energy", "multiplier", 1.2, "energy")
        self._create_achievement("Clicker", "Click 100 times", "clicks", 100.0, "", "multiplier", 1.05, "global")
        self._create_achievement("Dedicated", "Play for 300 seconds", "play_time", 300.0, "", "multiplier", 1.1, "global")
        self._create_achievement("Crystal Collector", "Earn 100 crystals", "resource_total", 100.0, "crystals", "multiplier", 1.15, "crystal")
        
        # Add systems
        self.engine.add_system(ResourceProductionSystem(self.resources_entity))
        self.engine.add_system(ResourceConversionSystem(self.resources_entity))
        self.engine.add_system(ParticleSystem(self.engine.world))
        self.engine.add_system(CooldownSystem())
        self.engine.add_system(StatsTrackingSystem(self.stats_entity, self.resources_entity))
        self.engine.add_system(AchievementSystem(self.stats_entity, self.resources_entity, self.engine))
        
        # Subscribe to events
        self.engine.subscribe("achievement_unlocked", self._on_achievement_unlocked)
    
    def _create_producer(self, name: str, resource_type: str, base_rate: float, 
                        cost: float, x: int, y: int) -> Entity:
        """Create a producer entity."""
        entity = self.engine.create_entity(name)
        entity.add_component(ResourceProducer(
            resource_type=resource_type,
            base_rate=base_rate,
            multiplier=1.0,
            level=0,
            cost_base=cost,
            cost_multiplier=1.15
        ))
        if not self.headless:
            entity.add_component(Transform(x=x, y=y))
            entity.add_component(Visual(
                color=self.theme.secondary,
                size=40.0,
                shape="circle"
            ))
        self.producer_entities.append(entity)
        return entity
    
    def _create_converter(self, name: str, input_type: str, output_type: str,
                         input_rate: float, output_rate: float, x: int, y: int) -> Entity:
        """Create a converter entity."""
        entity = self.engine.create_entity(name)
        entity.add_component(ResourceConverter(
            input_type=input_type,
            output_type=output_type,
            input_rate=input_rate,
            output_rate=output_rate,
            efficiency=1.0,
            level=0,
            enabled=False
        ))
        if not self.headless:
            entity.add_component(Transform(x=x, y=y))
        self.converter_entities.append(entity)
        return entity
    
    def _create_upgrade(self, name: str, description: str, cost: float,
                       resource_type: str, effect_type: str, effect_value: float) -> Entity:
        """Create an upgrade entity."""
        entity = self.engine.create_entity(name)
        entity.add_component(Upgrade(
            name=name,
            description=description,
            cost=cost,
            resource_type=resource_type,
            purchased=False,
            effect_type=effect_type,
            effect_value=effect_value,
            target=""
        ))
        self.upgrade_entities.append(entity)
        return entity
    
    def _create_achievement(self, name: str, description: str, req_type: str,
                          req_value: float, target: str, reward_type: str,
                          reward_value: float, reward_target: str) -> Entity:
        """Create an achievement entity."""
        entity = self.engine.create_entity(name)
        achievement = Achievement(
            name=name,
            description=description,
            requirement_type=req_type,
            requirement_value=req_value,
            unlocked=False,
            reward_type=reward_type,
            reward_value=reward_value
        )
        achievement.target = target  # Add target attribute
        entity.add_component(achievement)
        self.achievement_entities.append(entity)
        return entity
    
    def _on_achievement_unlocked(self, name: str, description: str):
        """Handle achievement unlock."""
        print(f"🏆 Achievement Unlocked: {name} - {description}")
        if not self.headless:
            # Create particle effect
            self._create_particle_burst(640, 100, self.theme.success, 30)
    
    def _create_particle_burst(self, x: float, y: float, color: tuple, count: int = 20):
        """Create a burst of particles."""
        if self.headless:
            return
        
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 200)
            entity = self.engine.create_entity("Particle")
            entity.add_component(Transform(x=x, y=y))
            entity.add_component(Particle(
                lifetime=random.uniform(0.5, 1.5),
                velocity_x=math.cos(angle) * speed,
                velocity_y=math.sin(angle) * speed,
                color=color,
                size=random.uniform(3, 8),
                fade=True
            ))
    
    def handle_click(self, mouse_x: int, mouse_y: int):
        """Handle mouse click."""
        if self.headless:
            return
        
        # Check if clicking on main generator
        click_gen = self.click_generator_entity.get_component(ClickGenerator)
        transform = self.click_generator_entity.get_component(Transform)
        clickable = self.click_generator_entity.get_component(Clickable)
        
        if all([click_gen, transform, clickable]):
            # Check distance
            dx = mouse_x - transform.x
            dy = mouse_y - transform.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance <= clickable.radius and clickable.enabled:
                # Generate resources
                resources = self.resources_entity.get_component(GameResources)
                stats = self.stats_entity.get_component(Stats)
                
                # Check for critical hit
                is_crit = random.random() < click_gen.critical_chance
                multiplier = click_gen.critical_multiplier if is_crit else 1.0
                amount = click_gen.click_value * multiplier
                
                resources.add_resource(click_gen.resource_type, amount)
                stats.total_clicks += 1
                stats.total_energy_earned += amount
                
                # Visual feedback
                color = self.theme.warning if is_crit else self.theme.primary
                self._create_particle_burst(mouse_x, mouse_y, color, 15 if is_crit else 10)
                
                # Cooldown (minimal)
                clickable.cooldown = 0.05
    
    def purchase_producer(self, index: int):
        """Purchase or upgrade a producer."""
        if index >= len(self.producer_entities):
            return
        
        entity = self.producer_entities[index]
        producer = entity.get_component(ResourceProducer)
        resources = self.resources_entity.get_component(GameResources)
        
        if producer and resources:
            cost = producer.upgrade_cost
            if resources.can_afford("energy", cost):
                resources.spend("energy", cost)
                producer.level += 1
                print(f"✅ Upgraded {entity.name} to level {producer.level}")
    
    def purchase_converter(self, index: int):
        """Purchase or upgrade a converter."""
        if index >= len(self.converter_entities):
            return
        
        entity = self.converter_entities[index]
        converter = entity.get_component(ResourceConverter)
        resources = self.resources_entity.get_component(GameResources)
        
        if converter and resources:
            if converter.level == 0:
                # Initial purchase
                cost = 1000.0
                if resources.can_afford("energy", cost):
                    resources.spend("energy", cost)
                    converter.level = 1
                    converter.enabled = True
                    print(f"✅ Unlocked {entity.name}")
            else:
                # Upgrade
                cost = 1000.0 * (1.2 ** converter.level)
                if resources.can_afford("energy", cost):
                    resources.spend("energy", cost)
                    converter.level += 1
                    print(f"✅ Upgraded {entity.name} to level {converter.level}")
    
    def purchase_upgrade(self, index: int):
        """Purchase an upgrade."""
        if index >= len(self.upgrade_entities):
            return
        
        entity = self.upgrade_entities[index]
        upgrade = entity.get_component(Upgrade)
        resources = self.resources_entity.get_component(GameResources)
        stats = self.stats_entity.get_component(Stats)
        
        if upgrade and resources and not upgrade.purchased:
            if resources.can_afford(upgrade.resource_type, upgrade.cost):
                resources.spend(upgrade.resource_type, upgrade.cost)
                upgrade.purchased = True
                stats.upgrades_purchased += 1
                
                # Apply upgrade effect
                self._apply_upgrade(upgrade)
                print(f"✅ Purchased {upgrade.name}")
    
    def _apply_upgrade(self, upgrade: Upgrade):
        """Apply upgrade effects."""
        if upgrade.effect_type == "click_multiplier":
            click_gen = self.click_generator_entity.get_component(ClickGenerator)
            if click_gen:
                click_gen.multiplier *= upgrade.effect_value
        
        elif upgrade.effect_type == "production_multiplier":
            for entity in self.producer_entities:
                producer = entity.get_component(ResourceProducer)
                if producer:
                    producer.multiplier *= upgrade.effect_value
        
        elif upgrade.effect_type == "efficiency":
            for entity in self.converter_entities:
                converter = entity.get_component(ResourceConverter)
                if converter:
                    converter.efficiency *= upgrade.effect_value
        
        elif upgrade.effect_type == "critical_chance":
            click_gen = self.click_generator_entity.get_component(ClickGenerator)
            if click_gen:
                click_gen.critical_chance += upgrade.effect_value
    
    def run(self):
        """Main game loop."""
        if self.headless:
            self._run_headless()
        else:
            self._run_with_display()
    
    def _run_headless(self):
        """Run in headless mode for testing."""
        self.engine.start()
        print("Running in headless mode. Press Ctrl+C to stop.")
        
        try:
            import time
            while self.engine.running:
                self.engine.update()
                time.sleep(1.0 / 60.0)  # Simulate 60 FPS
        except KeyboardInterrupt:
            print("\nStopping game...")
        
        self.engine.stop()
    
    def _run_with_display(self):
        """Run with Pygame display."""
        self.engine.start()
        self.engine.change_state(GameState.PLAYING)
        
        while self.engine.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.engine.stop()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(*event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.engine.stop()
                    elif event.key == pygame.K_1:
                        self.selected_tab = "main"
                    elif event.key == pygame.K_2:
                        self.selected_tab = "upgrades"
                    elif event.key == pygame.K_3:
                        self.selected_tab = "achievements"
                    elif event.key == pygame.K_4:
                        self.selected_tab = "stats"
                    elif event.key == pygame.K_p:
                        self.engine.toggle_pause()
                    # Quick purchase hotkeys
                    elif event.key == pygame.K_q:
                        self.purchase_producer(0)
                    elif event.key == pygame.K_w:
                        self.purchase_producer(1)
                    elif event.key == pygame.K_e:
                        self.purchase_producer(2)
                    elif event.key == pygame.K_r:
                        self.purchase_producer(3)
            
            # Update game logic
            self.engine.update()
            
            # Render
            self._render()
            
            # Control framerate
            self.clock.tick(self.engine.config.target_fps)
        
        pygame.quit()
    
    def _render(self):
        """Render the game."""
        if self.headless:
            return
        
        # Clear screen
        self.screen.fill(self.theme.background)
        
        # Render based on selected tab
        if self.selected_tab == "main":
            self._render_main_screen()
        elif self.selected_tab == "upgrades":
            self._render_upgrades_screen()
        elif self.selected_tab == "achievements":
            self._render_achievements_screen()
        elif self.selected_tab == "stats":
            self._render_stats_screen()
        
        # Render tab bar
        self._render_tab_bar()
        
        # Render resource display
        self._render_resource_display()
        
        # Render FPS
        self._render_fps()
        
        pygame.display.flip()
    
    def _render_main_screen(self):
        """Render main game screen."""
        # Render click generator
        transform = self.click_generator_entity.get_component(Transform)
        visual = self.click_generator_entity.get_component(Visual)
        
        if transform and visual:
            pygame.draw.circle(self.screen, visual.color, 
                             (int(transform.x), int(transform.y)), 
                             int(visual.size))
            
            # Render "CLICK ME" text
            text = self.font_medium.render("CLICK ME!", True, self.theme.text)
            text_rect = text.get_rect(center=(int(transform.x), int(transform.y)))
            self.screen.blit(text, text_rect)
        
        # Render producers
        y_offset = 100
        for i, entity in enumerate(self.producer_entities):
            producer = entity.get_component(ResourceProducer)
            if producer:
                # Background
                pygame.draw.rect(self.screen, (60, 80, 100), 
                               (20, y_offset, 300, 60), border_radius=5)
                
                # Name and level
                name_text = self.font_small.render(
                    f"{entity.name} (Lv{producer.level})", True, self.theme.text)
                self.screen.blit(name_text, (30, y_offset + 5))
                
                # Rate
                rate_text = self.font_small.render(
                    f"+{producer.production_rate:.1f}/s", True, self.theme.success)
                self.screen.blit(rate_text, (30, y_offset + 30))
                
                # Cost
                cost_text = self.font_small.render(
                    f"Cost: {self._format_number(producer.upgrade_cost)}", 
                    True, self.theme.warning)
                self.screen.blit(cost_text, (180, y_offset + 30))
                
                # Hotkey
                if i < 4:
                    hotkey = ['Q', 'W', 'E', 'R'][i]
                    hotkey_text = self.font_small.render(f"[{hotkey}]", True, self.theme.accent)
                    self.screen.blit(hotkey_text, (290, y_offset + 20))
                
                y_offset += 70
        
        # Render particles
        for entity in self.engine.world.entities:
            particle = entity.get_component(Particle)
            transform = entity.get_component(Transform)
            if particle and transform:
                pygame.draw.circle(self.screen, particle.color,
                                 (int(transform.x), int(transform.y)),
                                 int(particle.size))
    
    def _render_upgrades_screen(self):
        """Render upgrades screen."""
        title = self.font_large.render("UPGRADES", True, self.theme.text)
        self.screen.blit(title, (500, 100))
        
        y_offset = 180
        for entity in self.upgrade_entities:
            upgrade = entity.get_component(Upgrade)
            if upgrade:
                color = (80, 100, 120) if upgrade.purchased else (60, 80, 100)
                pygame.draw.rect(self.screen, color, 
                               (350, y_offset, 600, 70), border_radius=5)
                
                # Name
                name_text = self.font_medium.render(upgrade.name, True, self.theme.text)
                self.screen.blit(name_text, (360, y_offset + 5))
                
                # Description
                desc_text = self.font_small.render(upgrade.description, True, self.theme.text)
                self.screen.blit(desc_text, (360, y_offset + 35))
                
                # Cost or Purchased
                if upgrade.purchased:
                    status_text = self.font_small.render("PURCHASED", True, self.theme.success)
                else:
                    status_text = self.font_small.render(
                        f"{self._format_number(upgrade.cost)} {upgrade.resource_type}",
                        True, self.theme.warning)
                self.screen.blit(status_text, (750, y_offset + 25))
                
                y_offset += 80
    
    def _render_achievements_screen(self):
        """Render achievements screen."""
        title = self.font_large.render("ACHIEVEMENTS", True, self.theme.text)
        self.screen.blit(title, (450, 100))
        
        y_offset = 180
        for entity in self.achievement_entities:
            achievement = entity.get_component(Achievement)
            if achievement:
                color = self.theme.success if achievement.unlocked else (60, 80, 100)
                pygame.draw.rect(self.screen, color, 
                               (300, y_offset, 680, 60), border_radius=5)
                
                # Icon
                icon = "🏆" if achievement.unlocked else "🔒"
                icon_text = self.font_medium.render(icon, True, self.theme.text)
                self.screen.blit(icon_text, (310, y_offset + 10))
                
                # Name
                name_text = self.font_medium.render(achievement.name, True, self.theme.text)
                self.screen.blit(name_text, (350, y_offset + 5))
                
                # Description
                desc_text = self.font_small.render(achievement.description, True, self.theme.text)
                self.screen.blit(desc_text, (350, y_offset + 35))
                
                y_offset += 70
    
    def _render_stats_screen(self):
        """Render statistics screen."""
        title = self.font_large.render("STATISTICS", True, self.theme.text)
        self.screen.blit(title, (480, 100))
        
        stats = self.stats_entity.get_component(Stats)
        if stats:
            y_offset = 200
            stats_data = [
                ("Total Clicks", f"{stats.total_clicks:,}"),
                ("Total Energy Earned", self._format_number(stats.total_energy_earned)),
                ("Total Crystals Earned", self._format_number(stats.total_crystals_earned)),
                ("Play Time", f"{int(stats.play_time)}s"),
                ("Upgrades Purchased", str(stats.upgrades_purchased)),
                ("Achievements Unlocked", f"{stats.achievements_unlocked}/{len(self.achievement_entities)}"),
            ]
            
            for label, value in stats_data:
                # Label
                label_text = self.font_medium.render(label, True, self.theme.text)
                self.screen.blit(label_text, (350, y_offset))
                
                # Value
                value_text = self.font_medium.render(value, True, self.theme.accent)
                self.screen.blit(value_text, (750, y_offset))
                
                y_offset += 50
    
    def _render_tab_bar(self):
        """Render tab navigation."""
        tabs = [
            ("1: Main", "main"),
            ("2: Upgrades", "upgrades"),
            ("3: Achievements", "achievements"),
            ("4: Stats", "stats")
        ]
        
        x_offset = 20
        for label, tab_id in tabs:
            color = self.theme.primary if self.selected_tab == tab_id else (80, 100, 120)
            pygame.draw.rect(self.screen, color, (x_offset, 20, 150, 40), border_radius=5)
            
            text = self.font_small.render(label, True, self.theme.text)
            text_rect = text.get_rect(center=(x_offset + 75, 40))
            self.screen.blit(text, text_rect)
            
            x_offset += 160
    
    def _render_resource_display(self):
        """Render current resources."""
        resources = self.resources_entity.get_component(GameResources)
        if resources:
            y_offset = 20
            resource_data = [
                ("Energy", resources.energy, self.theme.primary),
                ("Crystals", resources.crystals, self.theme.secondary),
                ("Essence", resources.essence, self.theme.accent),
            ]
            
            for name, amount, color in resource_data:
                text = self.font_medium.render(
                    f"{name}: {self._format_number(amount)}", True, color)
                text_rect = text.get_rect(topright=(1260, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 35
    
    def _render_fps(self):
        """Render FPS counter."""
        fps_text = self.font_small.render(f"FPS: {int(self.engine.fps)}", 
                                         True, self.theme.text)
        self.screen.blit(fps_text, (1200, 680))
    
    def _format_number(self, num: float) -> str:
        """Format large numbers with suffixes."""
        if num < 1000:
            return f"{num:.1f}"
        elif num < 1000000:
            return f"{num/1000:.1f}K"
        elif num < 1000000000:
            return f"{num/1000000:.1f}M"
        else:
            return f"{num/1000000000:.1f}B"


def main():
    """Entry point for the game."""
    print("=" * 60)
    print("  THIRSTY'S GAME - ENERGY EMPIRE")
    print("  God-Tier Incremental Game")
    print("=" * 60)
    print()
    print("Controls:")
    print("  - Click the center circle to generate energy")
    print("  - Press Q/W/E/R to purchase producers")
    print("  - Press 1/2/3/4 to switch tabs")
    print("  - Press P to pause")
    print("  - Press ESC to quit")
    print()
    
    # Check if running in headless mode
    headless = not PYGAME_AVAILABLE or "--headless" in sys.argv
    
    game = ThirstysGame(headless=headless)
    game.run()


if __name__ == "__main__":
    main()
