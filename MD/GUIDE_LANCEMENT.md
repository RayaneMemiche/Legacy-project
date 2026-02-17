# Guide de Lancement - AWKWARD LEGACY

Ce guide explique comment démarrer le frontend, le backend et lancer tous les tests du projet AWKWARD LEGACY.

##  Table des Matières

1. [Prérequis](#prérequis)
2. [Installation](#installation)
3. [Lancement du Backend](#lancement-du-backend)
4. [Lancement du Frontend](#lancement-du-frontend)
5. [Lancement des Tests](#lancement-des-tests)
6. [Dépannage](#dépannage)

---

##  Prérequis

### Backend (Python)
- Python 3.8+
- pip
- virtualenv (recommandé)
- OCaml (pour GeneWeb)

### Frontend
- Navigateur moderne (Chrome, Firefox, Safari, Edge)
- Serveur web (Python HTTP server, Node.js serve, ou autre)

### Tests
- pytest
- locust (pour tests de performance)
- Toutes les dépendances Python du projet

---

##  Installation

### 1. Installer les dépendances Python

```bash
# Se placer dans le dossier du projet
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject

# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate  # Sur macOS/Linux
# ou
venv\Scripts\activate  # Sur Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Vérifier que les modules sont installés

```bash
# Vérifier les modules Python
python3 -c "import sys; sys.path.append('lib'); from security import SecurityManager; print(' Module security OK')"
```

---

##  Lancement du Backend

### Option 1: Backend Flask (Recommandé)

**Créer un serveur Flask simple** (si pas déjà créé):

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject
```

Créer un fichier `server.py`:

```python
#!/usr/bin/env python3
"""
Serveur API Flask pour AWKWARD LEGACY
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Ajouter le chemin des modules
sys.path.append('lib')

from security import SecurityManager

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

# Initialiser le security manager
security = SecurityManager.get_instance()

# Routes de test
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'AWKWARD LEGACY API',
        'version': '1.0.0'
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Simulation pour le développement
    token = security.create_jwt({'user_id': 1, 'email': email})

    return jsonify({
        'success': True,
        'token': token,
        'user': {
            'id': 1,
            'name': 'Test User',
            'email': email
        }
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Hash du mot de passe
    hashed = security.hash_password(password)

    return jsonify({
        'success': True,
        'message': 'User registered successfully'
    })

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    return jsonify({
        'totalPersons': 150,
        'totalFamilies': 45,
        'avgChildren': 2.3,
        'maxGenerations': 8,
        'lastUpdate': '2025-10-23T10:30:00Z',
        'centuryDistribution': {
            '18ème': 12,
            '19ème': 45,
            '20ème': 120,
            '21ème': 23
        },
        'topSurnames': {
            'Martin': 15,
            'Bernard': 12,
            'Dubois': 10,
            'Thomas': 8,
            'Robert': 7
        }
    })

@app.route('/api/persons/search', methods=['GET'])
def search_persons():
    query = request.args.get('query', '')

    # Données de démonstration
    persons = [
        {
            'id': '1',
            'firstName': 'Jean',
            'lastName': 'Martin',
            'birthDate': '1950-05-15',
            'birthPlace': 'Paris',
            'deathDate': None,
            'deathPlace': None
        },
        {
            'id': '2',
            'firstName': 'Marie',
            'lastName': 'Bernard',
            'birthDate': '1948-08-20',
            'birthPlace': 'Lyon',
            'deathDate': '2020-03-10',
            'deathPlace': 'Lyon'
        }
    ]

    return jsonify(persons)

@app.route('/api/activity/recent', methods=['GET'])
def get_recent_activity():
    activities = [
        {
            'type': 'create',
            'description': 'Nouvelle personne ajoutée: Jean Martin',
            'timestamp': '2025-10-23T09:30:00Z'
        },
        {
            'type': 'update',
            'description': 'Modification de Marie Bernard',
            'timestamp': '2025-10-23T08:15:00Z'
        }
    ]

    return jsonify(activities)

if __name__ == '__main__':
    print(" Démarrage du serveur API AWKWARD LEGACY...")
    print(" API disponible sur: http://localhost:8000")
    print(" Frontend à lancer sur: http://localhost:3000")
    app.run(host='0.0.0.0', port=8000, debug=True)
```

**Lancer le serveur**:

```bash
# Activer l'environnement virtuel si ce n'est pas fait
source venv/bin/activate

# Lancer le serveur
python3 server.py
```

Le serveur démarre sur `http://localhost:8000`

### Option 2: Backend GeneWeb (OCaml)

```bash
# Se placer dans le dossier geneweb
cd /Users/rayanememiche/Documents/Taff/Legal/geneweb

# Compiler GeneWeb (si pas déjà fait)
make

# Lancer GeneWeb
./gwd -bd /path/to/database -port 2317
```

---

##  Lancement du Frontend

### Option 1: Serveur Python (Recommandé pour le développement)

```bash
# Ouvrir un NOUVEAU terminal
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject/frontend

# Lancer le serveur HTTP Python
python3 -m http.server 3000
```

Le frontend est accessible sur `http://localhost:3000`

### Option 2: Serveur Node.js

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject/frontend

# Installer serve si nécessaire
npm install -g serve

# Lancer le serveur
npx serve -s . -p 3000
```

### Option 3: Nginx (Production)

Créer un fichier de configuration Nginx:

```nginx
server {
    listen 80;
    server_name localhost;

    root /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject/frontend;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

##  Lancement des Tests

### Tests Complets (Tous les tests)

```bash
# Se placer dans le dossier du projet
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject

# Activer l'environnement virtuel
source venv/bin/activate

# Lancer TOUS les tests
python3 test_modules.py
```

**Ce script lance :**
-  Tests du module Security
-  Vérification des fichiers de configuration
-  Vérification des rapports

---

### Tests par Catégorie

#### 1. Tests du Module Security

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject

# Lancer les tests de sécurité
python3 test_modules.py
```

**Tests effectués :**
- Hashage et vérification de mots de passe (PBKDF2/Bcrypt/Argon2)
- Création et vérification de tokens JWT
- Chiffrement et déchiffrement AES-256-GCM

---

#### 2. Tests d'Intégration

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject

# Lancer les tests d'intégration
python3 -m pytest tests/integration/test_integration_suite.py -v
```

**Tests effectués :**
- Vérification du bridge Python-OCaml
- Tests de bout en bout
- Vérification de l'intégration des modules

**Alternative :**
```bash
# Tests d'intégration complets
python3 -m pytest tests/integration/test_complete_integration.py -v
```

---

#### 3. Tests de Performance

##### Tests de Performance Simples

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject

# Lancer les tests de performance simplifiés
python3 test_performance_simple.py
```

**Ce test simule :**
- 10, 50, et 100 utilisateurs concurrents
- 5 requêtes par utilisateur
- Métriques: Throughput, P50, P95, P99

##### Tests de Performance Complets

```bash
# Lancer les benchmarks détaillés
python3 -m pytest tests/performance/test_benchmarks.py -v
```

##### Tests de Charge avec Locust

```bash
# Installer locust si nécessaire
pip install locust

# Lancer Locust
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject
locust -f tests/performance/locustfile.py --host=http://localhost:8000

# Ouvrir http://localhost:8089 dans le navigateur
# Configurer le nombre d'utilisateurs et lancer le test
```

---

#### 4. Tests de Conformité RGPD

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject

# Lancer le validateur RGPD
python3 tests/compliance/rgpd_validator.py
```

**Vérifications :**
- Consentement utilisateur
- Droit à l'oubli
- Portabilité des données
- Chiffrement des données sensibles
- Conservation des données

---

#### 5. Tests de Sécurité (Scanner OWASP)

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject

# Lancer le scanner de sécurité
python3 tests/security/security_scanner.py
```

**Vérifications OWASP Top 10 :**
- Injection SQL
- Authentification cassée
- Exposition de données sensibles
- XXE (XML External Entities)
- Contrôle d'accès cassé
- Mauvaise configuration de sécurité
- XSS (Cross-Site Scripting)
- Désérialisation non sécurisée
- Composants vulnérables
- Journalisation insuffisante

---

### Tests Unitaires (avec pytest)

```bash
# Lancer tous les tests unitaires
python3 -m pytest tests/ -v

# Lancer avec couverture de code
python3 -m pytest tests/ --cov=lib --cov-report=html

# Voir le rapport de couverture
open htmlcov/index.html
```

---

##  Commandes de Test Complètes

### Script de Test Global

Créer un script `run_all_tests.sh`:

```bash
#!/bin/bash

echo "======================================"
echo " AWKWARD LEGACY - Tests Complets"
echo "======================================"

# Activer l'environnement virtuel
source venv/bin/activate

# 1. Tests des modules
echo ""
echo "1  Tests des Modules..."
python3 test_modules.py

# 2. Tests d'intégration
echo ""
echo "2  Tests d'Intégration..."
python3 -m pytest tests/integration/ -v

# 3. Tests de performance
echo ""
echo "3  Tests de Performance..."
python3 test_performance_simple.py

# 4. Tests RGPD
echo ""
echo "4  Tests de Conformité RGPD..."
python3 tests/compliance/rgpd_validator.py

# 5. Tests de sécurité
echo ""
echo "5  Tests de Sécurité..."
python3 tests/security/security_scanner.py

echo ""
echo "======================================"
echo " Tests terminés!"
echo "======================================"
```

Rendre le script exécutable et le lancer:

```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```

---

##  Vérification de l'Installation

### Vérifier que tout fonctionne

```bash
# 1. Vérifier Python
python3 --version

# 2. Vérifier les modules Python
python3 -c "import sys; sys.path.append('LegacyProject/modernProject/lib'); from security import SecurityManager; print(' OK')"

# 3. Vérifier Flask
python3 -c "import flask; print(' Flask OK')"

# 4. Vérifier pytest
python3 -c "import pytest; print(' pytest OK')"

# 5. Tester l'API
curl http://localhost:8000/api/health
```

---

##  Dépannage

### Problème: Module non trouvé

```bash
# Solution: Ajouter le chemin des modules
export PYTHONPATH="${PYTHONPATH}:/Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject/lib"
```

### Problème: Port déjà utilisé

```bash
# Trouver le processus utilisant le port 8000
lsof -i :8000

# Tuer le processus
kill -9 <PID>

# Ou utiliser un autre port
python3 server.py --port 8001
```

### Problème: CORS Error

```bash
# Vérifier que CORS est activé dans server.py
# Vérifier que l'URL du frontend est correcte dans config.json
```

### Problème: Environnement virtuel non activé

```bash
# Vérifier si venv est activé
which python3

# Devrait afficher: /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject/venv/bin/python3

# Si non activé:
source venv/bin/activate
```

---

##  Structure des Commandes par Terminal

### Terminal 1: Backend

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject
source venv/bin/activate
python3 server.py
```

### Terminal 2: Frontend

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject/frontend
python3 -m http.server 3000
```

### Terminal 3: Tests

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject
source venv/bin/activate
./run_all_tests.sh
```

---

##  Checklist de Lancement

- [ ] Environnement virtuel créé et activé
- [ ] Dépendances Python installées
- [ ] Backend lancé sur port 8000
- [ ] Frontend lancé sur port 3000
- [ ] API accessible (test avec curl)
- [ ] Frontend accessible dans le navigateur
- [ ] Tests des modules passent
- [ ] Tests d'intégration passent
- [ ] Tests de performance passent

---

##  URLs à Retenir

| Service | URL | Description |
|---------|-----|-------------|
| Backend API | http://localhost:8000 | API Python Flask |
| Frontend | http://localhost:3000 | Interface web |
| API Health | http://localhost:8000/api/health | Vérification santé API |
| Locust | http://localhost:8089 | Interface tests de charge |

---

##  Support

En cas de problème, vérifier :
1. Les logs du backend (terminal 1)
2. Les logs du frontend (console navigateur F12)
3. La console Python pour les tests
4. Les fichiers de rapport générés

Bonne chance avec votre défense ! 