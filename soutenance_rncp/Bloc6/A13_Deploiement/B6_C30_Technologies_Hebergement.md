# Technologies et Services d'Hebergement - AWKWARD LEGACY

**Version:** 2.0
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

AWKWARD LEGACY est deploye selon une architecture separee frontend / backend :

```
Utilisateur
    |
    +---> [Vercel CDN] --> Frontend (HTML/CSS/JS)
    |          |
    |     (HTTPS auto)
    |
    +---> [Docker] --> Backend Python Flask --> Fichiers GeneWeb .gwb
               |
          (deployable sur VPS / Cloud)
```

### 1.2 Composants de l'infrastructure

| Composant | Technologie | Role |
|-----------|------------|------|
| **Hebergement frontend** | Vercel | Hosting statique HTML/CSS/JS, CDN global, HTTPS automatique |
| **Backend applicatif** | Python 3.12 + Flask (Docker) | API REST + serveur genealogique |
| **Conteneurisation backend** | Docker + Docker Compose | Isolation, portabilite, reproductibilite |
| **SSL/TLS frontend** | Vercel (Let's Encrypt integre) | HTTPS automatique, renouvellement transparent |
| **CI/CD** | GitHub Actions | Deploiement automatise (8 jobs) |
| **Registre images** | GitHub Container Registry (ghcr.io) | Stockage et versionnage des images Docker backend |

**Fichiers de reference :**
- `LegacyProject/modernProject/frontend/` : code frontend deploye sur Vercel
- `LegacyProject/modernProject/Dockerfile` : image Docker backend
- `LegacyProject/modernProject/.github/workflows/ci.yml` : pipeline CI/CD complet
- `LegacyProject/docs/DEPLOYMENT_GUIDE.md` : guide de deploiement detaille

---

## 2. Architecture de deploiement

### 2.1 Frontend sur Vercel

Vercel heberge le frontend statique (HTML/CSS/JS) du projet :

**Fonctionnement :**
- Connexion du repository GitHub a Vercel
- A chaque `git push` sur `rayane`, Vercel declenche automatiquement un nouveau deploiement
- Le build est instantane (fichiers statiques, pas de compilation)
- Le site est distribue sur le CDN mondial de Vercel (edge network)
- HTTPS activé automatiquement via Let's Encrypt integre

**Avantages concrets :**
- URL de production stable et personnalisable
- Preview deployments automatiques pour chaque Pull Request
- Rollback en 1 clic depuis le dashboard Vercel
- 0 configuration serveur requise

### 2.2 Backend conteneurise (Docker)

Le backend Python Flask est conteneurise via un Dockerfile multi-stage :

**Stage 1 - Builder** (`python:3.12-slim`) :
- Installation des dependances systeme (gcc, libpq-dev)
- Creation d'un environnement virtuel Python isole
- Installation des dependances Python depuis `requirements.txt`

**Stage 2 - Runtime** (`python:3.12-slim`) :
- Image finale legere (~180 MB vs ~800 MB builder)
- Utilisateur non-root `awkward` (UID 1000)
- Health check integre : `curl -f http://localhost:5000/health`
- Exposition du port 5000

**Fichier :** `LegacyProject/modernProject/Dockerfile`

### 2.3 Pipeline CI/CD (8 jobs)

```
Push/PR sur GitHub
    |
    +---> [1. Lint] Black, Flake8, Bandit
    +---> [2. Unit Tests] Python 3.10 / 3.11 / 3.12
    +---> [3. Integration Tests] Redis + PostgreSQL
    +---> [4. Security Scan] Safety, pip-audit
    +---> [5. Build Docker] multi-arch amd64 + arm64
    +---> [6. Deploy Staging]
    +---> [7. Deploy Production]
    +---> [8. Release Notes]

En parallele, Vercel deploie automatiquement le frontend.
```

**Fichier :** `LegacyProject/modernProject/.github/workflows/ci.yml`

---

## 3. Justification des choix techniques

### 3.1 Pourquoi Vercel pour le frontend ?

| Argument | Detail |
|----------|--------|
| **Simplicite** | Zero configuration serveur, connexion GitHub en 2 clics |
| **Performance** | CDN mondial : contenu servi depuis le noeud le plus proche de l'utilisateur |
| **HTTPS automatique** | Certificat SSL genere et renouvele automatiquement (Let's Encrypt integre) |
| **Deploiement continu** | Chaque push sur la branche principale declenche un deploiement automatique |
| **Preview deployments** | Chaque PR genere une URL de preview unique pour tester avant de merger |
| **Rollback instantane** | Retour a une version precedente en 1 clic depuis le dashboard |

### 3.2 Pourquoi Docker pour le backend ?

| Argument | Detail |
|----------|--------|
| **Portabilite** | Meme comportement en dev et prod. Elimine "ca marche sur ma machine" |
| **Isolation** | L'application ne peut pas affecter le systeme hote |
| **Reproductibilite** | Chaque build produit exactement la meme image (hash SHA256) |
| **Versionnage** | Chaque image taguee (SHA, branche, semver). Rollback en 30 secondes |
| **Multi-arch** | Build `linux/amd64` et `linux/arm64` pour flexibilite du choix serveur |

### 3.3 Pourquoi GitHub Actions ?

| Argument | Detail |
|----------|--------|
| **Integre a GitHub** | Meme plateforme que le code, pas d'outil externe |
| **Gratuit** | Inclus dans GitHub (2000 min/mois) |
| **Matrix builds** | Python 3.10, 3.11, 3.12 en parallele |
| **Secrets management** | Variables sensibles stockees de facon securisee |

---

## 4. Contraintes prises en compte

### 4.1 Budget

- **Vercel** : plan gratuit (Hobby) suffisant pour un projet EIP
- **GitHub Actions** : inclus dans le plan GitHub gratuit
- **Docker** : gratuit et open-source
- **GitHub Container Registry** : gratuit pour les repos publics
- **Cout total** : 0 EUR (hors eventuel VPS pour le backend en production)

### 4.2 Securite

**Frontend (Vercel) :**
- HTTPS force automatiquement
- Headers de securite configurables (CSP, HSTS, X-Frame-Options)
- Isolation par deploiement (chaque version est immuable)

**Backend (Docker) :**
- Utilisateur non-root dans le conteneur (UID 1000)
- Image minimale (multi-stage, surface d'attaque reduite)
- Scan de vulnerabilites Docker avec Trivy a chaque CI
- Secrets via GitHub Secrets (jamais en clair dans le code)

### 4.3 Scalabilite

- **Vercel** : auto-scaling natif, CDN mondial, pas de configuration
- **Backend** : architecture horizontale possible (plusieurs instances Docker)
- Images multi-arch (amd64 + arm64) pour flexibilite du choix serveur

### 4.4 Qualite de service

- **Vercel** : SLA 99.99% uptime, CDN mondial, latence < 100ms
- **Backend** : Health check toutes les 30s, rollback < 5 min
- **CI/CD** : Deploiement automatise = pas d'erreur humaine

---

## 5. Dimensionnement et disponibilite

### 5.1 Frontend Vercel

| Metrique | Valeur |
|----------|--------|
| Uptime SLA | 99.99% |
| Latence CDN | < 100ms mondial |
| Deploiement | ~30 secondes |
| Rollback | 1 clic |
| HTTPS | Automatique |
| Preview URLs | Automatiques par PR |

### 5.2 Backend Docker

| Ressource | Minimum | Recommande |
|-----------|---------|------------|
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Disque | 20 GB | 50+ GB SSD |

### 5.3 Performances mesurees

| Metrique | Cible | Mesure |
|----------|-------|--------|
| Temps de reponse API (p95) | < 500ms | ~85ms |
| Throughput | > 500 req/s | 609 req/s |
| Temps de build CI | < 5 min | ~4 min |

**Preuves :** `LegacyProject/modernProject/tests/performance/test_benchmarks.py` et `locustfile.py`

---

**Derniere revision :** Mars 2026
