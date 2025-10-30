# 📋 COMMANDES COPY-PASTE - AWKWARD LEGACY

Toutes les commandes prêtes à copier-coller pour lancer le projet.

---

## 🚀 DÉMARRAGE COMPLET

### 📍 Étape 1: Installer les Dépendances

**Copier-coller dans le terminal:**

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject
pip3 install flask flask-cors cryptography pyjwt bcrypt argon2-cffi pytest
```

---

### 🖥️ Étape 2: Lancer le Backend (Terminal 1)

**Ouvrir un NOUVEAU terminal et copier-coller:**

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject
python3 server.py
```

**Résultat attendu:**
```
🚀 Démarrage du serveur API AWKWARD LEGACY
📍 API disponible sur: http://localhost:8000
```

**⚠️ LAISSER CE TERMINAL OUVERT**

---

### 🌐 Étape 3: Lancer le Frontend (Terminal 2)

**Ouvrir un NOUVEAU terminal et copier-coller:**

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject/frontend
python3 -m http.server 3000
```

**Résultat attendu:**
```
Serving HTTP on 0.0.0.0 port 3000
```

**⚠️ LAISSER CE TERMINAL OUVERT**

---

### 🌍 Étape 4: Ouvrir le Navigateur

**Copier-coller cette URL dans le navigateur:**

```
http://localhost:3000
```

---

## 🧪 LANCER LES TESTS

### 🎯 Option A: Tous les Tests en Une Fois (Terminal 3)

**Ouvrir un NOUVEAU terminal et copier-coller:**

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject
./run_all_tests.sh
```

---

### 🔬 Option B: Tests Individuels

**Ouvrir un terminal et se placer dans le dossier:**

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject
```

#### Test 1: Tests des Modules Security

```bash
python3 test_modules.py
```

**Résultat attendu:**
```
✅ Module security importé avec succès
✅ Hashage/Vérification de mot de passe OK
✅ JWT création/vérification OK
✅ Chiffrement/Déchiffrement OK
```

---

#### Test 2: Tests de Performance

```bash
python3 test_performance_simple.py
```

**Résultat attendu:**
```
📊 Résultats:
  • Throughput: ~600 req/sec
  • Taux de succès: 99%+
  • Latence P95: <100ms
```

---

#### Test 3: Tests d'Intégration

```bash
python3 -m pytest tests/integration/test_integration_suite.py -v
```

---

#### Test 4: Tests RGPD

```bash
python3 tests/compliance/rgpd_validator.py
```

**Résultat attendu:**
```
Conformité RGPD: 79.3%
```

---

#### Test 5: Scanner de Sécurité

```bash
python3 tests/security/security_scanner.py
```

**Résultat attendu:**
```
Score de Sécurité: 85/100
```

---

## ✅ VÉRIFICATIONS

### Vérifier que l'API fonctionne

**Copier-coller dans un nouveau terminal:**

```bash
curl http://localhost:8000/api/health
```

**Résultat attendu:**
```json
{"status":"healthy","service":"AWKWARD LEGACY API","version":"1.0.0"}
```

---

### Vérifier les Statistiques

```bash
curl http://localhost:8000/api/statistics
```

---

### Tester la Recherche

```bash
curl "http://localhost:8000/api/persons/search?query=martin"
```

---

## 🛑 ARRÊTER LES SERVEURS

### Arrêter le Backend (Terminal 1)

```
Ctrl + C
```

### Arrêter le Frontend (Terminal 2)

```
Ctrl + C
```

---

## 🔧 DÉPANNAGE

### Problème: Port 8000 déjà utilisé

```bash
# Trouver le processus
lsof -i :8000

# Tuer le processus (remplacer <PID> par le numéro affiché)
kill -9 <PID>
```

---

### Problème: Port 3000 déjà utilisé

```bash
# Trouver le processus
lsof -i :3000

# Tuer le processus
kill -9 <PID>
```

---

### Problème: Module non trouvé

```bash
# Ajouter le chemin des modules
export PYTHONPATH="${PYTHONPATH}:/Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject/lib"
```

---

### Problème: Flask non installé

```bash
pip3 install flask flask-cors
```

---

### Problème: pytest non installé

```bash
pip3 install pytest
```

---

## 📊 CHECKLIST DE LANCEMENT

Cocher au fur et à mesure:

- [ ] Terminal 1: Backend lancé sur http://localhost:8000
- [ ] Terminal 2: Frontend lancé sur http://localhost:3000
- [ ] Navigateur: Page http://localhost:3000 s'affiche
- [ ] Vérification: `curl http://localhost:8000/api/health` fonctionne
- [ ] Tests: `./run_all_tests.sh` exécuté avec succès

---

## 🎬 COMMANDES POUR LA DÉMO

### Démo Complète en 5 Minutes

**Terminal 1 - Backend:**
```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject && python3 server.py
```

**Terminal 2 - Frontend:**
```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject/frontend && python3 -m http.server 3000
```

**Terminal 3 - Tests:**
```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject && ./run_all_tests.sh
```

**Navigateur:**
```
http://localhost:3000
```

---

## 📈 COMMANDES D'INSTALLATION COMPLÈTE

### Installation de Toutes les Dépendances

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject
pip3 install -r requirements.txt
```

---

### Créer un Environnement Virtuel (Recommandé)

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject

# Créer l'environnement
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate

# Installer les dépendances
pip3 install -r requirements.txt
```

---

## 🎯 COMMANDES POUR LES TESTS SPÉCIFIQUES

### Tests avec Couverture de Code

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject
python3 -m pytest tests/ --cov=lib --cov-report=html
```

### Ouvrir le Rapport de Couverture

```bash
open htmlcov/index.html
```

---

### Tests de Performance avec Locust

```bash
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject
pip3 install locust
locust -f tests/performance/locustfile.py --host=http://localhost:8000
```

**Puis ouvrir:**
```
http://localhost:8089
```

---

## 🎓 PRÉPARATION POUR LA DÉFENSE

### Commande Unique de Démonstration

**Copier cette commande pour tout démarrer rapidement:**

```bash
# Backend en arrière-plan
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject && python3 server.py &

# Attendre 2 secondes
sleep 2

# Frontend en arrière-plan
cd /Users/rayanememiche/Documents/Taff/Legal/LegacyProject/modernProject/frontend && python3 -m http.server 3000 &

# Attendre 2 secondes
sleep 2

# Ouvrir le navigateur (macOS)
open http://localhost:3000

echo "✅ Tout est lancé !"
```

---

## 📞 AIDE RAPIDE

### Voir les Logs du Backend

Le backend affiche les logs directement dans Terminal 1

### Voir les Logs du Frontend

Ouvrir la console du navigateur: `F12` ou `Cmd+Option+I` (Mac)

### Relancer un Serveur

1. Arrêter avec `Ctrl+C`
2. Re-lancer avec la même commande

---

## 🎉 FIN

**Toutes les commandes sont prêtes !**

Pour plus de détails:
- **Guide complet**: `GUIDE_LANCEMENT.md`
- **Démarrage rapide**: `QUICK_START.md`
- **Récapitulatif**: `RECAP_PROJET.md`

**Bon courage pour la défense ! 🚀**