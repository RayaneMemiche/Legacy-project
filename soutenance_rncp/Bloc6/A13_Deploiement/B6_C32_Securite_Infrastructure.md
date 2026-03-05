# Securite de l'Infrastructure - AWKWARD LEGACY

**Version:** 1.0
**Date:** Mars 2026
**Projet:** AWKWARD LEGACY - Modernisation de GeneWeb
**Referentiel RNCP:** Bloc 6 - C32.1, C32.2

---

## Table des Matieres

1. [Bonnes pratiques de securite appliquees](#1-bonnes-pratiques-de-securite-appliquees)
2. [Securisation de l'infrastructure Docker](#2-securisation-de-linfrastructure-docker)
3. [Securisation reseau et Nginx](#3-securisation-reseau-et-nginx)
4. [Securite applicative](#4-securite-applicative)
5. [Gestion des secrets](#5-gestion-des-secrets)
6. [Detection et prevention des intrusions](#6-detection-et-prevention-des-intrusions)
7. [Preuves d'implementation](#7-preuves-dimplementation)

---

## 1. Bonnes pratiques de securite appliquees

### 1.1 Referentiel OWASP

La securite d'AWKWARD LEGACY est construite autour de l'OWASP Top 10 2021 :

| Categorie OWASP | Mesure implementee | Outil de verification |
|-----------------|-------------------|----------------------|
| A01 - Broken Access Control | Authentification JWT, autorisation par role | `tests/test_security_coverage.py` |
| A02 - Cryptographic Failures | AES-256-GCM, bcrypt (rounds=12), TLS 1.2/1.3 | `lib/security.py` |
| A03 - Injection | Validation des entrees, pas de requetes SQL brutes | `tests/test_secure.py` |
| A04 - Insecure Design | Architecture defense-in-depth, principe moindre privilege | Dockerfile (utilisateur non-root) |
| A05 - Security Misconfiguration | Bandit + pre-commit, scan Trivy | `.pre-commit-config.yaml`, `ci.yml` |
| A06 - Vulnerable Components | Safety + pip-audit a chaque CI | `ci.yml` job security |
| A07 - Authentication Failures | JWT avec expiration, bcrypt | `lib/security.py` |
| A08 - Data Integrity Failures | Signatures HMAC, validation | `tests/test_security_coverage.py` |
| A09 - Logging Failures | Logs applicatifs, logrotate, journald | `DEPLOYMENT_GUIDE.md` section 5.3 |
| A10 - SSRF | Validation des URLs, pas de requetes externes non controlees | `security_scanner.py` |

**Scanner de reference :** `LegacyProject/modernProject/tests/security/security_scanner.py` (1240 lignes, couvre les 10 categories OWASP)

### 1.2 Defense en profondeur

La securite est implementee en plusieurs couches independantes :

```
Couche 1 : Reseau       -> Firewall UFW, ports limites
Couche 2 : Transport    -> TLS 1.2/1.3, HSTS
Couche 3 : Application  -> Headers CSP, X-Frame-Options
Couche 4 : Container    -> Utilisateur non-root, capabilities limitees
Couche 5 : Code         -> Bandit, MyPy, detect-secrets
Couche 6 : Tests        -> 74 tests securite (SecurityManager)
Couche 7 : Monitoring   -> Logs, alertes, fail2ban
```

---

## 2. Securisation de l'infrastructure Docker

### 2.1 Utilisateur non-root dans le conteneur

```dockerfile
# Creer utilisateur non-root pour securite
RUN useradd -m -u 1000 -s /bin/bash awkward && \
    mkdir -p /app /app/data /app/logs && \
    chown -R awkward:awkward /app

# Passer a l'utilisateur non-root
USER awkward
```

**Impact :** Meme si un attaquant exploite une faille dans l'application, il n'a pas les droits root sur le systeme hote.

**Fichier :** `LegacyProject/modernProject/Dockerfile` lignes 61-87

### 2.2 Image minimale (multi-stage)

- Stage builder : inclut gcc, g++, libpq-dev (outils de compilation)
- Stage runtime : seulement `libpq5`, `curl`, `ca-certificates`
- **Surface d'attaque reduite** : pas de compilateurs, pas de shell tools superflus dans l'image finale

### 2.3 Health check Docker

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1
```

**Impact :** Docker detecte automatiquement si l'application est unhealthy et peut la relancer.

### 2.4 Scan Trivy (vulnerabilites dans l'image)

A chaque build CI, l'image Docker est scannee par Trivy :
```yaml
- name: Scan image for vulnerabilities (Trivy)
  uses: aquasecurity/trivy-action@master
  with:
    format: 'sarif'
    output: 'trivy-results.sarif'
```

Les resultats sont uploades vers GitHub Security pour suivi.

---

## 3. Securisation reseau et Nginx

### 3.1 Firewall UFW

Ports ouverts uniquement :

| Port | Protocol | Acces |
|------|----------|-------|
| 22 | TCP | Admin uniquement (SSH avec cle) |
| 80 | TCP | Public (redirection HTTPS) |
| 443 | TCP | Public (HTTPS) |
| Tous les autres | - | BLOQUE |

```bash
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### 3.2 Configuration TLS dans Nginx

```nginx
# Protocoles securises uniquement
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:...';

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;

# Session SSL securisee
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

**Impact :** TLS 1.0 et 1.1 (vulnerables a POODLE, BEAST) sont desactives. Seuls les algorithmes modernes sont acceptes.

### 3.3 Headers de securite HTTP

```nginx
# HSTS : force HTTPS pendant 1 an
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

# Interdit l'affichage dans une iframe (clickjacking)
add_header X-Frame-Options "SAMEORIGIN" always;

# Interdit le sniffing de type MIME
add_header X-Content-Type-Options "nosniff" always;

# Protection XSS navigateur
add_header X-XSS-Protection "1; mode=block" always;

# Content Security Policy : limite les sources autorisees
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;

# Politique referrer
add_header Referrer-Policy "no-referrer-when-downgrade" always;
```

**Fichier de reference :** Section 4.2 de `LegacyProject/docs/DEPLOYMENT_GUIDE.md`

---

## 4. Securite applicative

### 4.1 Chiffrement des donnees (lib/security.py)

```python
# Chiffrement AES-256-GCM pour les donnees au repos
# Hachage bcrypt avec 12 rounds pour les mots de passe
# JWT avec expiration configurable (defaut 24h)
# HMAC-SHA256 pour la signature des tokens
```

**Tests :** `tests/test_security_coverage.py` - 74 tests couvrant le SecurityManager

### 4.2 Protection contre les injections

- Pas de requetes SQL brutes (utilisation de modules Python)
- Validation des chemins de fichiers (protection path traversal)
- Validation des entrees utilisateur

**Tests de path traversal :** `tests/test_secure.py`

```python
# Exemples de vecteurs testes
malicious_paths = [
    "../../../etc/passwd",
    "..\\..\\windows\\system32",
    "%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    "....//....//etc//passwd",
]
# Tous ces chemins doivent etre rejetes par le SecurityManager
```

### 4.3 Analyse statique avec Bandit

Bandit est configure dans le pre-commit ET dans le CI :

```bash
bandit -r lib/ -ll -x lib/__pycache__
```

Bandit detecte automatiquement :
- Utilisation de `eval()` (B307)
- Utilisation de `pickle` (B301, B302)
- Mots de passe en dur (B105, B106)
- Injection shell - `subprocess(shell=True)` (B602)
- Utilisation de `os.system()` (B605)
- Modules cryptographiques faibles (B304, B305)

**Preuve concrete :** La PR #1 (feature/add-export-csv) a ete bloquee par Bandit car `export_csv.py` contenait `eval()`, `pickle.load()`, `shell=True` et des mots de passe en dur.

### 4.4 Detection de secrets dans le code

`detect-secrets` dans le pre-commit scanne chaque commit :

```yaml
- repo: https://github.com/Yelp/detect-secrets
  rev: v1.4.0
  hooks:
    - id: detect-secrets
      args: ['--baseline', '.secrets.baseline']
```

**Impact :** Aucun secret (API key, mot de passe, token) ne peut etre commite accidentellement.

---

## 5. Gestion des secrets

### 5.1 Principes

- Les secrets **ne sont jamais** dans le code source
- Fichier `.env` **jamais commite** (detecte par pre-commit hook `check-env-file` et `detect-private-key`)
- Secrets de production stockes dans **GitHub Secrets** (chiffres au repos, masques dans les logs)

### 5.2 Generation des secrets

```bash
# SECRET_KEY (256 bits)
openssl rand -hex 32

# JWT_SECRET_KEY
openssl rand -hex 32

# ENCRYPTION_KEY (Fernet AES-128-CBC)
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 5.3 Permissions fichiers

```bash
# .env accessible uniquement par le proprietaire
chmod 600 .env
# Verification: -rw------- 1 awkward awkward
```

---

## 6. Detection et prevention des intrusions

### 6.1 Fail2ban (protection SSH)

```ini
[sshd]
enabled = true
maxretry = 3        # 3 tentatives echouees
bantime = 3600      # Ban 1 heure
findtime = 600      # Sur une periode de 10 minutes
```

**Impact :** Protection contre les attaques brute-force SSH.

### 6.2 Audit des dependances

A chaque execution de CI :
```bash
# Safety : base CVE des paquets Python connus vulnerables
safety check --json

# pip-audit : audit des dependances avec la base PyPI Advisory Database
pip-audit --desc
```

**Fichier :** `.github/workflows/ci.yml` - Job `security`

### 6.3 Logs de securite

- Logs Nginx : acces et erreurs (`/var/log/nginx/`)
- Logs applicatifs : niveaux DEBUG/INFO/WARNING/ERROR/CRITICAL
- Logs systemd : `journalctl -u awkward-legacy`
- Logrotate : rotation quotidienne, conservation 14 jours, compression

### 6.4 Checklist de securite post-deploiement

```
- Firewall configure (UFW/iptables)
- SSH avec cles uniquement (pas de mot de passe)
- Utilisateur root desactive pour SSH
- Certificat SSL valide et auto-renouvele
- Headers de securite configures (HSTS, CSP, etc.)
- Mots de passe forts generes (SECRET_KEY, etc.)
- Permissions fichiers correctes (600 pour .env)
- Backups chiffres (AES-256)
- Logs de securite actives
- Fail2ban installe et configure
- Mises a jour automatiques activees (unattended-upgrades)
```

---

## 7. Preuves d'implementation

### 7.1 Fichiers de code (preuves techniques)

| Fichier | Contenu securite | Critere |
|---------|-----------------|---------|
| `LegacyProject/modernProject/Dockerfile` | Utilisateur non-root, image minimale, healthcheck | C32.1, C32.2 |
| `LegacyProject/modernProject/lib/security.py` | AES-256-GCM, bcrypt, JWT | C32.1, C32.2 |
| `LegacyProject/modernProject/tests/security/security_scanner.py` | Scanner OWASP Top 10 (1240 lignes) | C32.1, C32.2 |
| `LegacyProject/modernProject/tests/test_security_coverage.py` | 74 tests SecurityManager | C32.2 |
| `LegacyProject/modernProject/tests/test_secure.py` | Tests path traversal | C32.2 |
| `.pre-commit-config.yaml` | Bandit, detect-secrets | C32.1 |
| `LegacyProject/modernProject/.github/workflows/ci.yml` | Safety, pip-audit, Trivy | C32.1, C32.2 |
| `LegacyProject/docs/DEPLOYMENT_GUIDE.md` | Section 10 : checklist securite | C32.1 |

### 7.2 Commandes de demonstration

**Demontrer Bandit en action :**
```bash
cd LegacyProject/modernProject
bandit -r lib/ -ll
# Resultat : No issues identified (code propre)

# Demontrer la detection sur code intentionnellement cassé
bandit LegacyProject/modernProject/lib/export_csv.py
# Resultat : 7 issues (HIGH severity) -> preuve que Bandit fonctionne
```

**Demontrer le scanner OWASP :**
```bash
cd LegacyProject/modernProject
python3 tests/security/security_scanner.py
```

**Demontrer les tests de securite :**
```bash
cd LegacyProject/modernProject
pytest tests/test_security_coverage.py tests/test_secure.py -v
```

### 7.3 Preuve via PR #1

La PR `feature/add-export-csv` est la preuve vivante que la securite fonctionne :
- Bandit a detecte `eval()`, `pickle.load()`, `subprocess(shell=True)`, mots de passe en dur
- CI bloque le merge
- Nicolas a fait une review "Request changes"
- Le code malveillant n'a pas pu entrer en production

**URL :** `https://github.com/NicolasPoupon/Legacy-project/pull/1`

---

**Derniere revision :** Mars 2026
