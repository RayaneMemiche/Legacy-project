# Guide de Déploiement - AWKWARD LEGACY

**Version:** 1.0
**Date:** 17 Octobre 2025
**Projet:** Modernisation de GeneWeb

---

## Table des matières

1. [Prérequis Système](#1-prérequis-système)
2. [Installation Étape par Étape](#2-installation-étape-par-étape)
3. [Configuration](#3-configuration)
4. [Déploiement](#4-déploiement)
5. [Monitoring](#5-monitoring)
6. [Maintenance](#6-maintenance)
7. [Troubleshooting](#7-troubleshooting)
8. [Mise à jour](#8-mise-à-jour)
9. [Rollback](#9-rollback)
10. [Sécurité](#10-sécurité)

---

## 1. Prérequis Système

### 1.1 Configuration minimale

| Composant | Minimum | Recommandé |
|-----------|---------|------------|
| OS | Ubuntu 20.04 LTS | Ubuntu 22.04 LTS |
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Disque | 20 GB | 50+ GB SSD |
| Réseau | 100 Mbps | 1 Gbps |

### 1.2 Logiciels requis

**Versions minimales:**
```bash
Python:     3.9+
OCaml:      4.14+
Docker:     20.10+
Docker Compose: 2.0+
Git:        2.30+
Make:       4.3+
```

**Vérification des versions:**
```bash
python3 --version
ocaml --version
docker --version
docker-compose --version
git --version
make --version
```

### 1.3 Ports réseau

**Ports à ouvrir:**

| Port | Protocole | Usage | Accès |
|------|-----------|-------|-------|
| 22 | TCP | SSH | Admin uniquement |
| 80 | TCP | HTTP (redirection HTTPS) | Public |
| 443 | TCP | HTTPS | Public |
| 8080 | TCP | Application (interne) | Localhost |
| 5432 | TCP | PostgreSQL (optionnel) | Localhost |

**Configuration firewall (UFW):**
```bash
# Activer le firewall
sudo ufw enable

# Autoriser SSH
sudo ufw allow 22/tcp

# Autoriser HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Vérifier le statut
sudo ufw status
```

---

## 2. Installation Étape par Étape

### 2.1 Préparation du serveur

#### Mise à jour du système
```bash
# Mise à jour des paquets
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y

# Installation des outils de base
sudo apt-get install -y \
    curl \
    wget \
    git \
    vim \
    htop \
    ca-certificates \
    gnupg \
    lsb-release
```

#### Création d'un utilisateur dédié
```bash
# Créer l'utilisateur awkward
sudo adduser --disabled-password --gecos "" awkward

# Ajouter aux groupes nécessaires
sudo usermod -aG docker awkward
sudo usermod -aG sudo awkward

# Basculer vers l'utilisateur
sudo su - awkward
```

### 2.2 Installation de Python

```bash
# Vérifier la version de Python
python3 --version

# Si version < 3.9, installer via deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update
sudo apt-get install -y \
    python3.9 \
    python3.9-venv \
    python3.9-dev \
    python3-pip

# Créer un lien symbolique
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Mettre à jour pip
python3 -m pip install --upgrade pip setuptools wheel
```

### 2.3 Installation d'OCaml

```bash
# Installer OCaml et OPAM
sudo apt-get install -y \
    ocaml \
    ocaml-native-compilers \
    opam \
    libgmp-dev \
    libssl-dev \
    pkg-config

# Initialiser OPAM
opam init --disable-sandboxing -y
eval $(opam env)

# Installer les dépendances OCaml
opam install -y \
    dune \
    camlp5 \
    calendars \
    unidecode
```

### 2.4 Installation de Docker

```bash
# Ajouter la clé GPG de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Ajouter le repository Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Installer Docker
sudo apt-get update
sudo apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-compose-plugin

# Vérifier l'installation
docker --version
docker compose version

# Démarrer Docker
sudo systemctl enable docker
sudo systemctl start docker

# Tester Docker
docker run hello-world
```

### 2.5 Clonage du repository

```bash
# Se placer dans le répertoire home
cd ~

# Cloner le repository
git clone https://github.com/yourusername/awkward-legacy.git
cd awkward-legacy

# Vérifier la branche
git branch
git status
```

### 2.6 Installation des dépendances Python

```bash
# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
cd LegacyProject
pip install -r requirements.txt

# Vérifier l'installation
pip list
```

### 2.7 Compilation du code OCaml

```bash
# Se placer dans le répertoire geneweb
cd ~/awkward-legacy/geneweb

# Configurer l'environnement OPAM
eval $(opam env)

# Compiler avec Dune
dune build

# Vérifier la compilation
ls _build/default/

# Retour au répertoire principal
cd ~/awkward-legacy
```

### 2.8 Compilation du wrapper Python

```bash
# Se placer dans LegacyProject
cd ~/awkward-legacy/LegacyProject

# Activer l'environnement virtuel
source ../venv/bin/activate

# Compiler
make clean
make all

# Vérifier la compilation
ls modernProject/lib/*.so 2>/dev/null || echo "Wrapper compilé"

# Tester l'import
python3 -c "from modernProject.lib import database; print('Import OK')"
```

---

## 3. Configuration

### 3.1 Variables d'environnement

#### Créer le fichier .env
```bash
cd ~/awkward-legacy
cp .env.example .env
vim .env
```

#### Contenu du fichier .env
```bash
# ============================================
# AWKWARD LEGACY - Configuration Environment
# ============================================

# --- Application ---
APP_NAME=AWKWARD_LEGACY
APP_ENV=production  # development, staging, production
APP_DEBUG=false

# --- Base de données ---
DATABASE_PATH=/var/lib/awkward-legacy/db
DATABASE_BACKUP_PATH=/var/lib/awkward-legacy/backups

# --- Serveur ---
HOST=0.0.0.0
PORT=8080
WORKERS=4
TIMEOUT=60

# --- Sécurité ---
# Générer avec: openssl rand -hex 32
SECRET_KEY=CHANGEME_GENERATE_RANDOM_KEY_HERE
JWT_SECRET_KEY=CHANGEME_ANOTHER_RANDOM_KEY
JWT_EXPIRATION=86400  # 24 heures en secondes
BCRYPT_ROUNDS=12

# --- Encryption ---
# Générer avec: python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
ENCRYPTION_KEY=CHANGEME_FERNET_KEY

# --- Logging ---
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=/var/log/awkward-legacy/app.log
LOG_MAX_BYTES=10485760  # 10 MB
LOG_BACKUP_COUNT=5

# --- RGPD ---
DATA_RETENTION_DAYS=1095  # 3 ans
ANONYMIZE_AFTER_DAYS=1825  # 5 ans

# --- Performance ---
CACHE_ENABLED=true
CACHE_TTL=3600  # 1 heure
MAX_CONNECTIONS=100
REQUEST_TIMEOUT=30

# --- Email ---
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USERNAME=noreply@awkward-legacy.com
SMTP_PASSWORD=CHANGEME_SMTP_PASSWORD
EMAIL_FROM=noreply@awkward-legacy.com

# --- External Services ---
# Sentry (monitoring)
SENTRY_DSN=

# AWS S3 (backups)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_BUCKET=awkward-legacy-backups
AWS_REGION=eu-west-1

# --- Monitoring ---
PROMETHEUS_ENABLED=true
PROMETHEUS_PORT=9090

# --- Domaine ---
DOMAIN=awkward-legacy.com
ALLOWED_HOSTS=localhost,awkward-legacy.com,www.awkward-legacy.com
```

#### Sécuriser le fichier .env
```bash
# Permissions strictes
chmod 600 .env

# Vérifier
ls -la .env
```

#### Générer les clés secrètes
```bash
# SECRET_KEY
openssl rand -hex 32

# JWT_SECRET_KEY
openssl rand -hex 32

# ENCRYPTION_KEY (Fernet)
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 3.2 Configuration de la base de données

#### Créer les répertoires
```bash
sudo mkdir -p /var/lib/awkward-legacy/db
sudo mkdir -p /var/lib/awkward-legacy/backups
sudo chown -R awkward:awkward /var/lib/awkward-legacy
sudo chmod 755 /var/lib/awkward-legacy
```

#### Initialiser la base de données
```bash
cd ~/awkward-legacy/LegacyProject
source ../venv/bin/activate

# Script d'initialisation
python3 << EOF
from modernProject.lib import database
import os

db_path = os.getenv('DATABASE_PATH', '/var/lib/awkward-legacy/db')
os.makedirs(db_path, exist_ok=True)

print(f"Database initialized at: {db_path}")
EOF
```

### 3.3 Configuration des logs

#### Créer les répertoires de logs
```bash
sudo mkdir -p /var/log/awkward-legacy
sudo chown -R awkward:awkward /var/log/awkward-legacy
sudo chmod 755 /var/log/awkward-legacy
```

#### Configuration de logrotate
```bash
sudo vim /etc/logrotate.d/awkward-legacy
```

Contenu:
```
/var/log/awkward-legacy/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 awkward awkward
    sharedscripts
    postrotate
        systemctl reload awkward-legacy >/dev/null 2>&1 || true
    endscript
}
```

### 3.4 Configuration SSL/TLS

#### Obtenir un certificat SSL (Let's Encrypt)
```bash
# Installer certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Obtenir le certificat
sudo certbot certonly --standalone -d awkward-legacy.com -d www.awkward-legacy.com

# Vérifier le certificat
sudo ls -la /etc/letsencrypt/live/awkward-legacy.com/
```

#### Renouvellement automatique
```bash
# Le renouvellement automatique est déjà configuré
# Vérifier avec:
sudo systemctl status certbot.timer

# Tester le renouvellement
sudo certbot renew --dry-run
```

---

## 4. Déploiement

### 4.1 Déploiement avec Docker

#### Construction des images
```bash
cd ~/awkward-legacy

# Construire l'image Docker
docker build -t awkward-legacy:latest .

# Vérifier l'image
docker images | grep awkward-legacy
```

#### Lancement avec Docker Compose
```bash
# Créer le fichier docker-compose.yml s'il n'existe pas
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  web:
    build: .
    image: awkward-legacy:latest
    container_name: awkward-legacy-web
    ports:
      - "8080:8080"
    volumes:
      - /var/lib/awkward-legacy:/data
      - /var/log/awkward-legacy:/var/log/awkward
    env_file:
      - .env
    environment:
      - DATABASE_PATH=/data/db
      - LOG_FILE=/var/log/awkward/app.log
      - PYTHONPATH=/app/LegacyProject/modernProject
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - awkward-net

  nginx:
    image: nginx:alpine
    container_name: awkward-legacy-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - web
    restart: unless-stopped
    networks:
      - awkward-net

networks:
  awkward-net:
    driver: bridge

volumes:
  data:
  logs:
EOF

# Lancer les conteneurs
docker-compose up -d

# Vérifier le statut
docker-compose ps

# Voir les logs
docker-compose logs -f
```

### 4.2 Configuration Nginx

#### Créer le fichier nginx.conf
```bash
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream awkward_backend {
        server web:8080;
    }

    # Redirection HTTP vers HTTPS
    server {
        listen 80;
        server_name awkward-legacy.com www.awkward-legacy.com;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://$server_name$request_uri;
        }
    }

    # Configuration HTTPS
    server {
        listen 443 ssl http2;
        server_name awkward-legacy.com www.awkward-legacy.com;

        # Certificats SSL
        ssl_certificate /etc/letsencrypt/live/awkward-legacy.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/awkward-legacy.com/privkey.pem;

        # Protocoles et ciphers
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers on;
        ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';

        # Session SSL
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        # OCSP Stapling
        ssl_stapling on;
        ssl_stapling_verify on;
        ssl_trusted_certificate /etc/letsencrypt/live/awkward-legacy.com/chain.pem;
        resolver 8.8.8.8 8.8.4.4 valid=300s;
        resolver_timeout 5s;

        # Headers de sécurité
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;

        # Taille max des uploads
        client_max_body_size 100M;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Logs
        access_log /var/log/nginx/awkward-access.log;
        error_log /var/log/nginx/awkward-error.log;

        # Proxy vers l'application
        location / {
            proxy_pass http://awkward_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
        }

        # Static files (si nécessaire)
        location /static/ {
            alias /app/static/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }

        # Health check (pas de log)
        location /health {
            access_log off;
            proxy_pass http://awkward_backend;
        }
    }
}
EOF
```

### 4.3 Service systemd (alternative à Docker)

#### Créer le service systemd
```bash
sudo vim /etc/systemd/system/awkward-legacy.service
```

Contenu:
```ini
[Unit]
Description=AWKWARD LEGACY Application
After=network.target

[Service]
Type=simple
User=awkward
Group=awkward
WorkingDirectory=/home/awkward/awkward-legacy/LegacyProject
Environment="PATH=/home/awkward/awkward-legacy/venv/bin"
Environment="PYTHONPATH=/home/awkward/awkward-legacy/LegacyProject/modernProject"
EnvironmentFile=/home/awkward/awkward-legacy/.env
ExecStart=/home/awkward/awkward-legacy/venv/bin/python3 modernProject/main.py
Restart=on-failure
RestartSec=5s
StandardOutput=journal
StandardError=journal
SyslogIdentifier=awkward-legacy

[Install]
WantedBy=multi-user.target
```

#### Activer et démarrer le service
```bash
# Recharger systemd
sudo systemctl daemon-reload

# Activer le service au démarrage
sudo systemctl enable awkward-legacy

# Démarrer le service
sudo systemctl start awkward-legacy

# Vérifier le statut
sudo systemctl status awkward-legacy

# Voir les logs
sudo journalctl -u awkward-legacy -f
```

### 4.4 Scripts de déploiement

#### Script deploy.sh
```bash
cat > scripts/deploy.sh << 'EOF'
#!/bin/bash
# Script de déploiement AWKWARD LEGACY

set -e

echo " Déploiement AWKWARD LEGACY..."

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonctions
function error() {
    echo -e "${RED} $1${NC}"
    exit 1
}

function success() {
    echo -e "${GREEN} $1${NC}"
}

function warning() {
    echo -e "${YELLOW}  $1${NC}"
}

# Vérifier les prérequis
echo " Vérification des prérequis..."
command -v docker >/dev/null 2>&1 || error "Docker requis mais non installé"
command -v docker-compose >/dev/null 2>&1 || error "Docker Compose requis mais non installé"
success "Prérequis OK"

# Vérifier le fichier .env
if [ ! -f .env ]; then
    error "Fichier .env manquant. Copiez .env.example et configurez-le."
fi
success "Fichier .env présent"

# Backup de la version actuelle
echo " Sauvegarde de la version actuelle..."
if [ -d "/var/lib/awkward-legacy/db" ]; then
    ./scripts/backup.sh
    success "Backup effectué"
else
    warning "Pas de données à sauvegarder (première installation)"
fi

# Arrêter les conteneurs existants
echo " Arrêt des conteneurs existants..."
docker-compose down || warning "Aucun conteneur à arrêter"

# Pull du code
echo " Pull des dernières modifications..."
git pull origin main || error "Échec du pull Git"
success "Code à jour"

# Construire les images
echo " Construction des images Docker..."
docker-compose build --no-cache || error "Échec de la construction"
success "Images construites"

# Démarrer les services
echo "  Démarrage des services..."
docker-compose up -d || error "Échec du démarrage"
success "Services démarrés"

# Attendre que les services soient prêts
echo " Attente du démarrage des services..."
sleep 10

# Health check
echo " Vérification de santé..."
for i in {1..30}; do
    if curl -f http://localhost:8080/health >/dev/null 2>&1; then
        success "Application opérationnelle"
        break
    fi
    if [ $i -eq 30 ]; then
        error "Timeout: application non disponible"
    fi
    echo "   Tentative $i/30..."
    sleep 2
done

# Afficher le statut
echo " Statut des conteneurs:"
docker-compose ps

# Afficher les logs récents
echo " Logs récents:"
docker-compose logs --tail=50

echo ""
success " Déploiement terminé!"
echo " Application disponible sur:"
echo "   - http://localhost:8080"
echo "   - https://awkward-legacy.com"
echo ""
echo "Commandes utiles:"
echo "  - Logs: docker-compose logs -f"
echo "  - Statut: docker-compose ps"
echo "  - Arrêt: docker-compose down"
echo "  - Restart: docker-compose restart"
EOF

chmod +x scripts/deploy.sh
```

#### Script backup.sh
```bash
cat > scripts/backup.sh << 'EOF'
#!/bin/bash
# Script de backup AWKWARD LEGACY

set -e

BACKUP_DIR="/var/lib/awkward-legacy/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="backup_${DATE}"

echo " Backup AWKWARD LEGACY - ${DATE}"

# Créer le répertoire de backup
mkdir -p "${BACKUP_DIR}"

# Backup de la base de données
echo " Backup de la base de données..."
if [ -d "/var/lib/awkward-legacy/db" ]; then
    tar -czf "${BACKUP_DIR}/${BACKUP_NAME}_db.tar.gz" \
        -C /var/lib/awkward-legacy db/
    echo " Base de données sauvegardée"
else
    echo "  Aucune base de données à sauvegarder"
fi

# Backup de la configuration
echo "  Backup de la configuration..."
if [ -f ".env" ]; then
    cp .env "${BACKUP_DIR}/${BACKUP_NAME}.env"
    echo " Configuration sauvegardée"
fi

# Chiffrer le backup (optionnel)
if command -v openssl >/dev/null 2>&1; then
    echo " Chiffrement du backup..."
    tar -czf - "${BACKUP_DIR}/${BACKUP_NAME}"* | \
        openssl enc -aes-256-cbc -salt -pbkdf2 \
        -out "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz.enc" \
        -pass pass:"${BACKUP_ENCRYPTION_KEY:-defaultkey}"

    # Supprimer les fichiers non chiffrés
    rm -f "${BACKUP_DIR}/${BACKUP_NAME}_db.tar.gz"
    rm -f "${BACKUP_DIR}/${BACKUP_NAME}.env"

    echo " Backup chiffré"
fi

# Supprimer les backups de plus de 90 jours
echo " Nettoyage des anciens backups..."
find "${BACKUP_DIR}" -name "backup_*.tar.gz*" -mtime +90 -delete
echo " Nettoyage effectué"

# Upload vers S3 (si configuré)
if [ -n "${AWS_S3_BUCKET}" ]; then
    echo "  Upload vers S3..."
    aws s3 cp "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz.enc" \
        "s3://${AWS_S3_BUCKET}/backups/" \
        --server-side-encryption AES256 || echo "  Upload S3 échoué"
fi

echo " Backup terminé: ${BACKUP_NAME}"
EOF

chmod +x scripts/backup.sh
```

#### Script restore.sh
```bash
cat > scripts/restore.sh << 'EOF'
#!/bin/bash
# Script de restauration AWKWARD LEGACY

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <backup_file>"
    echo "Exemples:"
    echo "  $0 backup_20251017_120000.tar.gz.enc"
    echo "  $0 latest"
    exit 1
fi

BACKUP_DIR="/var/lib/awkward-legacy/backups"
BACKUP_FILE="$1"

# Si "latest", prendre le plus récent
if [ "$BACKUP_FILE" == "latest" ]; then
    BACKUP_FILE=$(ls -t "${BACKUP_DIR}"/backup_*.tar.gz.enc | head -1)
    echo " Utilisation du backup le plus récent: $(basename ${BACKUP_FILE})"
fi

# Vérifier que le fichier existe
if [ ! -f "${BACKUP_DIR}/${BACKUP_FILE}" ]; then
    echo " Backup non trouvé: ${BACKUP_FILE}"
    exit 1
fi

echo "  ATTENTION: Cette opération va écraser les données actuelles!"
read -p "Continuer? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Restauration annulée"
    exit 0
fi

# Arrêter l'application
echo " Arrêt de l'application..."
docker-compose down || systemctl stop awkward-legacy || true

# Déchiffrer le backup
echo " Déchiffrement du backup..."
openssl enc -aes-256-cbc -d -pbkdf2 \
    -in "${BACKUP_DIR}/${BACKUP_FILE}" \
    -pass pass:"${BACKUP_ENCRYPTION_KEY:-defaultkey}" | \
    tar -xzf - -C /tmp/

# Restaurer la base de données
echo " Restauration de la base de données..."
rm -rf /var/lib/awkward-legacy/db
tar -xzf /tmp/backup_*_db.tar.gz -C /var/lib/awkward-legacy/

# Restaurer la configuration
if [ -f "/tmp/backup_*.env" ]; then
    echo "  Restauration de la configuration..."
    cp /tmp/backup_*.env .env.restored
    echo "  Configuration restaurée dans .env.restored (à vérifier)"
fi

# Nettoyer
rm -rf /tmp/backup_*

# Redémarrer l'application
echo "  Redémarrage de l'application..."
docker-compose up -d || systemctl start awkward-legacy

echo " Restauration terminée!"
EOF

chmod +x scripts/restore.sh
```

---

## 5. Monitoring

### 5.1 Health checks

#### Endpoint /health
```python
# Implémentation dans l'application
@app.route('/health')
def health_check():
    """Health check endpoint"""
    checks = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime': get_uptime_seconds(),
        'version': '1.0.0'
    }

    # Vérifier la base de données
    try:
        database_check()
        checks['database'] = 'ok'
    except Exception as e:
        checks['database'] = f'error: {str(e)}'
        checks['status'] = 'unhealthy'

    # Vérifier l'espace disque
    disk_usage = psutil.disk_usage('/')
    if disk_usage.percent > 90:
        checks['disk'] = 'warning: low space'
    else:
        checks['disk'] = 'ok'

    # Vérifier la mémoire
    mem = psutil.virtual_memory()
    if mem.percent > 90:
        checks['memory'] = 'warning: high usage'
    else:
        checks['memory'] = 'ok'

    status_code = 200 if checks['status'] == 'healthy' else 503
    return jsonify(checks), status_code
```

#### Test du health check
```bash
# Test manuel
curl -f http://localhost:8080/health

# Test automatique
watch -n 30 'curl -s http://localhost:8080/health | jq .'
```

### 5.2 Métriques et Prometheus

#### Endpoint /metrics
```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest

# Métriques
requests_total = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
requests_duration = Histogram('request_duration_seconds', 'Request duration')
active_users = Gauge('active_users', 'Number of active users')

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': 'text/plain'}
```

#### Configuration Prometheus
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'awkward-legacy'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: '/metrics'
```

### 5.3 Logs

#### Consultation des logs
```bash
# Logs Docker
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f web

# Logs systemd
sudo journalctl -u awkward-legacy -f

# Logs applicatifs
tail -f /var/log/awkward-legacy/app.log

# Logs nginx
tail -f /var/log/nginx/awkward-access.log
tail -f /var/log/nginx/awkward-error.log
```

#### Analyse des logs
```bash
# Rechercher les erreurs
grep ERROR /var/log/awkward-legacy/app.log

# Compter les erreurs par type
awk '/ERROR/ {print $5}' /var/log/awkward-legacy/app.log | sort | uniq -c

# Top 10 des IPs
awk '{print $1}' /var/log/nginx/awkward-access.log | sort | uniq -c | sort -rn | head -10
```

---

## 6. Maintenance

### 6.1 Mises à jour système

```bash
# Mises à jour de sécurité
sudo apt-get update
sudo apt-get upgrade -y

# Vérifier si redémarrage nécessaire
if [ -f /var/run/reboot-required ]; then
    echo "  Redémarrage nécessaire"
    cat /var/run/reboot-required.pkgs
fi

# Redémarrage programmé
sudo shutdown -r +5 "Redémarrage pour mises à jour de sécurité dans 5 minutes"
```

### 6.2 Rotation des logs

```bash
# Forcer la rotation
sudo logrotate -f /etc/logrotate.d/awkward-legacy

# Vérifier l'état
sudo logrotate -d /etc/logrotate.d/awkward-legacy
```

### 6.3 Backups automatiques

#### Cron job pour backups quotidiens
```bash
# Éditer le crontab
crontab -e

# Ajouter la ligne suivante pour backup quotidien à 2h du matin
0 2 * * * /home/awkward/awkward-legacy/scripts/backup.sh >> /var/log/awkward-legacy/backup.log 2>&1
```

### 6.4 Nettoyage

#### Nettoyage des images Docker
```bash
# Supprimer les images non utilisées
docker image prune -a

# Supprimer les volumes non utilisés
docker volume prune

# Supprimer tous les éléments non utilisés
docker system prune -a --volumes
```

#### Nettoyage des logs anciens
```bash
# Supprimer les logs de plus de 30 jours
find /var/log/awkward-legacy -name "*.log.*" -mtime +30 -delete
```

---

## 7. Troubleshooting

### 7.1 Problèmes courants

#### 1. Application ne démarre pas

**Symptômes:**
```bash
docker-compose ps
# web | Exit 1
```

**Diagnostic:**
```bash
# Voir les logs d'erreur
docker-compose logs web

# Vérifier la configuration
docker-compose config

# Tester la configuration Python
docker-compose run --rm web python3 -c "import sys; print(sys.version)"
```

**Solutions:**
- Vérifier le fichier .env
- Vérifier les permissions sur /var/lib/awkward-legacy
- Vérifier les dépendances Python
- Vérifier la compilation OCaml

#### 2. Base de données verrouillée

**Symptômes:**
```
sqlite3.OperationalError: database is locked
```

**Solutions:**
```bash
# Identifier les processus utilisant la base
lsof /var/lib/awkward-legacy/db/*.gwb

# Supprimer les fichiers de lock
rm /var/lib/awkward-legacy/db/*.lock

# Redémarrer l'application
docker-compose restart web
```

#### 3. Erreur de permission

**Symptômes:**
```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**
```bash
# Vérifier les permissions
ls -la /var/lib/awkward-legacy

# Corriger les permissions
sudo chown -R awkward:awkward /var/lib/awkward-legacy
sudo chmod -R 755 /var/lib/awkward-legacy

# Permissions spécifiques pour les logs
sudo chown -R awkward:awkward /var/log/awkward-legacy
sudo chmod -R 755 /var/log/awkward-legacy
```

#### 4. Out of memory

**Symptômes:**
```
MemoryError
docker: Error response from daemon: OCI runtime create failed
```

**Solutions:**
```bash
# Vérifier l'utilisation mémoire
free -h
docker stats

# Augmenter la swap (temporaire)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Limiter la mémoire Docker
# Dans docker-compose.yml:
services:
  web:
    mem_limit: 2g
    memswap_limit: 2g
```

#### 5. Port déjà utilisé

**Symptômes:**
```
Error: bind: address already in use
```

**Solutions:**
```bash
# Identifier le processus utilisant le port
sudo lsof -i :8080
sudo netstat -tulpn | grep 8080

# Tuer le processus
sudo kill -9 <PID>

# Ou changer le port dans .env
PORT=8081
```

### 7.2 Logs de débogage

#### Activer le mode debug
```bash
# Dans .env
APP_DEBUG=true
LOG_LEVEL=DEBUG

# Redémarrer
docker-compose restart web
```

#### Activer les logs SQL
```python
# Dans le code Python
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

### 7.3 Outils de diagnostic

```bash
# Vérifier l'état de tous les services
./scripts/check-health.sh

# Contenu du script check-health.sh:
cat > scripts/check-health.sh << 'EOF'
#!/bin/bash
echo "=== AWKWARD LEGACY - Health Check ==="

# Application
echo -n "Application: "
curl -sf http://localhost:8080/health >/dev/null && echo " OK" || echo " DOWN"

# Docker
echo -n "Docker: "
docker ps | grep awkward-legacy-web >/dev/null && echo " OK" || echo " DOWN"

# Nginx
echo -n "Nginx: "
docker ps | grep awkward-legacy-nginx >/dev/null && echo " OK" || echo " DOWN"

# Base de données
echo -n "Database: "
[ -f /var/lib/awkward-legacy/db ] && echo " OK" || echo "  Missing"

# Disque
echo "Disk usage:"
df -h /var/lib/awkward-legacy

# Mémoire
echo "Memory:"
free -h

# Load
echo "Load average:"
uptime
EOF

chmod +x scripts/check-health.sh
```

---

## 8. Mise à jour

### 8.1 Mise à jour mineure

```bash
# Sauvegarder
./scripts/backup.sh

# Pull des modifications
git pull origin main

# Rebuild et redémarrage
docker-compose build
docker-compose up -d

# Vérifier
docker-compose ps
curl http://localhost:8080/health
```

### 8.2 Mise à jour majeure

```bash
# 1. Notification aux utilisateurs
echo "Maintenance programmée dans 1 heure"

# 2. Backup complet
./scripts/backup.sh

# 3. Arrêt de l'application
docker-compose down

# 4. Mise à jour du code
git checkout v2.0.0  # Tag de la nouvelle version

# 5. Migration de la base de données (si nécessaire)
./scripts/migrate-db.sh

# 6. Rebuild complet
docker-compose build --no-cache

# 7. Démarrage
docker-compose up -d

# 8. Tests smoke
./scripts/smoke-tests.sh

# 9. Monitoring intensif pendant 1h
watch -n 10 './scripts/check-health.sh'
```

---

## 9. Rollback

### 9.1 Rollback rapide

```bash
#!/bin/bash
# rollback.sh

echo " Rollback vers version précédente..."

# Arrêter la version actuelle
docker-compose down

# Revenir au commit précédent
git reset --hard HEAD~1

# Ou revenir à un tag spécifique
# git checkout v1.0.0

# Rebuild
docker-compose build

# Restaurer la base de données
./scripts/restore.sh latest

# Démarrer
docker-compose up -d

# Vérifier
./scripts/check-health.sh

echo " Rollback terminé"
```

### 9.2 Rollback avec restauration complète

```bash
# 1. Arrêter l'application
docker-compose down

# 2. Restaurer le code
git checkout <commit-previous-working>

# 3. Restaurer la base de données
./scripts/restore.sh backup_20251017_120000.tar.gz.enc

# 4. Restaurer la configuration
cp /var/lib/awkward-legacy/backups/backup_20251017_120000.env .env

# 5. Rebuild et redémarrage
docker-compose build
docker-compose up -d

# 6. Vérification approfondie
./scripts/smoke-tests.sh
```

---

## 10. Sécurité

### 10.1 Checklist de sécurité

```markdown
## Post-Deployment Security Checklist

- [ ] Firewall configuré (UFW/iptables)
- [ ] SSH avec clés uniquement (pas de mot de passe)
- [ ] Utilisateur root désactivé
- [ ] Certificat SSL valide et auto-renouvelé
- [ ] Headers de sécurité configurés (HSTS, CSP, etc.)
- [ ] Mots de passe forts générés (SECRET_KEY, etc.)
- [ ] Permissions fichiers correctes (600 pour .env)
- [ ] Backups chiffrés
- [ ] Logs de sécurité activés
- [ ] Rate limiting configuré
- [ ] Fail2ban installé
- [ ] Mises à jour automatiques activées
```

### 10.2 Fail2ban pour SSH

```bash
# Installer fail2ban
sudo apt-get install -y fail2ban

# Configurer pour SSH
sudo vim /etc/fail2ban/jail.local
```

Contenu:
```ini
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
```

```bash
# Démarrer fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Vérifier le statut
sudo fail2ban-client status sshd
```

### 10.3 Scans de sécurité

```bash
# Scan de vulnérabilités Docker
docker scan awkward-legacy:latest

# Scan des dépendances Python
pip install safety
safety check -r requirements.txt

# Audit npm (si applicable)
npm audit

# Scan du serveur
sudo apt-get install -y lynis
sudo lynis audit system
```

---

## 11. Annexes

### 11.1 Commandes utiles

```bash
# Docker Compose
docker-compose ps                    # Statut des conteneurs
docker-compose logs -f              # Logs en temps réel
docker-compose restart web          # Redémarrer un service
docker-compose exec web bash        # Shell dans le conteneur
docker-compose down -v              # Tout arrêter et supprimer volumes

# Docker
docker ps                           # Conteneurs en cours
docker images                       # Images disponibles
docker system df                    # Utilisation disque
docker system prune -a              # Nettoyage complet

# Systemd
sudo systemctl status awkward-legacy    # Statut du service
sudo systemctl restart awkward-legacy   # Redémarrer
sudo journalctl -u awkward-legacy -f   # Logs en temps réel

# Monitoring
htop                               # CPU/Mémoire
iotop                              # I/O disque
nethogs                            # Bande passante
```

### 11.2 Contacts

**Support technique:**
- Email: support@awkward-legacy.com
- Téléphone: [À définir]

**Urgences (24/7):**
- Email: oncall@awkward-legacy.com
- PagerDuty: [À définir]

---

**Dernière mise à jour:** 17 Octobre 2025
**Version du document:** 1.0
**Auteur:** [Équipe DevOps]