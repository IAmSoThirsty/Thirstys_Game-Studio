"""
Marketplace system for in-game economy and cosmetics.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class ItemType(Enum):
    """Types of marketplace items."""
    WEAPON_SKIN = "weapon_skin"
    CHARACTER_SKIN = "character_skin"
    EMOTE = "emote"
    BOOST = "boost"
    BUNDLE = "bundle"


@dataclass
class MarketplaceItem:
    """Marketplace item definition."""
    id: str
    name: str
    description: str
    item_type: ItemType
    price: float
    currency: str = "USD"
    
    # Visual
    icon_path: Optional[str] = None
    preview_image: Optional[str] = None
    
    # Availability
    is_available: bool = True
    is_limited_time: bool = False
    requires_level: int = 0
    
    # Bundle contents (if bundle)
    bundle_items: Optional[List[str]] = None
    
    # Tags for filtering
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


# Premium cosmetics marketplace
MARKETPLACE_ITEMS = [
    # Premium Packs
    MarketplaceItem(
        id="premium_pack_01",
        name="Ultimate Warrior Pack",
        description="Complete collection of premium skins and boosts for all classes",
        item_type=ItemType.BUNDLE,
        price=10.00,
        bundle_items=[
            "skin_mage_archmage",
            "skin_commando_spec_ops",
            "skin_runner_phantom",
            "skin_paladin_celestial",
            "boost_xp_2x_7day"
        ],
        tags=["premium", "bundle", "popular"]
    ),
    
    # Starter Packs
    MarketplaceItem(
        id="starter_pack_01",
        name="Beginner's Advantage",
        description="Perfect starter pack with currency and boosts",
        item_type=ItemType.BUNDLE,
        price=5.00,
        bundle_items=[
            "currency_1000",
            "boost_xp_1.5x_3day",
            "boost_damage_1.2x_3day"
        ],
        tags=["starter", "bundle", "value"]
    ),
    
    # Coffee Buy - Micro Transactions
    MarketplaceItem(
        id="coffee_boost_xp",
        name="XP Coffee Boost",
        description="2x XP for 24 hours - support development!",
        item_type=ItemType.BOOST,
        price=1.99,
        tags=["coffee", "boost", "xp"]
    ),
    
    MarketplaceItem(
        id="coffee_boost_currency",
        name="Currency Coffee Boost",
        description="1.5x currency gain for 24 hours",
        item_type=ItemType.BOOST,
        price=1.99,
        tags=["coffee", "boost", "currency"]
    ),
    
    # Micro Boosts (sub $1)
    MarketplaceItem(
        id="micro_revive",
        name="Instant Revive",
        description="Skip respawn timer once",
        item_type=ItemType.BOOST,
        price=0.99,
        tags=["micro", "convenience"]
    ),
    
    MarketplaceItem(
        id="micro_ammo",
        name="Ammo Pack",
        description="Full ammo refill for all weapons",
        item_type=ItemType.BOOST,
        price=0.49,
        tags=["micro", "consumable"]
    ),
    
    # Character Skins - Mage
    MarketplaceItem(
        id="skin_mage_archmage",
        name="Archmage Robes",
        description="Legendary archmage cosmetic skin for Mage class",
        item_type=ItemType.CHARACTER_SKIN,
        price=4.99,
        requires_level=10,
        tags=["mage", "legendary", "purple"]
    ),
    
    MarketplaceItem(
        id="skin_mage_frost",
        name="Frost Mage",
        description="Icy themed skin with frost particle effects",
        item_type=ItemType.CHARACTER_SKIN,
        price=3.99,
        requires_level=5,
        tags=["mage", "frost", "blue"]
    ),
    
    # Character Skins - Commando
    MarketplaceItem(
        id="skin_commando_spec_ops",
        name="Spec Ops Operative",
        description="Elite special operations tactical gear",
        item_type=ItemType.CHARACTER_SKIN,
        price=4.99,
        requires_level=10,
        tags=["commando", "military", "black"]
    ),
    
    MarketplaceItem(
        id="skin_commando_desert",
        name="Desert Storm",
        description="Desert camo tactical outfit",
        item_type=ItemType.CHARACTER_SKIN,
        price=3.99,
        requires_level=5,
        tags=["commando", "camo", "tan"]
    ),
    
    # Character Skins - Dimension Runner
    MarketplaceItem(
        id="skin_runner_phantom",
        name="Phantom Assassin",
        description="Ethereal assassin skin with void particles",
        item_type=ItemType.CHARACTER_SKIN,
        price=4.99,
        requires_level=10,
        tags=["runner", "legendary", "void"]
    ),
    
    MarketplaceItem(
        id="skin_runner_neon",
        name="Neon Runner",
        description="Cyberpunk neon-themed skin with trails",
        item_type=ItemType.CHARACTER_SKIN,
        price=3.99,
        requires_level=5,
        tags=["runner", "cyberpunk", "neon"]
    ),
    
    # Character Skins - Biotech Paladin
    MarketplaceItem(
        id="skin_paladin_celestial",
        name="Celestial Guardian",
        description="Divine armor with holy light effects",
        item_type=ItemType.CHARACTER_SKIN,
        price=4.99,
        requires_level=10,
        tags=["paladin", "holy", "gold"]
    ),
    
    MarketplaceItem(
        id="skin_paladin_tech",
        name="Tech Crusader",
        description="Bio-mechanical fusion armor",
        item_type=ItemType.CHARACTER_SKIN,
        price=3.99,
        requires_level=5,
        tags=["paladin", "tech", "silver"]
    ),
    
    # Weapon Skins
    MarketplaceItem(
        id="weapon_skin_golden",
        name="Golden Arsenal",
        description="Gold-plated skin for all weapons",
        item_type=ItemType.WEAPON_SKIN,
        price=2.99,
        tags=["weapon", "gold", "prestige"]
    ),
    
    MarketplaceItem(
        id="weapon_skin_plasma",
        name="Plasma Weapons",
        description="Sci-fi plasma effect for all weapons",
        item_type=ItemType.WEAPON_SKIN,
        price=2.99,
        tags=["weapon", "scifi", "energy"]
    ),
]


class Marketplace:
    """Marketplace manager."""
    
    def __init__(self):
        self.items = {item.id: item for item in MARKETPLACE_ITEMS}
    
    def get_item(self, item_id: str) -> Optional[MarketplaceItem]:
        """Get item by ID."""
        return self.items.get(item_id)
    
    def get_available_items(self, player_level: int = 0) -> List[MarketplaceItem]:
        """Get all available items for player level."""
        return [
            item for item in self.items.values()
            if item.is_available and item.requires_level <= player_level
        ]
    
    def get_items_by_type(self, item_type: ItemType, player_level: int = 0) -> List[MarketplaceItem]:
        """Get items by type."""
        return [
            item for item in self.items.values()
            if item.item_type == item_type 
            and item.is_available 
            and item.requires_level <= player_level
        ]
    
    def get_items_by_tag(self, tag: str, player_level: int = 0) -> List[MarketplaceItem]:
        """Get items by tag."""
        return [
            item for item in self.items.values()
            if tag in item.tags
            and item.is_available
            and item.requires_level <= player_level
        ]
    
    def get_featured_items(self) -> List[MarketplaceItem]:
        """Get featured/promoted items."""
        # In production, would be dynamically managed
        return [
            item for item in self.items.values()
            if "popular" in item.tags or "bundle" in item.tags
        ][:6]
    
    def purchase_item(self, item_id: str, player_level: int) -> tuple[bool, str]:
        """
        Validate a purchase.
        Returns (success, message)
        """
        item = self.get_item(item_id)
        
        if not item:
            return False, "Item not found"
        
        if not item.is_available:
            return False, "Item not available"
        
        if item.requires_level > player_level:
            return False, f"Requires level {item.requires_level}"
        
        return True, "Purchase validated"
