#  Guide Docker & CI/CD - AWKWARD LEGACY

**Date:** 30 Octobre 2025
**Version:** 1.0
**Auteur:** CoinLegacy Inc. + Claude Code

---

##  Table des Matières

1. [Vue d'Ensemble](#-vue-densemble)
2. [Docker](#-docker)
3. [CI/CD GitHub Actions](#-cicd-github-actions)
4. [Commandes Docker](#-commandes-docker)
5. [Déploiement](#-déploiement)
6. [Monitoring](#-monitoring)
7. [Troubleshooting](#-troubleshooting)

---

##  Vue d'Ensemble

Le projet AWKWARD LEGACY est entièrement dockerisé avec:
- **Docker multi-stage** pour optimiser la taille des images
- **Docker Compose** avec 8 services orchestrés
- **CI/CD GitHub Actions** avec 8 jobs automatisés
- **Monitoring** complet (Prometheus + Grafana)

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    NGINX (Reverse Proxy)                │
│                  Port 80/443 (SSL/TLS)                  │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│               Flask App (modernProject)                 │
│                    Port 5000                            │
└───────┬──────────────┬──────────────┬──────────────────┘
        │              │              │
        ▼              ▼              ▼
   ┌────────┐    ┌──────────┐   ┌──────────┐
   │ Redis  │    │PostgreSQL│   │Prometheus│
   │ Cache  │    │   DB     │   │ Metrics  │
   └────────┘    └──────────┘   └──────────┘
                                      │
                                      ▼
                                 ┌──────────┐
                                 │ Grafana  │
                                 │Dashboard │
                                 └──────────┘
```

---

##  Docker

### Fichiers Docker

Le projet contient:

1. **`Dockerfile`** - Image multi-stage optimisée
2. **`docker-compose.yml`** - Orchestration complète (8 services)
3. **`docker-entrypoint.sh`** - Script d'initialisation
4. **`.dockerignore`** - Exclusions pour build rapide
5. **`.env.example`** - Template de configuration

### Structure du Dockerfile

```dockerfile
# Stage 1: Builder - Installation dépendances
FROM python:3.12-slim as builder
  → Installe gcc, dépendances système
  → Crée venv avec toutes les dépendances Python
  → Optimise pour taille minimale

# Stage 2: Runtime - Image finale
FROM python:3.12-slim
  → Copie uniquement le venv du builder
  → Utilisateur non-root (sécurité)
  → Health check intégré
  → Image finale < 500MB
```

### Services Docker Compose

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| **web** | `awkward-legacy:latest` | 5000 | Application Flask principale |
| **nginx** | `nginx:1.21-alpine` | 80, 443 | Reverse proxy + SSL |
| **redis** | `redis:7-alpine` | 6379 | Cache & sessions |
| **postgres** | `postgres:14-alpine` | 5432 | Base de données |
| **prometheus** | `prom/prometheus:latest` | 9090 | Métriques |
| **grafana** | `grafana/grafana:latest` | 3000 | Dashboards |
| **backup** | `alpine:latest` | - | Sauvegardes automatiques |
| **certbot** | `certbot/certbot:latest` | - | Renouvellement SSL |

---

##  CI/CD GitHub Actions

### Pipeline Complet

Le fichier `.github/workflows/ci.yml` contient **8 jobs**:

```
┌────────────────────────────────────────────────────────┐
│                    CI/CD Pipeline                       │
└────────────────────────────────────────────────────────┘
    │
    ├─► Job 1: Lint & Code Quality
    │   └─ Black, isort, Pylint, Flake8, Bandit
    │
    ├─► Job 2: Unit Tests (Matrix: Python 3.10, 3.11, 3.12)
    │   └─ Pytest + Coverage → Codecov
    │
    ├─► Job 3: Integration Tests
    │   └─ Tests avec Redis + PostgreSQL
    │
    ├─► Job 4: Security Scan
    │   └─ Safety, pip-audit, Trivy
    │
    ├─► Job 5: Build Docker Image
    │   └─ Multi-arch (amd64, arm64) → GHCR
    │
    ├─► Job 6: Deploy to Staging (auto)
    │   └─ Si push sur develop
    │
    ├─► Job 7: Deploy to Production (manual)
    │   └─ Si push sur main + approval
    │
    └─► Job 8: Generate Release Notes
        └─ Changelog + GitHub Release
```

### Triggers

-  **Push** sur `main`, `rayane`, `develop`
-  **Pull Request** vers `main`, `rayane`
-  **Manual trigger** (workflow_dispatch)

### Artefacts Générés

| Artefact | Description |
|----------|-------------|
| `bandit-report.json` | Scan de sécurité |
| `coverage-html-*` | Rapports coverage HTML |
| `test-results-*` | Résultats JUnit XML |
| `safety-report.json` | Vulnérabilités dépendances |
| `trivy-results.sarif` | Scan image Docker |

---

##  Commandes Docker

### Configuration Initiale

```bash
# 1. Cloner le repo
git clone https://github.com/NicolasPoupon/Legacy-project.git
cd Legacy-project/LegacyProject/modernProject

# 2. Copier et configurer .env
cp .env.example .env
nano .env  # Éditer les valeurs

# 3. Construire les images
docker-compose build

# 4. Démarrer tous les services
docker-compose up -d
```

### Démarrage et Arrêt

```bash
# Démarrer tous les services
docker-compose up -d

# Démarrer en mode verbose (logs visibles)
docker-compose up

# Démarrer un service spécifique
docker-compose up -d web

# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes ( PERTE DE DONNÉES)
docker-compose down -v

# Redémarrer un service
docker-compose restart web
```

### Build et Rebuild

```bash
# Build sans cache
docker-compose build --no-cache

# Build avec pull des dernières images de base
docker-compose build --pull

# Rebuild et redémarrer
docker-compose up -d --build

# Rebuild après changement de code
docker-compose build web && docker-compose up -d web
```

### Logs et Debugging

```bash
# Voir les logs de tous les services
docker-compose logs

# Logs en temps réel
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f web

# Dernières 100 lignes
docker-compose logs --tail=100 web

# Entrer dans un conteneur
docker-compose exec web bash

# Exécuter une commande
docker-compose exec web python -c "print('Hello')"
```

### Gestion des Volumes

```bash
# Lister les volumes
docker volume ls

# Voir les détails d'un volume
docker volume inspect awkward-legacy-data

# Backup manuel d'un volume
docker run --rm -v awkward-legacy-data:/data \
  -v $(pwd):/backup alpine \
  tar czf /backup/data-backup-$(date +%Y%m%d).tar.gz /data

# Restore d'un volume
docker run --rm -v awkward-legacy-data:/data \
  -v $(pwd):/backup alpine \
  tar xzf /backup/data-backup-20251030.tar.gz -C /
```

### Scaling

```bash
# Mettre à l'échelle le service web (3 instances)
docker-compose up -d --scale web=3

# Vérifier les instances
docker-compose ps
```

### Health Checks

```bash
# Vérifier le statut de tous les services
docker-compose ps

# Health check manuel
curl http://localhost:5000/health

# Inspect health d'un conteneur
docker inspect awkward-legacy-web | grep -A 10 Health
```

---

##  Déploiement

### Déploiement Local (Développement)

```bash
# 1. Setup
cd LegacyProject/modernProject
cp .env.example .env

# 2. Build et démarrage
docker-compose up -d

# 3. Vérifier
curl http://localhost:5000/health

# 4. Accès services
# - App: http://localhost:5000
# - Grafana: http://localhost:3000 (admin/changeme)
# - Prometheus: http://localhost:9090
```

### Déploiement Staging (Auto via CI/CD)

**Trigger**: Push sur branche `develop`

```bash
# Le CI/CD fait automatiquement:
# 1. Run tous les tests
# 2. Build image Docker
# 3. Push vers registry
# 4. SSH vers serveur staging
# 5. Pull nouvelle image
# 6. Restart services
# 7. Health check
```

**Configuration requise**:

Secrets GitHub à configurer:
```
STAGING_HOST=staging.awkward-legacy.com
STAGING_USER=deploy
STAGING_SSH_KEY=<private_key>
```

### Déploiement Production (Manuel via CI/CD)

**Trigger**: Push sur branche `main` + **Approval manuelle**

```bash
# 1. Push sur main
git checkout main
git merge rayane
git push origin main

# 2. Aller sur GitHub Actions
# 3. Approuver le déploiement production
# 4. Le CI/CD déploie automatiquement
```

### Déploiement Manuel (Serveur distant)

```bash
# Sur le serveur de production
ssh user@production-server

cd /opt/awkward-legacy

# Pull dernière image
docker-compose pull

# Redémarrer avec nouvelle image
docker-compose up -d --force-recreate

# Vérifier
docker-compose ps
curl https://awkward-legacy.com/health
```

---

##  Monitoring

### Prometheus (Métriques)

**URL**: `http://localhost:9090`

**Métriques disponibles**:
- Requêtes HTTP (`http_requests_total`)
- Latence (`http_request_duration_seconds`)
- Erreurs (`http_errors_total`)
- CPU/Memory des conteneurs
- État des services

**Queries utiles**:
```promql
# Taux de requêtes par seconde
rate(http_requests_total[5m])

# Latence P95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Taux d'erreur
rate(http_errors_total[5m]) / rate(http_requests_total[5m])
```

### Grafana (Dashboards)

**URL**: `http://localhost:3000`
**Login**: `admin` / `changeme` (à changer!)

**Dashboards pré-configurés**:
1. **Application Overview** - Métriques globales
2. **Docker Metrics** - État des conteneurs
3. **Database Performance** - PostgreSQL stats
4. **Redis Performance** - Cache hit/miss ratio

### Logs Centralisés

```bash
# Logs de tous les services
docker-compose logs -f

# Filtrer par niveau
docker-compose logs | grep ERROR

# Exporter les logs
docker-compose logs > logs-$(date +%Y%m%d).txt
```

---

##  Troubleshooting

### Problème: Conteneur ne démarre pas

```bash
# 1. Vérifier les logs
docker-compose logs web

# 2. Vérifier la config
docker-compose config

# 3. Inspecter le conteneur
docker inspect awkward-legacy-web

# 4. Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Problème: Permission denied

```bash
# Vérifier les permissions des volumes
docker-compose exec web ls -la /app

# Fix permissions
docker-compose exec web chown -R awkward:awkward /app/data
```

### Problème: Out of memory

```bash
# Vérifier l'utilisation mémoire
docker stats

# Augmenter la limite dans docker-compose.yml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 4G  # Augmenter ici
```

### Problème: Port déjà utilisé

```bash
# Trouver le processus utilisant le port
lsof -i :5000

# Tuer le processus
kill -9 <PID>

# OU changer le port dans .env
PORT=5001
```

### Problème: Base de données inaccessible

```bash
# Vérifier que PostgreSQL est démarré
docker-compose ps postgres

# Restart PostgreSQL
docker-compose restart postgres

# Voir les logs
docker-compose logs postgres

# Tester la connexion
docker-compose exec postgres psql -U awkward -d awkward_legacy
```

### Problème: CI/CD échoue

**Tests échouent:**
```bash
# Lancer les tests localement
docker-compose exec web pytest tests/ -v

# Voir les détails dans GitHub Actions
# → Cliquer sur le job échoué
# → Lire les logs complets
```

**Build Docker échoue:**
```bash
# Build local avec logs verbeux
docker-compose build --no-cache --progress=plain

# Vérifier .dockerignore
cat .dockerignore
```

**Déploiement échoue:**
```bash
# Vérifier les secrets GitHub
# Settings → Secrets and variables → Actions

# Tester SSH manuellement
ssh -i ~/.ssh/deploy_key user@production-server
```

---

##  Ressources Supplémentaires

### Documentation

- [COMMANDES.md](COMMANDES.md) - Toutes les commandes du projet
- [METHODOLOGIE_TESTS.md](METHODOLOGIE_TESTS.md) - Stratégie de test
- [PRODUCTION_DEPLOYMENT_PLAN.md](PRODUCTION_DEPLOYMENT_PLAN.md) - Plan de déploiement
- [README.md](README.md) - Vue d'ensemble

### Configuration

- [.env.example](.env.example) - Template variables d'environnement
- [docker-compose.yml](docker-compose.yml) - Orchestration services
- [Dockerfile](Dockerfile) - Build image
- [.github/workflows/ci.yml](.github/workflows/ci.yml) - Pipeline CI/CD

### Monitoring

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- Application: http://localhost:5000

---

##  Quick Start Complet

### Pour Développement

```bash
# 1. Clone
git clone https://github.com/NicolasPoupon/Legacy-project.git
cd Legacy-project/LegacyProject/modernProject

# 2. Setup environnement
cp .env.example .env
nano .env  # Éditer si nécessaire

# 3. Build et démarrage
docker-compose build
docker-compose up -d

# 4. Vérifier
curl http://localhost:5000/health
```

### Pour Production

```bash
# 1. Sur le serveur
ssh user@production-server
cd /opt/awkward-legacy

# 2. Configurer
cp .env.example .env
nano .env  # Configurer pour production

# 3. SSL (Let's Encrypt)
docker-compose run certbot certonly --webroot \
  -w /var/www/certbot \
  -d awkward-legacy.com

# 4. Démarrer
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 5. Vérifier
curl https://awkward-legacy.com/health
```

---

**Date:** 30 Octobre 2025
**Version:** 1.0
**Status:**  PRODUCTION-READY

 **Docker is ready!**  **CI/CD is configured!**
