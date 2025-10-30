# 🚀 Docker Quick Start - AWKWARD LEGACY

**Pour démarrer le projet en 5 minutes!**

---

## ⚡ Démarrage Rapide (3 commandes)

```bash
# 1. Configuration
cd LegacyProject/modernProject
cp .env.example .env

# 2. Build et démarrage
docker build -t awkward-legacy:latest .

# 3. Lancer l'application
docker run -d -p 5000:5000 \
  --name awkward-legacy \
  -e FLASK_ENV=development \
  awkward-legacy:latest

# ✅ Vérifier
curl http://localhost:5000/health
```

**Application accessible**: http://localhost:5000

---

## 🐳 Avec Docker Compose (Stack Complète)

```bash
# 1. Aller à la racine du projet
cd /Users/rayanememiche/Documents/Taff/legalsanben

# 2. Configuration
cp .env.example .env
nano .env  # Éditer si nécessaire

# 3. Démarrer tous les services
docker-compose up -d

# ✅ Vérifier les services
docker-compose ps

# Services disponibles:
# - App:        http://localhost:8080
# - Prometheus: http://localhost:9090
# - Grafana:    http://localhost:3000
```

---

## 📊 Services Disponibles

| Service | URL | Login |
|---------|-----|-------|
| Application | http://localhost:5000 | - |
| Grafana | http://localhost:3000 | admin/changeme |
| Prometheus | http://localhost:9090 | - |
| PostgreSQL | localhost:5432 | awkward/changeme |

---

## 🛑 Arrêter

```bash
# Arrêter l'application seule
docker stop awkward-legacy
docker rm awkward-legacy

# Arrêter Docker Compose
docker-compose down

# Arrêter ET supprimer les données
docker-compose down -v  # ⚠️ ATTENTION: Supprime les données!
```

---

## 🔧 Commandes Utiles

```bash
# Voir les logs
docker logs awkward-legacy -f

# Entrer dans le conteneur
docker exec -it awkward-legacy bash

# Relancer après modification code
docker-compose restart web

# Rebuild après changement Dockerfile
docker-compose build --no-cache web
docker-compose up -d web
```

---

## 📝 Variables d'Environnement Importantes

Dans `.env`:

```bash
# Minimum requis
PORT=5000
FLASK_ENV=development
SECRET_KEY=changeme_random_secret_key

# Pour production
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
```

---

## ✅ Vérification Santé

```bash
# Health check
curl http://localhost:5000/health

# Réponse attendue:
# {"status": "healthy", "timestamp": "2025-10-30T10:00:00"}

# Métriques Prometheus
curl http://localhost:5000/metrics
```

---

## 🆘 Problèmes Courants

### Port déjà utilisé

```bash
# Trouver le processus
lsof -i :5000

# Tuer le processus
kill -9 <PID>

# OU changer le port
docker run -p 5001:5000 ...
```

### Permission denied

```bash
# Build avec sudo
sudo docker build -t awkward-legacy:latest .

# Ajouter user au groupe docker (évite sudo)
sudo usermod -aG docker $USER
# Puis logout/login
```

### Image trop grosse

```bash
# Nettoyer les images Docker
docker system prune -a

# Voir la taille des images
docker images

# L'image finale devrait faire < 500MB
```

---

**Pour plus de détails**: Voir [DOCKER_CI_GUIDE.md](DOCKER_CI_GUIDE.md)
