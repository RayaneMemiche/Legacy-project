# Procedure de Deploiement - AWKWARD LEGACY

**Version:** 1.0
**Date:** Mars 2026
**Projet:** AWKWARD LEGACY - Modernisation de GeneWeb
**Referentiel RNCP:** Bloc 6 - C31.1, C31.2

---

## Table des Matieres

1. [Vue d'ensemble de la procedure](#1-vue-densemble-de-la-procedure)
2. [Prerequis et preparation](#2-prerequis-et-preparation)
3. [Deploiement automatise via CI/CD](#3-deploiement-automatise-via-cicd)
4. [Deploiement manuel (procedure de secours)](#4-deploiement-manuel-procedure-de-secours)
5. [Verification et tests post-deploiement](#5-verification-et-tests-post-deploiement)
6. [Rollback](#6-rollback)
7. [Preuves de fonctionnement](#7-preuves-de-fonctionnement)

---

## 1. Vue d'ensemble de la procedure

### 1.1 Principe

Le deploiement d'AWKWARD LEGACY est **entierement automatise** via GitHub Actions. Un simple `git push` sur la branche `main` declenche le pipeline complet qui va :

1. Verifier la qualite du code (lint, securite)
2. Executer tous les tests (unitaires, integration, securite)
3. Construire l'image Docker
4. Deployer en staging puis production
5. Effectuer un health check
6. Generer les release notes

### 1.2 Flux de deploiement

```
Developer
    |
    | git push origin main
    v
GitHub Actions (CI/CD)
    |
    +---> Lint & Quality (2 min)
    |           |
    |           v OK
    +---> Tests Python 3.10/3.11/3.12 (4 min, parallele)
    |           |
    |           v OK
    +---> Integration Tests Redis+PostgreSQL (3 min)
    |           |
    |           v OK
    +---> Security Scan - Safety + pip-audit (2 min)
    |           |
    |           v OK
    +---> Build Docker multi-arch (amd64 + arm64) (8 min)
    |           |
    |           v OK
    +---> Push image vers ghcr.io
    |           |
    |           v
    +---> Deploy Staging (develop branch)
    |     OU
    +---> Deploy Production (main branch)
    |           |
    |           v
    +---> Health Check (/health endpoint)
    |           |
    |           v OK
    +---> Release Notes (git-cliff + GitHub Release)
    |
    v
Application disponible
```

**Temps total : ~15-20 minutes de bout en bout**

---

## 2. Prerequis et preparation

### 2.1 Cote serveur

```bash
# 1. Installer Docker
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl enable docker && sudo systemctl start docker

# 2. Creer l'utilisateur applicatif
sudo adduser --disabled-password awkward
sudo usermod -aG docker awkward

# 3. Creer les repertoires
sudo mkdir -p /var/lib/awkward-legacy/db /var/lib/awkward-legacy/backups
sudo mkdir -p /var/log/awkward-legacy
sudo chown -R awkward:awkward /var/lib/awkward-legacy /var/log/awkward-legacy

# 4. Configurer SSL
sudo certbot certonly --standalone -d awkward-legacy.com

# 5. Configurer le firewall
sudo ufw allow 22/tcp && sudo ufw allow 80/tcp && sudo ufw allow 443/tcp
sudo ufw enable
```

### 2.2 Cote GitHub (Secrets)

Dans `Settings > Secrets and variables > Actions`, configurer :

| Secret | Valeur | Usage |
|--------|--------|-------|
| `STAGING_HOST` | IP du serveur staging | SSH deploy staging |
| `STAGING_USER` | `awkward` | Utilisateur SSH |
| `STAGING_SSH_KEY` | Cle privee SSH | Authentification |
| `PRODUCTION_HOST` | IP du serveur prod | SSH deploy production |
| `PRODUCTION_USER` | `awkward` | Utilisateur SSH |
| `PRODUCTION_SSH_KEY` | Cle privee SSH | Authentification |
| `SLACK_WEBHOOK` | URL webhook Slack | Notifications |

### 2.3 Protection de branche

La branche `rayane` (branche principale) est protegee :
- 4 checks CI requis avant merge
- 1 review obligatoire
- Branche a jour avec la base

**Preuve :** Branch protection configuree via GitHub API (voir PR #1)

---

## 3. Deploiement automatise via CI/CD

### 3.1 Declencheur

Le pipeline se declenche automatiquement sur :
- `push` sur `main`, `rayane`, `develop`
- `pull_request` vers `main` ou `rayane`
- `workflow_dispatch` (declenchement manuel depuis l'UI GitHub)

### 3.2 Job 1 : Lint & Code Quality

```yaml
- Black: formatage Python (echec = pipeline bloque)
- isort: ordre des imports
- Pylint: qualite du code (score > 8/10)
- Flake8: style PEP 8
- Bandit: scan securite statique (echec = pipeline bloque)
```

**Artefact produit :** `bandit-report.json` (conserve 90 jours)

### 3.3 Job 2 : Unit Tests (matrix 3.10 / 3.11 / 3.12)

```bash
pytest tests/test_*.py \
  --cov=lib \
  --cov-report=xml \
  --cov-report=html \
  --cov-fail-under=75 \
  -v
```

**Artefacts produits :**
- `junit-3.10.xml`, `junit-3.11.xml`, `junit-3.12.xml` : resultats de tests
- `htmlcov/` : rapport de couverture HTML

### 3.4 Job 3 : Integration Tests

Services lances automatiquement par GitHub Actions :
- Redis 7 (Alpine) sur port 6379
- PostgreSQL 14 (Alpine) sur port 5432

```bash
pytest tests/integration/ -v --tb=short
```

### 3.5 Job 4 : Security Scan

```bash
safety check --json --output safety-report.json
pip-audit --desc
```

**Artefact produit :** `safety-report.json`

### 3.6 Job 5 : Build Docker

```yaml
platforms: linux/amd64,linux/arm64
cache-from: type=gha
cache-to: type=gha,mode=max
push: true  # uniquement si pas une PR
```

Scan de vulnerabilites avec Trivy (SARIF upload vers GitHub Security)

### 3.7 Jobs 6 & 7 : Deploy Staging / Production

```bash
# Sur le serveur via SSH
cd /opt/awkward-legacy
docker-compose pull
docker-compose up -d --force-recreate
docker-compose ps
```

**Health check post-deploiement :**
```bash
sleep 30
curl -f https://awkward-legacy.com/health || exit 1
```

Si le health check echoue, le pipeline echoue et le deploiement est marque comme failed.

### 3.8 Job 8 : Release Notes

Generation automatique du CHANGELOG via `git-cliff` et creation d'une GitHub Release.

---

## 4. Deploiement manuel (procedure de secours)

En cas de probleme avec le CI/CD, la procedure manuelle est documentee dans `LegacyProject/docs/DEPLOYMENT_GUIDE.md`.

### Etape rapide

```bash
# 1. Cloner le repo
git clone https://github.com/NicolasPoupon/Legacy-project.git
cd Legacy-project/LegacyProject/modernProject

# 2. Configurer l'environnement
cp .env.example .env
vim .env  # Renseigner les secrets

# 3. Construire et lancer
docker build -t awkward-legacy:latest .
docker-compose up -d

# 4. Verifier
docker-compose ps
curl http://localhost:5000/health
```

### Gestion du cycle de vie

```bash
# Logs en temps reel
docker-compose logs -f

# Redemarrer un service
docker-compose restart web

# Arreter
docker-compose down

# Statut
docker-compose ps
```

---

## 5. Verification et tests post-deploiement

### 5.1 Health check endpoint

L'endpoint `/health` verifie :
- Statut de l'application
- Connectivite base de donnees
- Espace disque disponible
- Utilisation memoire

```bash
curl -f http://localhost:5000/health
# Reponse attendue: {"status": "healthy", "timestamp": "...", "database": "ok", "disk": "ok"}
```

### 5.2 Smoke tests automatiques

```bash
# Tester les routes principales
curl http://localhost:5000/health      # 200 OK
curl http://localhost:5000/api/persons # 200 OK ou 401 (auth requise)
```

### 5.3 Monitoring

- **Prometheus** : scrape `/metrics` toutes les 15s
- **Grafana** : dashboards temps reel (CPU, memoire, requetes/s, erreurs)
- **Alertes** : notification Slack si uptime < 99.9%

---

## 6. Rollback

### 6.1 Rollback rapide (< 5 minutes)

```bash
# Revenir a l'image precedente
docker-compose down
git checkout v<version-precedente>
docker-compose pull
docker-compose up -d
curl -f http://localhost:5000/health
```

### 6.2 Rollback avec restauration de donnees

```bash
# Arreter l'application
docker-compose down

# Restaurer depuis un backup
./scripts/restore.sh latest

# OU restaurer un backup specifique
./scripts/restore.sh backup_20251017_120000.tar.gz.enc

# Redemarrer
docker-compose up -d
./scripts/check-health.sh
```

### 6.3 Backup automatique

Un backup quotidien est execute via cron a 2h du matin :
```bash
0 2 * * * /home/awkward/scripts/backup.sh >> /var/log/awkward-legacy/backup.log 2>&1
```

Chaque backup :
- Archive la base de donnees GeneWeb (.gwb)
- Chiffre avec AES-256-CBC
- Upload optionnel vers S3 (stockage distant)
- Supprime automatiquement les backups de plus de 90 jours

---

## 7. Preuves de fonctionnement

### 7.1 Fichiers de preuve dans le depot

| Fichier | Contenu | Critere |
|---------|---------|---------|
| `LegacyProject/modernProject/Dockerfile` | Image multi-stage, healthcheck | C31.1 |
| `LegacyProject/modernProject/.github/workflows/ci.yml` | Pipeline 8 jobs | C31.1, C31.2 |
| `LegacyProject/modernProject/docker-entrypoint.sh` | Script d'entree Docker | C31.1 |
| `LegacyProject/docs/DEPLOYMENT_GUIDE.md` | Guide complet 1547 lignes | C31.1 |
| `LegacyProject/modernProject/tests/performance/locustfile.py` | Tests de charge | C31.2 |

### 7.2 Preuves CI/CD (GitHub)

- Pipeline GitHub Actions visible sur : `https://github.com/NicolasPoupon/Legacy-project/actions`
- PR #1 (feature/add-export-csv) : demonstration du pipeline qui bloque le merge
- Historique des commits : deploiements traces via conventional commits

### 7.3 Commande de demonstration

Pour demontrer que le deploiement est fonctionnel localement :

```bash
cd LegacyProject/modernProject
docker build -t awkward-legacy:demo .
docker run -d -p 5000:5000 --name demo awkward-legacy:demo
sleep 10
curl -f http://localhost:5000/health
docker logs demo
docker stop demo && docker rm demo
```

---

**Derniere revision :** Mars 2026
