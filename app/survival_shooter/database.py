"""
Database layer for persistent player state and progression.
"""
import aiosqlite
import json
from typing import Optional, Dict, List
from dataclasses import asdict
import logging

from .entities import Player, Squad

logger = logging.getLogger(__name__)


class Database:
    """Database manager for persistent storage."""
    
    def __init__(self, db_path: str = "game.db"):
        self.db_path = db_path
        self.db: Optional[aiosqlite.Connection] = None
    
    async def connect(self):
        """Connect to database and initialize schema."""
        self.db = await aiosqlite.connect(self.db_path)
        await self._init_schema()
        logger.info(f"Database connected: {self.db_path}")
    
    async def close(self):
        """Close database connection."""
        if self.db:
            await self.db.close()
            logger.info("Database closed")
    
    async def _init_schema(self):
        """Initialize database schema."""
        # Players table
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                player_class TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                experience INTEGER DEFAULT 0,
                currency INTEGER DEFAULT 0,
                upgrades TEXT DEFAULT '{}',
                unlocked_skins TEXT DEFAULT '[]',
                stats TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Squads table
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS squads (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                leader_id TEXT,
                total_kills INTEGER DEFAULT 0,
                total_waves_survived INTEGER DEFAULT 0,
                squad_level INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Squad members table
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS squad_members (
                squad_id TEXT NOT NULL,
                player_id TEXT NOT NULL,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (squad_id, player_id),
                FOREIGN KEY (squad_id) REFERENCES squads(id),
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        """)
        
        # Marketplace purchases table
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id TEXT NOT NULL,
                item_type TEXT NOT NULL,
                item_id TEXT NOT NULL,
                price REAL NOT NULL,
                currency TEXT DEFAULT 'USD',
                purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        """)
        
        # Leaderboards table
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS leaderboards (
                player_id TEXT PRIMARY KEY,
                total_kills INTEGER DEFAULT 0,
                waves_survived INTEGER DEFAULT 0,
                playtime_seconds INTEGER DEFAULT 0,
                highest_wave INTEGER DEFAULT 0,
                score INTEGER DEFAULT 0,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        """)
        
        await self.db.commit()
    
    async def save_player(self, player: Player):
        """Save or update player data."""
        await self.db.execute("""
            INSERT OR REPLACE INTO players 
            (id, name, player_class, level, experience, currency, upgrades, unlocked_skins, last_played)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            player.id,
            player.name,
            player.player_class,
            player.level,
            player.experience,
            player.currency,
            json.dumps(player.upgrades),
            json.dumps(player.unlocked_skins)
        ))
        await self.db.commit()
    
    async def load_player(self, player_id: str) -> Optional[Dict]:
        """Load player data from database."""
        cursor = await self.db.execute(
            "SELECT * FROM players WHERE id = ?",
            (player_id,)
        )
        row = await cursor.fetchone()
        
        if not row:
            return None
        
        return {
            "id": row[0],
            "name": row[1],
            "player_class": row[2],
            "level": row[3],
            "experience": row[4],
            "currency": row[5],
            "upgrades": json.loads(row[6]),
            "unlocked_skins": json.loads(row[7]),
        }
    
    async def record_purchase(self, player_id: str, item_type: str, item_id: str, price: float):
        """Record a marketplace purchase."""
        await self.db.execute("""
            INSERT INTO purchases (player_id, item_type, item_id, price)
            VALUES (?, ?, ?, ?)
        """, (player_id, item_type, item_id, price))
        await self.db.commit()
    
    async def get_player_purchases(self, player_id: str) -> List[Dict]:
        """Get all purchases for a player."""
        cursor = await self.db.execute("""
            SELECT item_type, item_id, price, purchased_at
            FROM purchases
            WHERE player_id = ?
            ORDER BY purchased_at DESC
        """, (player_id,))
        
        rows = await cursor.fetchall()
        return [
            {
                "item_type": row[0],
                "item_id": row[1],
                "price": row[2],
                "purchased_at": row[3]
            }
            for row in rows
        ]
    
    async def update_leaderboard(self, player_id: str, stats: Dict):
        """Update player leaderboard stats."""
        await self.db.execute("""
            INSERT OR REPLACE INTO leaderboards
            (player_id, total_kills, waves_survived, playtime_seconds, highest_wave, score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            player_id,
            stats.get("total_kills", 0),
            stats.get("waves_survived", 0),
            stats.get("playtime_seconds", 0),
            stats.get("highest_wave", 0),
            stats.get("score", 0)
        ))
        await self.db.commit()
    
    async def get_leaderboard(self, stat: str = "score", limit: int = 100) -> List[Dict]:
        """Get leaderboard rankings."""
        valid_stats = ["total_kills", "waves_survived", "highest_wave", "score"]
        if stat not in valid_stats:
            stat = "score"
        
        cursor = await self.db.execute(f"""
            SELECT 
                l.player_id,
                p.name,
                l.total_kills,
                l.waves_survived,
                l.highest_wave,
                l.score
            FROM leaderboards l
            JOIN players p ON l.player_id = p.id
            ORDER BY l.{stat} DESC
            LIMIT ?
        """, (limit,))
        
        rows = await cursor.fetchall()
        return [
            {
                "player_id": row[0],
                "name": row[1],
                "total_kills": row[2],
                "waves_survived": row[3],
                "highest_wave": row[4],
                "score": row[5]
            }
            for row in rows
        ]
