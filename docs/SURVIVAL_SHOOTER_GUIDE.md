# Blood-Thirsty Game - Complete Documentation

## 🎮 Game Overview

**Blood-Thirsty** is a production-grade, multiplayer survival shooter featuring:
- 4-player co-op PvE gameplay
- Wave-based survival mechanics
- Hold-the-zone objectives with rescue bus system
- Multiple player classes with unique abilities
- Massive themed zones across fantasy, sci-fi, and horror settings
- Full marketplace with cosmetics and boosts
- Server-authoritative architecture with client prediction
- Scalable infrastructure supporting 100+ concurrent players

## 🏗️ Architecture

### Technology Stack

**Backend:**
- Python 3.12+
- Pygame for client rendering
- WebSockets for real-time networking
- aiosqlite for persistent player data
- asyncio for concurrent operations

**Infrastructure:**
- Kubernetes for orchestration
- Docker for containerization
- Horizontal Pod Autoscaling (3-20 replicas)
- Persistent storage for player data
- LoadBalancer service for client connections

### Server-Client Architecture

```
┌─────────────┐         WebSocket (8765)        ┌──────────────┐
│   Clients   │ ◄─────────────────────────────► │ Game Servers │
│  (Pygame)   │                                  │   (Python)   │
└─────────────┘                                  └──────┬───────┘
                                                        │
                                                        ▼
                                                 ┌──────────────┐
                                                 │   Database   │
                                                 │  (SQLite)    │
                                                 └──────────────┘
```

## 🎯 Gameplay Mechanics

### Core Gameplay Loop

1. **Spawn**: Players spawn in squads of up to 4
2. **Zone Control**: Active zone appears on map
3. **Hold the Zone**: Squad must hold zone for 60 seconds
4. **Wave Survival**: Endless waves of enemies attack
5. **Rescue Bus**: Bus arrives every 2 minutes at active zone
6. **Extraction**: Board bus to complete match and earn rewards

### Player Classes

#### 1. Mage
- **Role**: Ranged DPS / Area Control
- **Base Health**: 80
- **Base Damage**: 15
- **Movement Speed**: 280
- **Abilities**:
  - Fireball: Projectile attack
  - Ice Nova: Area freeze
  - Lightning Chain: Bouncing damage
  - Arcane Shield: Damage absorption

#### 2. Commando
- **Role**: Heavy DPS / Tank
- **Base Health**: 120
- **Base Damage**: 12
- **Movement Speed**: 260
- **Abilities**:
  - Assault Rifle: Rapid fire
  - Rocket Launcher: Explosive damage
  - Tactical Grenade: Area denial
  - Armor Plating: Damage reduction

#### 3. Dimension Runner
- **Role**: High Mobility / Assassin
- **Base Health**: 90
- **Base Damage**: 18
- **Movement Speed**: 350
- **Abilities**:
  - Blink Strike: Teleport attack
  - Shadow Step: Invisibility
  - Phase Shift: Dodge ability
  - Temporal Blade: Critical strikes

#### 4. Biotech Paladin
- **Role**: Support / Healer
- **Base Health**: 110
- **Base Damage**: 10
- **Movement Speed**: 270
- **Abilities**:
  - Healing Pulse: AoE heal
  - Divine Smite: Holy damage
  - Regeneration Field: HoT aura
  - Resurrection: Revive fallen allies

### Themed Zones

1. **Ruined Citadel** (Fantasy)
   - Difficulty: 1.0x
   - Enemies: Undead Warriors, Skeleton Archers, Necromancers
   - Hazards: Cursed Ground, Falling Debris

2. **Abandoned Labs** (Sci-Fi)
   - Difficulty: 1.2x
   - Enemies: Mutant Soldiers, Cyber Drones, Rogue AI
   - Hazards: Toxic Gas, Electrical Hazards

3. **Haunted Township** (Horror)
   - Difficulty: 1.1x
   - Enemies: Zombie Hordes, Possessed Civilians, Wraiths
   - Hazards: Fog of Madness, Blood Pools

4. **Mythic Forest** (Mythological)
   - Difficulty: 1.3x
   - Enemies: Corrupted Treants, Shadow Beasts, Ancient Guardians
   - Hazards: Entangling Roots, Spirit Wisps

5. **Alien Wasteland** (Sci-Fi Horror)
   - Difficulty: 1.4x
   - Enemies: Xenomorph Swarms, Alien Brutes, Mind Controllers
   - Hazards: Acid Pools, Gravity Anomalies

6. **Eldritch Demiplane** (Cosmic Horror)
   - Difficulty: 1.5x
   - Enemies: Cosmic Horrors, Void Tentacles, Reality Warpers
   - Hazards: Sanity Drain, Dimensional Rifts

### Wave System

- **Wave Interval**: 30 seconds between waves
- **Scaling**: +5 enemies per wave
- **Difficulty**: Enemies gain 15% health per wave
- **Enemy Types**: Basic, Fast, Tank, Ranged
- **Rewards**: Currency and XP scale with wave number

## 💰 Economy & Marketplace

### Currency System

Players earn currency through:
- Enemy kills (10-100 per kill, scales with difficulty)
- Wave completion bonuses (50+ base)
- Zone control rewards
- Daily missions (when implemented)

### Marketplace Items

#### Premium Packs ($10.00)
- **Ultimate Warrior Pack**: All class skins + 7-day 2x XP boost

#### Starter Packs ($5.00)
- **Beginner's Advantage**: Currency + boosts bundle

#### Coffee Boosts ($1.99)
- **XP Coffee Boost**: 2x XP for 24 hours
- **Currency Coffee Boost**: 1.5x currency for 24 hours

#### Micro Items ($0.99)
- **Instant Revive**: Skip respawn timer
- **Ammo Pack**: Full ammo refill

#### Character Skins ($3.99 - $4.99)
Each class has multiple skins:
- Legendary skins (Level 10+): $4.99
- Epic skins (Level 5+): $3.99

#### Weapon Skins ($2.99)
- **Golden Arsenal**: Gold weapons
- **Plasma Weapons**: Sci-fi energy effects

## 🚀 Getting Started

### Server Setup

#### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt
```

#### Run Server Locally
```bash
cd app/survival_shooter
python server.py
```

Server will start on `ws://0.0.0.0:8765`

#### Run Client
```bash
python -m app.survival_shooter.client --name "YourName" --class commando --server ws://localhost:8765
```

### Docker Deployment

#### Build Image
```bash
docker build -f Dockerfile.survival_shooter -t survival-shooter:latest .
```

#### Run Container
```bash
docker run -p 8765:8765 survival-shooter:latest
```

### Kubernetes Deployment

#### Deploy to Cluster
```bash
kubectl apply -f k8s/survival-shooter-deployment.yaml
```

#### Check Status
```bash
kubectl get pods -n survival-shooter
kubectl get svc -n survival-shooter
```

#### Scale Servers
```bash
kubectl scale deployment survival-shooter-server --replicas=10 -n survival-shooter
```

## 🎨 Client Controls

### Keyboard Controls
- **WASD / Arrow Keys**: Move
- **Mouse**: Aim
- **Left Click**: Primary attack
- **Right Click**: Secondary ability
- **1-4 Keys**: Use abilities
- **E**: Interact / Board bus
- **Tab**: Scoreboard
- **ESC**: Menu

### Mobile Controls (Future)
- **Virtual Joystick**: Movement
- **Touch Aim**: Look around
- **Ability Buttons**: On-screen abilities
- **Auto-fire**: Optional

## 🗂️ Code Structure

```
app/survival_shooter/
├── __init__.py           # Module exports
├── config.py            # Game configuration & constants
├── entities.py          # Game entity definitions
├── systems.py           # Wave & zone management systems
├── network.py           # Networking & matchmaking
├── server.py            # Main game server
├── client.py            # Game client with rendering
├── database.py          # Persistent storage layer
└── marketplace.py       # Economy & shop system
```

## 🔧 Configuration

### Game Config (config.py)

```python
SERVER_PORT = 8765
MAX_PLAYERS_PER_SQUAD = 4
MAX_CONCURRENT_PLAYERS = 100
TICK_RATE = 60  # Server updates per second
ZONE_HOLD_TIME = 60.0  # Seconds to hold zone
BUS_ROTATION_INTERVAL = 120.0  # Seconds between bus arrivals
```

### Environment Variables

```bash
SERVER_MODE=production
TICK_RATE=60
MAX_PLAYERS_PER_SERVER=100
DB_PATH=/data/game.db
LOG_LEVEL=INFO
```

## 📊 Monitoring & Metrics

### Server Metrics
- Connected players count
- Active matches
- Messages sent/received
- Network bandwidth usage
- CPU/Memory usage per pod

### Game Metrics
- Average wave reached
- Player retention
- Currency earned
- Items purchased
- Server tick rate stability

## 🔐 Security

### Server-Authoritative Design
- All game logic runs on server
- Client inputs are validated
- Position/damage calculated server-side
- Anti-cheat measures built-in

### Data Protection
- Player data encrypted at rest
- Secure WebSocket connections (WSS in production)
- Rate limiting on API endpoints
- Input sanitization

## 🧪 Testing

### Run Unit Tests
```bash
pytest tests/test_survival_shooter.py -v
```

### Load Testing
```bash
# Simulate 100 concurrent players
python tests/load_test_server.py --players 100
```

## 📈 Performance

### Server Performance
- **Target Tick Rate**: 60 TPS (ticks per second)
- **Player Capacity**: 100 concurrent players per server
- **Network Latency**: <100ms target
- **Memory Usage**: ~2GB per server instance

### Scaling
- Horizontal: 3-20 server replicas
- Load balancing: Session affinity enabled
- Database: Shared persistent storage
- Auto-scaling triggers at 70% CPU

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

1. **Build & Test**
   - Lint code
   - Run unit tests
   - Build Docker image

2. **Deploy**
   - Push to container registry
   - Update Kubernetes deployment
   - Health check validation

3. **Monitor**
   - Performance metrics
   - Error tracking
   - Player analytics

## 🎯 Roadmap

### Phase 1 ✅ (Current)
- [x] Core gameplay systems
- [x] 4 player classes
- [x] 6 themed zones
- [x] Wave survival mechanics
- [x] Networking infrastructure
- [x] Marketplace system
- [x] K8s deployment configs

### Phase 2 (Next)
- [ ] Android native UI integration
- [ ] Full ability system implementation
- [ ] Advanced AI behaviors
- [ ] Narrative/lore system
- [ ] Procedural map generation
- [ ] Squad matchmaking

### Phase 3 (Future)
- [ ] Cross-platform clients (Unity, Unreal, Web)
- [ ] VR support
- [ ] Mod support
- [ ] Tournament mode
- [ ] Seasonal events
- [ ] Advanced graphics pipeline

## 📝 API Reference

### Network Protocol

#### Message Types

**PLAYER_JOIN**
```json
{
  "type": "player_join",
  "data": {
    "name": "PlayerName",
    "class": "commando"
  }
}
```

**PLAYER_INPUT**
```json
{
  "type": "player_input",
  "data": {
    "type": "move",
    "direction": {"x": 1.0, "y": 0.0}
  }
}
```

**GAME_STATE**
```json
{
  "type": "game_state",
  "data": {
    "game_time": 123.45,
    "current_wave": 5,
    "wave_active": true,
    "active_zone_id": "zone_id"
  }
}
```

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

## 📄 License

MIT License - See [LICENSE](../LICENSE) for details.

## 🙏 Credits

Built by Thirsty's Game Studio
- Architecture: Production-grade ECS
- Networking: Server-authoritative multiplayer
- Infrastructure: Kubernetes + Docker
- Design: F2P-friendly monetization

---

**For technical support or questions, open an issue on GitHub.**
