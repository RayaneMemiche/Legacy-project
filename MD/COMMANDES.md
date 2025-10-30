# 🚀 Guide des Commandes - AWKWARD LEGACY

**Projet:** AWKWARD LEGACY (Modernisation GeneWeb)
**Date:** 30 Octobre 2025
**Version:** 1.0

Ce document regroupe **TOUTES** les commandes nécessaires pour travailler sur le projet AWKWARD LEGACY.

---

## 📋 Table des Matières

1. [Configuration Initiale](#-configuration-initiale)
2. [Lancer le Projet](#-lancer-le-projet)
3. [Tests](#-tests)
4. [Coverage](#-coverage)
5. [Développement](#-développement)
6. [Git & Versioning](#-git--versioning)
7. [Docker](#-docker)
8. [Base de Données](#-base-de-données)
9. [Sécurité & Conformité](#-sécurité--conformité)
10. [Production](#-production)

---

## 🔧 Configuration Initiale

### 1. Cloner le Projet

```bash
# Cloner le repo
git clone https://github.com/NicolasPoupon/Legacy-project.git
cd Legacy-project

# Créer votre branche
git checkout -b votre-nom
```

### 2. Créer l'Environnement Virtuel

```bash
# Créer le venv
python3 -m venv venv

# Activer le venv (macOS/Linux)
source venv/bin/activate

# Activer le venv (Windows)
venv\Scripts\activate
```

### 3. Installer les Dépendances

```bash
# Activer le venv
source venv/bin/activate

# Installer toutes les dépendances
pip install -r requirements.txt

# OU installer manuellement:
pip install flask flask-cors
pip install pytest pytest-cov pytest-mock pytest-asyncio
pip install locust
pip install bcrypt argon2-cffi pyjwt cryptography
pip install pylint flake8 black isort mypy
pip install bandit safety
```

### 4. Vérifier l'Installation

```bash
# Vérifier Python
python3 --version
# Attendu: Python 3.12.12

# Vérifier pytest
pytest --version
# Attendu: pytest 7.4.3

# Vérifier pip
pip list
```

---

## 🚀 Lancer le Projet

### Mode Développement (Backend seul)

```bash
# Se placer dans le bon dossier
cd LegacyProject/modernProject

# Activer le venv
source venv/bin/activate

# Lancer le serveur Flask
python3 -m flask --app lib.wserver run --debug --port 5000

# OU via le script
python3 lib/wserver.py
```

**Le serveur sera accessible à**: `http://localhost:5000`

### Mode Production (Docker)

```bash
# Build et démarrage de tous les services
docker-compose up -d

# Vérifier les services
docker-compose ps

# Logs en temps réel
docker-compose logs -f

# Arrêter tous les services
docker-compose down
```

**Services disponibles**:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:5000`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
- Nginx: `http://localhost:80`
- Monitoring: `http://localhost:9090` (Prometheus)
- Grafana: `http://localhost:3001`

### Lancer Frontend + Backend (Développement)

```bash
# Terminal 1 - Backend
cd LegacyProject/modernProject
source venv/bin/activate
python3 -m flask --app lib.wserver run --debug --port 5000

# Terminal 2 - Frontend (si React/Vue)
cd frontend
npm install
npm run dev
```

---

## 🧪 Tests

### Lancer TOUS les Tests

```bash
# Se placer dans le bon dossier
cd LegacyProject/modernProject

# Activer le venv
source venv/bin/activate

# Lancer tous les tests
pytest tests/ -v

# Avec output détaillé
pytest tests/ -vv

# Avec temps d'exécution
pytest tests/ -v --durations=10
```

### Tests par Catégorie

#### Tests Unitaires

```bash
# Tous les tests unitaires
pytest tests/test_*.py -v

# Tests d'un module spécifique
pytest tests/test_calendar.py -v
pytest tests/test_ast.py -v
pytest tests/test_database.py -v
```

#### Tests Fonctionnels

```bash
# Tous les tests fonctionnels
pytest tests/functional/ -v

# Tests spécifiques
pytest tests/functional/test_person_management.py -v
pytest tests/functional/test_family_relationships.py -v
pytest tests/functional/test_search_functionality.py -v
```

#### Tests d'Intégration

```bash
# Tous les tests d'intégration
pytest tests/integration/ -v

# Suite d'intégration basique
pytest tests/integration/test_integration_suite.py -v

# Suite d'intégration complète
pytest tests/integration/test_complete_integration.py -v

# Tests API
pytest tests/integration/test_api_integration.py -v
```

#### Tests de Performance

```bash
# Benchmarks unitaires
pytest tests/performance/test_benchmarks.py -v

# Tests de charge (Locust)
cd tests/performance
locust -f test_load_testing.py --headless -u 100 -r 10 -t 5m --host=http://localhost:5000

# Avec interface web
locust -f test_load_testing.py --host=http://localhost:5000
# Puis ouvrir: http://localhost:8089
```

#### Tests de Sécurité

```bash
# Tests OWASP Top 10
pytest tests/security/test_owasp_top10.py -v

# Tests authentification
pytest tests/security/test_authentication.py -v

# Tests autorisation (RBAC)
pytest tests/security/test_authorization.py -v

# Tests chiffrement
pytest tests/security/test_encryption.py -v

# Scan de sécurité complet (Bandit)
bandit -r lib/ -f json -o security_report.json
bandit -r lib/ -ll  # Affiche seulement High/Medium severity
```

#### Tests de Conformité RGPD

```bash
# Tests droits RGPD
pytest tests/compliance/test_rgpd_rights.py -v

# Tests consentement
pytest tests/compliance/test_rgpd_consent.py -v

# Tests protection données
pytest tests/compliance/test_rgpd_data_protection.py -v

# Tests portabilité
pytest tests/compliance/test_rgpd_portability.py -v
```

### Tests Spécifiques

```bash
# Test une classe spécifique
pytest tests/test_calendar.py::TestSDNGregorian -v

# Test une méthode spécifique
pytest tests/test_calendar.py::TestSDNGregorian::test_gregorian_roundtrip -v

# Tests avec pattern matching
pytest tests/ -k "calendar" -v
pytest tests/ -k "not slow" -v

# Tests avec markers
pytest tests/ -m "integration" -v
pytest tests/ -m "not slow" -v
```

### Script de Test Complet

```bash
# Utiliser le script fourni
cd LegacyProject/modernProject
./run_all_tests.sh

# OU créer votre propre script:
cat > run_tests.sh << 'EOF'
#!/bin/bash
echo "🧪 Lancement des tests..."
source venv/bin/activate

echo "1. Tests unitaires..."
pytest tests/test_*.py -v

echo "2. Tests fonctionnels..."
pytest tests/functional/ -v

echo "3. Tests d'intégration..."
pytest tests/integration/ -v

echo "4. Tests de performance..."
pytest tests/performance/test_benchmarks.py -v

echo "5. Tests de sécurité..."
pytest tests/security/ -v

echo "6. Tests RGPD..."
pytest tests/compliance/ -v

echo "✅ Tous les tests terminés!"
EOF

chmod +x run_tests.sh
./run_tests.sh
```

---

## 📊 Coverage

### Générer le Coverage

```bash
# Coverage avec rapport terminal
pytest tests/ --cov=lib --cov-report=term

# Coverage avec rapport HTML
pytest tests/ --cov=lib --cov-report=html

# Coverage avec lignes manquantes
pytest tests/ --cov=lib --cov-report=term-missing

# Coverage complet (HTML + terminal)
pytest tests/ --cov=lib --cov-report=html --cov-report=term-missing -v
```

### Visualiser le Coverage

```bash
# Ouvrir le rapport HTML
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Coverage par Module

```bash
# Coverage d'un module spécifique
pytest tests/test_calendar.py --cov=lib.gwcalendar --cov-report=term

# Coverage de plusieurs modules
pytest tests/ --cov=lib.gwcalendar --cov=lib.gwast --cov-report=html
```

### Coverage avec Seuil Minimum

```bash
# Échouer si coverage < 80%
pytest tests/ --cov=lib --cov-fail-under=80

# Avec rapport HTML
pytest tests/ --cov=lib --cov-report=html --cov-fail-under=80
```

---

## 💻 Développement

### Linting & Formatting

```bash
# Pylint (analyse statique)
pylint lib/ --rcfile=.pylintrc

# Flake8 (style PEP8)
flake8 lib/ --max-line-length=100

# Black (auto-formatting)
black lib/ tests/

# isort (tri des imports)
isort lib/ tests/

# Tout en une commande
black lib/ tests/ && isort lib/ tests/ && pylint lib/ && flake8 lib/
```

### Type Checking

```bash
# MyPy (vérification types)
mypy lib/

# Avec rapport détaillé
mypy lib/ --show-error-codes --pretty
```

### Pre-commit Hooks

```bash
# Installer pre-commit
pip install pre-commit

# Installer les hooks
pre-commit install

# Lancer manuellement
pre-commit run --all-files
```

### Debugging

```bash
# Lancer pytest avec debugger
pytest tests/test_calendar.py --pdb

# S'arrêter à la première erreur
pytest tests/ -x --pdb

# Afficher print() dans les tests
pytest tests/ -v -s

# Verbose maximum
pytest tests/ -vv -s
```

---

## 🌿 Git & Versioning

### Workflow Git

```bash
# Vérifier l'état
git status

# Créer une nouvelle branche
git checkout -b feature/ma-fonctionnalite

# Ajouter les modifications
git add .

# Commit professionnel
git commit -m "feat(module): Description courte

- Détail 1
- Détail 2

Fixes #123"

# Push vers remote
git push origin feature/ma-fonctionnalite

# Pull depuis remote
git pull origin rayane
```

### Commits Propres

```bash
# Voir les derniers commits
git log --oneline -10

# Amend le dernier commit
git commit --amend

# Rebase interactif
git rebase -i HEAD~3

# Cherry-pick un commit
git cherry-pick abc123
```

### Gestion des Branches

```bash
# Lister les branches
git branch -a

# Changer de branche
git checkout rayane

# Merger une branche
git merge feature/ma-fonctionnalite

# Supprimer une branche locale
git branch -d feature/ma-fonctionnalite

# Supprimer une branche remote
git push origin --delete feature/ma-fonctionnalite
```

---

## 🐳 Docker

### Build & Run

```bash
# Build l'image
docker build -t awkward-legacy:latest .

# Run le conteneur
docker run -d -p 5000:5000 --name awkward awkward-legacy:latest

# Logs du conteneur
docker logs -f awkward

# Arrêter le conteneur
docker stop awkward

# Supprimer le conteneur
docker rm awkward
```

### Docker Compose

```bash
# Build et démarrer tous les services
docker-compose up -d

# Build sans cache
docker-compose build --no-cache

# Démarrer un service spécifique
docker-compose up -d backend

# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v

# Voir les logs
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f backend

# Entrer dans un conteneur
docker-compose exec backend bash

# Redémarrer un service
docker-compose restart backend

# Voir l'état des services
docker-compose ps
```

### Nettoyage Docker

```bash
# Supprimer conteneurs arrêtés
docker container prune

# Supprimer images non utilisées
docker image prune

# Supprimer volumes non utilisés
docker volume prune

# Nettoyage complet
docker system prune -a --volumes
```

---

## 🗄️ Base de Données

### PostgreSQL (Production)

```bash
# Se connecter à la DB
docker-compose exec postgres psql -U awkward -d awkward_db

# Via psql local
psql -h localhost -U awkward -d awkward_db

# Dump de la DB
pg_dump -h localhost -U awkward awkward_db > backup.sql

# Restore de la DB
psql -h localhost -U awkward awkward_db < backup.sql

# Créer une DB de test
createdb -h localhost -U awkward awkward_test
```

### Commandes SQL Utiles

```sql
-- Lister les tables
\dt

-- Describe une table
\d persons

-- Compter les entrées
SELECT COUNT(*) FROM persons;

-- Voir les 10 dernières personnes
SELECT * FROM persons ORDER BY created_at DESC LIMIT 10;

-- Chercher une personne
SELECT * FROM persons WHERE name LIKE '%Doe%';

-- Quitter
\q
```

### Migrations (Alembic)

```bash
# Installer Alembic
pip install alembic

# Initialiser
alembic init migrations

# Créer une migration
alembic revision -m "Add new column"

# Appliquer les migrations
alembic upgrade head

# Rollback une migration
alembic downgrade -1

# Voir l'historique
alembic history
```

---

## 🔒 Sécurité & Conformité

### Scan de Vulnérabilités

```bash
# Bandit (SAST)
bandit -r lib/ -f json -o security_report.json
bandit -r lib/ -ll  # High/Medium seulement

# Safety (dépendances)
safety check

# Pip-audit
pip install pip-audit
pip-audit

# Trivy (conteneurs)
trivy image awkward-legacy:latest
```

### Tests Sécurité OWASP

```bash
# Suite complète OWASP
pytest tests/security/test_owasp_top10.py -v

# ZAP Proxy (si installé)
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t http://localhost:5000 \
  -r security_scan.html
```

### Validation RGPD

```bash
# Tests RGPD complets
pytest tests/compliance/ -v

# Export des données utilisateur (Art. 20)
python3 -c "
from lib.rgpd import export_user_data
export_user_data(user_id=1, format='json')
"

# Suppression données (Art. 17)
python3 -c "
from lib.rgpd import delete_user_data
delete_user_data(user_id=1)
"
```

---

## 🏭 Production

### Vérifications Pré-déploiement

```bash
# 1. Tests complets
pytest tests/ -v --cov=lib --cov-fail-under=80

# 2. Linting
pylint lib/ && flake8 lib/

# 3. Type checking
mypy lib/

# 4. Scan sécurité
bandit -r lib/ -ll
safety check

# 5. Tests de charge
cd tests/performance
locust -f test_load_testing.py --headless -u 500 -r 50 -t 10m --host=http://localhost:5000
```

### Déploiement Docker

```bash
# Build pour production
docker build -t awkward-legacy:v1.0 -f Dockerfile.prod .

# Tag pour registry
docker tag awkward-legacy:v1.0 registry.example.com/awkward-legacy:v1.0

# Push vers registry
docker push registry.example.com/awkward-legacy:v1.0

# Deploy avec docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

### Monitoring Production

```bash
# Logs en temps réel
docker-compose logs -f backend

# Métriques Prometheus
curl http://localhost:9090/metrics

# Health check
curl http://localhost:5000/health

# Status API
curl http://localhost:5000/api/status
```

### Backup & Restore

```bash
# Backup complet
./scripts/backup.sh

# Backup DB seulement
pg_dump -h localhost -U awkward awkward_db | gzip > backup_$(date +%Y%m%d).sql.gz

# Restore
gunzip -c backup_20251030.sql.gz | psql -h localhost -U awkward awkward_db

# Backup volumes Docker
docker run --rm -v awkward_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/data_backup.tar.gz /data
```

---

## 📚 Commandes Utiles Rapides

### Développement Quotidien

```bash
# Setup complet
git pull && source venv/bin/activate && pip install -r requirements.txt

# Lancer tests + coverage
pytest tests/ --cov=lib --cov-report=html -v

# Lancer le serveur
python3 -m flask --app lib.wserver run --debug

# Format + lint
black lib/ tests/ && isort lib/ tests/ && pylint lib/

# Commit + push
git add . && git commit -m "feat: ma description" && git push
```

### Debugging Rapide

```bash
# Tests avec output
pytest tests/test_calendar.py -v -s

# Tests avec pdb
pytest tests/test_calendar.py --pdb

# Trouver tests lents
pytest tests/ --durations=10

# Logs Flask
FLASK_ENV=development python3 lib/wserver.py
```

### Checks Qualité

```bash
# Quick check
black lib/ --check && flake8 lib/ && pytest tests/ -v

# Full check
black lib/ tests/ && isort lib/ tests/ && pylint lib/ && \
mypy lib/ && bandit -r lib/ && pytest tests/ --cov=lib --cov-fail-under=80
```

---

## 🆘 Troubleshooting

### Problèmes Courants

#### Module Not Found
```bash
# Vérifier le PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# OU installer en mode dev
pip install -e .
```

#### Tests Échouent
```bash
# Nettoyer le cache
rm -rf .pytest_cache __pycache__

# Réinstaller dépendances
pip install -r requirements.txt --force-reinstall

# Vérifier la DB de test
pytest tests/ --create-db
```

#### Docker Issues
```bash
# Rebuild complet
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# Nettoyer Docker
docker system prune -a --volumes
```

#### Port Déjà Utilisé
```bash
# Trouver le processus
lsof -i :5000

# Tuer le processus
kill -9 <PID>
```

---

## 📖 Documentation Complète

Pour plus de détails, consulter:

- [README.md](README.md) - Vue d'ensemble du projet
- [INDEX.md](INDEX.md) - Navigation complète
- [METHODOLOGIE_TESTS.md](METHODOLOGIE_TESTS.md) - Stratégie de test
- [GUIDE_LANCEMENT.md](GUIDE_LANCEMENT.md) - Guide de démarrage
- [PRODUCTION_DEPLOYMENT_PLAN.md](PRODUCTION_DEPLOYMENT_PLAN.md) - Plan de déploiement
- [avancement/README.md](avancement/README.md) - Historique du projet

---

## 📞 Support

Pour toute question:
1. Consulter la documentation ci-dessus
2. Voir les exemples dans `tests/`
3. Contacter l'équipe CoinLegacy Inc.

---

**Date:** 30 Octobre 2025
**Version:** 1.0
**Auteur:** CoinLegacy Inc. + Claude Code
**Statut:** ✅ PRODUCTION-READY

🚀 **HAPPY CODING!** 🚀
