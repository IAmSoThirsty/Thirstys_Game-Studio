"""
Save/load system for game state persistence.
"""
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime


class SaveSystem:
    """
    Handles saving and loading game state.
    Stores player progress between sessions.
    """
    
    def __init__(self, save_dir: str = "saves"):
        self.save_dir = save_dir
        self.save_file = os.path.join(save_dir, "savegame.json")
        
        # Create save directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def save_game(self, game_state: Dict[str, Any]) -> bool:
        """
        Save game state to file.
        
        Args:
            game_state: Dictionary containing game state
            
        Returns:
            True if save successful, False otherwise
        """
        try:
            # Add metadata
            save_data = {
                "version": "1.0",
                "timestamp": datetime.now().isoformat(),
                "state": game_state
            }
            
            # Write to file
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            print(f"✅ Game saved to {self.save_file}")
            return True
        
        except Exception as e:
            print(f"❌ Error saving game: {e}")
            return False
    
    def load_game(self) -> Optional[Dict[str, Any]]:
        """
        Load game state from file.
        
        Returns:
            Game state dictionary or None if load failed
        """
        try:
            if not os.path.exists(self.save_file):
                print("ℹ️  No save file found")
                return None
            
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
            
            print(f"✅ Game loaded from {self.save_file}")
            return save_data.get("state")
        
        except Exception as e:
            print(f"❌ Error loading game: {e}")
            return None
    
    def has_save(self) -> bool:
        """Check if a save file exists."""
        return os.path.exists(self.save_file)
    
    def delete_save(self) -> bool:
        """Delete the save file."""
        try:
            if os.path.exists(self.save_file):
                os.remove(self.save_file)
                print("✅ Save file deleted")
                return True
            return False
        except Exception as e:
            print(f"❌ Error deleting save: {e}")
            return False


def serialize_game_state(game) -> Dict[str, Any]:
    """
    Convert game state to serializable dictionary.
    
    Args:
        game: ThirstysGame instance
        
    Returns:
        Dictionary containing game state
    """
    from app.components import (
        GameResources, Stats, ResourceProducer, ResourceConverter, 
        ClickGenerator, Upgrade, Achievement
    )
    
    # Get core components
    resources = game.resources_entity.get_component(GameResources)
    stats = game.stats_entity.get_component(Stats)
    click_gen = game.click_generator_entity.get_component(ClickGenerator)
    
    state = {
        "resources": {
            "energy": resources.energy,
            "crystals": resources.crystals,
            "essence": resources.essence,
            "prestige_points": resources.prestige_points,
            "energy_multiplier": resources.energy_multiplier,
            "crystal_multiplier": resources.crystal_multiplier,
            "essence_multiplier": resources.essence_multiplier,
            "global_multiplier": resources.global_multiplier,
        },
        "stats": stats.to_dict(),
        "click_generator": {
            "amount": click_gen.amount,
            "multiplier": click_gen.multiplier,
            "critical_chance": click_gen.critical_chance,
            "critical_multiplier": click_gen.critical_multiplier,
        },
        "producers": [],
        "converters": [],
        "upgrades": [],
        "achievements": []
    }
    
    # Save producers
    for entity in game.producer_entities:
        producer = entity.get_component(ResourceProducer)
        if producer:
            state["producers"].append({
                "name": entity.name,
                "resource_type": producer.resource_type,
                "base_rate": producer.base_rate,
                "multiplier": producer.multiplier,
                "level": producer.level,
                "cost_base": producer.cost_base,
                "cost_multiplier": producer.cost_multiplier,
            })
    
    # Save converters
    for entity in game.converter_entities:
        converter = entity.get_component(ResourceConverter)
        if converter:
            state["converters"].append({
                "name": entity.name,
                "input_type": converter.input_type,
                "output_type": converter.output_type,
                "input_rate": converter.input_rate,
                "output_rate": converter.output_rate,
                "efficiency": converter.efficiency,
                "level": converter.level,
                "enabled": converter.enabled,
            })
    
    # Save upgrades
    for entity in game.upgrade_entities:
        upgrade = entity.get_component(Upgrade)
        if upgrade:
            state["upgrades"].append({
                "name": upgrade.name,
                "description": upgrade.description,
                "cost": upgrade.cost,
                "resource_type": upgrade.resource_type,
                "purchased": upgrade.purchased,
                "effect_type": upgrade.effect_type,
                "effect_value": upgrade.effect_value,
                "target": upgrade.target,
            })
    
    # Save achievements
    for entity in game.achievement_entities:
        achievement = entity.get_component(Achievement)
        if achievement:
            state["achievements"].append({
                "name": achievement.name,
                "description": achievement.description,
                "requirement_type": achievement.requirement_type,
                "requirement_value": achievement.requirement_value,
                "unlocked": achievement.unlocked,
                "reward_type": achievement.reward_type,
                "reward_value": achievement.reward_value,
            })
    
    return state


def deserialize_game_state(game, state: Dict[str, Any]) -> bool:
    """
    Load game state from dictionary.
    
    Args:
        game: ThirstysGame instance
        state: Dictionary containing game state
        
    Returns:
        True if successful, False otherwise
    """
    try:
        from app.components import (
            GameResources, Stats, ResourceProducer, ResourceConverter, 
            ClickGenerator, Upgrade, Achievement
        )
        
        # Restore resources
        resources = game.resources_entity.get_component(GameResources)
        res_data = state["resources"]
        resources.energy = res_data["energy"]
        resources.crystals = res_data["crystals"]
        resources.essence = res_data["essence"]
        resources.prestige_points = res_data["prestige_points"]
        resources.energy_multiplier = res_data["energy_multiplier"]
        resources.crystal_multiplier = res_data["crystal_multiplier"]
        resources.essence_multiplier = res_data["essence_multiplier"]
        resources.global_multiplier = res_data["global_multiplier"]
        
        # Restore stats
        stats = game.stats_entity.get_component(Stats)
        stats_data = state["stats"]
        stats.total_clicks = stats_data["total_clicks"]
        stats.total_energy_earned = stats_data["total_energy_earned"]
        stats.total_crystals_earned = stats_data["total_crystals_earned"]
        stats.total_essence_earned = stats_data["total_essence_earned"]
        stats.play_time = stats_data["play_time"]
        stats.highest_energy = stats_data["highest_energy"]
        stats.highest_crystals = stats_data["highest_crystals"]
        stats.upgrades_purchased = stats_data["upgrades_purchased"]
        stats.achievements_unlocked = stats_data["achievements_unlocked"]
        
        # Restore click generator
        click_gen = game.click_generator_entity.get_component(ClickGenerator)
        cg_data = state["click_generator"]
        click_gen.amount = cg_data["amount"]
        click_gen.multiplier = cg_data["multiplier"]
        click_gen.critical_chance = cg_data["critical_chance"]
        click_gen.critical_multiplier = cg_data["critical_multiplier"]
        
        # Restore producers
        for i, prod_data in enumerate(state["producers"]):
            if i < len(game.producer_entities):
                producer = game.producer_entities[i].get_component(ResourceProducer)
                producer.base_rate = prod_data["base_rate"]
                producer.multiplier = prod_data["multiplier"]
                producer.level = prod_data["level"]
                producer.cost_base = prod_data["cost_base"]
                producer.cost_multiplier = prod_data["cost_multiplier"]
        
        # Restore converters
        for i, conv_data in enumerate(state["converters"]):
            if i < len(game.converter_entities):
                converter = game.converter_entities[i].get_component(ResourceConverter)
                converter.input_rate = conv_data["input_rate"]
                converter.output_rate = conv_data["output_rate"]
                converter.efficiency = conv_data["efficiency"]
                converter.level = conv_data["level"]
                converter.enabled = conv_data["enabled"]
        
        # Restore upgrades
        for i, upg_data in enumerate(state["upgrades"]):
            if i < len(game.upgrade_entities):
                upgrade = game.upgrade_entities[i].get_component(Upgrade)
                upgrade.purchased = upg_data["purchased"]
        
        # Restore achievements
        for i, ach_data in enumerate(state["achievements"]):
            if i < len(game.achievement_entities):
                achievement = game.achievement_entities[i].get_component(Achievement)
                achievement.unlocked = ach_data["unlocked"]
        
        print("✅ Game state restored")
        return True
    
    except Exception as e:
        print(f"❌ Error restoring game state: {e}")
        return False
