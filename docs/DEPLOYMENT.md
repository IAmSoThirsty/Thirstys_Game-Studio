# 🚀 End-to-End Deployment Guide
## God-Tier Monolithic Architecture

This guide covers complete deployment of **Thirsty's Game Studio**, including the game and agent system, from development to production.

---

## 📋 Table of Contents

1. [Quick Start - Single Command Deployment](#quick-start)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Production Deployment](#production-deployment)
7. [Monitoring & Observability](#monitoring)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Quick Start - Single Command Deployment {#quick-start}

### Complete Stack Deployment (God-Tier Monolithic)

Deploy everything with a single command:

```bash
make deploy-all
```

This will:
- Build both game and agent Docker images
- Start all services (game + agent)
- Configure networking and volumes
- Set up health checks
- Display deployment status

**Check status:**
```bash
make deploy-status
```

**Stop all services:**
```bash
make deploy-stop
```

---

## 💻 Local Development {#local-development}

### Prerequisites

- Python 3.12+
- Docker 20.10+ (optional)
- Docker Compose 2.0+ (optional)
- Make (optional, but recommended)

### Setup

```bash
# 1. Clone repository
git clone https://github.com/IAmSoThirsty/Thirstys_Game-Studio.git
cd Thirstys_Game-Studio

# 2. Complete setup (creates venv, installs dependencies)
make setup

# 3. Activate virtual environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### Run Locally

**Game:**
```bash
make game-run
# or
python main.py
```

**Agent System:**
```bash
make run
# or
python -m agent.runner --output-dir output
```

**Tests:**
```bash
# All tests
make test

# Game tests only
make test-game

# Specific test file
pytest tests/test_engine.py -v
```

---

## 🐳 Docker Deployment {#docker-deployment}

### Quick Docker Commands

```bash
# Build game image
make game-build

# Run game in Docker (headless)
make game-docker

# Run complete stack
make deploy-all

# Stop all services
make deploy-stop

# Clean up Docker resources
make docker-clean
```

### Manual Docker Commands

**Build Images:**
```bash
# Game image
docker build -t thirsty-game:latest -f Dockerfile.game .

# Agent image
docker build -t thirsty-game-studio-agent:latest -f Dockerfile .
```

**Run Containers:**
```bash
# Run game (headless)
docker run -d \
  --name thirsty-game \
  -v $(pwd)/saves:/app/saves \
  -e SDL_VIDEODRIVER=dummy \
  thirsty-game:latest

# Run agent
docker run -d \
  --name thirsty-agent \
  -v $(pwd)/output:/app/output \
  thirsty-game-studio-agent:latest
```

### Docker Compose

**Start specific services:**
```bash
# Game server only
docker-compose --profile game up -d game-server

# Agent only
docker-compose up -d agent

# Both (complete stack)
docker-compose --profile game up -d agent game-server

# Development mode (interactive shell)
docker-compose --profile game-dev up game-dev
```

**View logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f game-server
docker-compose logs -f agent
```

**Stop services:**
```bash
# Stop all
docker-compose --profile game down

# Stop and remove volumes
docker-compose --profile game down -v
```

---

## ☸️ Kubernetes Deployment {#kubernetes-deployment}

### Prerequisites

- Kubernetes cluster (1.20+)
- kubectl configured
- Sufficient resources (2 CPU, 4GB RAM minimum)

### Deploy to Kubernetes

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get all -n thirsty-game-studio

# Watch pods
kubectl get pods -n thirsty-game-studio -w

# View logs
kubectl logs -n thirsty-game-studio -l app=game-server -f
```

### Kubernetes Architecture

The deployment includes:

- **Namespace**: `thirsty-game-studio`
- **Deployment**: `game-server` (1-5 replicas with HPA)
- **Service**: `game-server-service` (ClusterIP)
- **PVC**: `game-saves-pvc` (1Gi persistent storage)
- **ConfigMap**: `game-config` (environment configuration)
- **HPA**: Auto-scaling based on CPU/Memory (70%/80% thresholds)

### Scaling

**Manual scaling:**
```bash
kubectl scale deployment game-server -n thirsty-game-studio --replicas=3
```

**Auto-scaling** is configured via HPA:
- Min replicas: 1
- Max replicas: 5
- CPU target: 70%
- Memory target: 80%

### Monitoring

```bash
# Resource usage
kubectl top pods -n thirsty-game-studio

# Events
kubectl get events -n thirsty-game-studio --sort-by='.lastTimestamp'

# Describe deployment
kubectl describe deployment game-server -n thirsty-game-studio
```

### Cleanup

```bash
# Delete all resources
kubectl delete -f k8s/

# Or delete namespace
kubectl delete namespace thirsty-game-studio
```

---

## 🔄 CI/CD Pipeline {#cicd-pipeline}

### GitHub Actions Workflows

The repository includes automated CI/CD:

**1. Game CI/CD** (`.github/workflows/game-ci.yml`)
- Runs on push to `main` or `copilot/**` branches
- Tests game functionality
- Builds Docker images
- Scans for security vulnerabilities
- Runs performance tests
- Deploys to production

**2. Agent Team** (`.github/workflows/agent_team.yml`)
- Runs daily at 6 AM UTC
- Executes agent system
- Generates community insights

**3. Android Build** (`.github/workflows/android_build.yml`)
- Builds Android APK
- Runs Android tests

### Trigger Manual Deployment

```bash
# Trigger via GitHub CLI
gh workflow run game-ci.yml

# Or via web interface
# Actions tab → Game CI/CD Pipeline → Run workflow
```

### Build Artifacts

Docker images are published to:
- **GHCR**: `ghcr.io/iamsothirsty/thirsty-game:latest`

Pull latest image:
```bash
docker pull ghcr.io/iamsothirsty/thirsty-game:latest
```

---

## 🏭 Production Deployment {#production-deployment}

### Deployment Options

#### 1. **Docker Compose (Recommended for Single Server)**

```bash
# Production configuration
docker-compose --profile game up -d agent game-server

# With custom environment
LOG_LEVEL=INFO docker-compose --profile game up -d
```

#### 2. **Kubernetes (Recommended for Cloud/Scale)**

```bash
# Deploy to cluster
kubectl apply -f k8s/

# Expose via LoadBalancer (cloud)
kubectl patch svc game-server-service -n thirsty-game-studio -p '{"spec":{"type":"LoadBalancer"}}'

# Or Ingress (recommended)
kubectl apply -f k8s/ingress.yaml  # Create this for your ingress controller
```

#### 3. **Standalone Docker**

```bash
# Run game server
docker run -d \
  --name thirsty-game-prod \
  --restart unless-stopped \
  -v /opt/thirsty-game/saves:/app/saves \
  -e SDL_VIDEODRIVER=dummy \
  -e PYTHONUNBUFFERED=1 \
  --memory 512m \
  --cpus 0.5 \
  thirsty-game:latest
```

### Environment Variables

**Game Server:**
- `SDL_VIDEODRIVER=dummy` - Run in headless mode
- `SDL_AUDIODRIVER=dummy` - Disable audio
- `PYTHONUNBUFFERED=1` - Enable logging
- `LOG_LEVEL=INFO` - Logging verbosity

**Agent System:**
- `OUTPUT_DIR=/app/output` - Output directory
- `LOG_LEVEL=INFO` - Logging level
- `REDDIT_CLIENT_ID` - Reddit API credentials
- `DISCORD_BOT_TOKEN` - Discord bot token
- `STEAM_API_KEY` - Steam API key

### Resource Requirements

**Minimum (Single Instance):**
- CPU: 0.5 cores
- RAM: 512MB
- Disk: 1GB

**Recommended (Production):**
- CPU: 1-2 cores per instance
- RAM: 1-2GB per instance
- Disk: 5GB (with logs/saves)

**Scaling Guidelines:**
- Each game instance can handle ~1000 concurrent operations
- Agent system: 1 instance sufficient (cron-based)
- Storage scales with save files (~1MB per save)

### Health Checks

**Game Server:**
```bash
# Docker
docker exec thirsty-game python -c "import app; print('healthy')"

# Kubernetes
kubectl exec -n thirsty-game-studio game-server-xxx -- python -c "import app; print('healthy')"

# Manual
curl http://localhost:8080/health  # If web interface added
```

### Backup Strategy

**Save Files:**
```bash
# Local Docker
docker cp thirsty-game:/app/saves ./backup-$(date +%Y%m%d)

# Kubernetes
kubectl cp thirsty-game-studio/game-server-xxx:/app/saves ./backup-$(date +%Y%m%d)
```

**Database/State:**
- Save files are stored in `/app/saves`
- Mount persistent volume for durability
- Regular backups recommended (daily)

---

## 📊 Monitoring & Observability {#monitoring}

### Built-in Health Checks

**Docker:**
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

**Kubernetes:**
```bash
kubectl get pods -n thirsty-game-studio -o wide
```

### Resource Monitoring

**Docker Stats:**
```bash
docker stats thirsty-game thirsty-agent
```

**Kubernetes Metrics:**
```bash
kubectl top pods -n thirsty-game-studio
kubectl top nodes
```

### Logs

**Docker:**
```bash
# View logs
docker logs -f thirsty-game

# Last 100 lines
docker logs --tail 100 thirsty-game

# Since timestamp
docker logs --since 1h thirsty-game
```

**Kubernetes:**
```bash
# Pod logs
kubectl logs -n thirsty-game-studio -l app=game-server -f

# Previous container (if crashed)
kubectl logs -n thirsty-game-studio game-server-xxx --previous
```

### Recommended Monitoring Stack

For production, integrate with:

- **Prometheus** - Metrics collection
- **Grafana** - Visualization
- **Loki** - Log aggregation
- **Alertmanager** - Alerting

Example metrics to track:
- CPU/Memory usage
- Request latency
- Error rate
- Save file count/size
- Active game sessions

---

## 🔧 Troubleshooting {#troubleshooting}

### Common Issues

**1. Game won't start**
```bash
# Check logs
docker logs thirsty-game

# Verify image
docker images | grep thirsty-game

# Rebuild if necessary
make game-build
```

**2. Pygame errors in Docker**
```bash
# Ensure headless mode
docker run -e SDL_VIDEODRIVER=dummy thirsty-game:latest
```

**3. Save files not persisting**
```bash
# Check volume mount
docker inspect thirsty-game | grep Mounts -A 10

# Verify directory exists
docker exec thirsty-game ls -la /app/saves
```

**4. High memory usage**
```bash
# Check current usage
docker stats thirsty-game --no-stream

# Set memory limit
docker run --memory 512m thirsty-game:latest
```

**5. Kubernetes pod not ready**
```bash
# Describe pod
kubectl describe pod -n thirsty-game-studio game-server-xxx

# Check events
kubectl get events -n thirsty-game-studio --sort-by='.lastTimestamp'

# View logs
kubectl logs -n thirsty-game-studio game-server-xxx
```

### Debug Mode

**Enable debug logging:**
```bash
# Docker
docker run -e LOG_LEVEL=DEBUG thirsty-game:latest

# Kubernetes
kubectl set env deployment/game-server LOG_LEVEL=DEBUG -n thirsty-game-studio
```

**Interactive debugging:**
```bash
# Docker
docker-compose --profile game-dev up game-dev

# Then in container
python main.py --headless
```

### Performance Tuning

**Optimize Docker image:**
```bash
# Multi-stage build already optimized
# Image size: ~300MB (from ~1GB+ without optimization)
```

**Reduce startup time:**
- Use image caching
- Pre-pull images: `docker pull thirsty-game:latest`
- Use local registry for frequent deployments

**Scale for performance:**
```bash
# Kubernetes HPA already configured
# Manual: kubectl scale deployment game-server --replicas=3
```

---

## 🎯 Deployment Checklist

### Pre-Deployment

- [ ] All tests passing (`make test`)
- [ ] Docker images built (`make game-build`)
- [ ] Environment variables configured
- [ ] Persistent storage configured
- [ ] Resource limits set
- [ ] Health checks validated

### Post-Deployment

- [ ] Services running (`make deploy-status`)
- [ ] Health checks passing
- [ ] Logs show no errors
- [ ] Save files persisting
- [ ] Resource usage normal
- [ ] Backups configured

### Production Readiness

- [ ] CI/CD pipeline configured
- [ ] Monitoring setup
- [ ] Alerting configured
- [ ] Backup strategy implemented
- [ ] Rollback plan documented
- [ ] Load testing completed
- [ ] Security scan passed
- [ ] Documentation updated

---

## 📚 Additional Resources

- [README.md](../README.md) - Project overview
- [GAME_GUIDE.md](../docs/GAME_GUIDE.md) - Game documentation
- [PROJECT_COMPLETE.md](../PROJECT_COMPLETE.md) - Implementation details
- [QUICKSTART.md](../QUICKSTART.md) - Quick start guide

---

## 🆘 Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review GitHub Issues
3. Check application logs
4. Verify deployment status

---

**Built with ❤️ by Thirsty's Game Studio**
*God-Tier Architecture | Monolithic Density | Production Ready* 🚀
