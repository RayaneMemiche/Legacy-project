# 🚀 QUICK START - AWKWARD LEGACY

Guide rapide pour démarrer le projet en 5 minutes.

## 📋 Prérequis

- Python 3.8+
- Navigateur web moderne

## ⚡ Démarrage Rapide (3 terminaux)

### Terminal 1: Backend API

```bash
# Se placer dans le dossier
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject

# Installer Flask si nécessaire
pip3 install flask flask-cors

# Lancer le serveur
python3 server.py
```

**Résultat attendu:**
```
🚀 Démarrage du serveur API AWKWARD LEGACY...
📍 API disponible sur: http://localhost:8000
```

### Terminal 2: Frontend Web

```bash
# Se placer dans le dossier frontend
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject/frontend

# Lancer le serveur web
python3 -m http.server 3000
```

**Résultat attendu:**
```
Serving HTTP on 0.0.0.0 port 3000 (http://0.0.0.0:3000/) ...
```

### Terminal 3: Tests

```bash
# Se placer dans le dossier
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject

# Lancer tous les tests
./run_all_tests.sh
```

## 🌐 Accéder à l'Application

1. **Frontend**: Ouvrir http://localhost:3000 dans le navigateur
2. **API**: http://localhost:8000/api/health

## ✅ Vérification Rapide

```bash
# Tester l'API
curl http://localhost:8000/api/health

# Devrait retourner:
# {"status":"healthy","service":"AWKWARD LEGACY API",...}
```

## 🧪 Lancer les Tests Rapidement

### Option 1: Tous les tests
```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject
./run_all_tests.sh
```

### Option 2: Tests spécifiques

**Tests des modules:**
```bash
python3 test_modules.py
```

**Tests de performance:**
```bash
python3 test_performance_simple.py
```

**Tests d'intégration:**
```bash
python3 -m pytest tests/integration/ -v
```

## 📊 Résultats Attendus

### Tests des Modules
```
✅ Module importé avec succès
✅ Hashage/Vérification de mot de passe OK
✅ JWT création/vérification OK
✅ Chiffrement/Déchiffrement OK
```

### Tests de Performance
```
Total requêtes: 500
Throughput: ~600 req/sec
Taux de succès: 99%
Latence P95: < 100ms
```

## 🔧 Dépendances Minimales

```bash
# Installer les dépendances essentielles
pip3 install flask flask-cors pytest cryptography pyjwt bcrypt argon2-cffi
```

## 📁 Structure des Fichiers Importants

```
Legal/
├── GUIDE_LANCEMENT.md          # Guide détaillé
├── QUICK_START.md              # Ce fichier
└── LegacyProject/
    └── modernProject/
        ├── server.py           # Serveur API Flask
        ├── run_all_tests.sh    # Script de tests
        ├── test_modules.py     # Tests des modules
        ├── lib/
        │   └── security.py     # Module de sécurité
        └── frontend/
            ├── index.html      # Interface web
            ├── app.js          # Logique frontend
            ├── styles.css      # Styles
            └── config.json     # Configuration
```

## 🐛 Problèmes Courants

### Port déjà utilisé
```bash
# Tuer le processus sur le port 8000
lsof -i :8000
kill -9 <PID>
```

### Module non trouvé
```bash
# Ajouter le chemin des modules
export PYTHONPATH="${PYTHONPATH}:$(pwd)/lib"
```

### CORS Error
- Vérifier que le backend est sur port 8000
- Vérifier que le frontend est sur port 3000
- Redémarrer les deux serveurs

## 📝 Utilisation du Frontend

1. **Page d'accueil**: Vue d'ensemble et statistiques
2. **Recherche**: Trouver des personnes par nom, date, lieu
3. **Arbre**: Visualiser les liens familiaux
4. **Statistiques**: Graphiques et métriques

### Première connexion
- Cliquer sur "Inscription"
- Créer un compte test
- Se connecter avec les identifiants

## 🎯 Endpoints API Principaux

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/health` | GET | Santé de l'API |
| `/api/auth/login` | POST | Connexion |
| `/api/auth/register` | POST | Inscription |
| `/api/persons` | GET | Liste des personnes |
| `/api/persons/search` | GET | Recherche de personnes |
| `/api/statistics` | GET | Statistiques globales |
| `/api/tree/<id>` | GET | Arbre généalogique |

## 📞 Aide

- Documentation complète: `GUIDE_LANCEMENT.md`
- Tests détaillés: `./run_all_tests.sh -v`
- Logs backend: Voir Terminal 1
- Logs frontend: Console du navigateur (F12)

## ✨ Fonctionnalités Testées

- ✅ Authentification JWT
- ✅ Recherche de personnes
- ✅ Visualisation d'arbres
- ✅ Statistiques
- ✅ Conformité RGPD
- ✅ Sécurité OWASP
- ✅ Performance (600+ req/sec)

---

**Temps total de setup: ~5 minutes**

Pour aller plus loin, consultez le fichier `GUIDE_LANCEMENT.md`.