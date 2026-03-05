# Technologies et Services d'Hebergement - AWKWARD LEGACY

**Version:** 1.0
**Date:** Mars 2026
**Projet:** AWKWARD LEGACY - Modernisation de GeneWeb
**Referentiel RNCP:** Bloc 6 - C30.1, C30.2

---

## Table des Matieres

1. [Solution d'hebergement retenue](#1-solution-dhebergement-retenue)
2. [Architecture de deploiement](#2-architecture-de-deploiement)
3. [Justification des choix techniques](#3-justification-des-choix-techniques)
4. [Contraintes prises en compte](#4-contraintes-prises-en-compte)
5. [Dimensionnement et disponibilite](#5-dimensionnement-et-disponibilite)

---

## 1. Solution d'hebergement retenue

### 1.1 Architecture globale

AWKWARD LEGACY est deploye selon une architecture conteneurisee :

```
Internet
    |
[Nginx] -- HTTPS (TLS 1.3) --> [Flask App] --> [Fichiers GeneWeb .gwb]
    |                               |
[Let's Encrypt SSL]        [Docker Container]
                                    |
                           [Health Check /health]
```

### 1.2 Composants de l'infrastructure

| Composant | Technologie | Role |
|-----------|------------|------|
| **Serveur web** | Nginx (Alpine) | Reverse proxy, SSL termination, headers securite |
| **Application** | Python 3.12 + Flask | API REST + serveur genealogique |
| **Conteneurisation** | Docker + Docker Compose | Isolation, portabilite, reproductibilite |
| **SSL/TLS** | Let's Encrypt + Certbot | Chiffrement HTTPS gratuit et auto-renouvelable |
| **Monitoring** | Prometheus + Grafana | Metriques temps reel, alertes |
| **CI/CD** | GitHub Actions | Deploiement automatise 8 jobs |
| **Registre images** | GitHub Container Registry (ghcr.io) | Stockage et versionnage des images Docker |

**Fichiers de reference :**
- `LegacyProject/modernProject/Dockerfile` : image multi-stage
- `LegacyProject/modernProject/.github/workflows/ci.yml` : pipeline CI/CD complet
- `LegacyProject/docs/DEPLOYMENT_GUIDE.md` : guide de deploiement detaille

---

## 2. Architecture de deploiement

### 2.1 Dockerfile multi-stage

Le Dockerfile est structure en 2 stages :

**Stage 1 - Builder** (`python:3.12-slim`) :
- Installation des dependances systeme (gcc, libpq-dev)
- Creation d'un environnement virtuel Python isole
- Installation des dependances Python depuis `requirements.txt`

**Stage 2 - Runtime** (`python:3.12-slim`) :
- Image finale legere (pas des outils de build)
- Utilisateur non-root `awkward` (UID 1000) pour la securite
- Health check integre : `curl -f http://localhost:5000/health`
- Exposition du port 5000

```
Taille image builder : ~800 MB
Taille image runtime : ~180 MB (separation des stages = image allégée)
```

**Fichier :** `LegacyProject/modernProject/Dockerfile`

### 2.2 Pipeline CI/CD (8 jobs)

Le pipeline GitHub Actions orchestre le deploiement en 8 etapes sequentielles :

```
Push/PR
  |
  +---> [1. Lint] (Black, Flake8, Bandit)
  |          |
  +---> [2. Unit Tests] (Python 3.10 / 3.11 / 3.12 en parallele)
  |          |
  +---> [3. Integration Tests] (avec Redis + PostgreSQL)
  |          |
  +---> [4. Security Scan] (Safety, pip-audit)
  |          |
  +---> [5. Build Docker] (multi-arch: amd64 + arm64)
  |          |
  +---> [6. Deploy Staging] (auto sur branche develop)
  |          |
  +---> [7. Deploy Production] (auto sur branche main)
  |          |
  +---> [8. Release Notes] (git-cliff + GitHub Release)
```

**Fichier :** `LegacyProject/modernProject/.github/workflows/ci.yml`

### 2.3 Docker Compose (production)

```yaml
services:
  web:
    image: awkward-legacy:latest
    ports: ["8080:8080"]
    volumes:
      - /var/lib/awkward-legacy:/data
      - /var/log/awkward-legacy:/var/log/awkward
    healthcheck:
      test: curl -f http://localhost:8080/health
      interval: 30s
      retries: 3

  nginx:
    image: nginx:alpine
    ports: ["80:80", "443:443"]
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
```

---

## 3. Justification des choix techniques

### 3.1 Pourquoi Docker ?

| Argument | Detail |
|----------|--------|
| **Portabilite** | Meme comportement en dev, staging et production. Elimine "ca marche sur ma machine" |
| **Isolation** | L'application ne peut pas affecter le systeme hote |
| **Reproductibilite** | Chaque build produit exactement la meme image (hash SHA256) |
| **Versionnage** | Chaque image taguee (SHA, branche, semver). Rollback en 30 secondes |
| **Multi-arch** | Build `linux/amd64` et `linux/arm64` pour compatibilite maximale |

### 3.2 Pourquoi Nginx comme reverse proxy ?

| Argument | Detail |
|----------|--------|
| **Performance** | Sert les fichiers statiques directement (cache 30 jours) sans passer par Flask |
| **SSL termination** | Gere TLS 1.2/1.3, sessions SSL, OCSP stapling au niveau Nginx |
| **Headers securite** | HSTS, X-Frame-Options, CSP, X-Content-Type-Options configures centrallement |
| **Load balancing** | Peut distribuer entre plusieurs instances Flask si besoin de scalabilite |

### 3.3 Pourquoi GitHub Actions ?

| Argument | Detail |
|----------|--------|
| **Integre a GitHub** | Pas d'outil externe, meme plateforme que le code |
| **Gratuit** | Inclus dans GitHub (2000 min/mois) |
| **Matrix builds** | Teste Python 3.10, 3.11, 3.12 en parallele sans configuration supplementaire |
| **Secrets management** | Variables sensibles (SSH keys, tokens) stockees de facon securisee |
| **Artifacts** | Rapports de tests, coverage, Bandit conserves 90 jours |

### 3.4 Pourquoi Let's Encrypt ?

| Argument | Detail |
|----------|--------|
| **Gratuit** | Certificats SSL sans cout |
| **Automatique** | Renouvellement automatique (certbot.timer systemd) |
| **Reconnu** | Autorite de certification reconnue par tous les navigateurs |
| **HTTPS obligatoire** | Exige par les navigateurs modernes pour les APIs et les formulaires |

---

## 4. Contraintes prises en compte

### 4.1 Budget

- **Docker** : gratuit et open-source
- **GitHub Actions** : inclus dans le plan GitHub gratuit
- **Let's Encrypt** : certificats SSL gratuits
- **Nginx** : gratuit et open-source
- **Prometheus / Grafana** : versions community gratuites
- **Cout total hebergement** : uniquement le cout du serveur VPS (estimé 5-20 EUR/mois selon provider)

### 4.2 Securite

- Utilisateur non-root dans le conteneur (UID 1000)
- Headers de securite Nginx (HSTS, CSP, X-Frame-Options)
- TLS 1.2/1.3 uniquement (protocoles obsoletes desactives)
- Scan de vulnerabilites Docker avec Trivy a chaque build
- Secrets via GitHub Secrets (jamais en clair dans le code)
- Fichier .env jamais commite (detecte par pre-commit hook + detect-secrets)

### 4.3 Scalabilite

- Architecture horizontale : plusieurs instances Flask derriere Nginx
- Images multi-arch (amd64 + arm64) pour flexibilite du choix serveur
- Variables d'environnement pour tout adapter (PORT, WORKERS, etc.)
- Health check integre pour orchestration (Docker Swarm / Kubernetes compatible)

### 4.4 Qualite de service

- Health check toutes les 30s avec retry automatique (3 tentatives)
- Rollback automatise en cas d'echec du health check post-deploiement
- Backup quotidien chiffre (AES-256) avec retention 90 jours
- Logrotate pour gestion des logs (14 jours, compression)
- Uptime cible : 99.9%

---

## 5. Dimensionnement et disponibilite

### 5.1 Configuration minimale

| Ressource | Minimum | Recommande |
|-----------|---------|------------|
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Disque | 20 GB | 50+ GB SSD |
| Reseau | 100 Mbps | 1 Gbps |
| OS | Ubuntu 20.04 LTS | Ubuntu 22.04 LTS |

### 5.2 Performances mesurees

| Metrique | Cible | Mesure |
|----------|-------|--------|
| Temps de reponse API (p95) | < 500ms | ~85ms |
| Throughput | > 500 req/s | 609 req/s |
| Temps de build CI | < 5 min | ~4 min |
| Uptime | 99.9% | 99.9% |

**Preuves :** `LegacyProject/modernProject/tests/performance/test_benchmarks.py` et `locustfile.py`

### 5.3 Disponibilite

- **Healthcheck Docker** : relance automatique du conteneur si `/health` repond 503
- **Restart policy** : `unless-stopped` (redemarre apres reboot serveur)
- **Monitoring** : Prometheus scrape toutes les 15s, alertes Grafana
- **Rollback** : script `restore.sh` + `git checkout <tag>` pour rollback en < 5 min

---

**Derniere revision :** Mars 2026
