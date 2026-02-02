"""
Network management for multiplayer functionality.
Server-authoritative architecture with client prediction.
"""
import asyncio
import json
from typing import Dict, Optional, Callable, Any
from dataclasses import asdict
import logging

try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    logging.warning("websockets not available - networking disabled")


class NetworkMessage:
    """Network message protocol."""
    
    # Message types
    PLAYER_JOIN = "player_join"
    PLAYER_LEAVE = "player_leave"
    PLAYER_INPUT = "player_input"
    PLAYER_STATE = "player_state"
    GAME_STATE = "game_state"
    WAVE_START = "wave_start"
    WAVE_COMPLETE = "wave_complete"
    ZONE_UPDATE = "zone_update"
    ENEMY_SPAWN = "enemy_spawn"
    ENEMY_DEATH = "enemy_death"
    DAMAGE_DEALT = "damage_dealt"
    PLAYER_RESPAWN = "player_respawn"
    
    def __init__(self, msg_type: str, data: Dict[str, Any]):
        self.type = msg_type
        self.data = data
        self.timestamp = asyncio.get_event_loop().time()
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps({
            "type": self.type,
            "data": self.data,
            "timestamp": self.timestamp
        })
    
    @classmethod
    def from_json(cls, json_str: str) -> 'NetworkMessage':
        """Create from JSON string."""
        data = json.loads(json_str)
        msg = cls(data["type"], data["data"])
        msg.timestamp = data.get("timestamp", 0)
        return msg


class NetworkManager:
    """
    Network manager for client-server communication.
    Server-authoritative with client prediction for smooth gameplay.
    """
    
    def __init__(self, is_server: bool = True):
        self.is_server = is_server
        self.connections: Dict[str, Any] = {}  # client_id -> websocket
        self.message_handlers: Dict[str, Callable] = {}
        self.pending_messages = []
        
        # Server state
        self.server = None
        self.host = "0.0.0.0"
        self.port = 8765
        
        # Client state
        self.client_ws = None
        self.client_id = None
        
        # Performance metrics
        self.messages_sent = 0
        self.messages_received = 0
        self.bytes_sent = 0
        self.bytes_received = 0
    
    def register_handler(self, message_type: str, handler: Callable):
        """Register a message handler."""
        self.message_handlers[message_type] = handler
    
    async def start_server(self, host: str = "0.0.0.0", port: int = 8765):
        """Start the server."""
        if not WEBSOCKETS_AVAILABLE:
            logging.error("Cannot start server - websockets not available")
            return
        
        self.host = host
        self.port = port
        
        async def handler(websocket, path):
            await self._handle_client_connection(websocket, path)
        
        self.server = await websockets.serve(handler, host, port)
        logging.info(f"Server started on {host}:{port}")
    
    async def connect_client(self, server_url: str):
        """Connect as client to server."""
        if not WEBSOCKETS_AVAILABLE:
            logging.error("Cannot connect - websockets not available")
            return
        
        self.client_ws = await websockets.connect(server_url)
        logging.info(f"Connected to server: {server_url}")
        
        # Start receiving messages
        asyncio.create_task(self._receive_loop())
    
    async def _handle_client_connection(self, websocket, path):
        """Handle a client connection."""
        client_id = str(id(websocket))
        self.connections[client_id] = websocket
        
        try:
            # Notify of new connection
            if NetworkMessage.PLAYER_JOIN in self.message_handlers:
                await self.message_handlers[NetworkMessage.PLAYER_JOIN](client_id, {})
            
            # Receive messages
            async for message in websocket:
                await self._handle_message(client_id, message)
        
        except websockets.exceptions.ConnectionClosed:
            pass
        
        finally:
            # Clean up connection
            if client_id in self.connections:
                del self.connections[client_id]
            
            if NetworkMessage.PLAYER_LEAVE in self.message_handlers:
                await self.message_handlers[NetworkMessage.PLAYER_LEAVE](client_id, {})
    
    async def _handle_message(self, client_id: str, message_str: str):
        """Handle incoming message."""
        try:
            message = NetworkMessage.from_json(message_str)
            self.messages_received += 1
            self.bytes_received += len(message_str)
            
            # Call registered handler
            if message.type in self.message_handlers:
                await self.message_handlers[message.type](client_id, message.data)
        
        except Exception as e:
            logging.error(f"Error handling message: {e}")
    
    async def _receive_loop(self):
        """Client receive loop."""
        try:
            async for message in self.client_ws:
                await self._handle_message(self.client_id or "client", message)
        except Exception as e:
            logging.error(f"Receive loop error: {e}")
    
    async def broadcast(self, message: NetworkMessage, exclude_client: Optional[str] = None):
        """Broadcast message to all clients (server only)."""
        if not self.is_server:
            return
        
        message_str = message.to_json()
        self.messages_sent += len(self.connections)
        self.bytes_sent += len(message_str) * len(self.connections)
        
        for client_id, ws in self.connections.items():
            if client_id != exclude_client:
                try:
                    await ws.send(message_str)
                except Exception as e:
                    logging.error(f"Error broadcasting to {client_id}: {e}")
    
    async def send_to_client(self, client_id: str, message: NetworkMessage):
        """Send message to specific client (server only)."""
        if not self.is_server:
            return
        
        ws = self.connections.get(client_id)
        if ws:
            message_str = message.to_json()
            self.messages_sent += 1
            self.bytes_sent += len(message_str)
            
            try:
                await ws.send(message_str)
            except Exception as e:
                logging.error(f"Error sending to {client_id}: {e}")
    
    async def send_to_server(self, message: NetworkMessage):
        """Send message to server (client only)."""
        if self.is_server or not self.client_ws:
            return
        
        message_str = message.to_json()
        self.messages_sent += 1
        self.bytes_sent += len(message_str)
        
        try:
            await self.client_ws.send(message_str)
        except Exception as e:
            logging.error(f"Error sending to server: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get network statistics."""
        return {
            "connected_clients": len(self.connections),
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
            "bytes_sent": self.bytes_sent,
            "bytes_received": self.bytes_received,
        }


class MatchmakingManager:
    """Manages matchmaking for squads."""
    
    def __init__(self):
        self.queue: list = []
        self.matches: Dict[str, Dict] = {}
        self.skill_tolerance = 200.0  # ELO tolerance for matchmaking
    
    async def add_to_queue(self, squad_id: str, average_skill: float):
        """Add squad to matchmaking queue."""
        self.queue.append({
            "squad_id": squad_id,
            "skill": average_skill,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        # Try to create matches
        await self._try_create_matches()
    
    async def _try_create_matches(self):
        """Attempt to create matches from queue."""
        if len(self.queue) < 1:
            return
        
        # Sort by skill rating
        self.queue.sort(key=lambda x: x["skill"])
        
        # Try to group squads with similar skill levels
        matches_to_create = []
        used_indices = set()
        
        for i, squad in enumerate(self.queue):
            if i in used_indices:
                continue
            
            # Find similar skill squads
            match_squads = [squad]
            for j, other in enumerate(self.queue[i+1:], start=i+1):
                if j in used_indices:
                    continue
                
                if abs(squad["skill"] - other["skill"]) <= self.skill_tolerance:
                    match_squads.append(other)
                    used_indices.add(j)
                    
                    # Max 4 squads per match (4x4 = 16 players max)
                    if len(match_squads) >= 4:
                        break
            
            if len(match_squads) >= 1:  # Can start with just 1 squad
                matches_to_create.append(match_squads)
                used_indices.add(i)
        
        # Remove used squads from queue
        self.queue = [s for i, s in enumerate(self.queue) if i not in used_indices]
        
        # Create matches
        for squads in matches_to_create:
            await self._create_match(squads)
    
    async def _create_match(self, squads: list):
        """Create a match from squads."""
        import uuid
        match_id = str(uuid.uuid4())
        
        self.matches[match_id] = {
            "match_id": match_id,
            "squads": [s["squad_id"] for s in squads],
            "status": "starting",
            "created_at": asyncio.get_event_loop().time()
        }
        
        logging.info(f"Created match {match_id} with {len(squads)} squads")
