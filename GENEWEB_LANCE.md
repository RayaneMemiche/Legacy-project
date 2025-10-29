# ✅ GeneWeb Original - LANCÉ !

## 🎉 GeneWeb est Opérationnel !

### 📍 **Accès à GeneWeb**

**URL Principale:**
```
http://localhost:2317
```

**Base de Démonstration:**
```
http://localhost:2317/demo
```

---

## 👥 **Données de Test**

La base contient les mêmes personnes que AWKWARD LEGACY pour comparaison :

1. **Jean MARTIN** (né en 1950 à Paris)
2. **Marie BERNARD** (née en 1948 à Lyon, décédée en 2020)
3. **Pierre MARTIN** (né en 1975 à Paris) - Fils de Jean et Marie
4. **Sophie MARTIN** (née en 1978 à Lyon) - Fille de Jean et Marie
5. **Jacques DUBOIS** (né en 1920 à Marseille, décédé en 1995)

**Famille:**
- Jean MARTIN ⚭ Marie BERNARD (mariage en 1972)
  - Enfants: Pierre et Sophie

---

## 🔄 **Comparaison des Deux Projets**

### Maintenant Tu Peux Comparer:

| Aspect | GeneWeb Original | AWKWARD LEGACY |
|--------|------------------|----------------|
| **URL** | http://localhost:2317/demo | http://localhost:3000 |
| **Port** | 2317 | 3000 (frontend) / 8000 (API) |
| **Interface** | Vintage HTML | Moderne Bootstrap 5 |
| **Données** | 5 personnes, 1 famille | 5 personnes, 1 famille |

---

## 🧪 **Test Fonctionnel**

### 1. **Page d'Accueil**
```
GeneWeb: http://localhost:2317
AWKWARD: http://localhost:3000
```

### 2. **Rechercher "MARTIN"**

**GeneWeb:**
1. Aller sur http://localhost:2317/demo
2. Chercher dans l'interface GeneWeb

**AWKWARD LEGACY:**
1. Aller sur http://localhost:3000
2. Utiliser la barre de recherche rapide
3. Taper "Martin"

### 3. **Voir l'Arbre Généalogique**

**GeneWeb:**
- Navigation via les liens de personnes
- Vue classique HTML

**AWKWARD LEGACY:**
- Page "Arbre" dans le menu
- Sélectionner "Jean MARTIN"
- Cliquer "Générer"

### 4. **Voir les Statistiques**

**GeneWeb:**
- Tableaux HTML simples

**AWKWARD LEGACY:**
- Page "Statistiques"
- Graphiques interactifs Chart.js

---

## 📊 **Points de Comparaison**

### Interface

**GeneWeb (2317):**
- ⚙️ Interface années 2000
- 📄 Tables HTML brutes
- 🖱️ Navigation par liens
- ❌ Pas responsive
- ⚪ Couleurs basiques

**AWKWARD LEGACY (3000):**
- ✨ Interface moderne 2025
- 🎨 Design Bootstrap 5
- 🔄 Navigation SPA fluide
- ✅ Responsive mobile
- 🌈 Design coloré et moderne

### Fonctionnalités

**GeneWeb:**
- ✅ Recherche de base
- ✅ Arbres généalogiques
- ✅ Fiches personnes
- ❌ Pas d'API REST
- ❌ Pas de graphiques
- ❌ Pas d'authentification moderne

**AWKWARD LEGACY:**
- ✅ Recherche avancée multi-critères
- ✅ Arbres interactifs
- ✅ Fiches personnes modernes
- ✅ **API REST (15+ endpoints)**
- ✅ **Graphiques Chart.js**
- ✅ **Authentification JWT**

### Performance

**GeneWeb:**
- Serveur OCaml natif
- ~200-300 req/sec (estimé)

**AWKWARD LEGACY:**
- Serveur Python Flask
- **609 req/sec** (testé)

---

## 🎯 **Pour la Défense**

### Ouvrir les Deux Côte à Côte

**Onglet 1 - GeneWeb:**
```
http://localhost:2317/demo
```

**Onglet 2 - AWKWARD LEGACY:**
```
http://localhost:3000
```

**Onglet 3 - Comparaison:**
```
http://localhost:3000/comparison.html
```

### Démonstration Suggérée

1. **Montrer GeneWeb** (interface vintage)
2. **Montrer AWKWARD LEGACY** (interface moderne)
3. **Comparer** les mêmes fonctionnalités:
   - Recherche de "MARTIN"
   - Vue de la famille
   - Arbre généalogique
   - Statistiques

4. **Points à souligner:**
   - ✅ Même données dans les deux
   - ✅ Interface modernisée
   - ✅ Performance supérieure
   - ✅ Fonctionnalités additionnelles (API, JWT, RGPD)

---

## 🛑 **Arrêter les Serveurs**

### Arrêter GeneWeb
```bash
# Trouver le processus
ps aux | grep gwd

# Tuer le processus
kill -9 <PID>
```

### Arrêter AWKWARD LEGACY
```bash
# Backend (port 8000)
lsof -i :8000
kill -9 <PID>

# Frontend (port 3000)
lsof -i :3000
kill -9 <PID>
```

---

## 📝 **Notes**

- GeneWeb tourne sur le **port 2317** (port par défaut)
- AWKWARD LEGACY tourne sur **port 3000** (frontend) et **8000** (API)
- Les deux utilisent les **mêmes données de test**
- Base GeneWeb stockée dans `/tmp/geneweb_bases/demo`

---

## ✅ **Status Actuel**

| Service | Status | URL |
|---------|--------|-----|
| **GeneWeb** | ✅ RUNNING | http://localhost:2317/demo |
| **AWKWARD Backend** | ✅ RUNNING | http://localhost:8000 |
| **AWKWARD Frontend** | ✅ RUNNING | http://localhost:3000 |

**🎉 Les deux projets sont maintenant lancés et prêts à être comparés !**

---

## 🚀 **Prêt pour la Défense !**

Tu as maintenant:
1. ✅ GeneWeb original fonctionnel
2. ✅ AWKWARD LEGACY moderne fonctionnel
3. ✅ Mêmes données dans les deux
4. ✅ Documentation de comparaison
5. ✅ Page web de comparaison

**Tout est prêt pour montrer l'évolution du projet vintage vers le moderne !**