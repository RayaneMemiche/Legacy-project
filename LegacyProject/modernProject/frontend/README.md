# AWKWARD LEGACY - Frontend Web

Interface web moderne pour le système de gestion généalogique AWKWARD LEGACY, basé sur GeneWeb.

##  Fonctionnalités

### Interface Utilisateur
- **Design Moderne**: Interface responsive avec Bootstrap 5 et Bootstrap Icons
- **Navigation Intuitive**: Menu de navigation avec dropdowns pour analyses et GEDCOM
- **Notifications Toast**: Système de notifications élégant et non-intrusif
- **Cartes Interactives**: Cartes animées avec effets hover pour chaque fonctionnalité
- **Loading Spinners**: Indicateurs de chargement pour toutes les opérations asynchrones

### Fonctionnalités Principales

####  Page d'Accueil
- **Recherche Rapide**: Barre de recherche immédiate sur la page d'accueil
- **Statistiques en Direct**: 4 cartes affichant personnes, familles, générations, période
- **Cartes de Fonctionnalités**: 6 cartes interactives menant aux fonctions principales
- **Activité Récente**: Journal des dernières actions effectuées

####  Recherche Avancée
- **Filtres Multi-critères**: Prénom, nom, année de naissance/décès, lieux, sexe
- **Résultats Enrichis**: Cartes détaillées avec informations complètes
- **Navigation Directe**: Liens vers ascendants et descendants

####  Analyse de Consanguinité
- **Calcul de Parenté**: Coefficient de parenté (φ) entre deux personnes
- **Coefficient de Consanguinité**: Coefficient F pour une personne donnée
- **Noms de Relations**: Traduction automatique en termes familiaux (cousins germains, etc.)
- **Chemins Généalogiques**: Affichage des chemins communs entre individus

####  Analyse de Lignées
- **Composantes Connexes**: Identification des lignées distinctes dans la base
- **Plus Grande Lignée**: Affichage de la lignée la plus importante
- **Personnes Isolées**: Liste des individus sans connexions familiales
- **Statistiques par Lignée**: Nombre de personnes, générations estimées

####  Dashboard Statistiques
- **Graphiques Interactifs**: Chart.js pour visualisations dynamiques
- **Top Noms de Famille**: Graphique à barres des 20 noms les plus fréquents
- **Distribution Temporelle**: Graphique en ligne par siècle
- **Métriques Générales**: Totaux, moyennes, répartitions par sexe

####  GEDCOM
- **Import GEDCOM**: Interface pour importer des fichiers GEDCOM 5.5/5.5.1
- **Export GEDCOM**: Génération de fichiers GEDCOM conformes au standard
- **Outils CLI**: Documentation intégrée pour ged2gwb.py et gwb2ged.py
- **Statistiques d'Import**: Compte des personnes et familles importées

####  Arbre Généalogique
- **Visualisation Interactive**: Arbre généalogique avec navigation
- **Ascendants/Descendants**: Filtres pour afficher ancêtres ou descendants
- **Multi-générations**: Configuration du nombre de générations à afficher

####  Authentification
- **Système JWT**: Connexion sécurisée avec tokens JWT
- **Inscription**: Création de compte utilisateur
- **Profil Utilisateur**: Gestion du profil et des préférences
- **Déconnexion**: Gestion sécurisée des sessions

### Sécurité et Conformité
- **RGPD**: Export et suppression des données personnelles
- **Chiffrement**: Communications sécurisées avec l'API (HTTPS en production)
- **Validation**: Validation côté client et serveur
- **Session**: Gestion automatique de l'expiration des tokens

##  Structure des Fichiers

```
frontend/
├── index.html          # Page principale HTML (version originale)
├── index_new.html      # Interface complète modernisée avec toutes les fonctionnalités
├── app.js              # Logique JavaScript de base
├── app_complete.js     # Application JavaScript complète avec tous les modules
├── styles.css          # Feuille de styles personnalisée
├── config.json         # Configuration de l'application (optionnel)
└── README.md           # Documentation complète
```

### Fichiers Principaux

#### `index_new.html`
Interface utilisateur complète avec:
- Navigation responsive avec dropdowns
- 8 pages distinctes (Accueil, Recherche, Consanguinité, Lignées, Arbre, Stats, Import, Export)
- Système de toast notifications
- Loading spinners
- Cartes statistiques et feature cards
- Design moderne avec variables CSS personnalisées

#### `app_complete.js`
Application JavaScript modulaire contenant:
- **APIClient**: Classe pour toutes les requêtes API REST
  - 25+ méthodes pour personnes, familles, recherche, statistiques, GEDCOM
- **Page Loaders**: Fonctions pour charger dynamiquement chaque page
  - `loadSearchPage()`: Interface de recherche avancée
  - `loadConsanguinityPage()`: Calculateur de consanguinité
  - `loadLineagesPage()`: Analyseur de lignées
  - `loadStatsPage()`: Dashboard statistiques avec Chart.js
  - `loadTreePage()`: Visualisateur d'arbres
  - `loadImportPage()`: Interface d'import GEDCOM
  - `loadExportPage()`: Interface d'export GEDCOM
- **Utilities**: Navigation, toasts, formatage de données
- **Event Handlers**: Gestion des formulaires et interactions utilisateur

##  Installation et Démarrage

### Prérequis
- **Python 3.9+** avec l'API FastAPI fonctionnelle
- **Navigateur moderne** (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- **Serveur web** (pour servir les fichiers statiques)

### Étape 1: Démarrer l'API Backend

L'API REST doit être lancée avant d'utiliser le frontend.

```bash
# Depuis le répertoire racine du projet
cd LegacyProject/modernProject

# Activer l'environnement virtuel (si utilisé)
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Lancer l'API FastAPI
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Ou utiliser le Makefile
make run-api
```

L'API sera accessible sur **http://localhost:8000**

**Vérification**: Ouvrir http://localhost:8000/docs pour voir la documentation OpenAPI interactive.

### Étape 2: Servir le Frontend

#### Option 1: Python HTTP Server (développement)
```bash
cd LegacyProject/modernProject/frontend
python3 -m http.server 3000
```

#### Option 2: Node.js serve (développement)
```bash
cd LegacyProject/modernProject/frontend
npx serve -s . -p 3000
```

#### Option 3: Ouvrir directement (développement local)
```bash
# Ouvrir le fichier dans un navigateur
open index_new.html  # Mac
xdg-open index_new.html  # Linux
start index_new.html  # Windows
```

**Note**: L'option 3 peut avoir des limitations CORS avec certains navigateurs.

#### Option 4: Nginx (production)
```nginx
server {
    listen 80;
    server_name awkward-legacy.local;
    root /path/to/modernProject/frontend;
    index index_new.html;

    location / {
        try_files $uri $uri/ /index_new.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Étape 3: Accéder à l'Application

Ouvrir le navigateur sur:
- **Frontend**: http://localhost:3000/index_new.html
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

##  Configuration

### Configuration API dans le Code

L'URL de l'API est définie dans `app_complete.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

Pour changer l'URL de l'API (production, staging, etc.):

```javascript
// En développement
const API_BASE_URL = 'http://localhost:8000/api';

// En production
const API_BASE_URL = 'https://api.awkward-legacy.com/api';
```

### Configuration CORS de l'API

L'API FastAPI est déjà configurée pour accepter les requêtes CORS dans `api/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production: spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production**: Remplacer `allow_origins=["*"]` par les domaines spécifiques:
```python
allow_origins=["https://awkward-legacy.com", "https://www.awkward-legacy.com"]
```

##  Guide d'Utilisation Détaillé

### Page d'Accueil

#### Statistiques Rapides
Les 4 cartes en haut affichent automatiquement:
- **Personnes**: Nombre total d'individus dans la base
- **Familles**: Nombre de familles enregistrées
- **Générations**: Profondeur généalogique
- **Période**: Plage d'années couverte

#### Recherche Rapide
1. Utiliser la barre de recherche sur la page d'accueil
2. Taper un nom, prénom ou lieu
3. Appuyer sur Entrée ou cliquer sur "Rechercher"
4. Les résultats s'affichent immédiatement

#### Cartes de Fonctionnalités
Cliquer sur les cartes pour accéder directement aux fonctionnalités:
- **Consanguinité**: Analyse de parenté
- **Lignées**: Analyse de connectivité
- **GEDCOM**: Import/Export
- **Recherche Avancée**: Filtres multiples
- **Statistiques**: Visualisations
- **Arbre Généalogique**: Navigation familiale

### Recherche Avancée

1. Cliquer sur **"Recherche Avancée"** dans le menu
2. Remplir les critères souhaités:
   - **Prénom**: Recherche exacte ou partielle
   - **Nom**: Recherche sur le nom de famille
   - **Année de naissance**: Année exacte (ex: 1850)
   - **Année de décès**: Année exacte
   - **Lieu de naissance**: Ville ou région
   - **Lieu de décès**: Ville ou région
   - **Sexe**: Homme, Femme, ou tous
3. Cliquer sur **"Rechercher"**
4. Les résultats s'affichent sous forme de cartes avec:
   - Nom complet
   - Dates de naissance/décès
   - Lieux
   - Liens vers ascendants et descendants

### Analyse de Consanguinité

#### Calculer le Coefficient de Parenté
1. Naviguer vers **Analyses > Consanguinité**
2. Dans la section "Coefficient de Parenté":
   - Sélectionner la **Personne 1** (menu déroulant)
   - Sélectionner la **Personne 2** (menu déroulant)
   - Cliquer sur **"Calculer la Parenté"**
3. Le résultat affiche:
   - Coefficient φ (valeur entre 0 et 1)
   - Nom de la relation (ex: "cousins germains")
   - Interprétation du lien familial

**Valeurs de référence**:
- 0.50: Parent-enfant
- 0.25: Frères/sœurs, grand-parent-petit-enfant
- 0.125: Oncle/tante-neveu/nièce
- 0.0625: Cousins germains

#### Calculer le Coefficient de Consanguinité
1. Dans la section "Coefficient de Consanguinité":
   - Sélectionner une **Personne**
   - Cliquer sur **"Calculer la Consanguinité"**
2. Le résultat affiche:
   - Coefficient F (mesure de la consanguinité)
   - Statut: "Non consanguin" si F = 0, sinon le niveau de consanguinité

### Analyse de Lignées

1. Naviguer vers **Analyses > Lignées**
2. Cliquer sur **"Analyser les Lignées"**
3. L'interface affiche:
   - **Nombre total de personnes**
   - **Nombre de lignées distinctes**: Composantes connexes indépendantes
   - **Plus grande lignée**: Taille de la lignée la plus importante
   - **Personnes isolées**: Individus sans connexions familiales
4. La liste détaillée montre chaque lignée avec:
   - Taille (nombre de personnes)
   - Nombre de fondateurs (racines)
   - Générations estimées
   - Nombre de mariages

### Dashboard Statistiques

1. Naviguer vers **Statistiques** dans le menu
2. Cliquer sur **"Charger les Statistiques"**
3. Les graphiques s'affichent automatiquement:

#### Graphiques Disponibles
- **Top 20 Noms de Famille**: Graphique à barres horizontal
  - Affiche les noms les plus fréquents
  - Nombre d'occurrences pour chaque nom
- **Distribution par Siècle**: Graphique en ligne
  - Évolution du nombre de naissances par siècle
  - Visualisation des tendances temporelles

#### Métriques Générales
- Total de personnes et familles
- Répartition par sexe (hommes/femmes)
- Moyenne d'enfants par famille
- Plus ancienne et plus récente naissance

### Import GEDCOM

1. Naviguer vers **GEDCOM > Importer**
2. L'interface explique comment importer:
   ```bash
   # Via l'outil CLI
   cd LegacyProject/modernProject
   ./bin/ged2gwb.py fichier.ged dossier_sortie --verbose --stats
   ```
3. Options disponibles:
   - `--verbose`: Affichage détaillé du processus
   - `--stats`: Statistiques d'import (personnes, familles)
4. Le fichier .ged est parsé et converti en format interne

**Note**: L'import se fait via CLI car le parsing GEDCOM est complexe et mieux géré côté serveur.

### Export GEDCOM

1. Naviguer vers **GEDCOM > Exporter**
2. L'interface explique comment exporter:
   ```bash
   # Via l'outil CLI
   cd LegacyProject/modernProject
   ./bin/gwb2ged.py dossier_entree fichier_sortie.ged --verbose
   ```
3. Le fichier GEDCOM généré est conforme au standard 5.5.1
4. Compatible avec tous les logiciels de généalogie standards

### Visualisation de l'Arbre Généalogique

1. Naviguer vers **Arbre Généalogique**
2. Sélectionner une personne centrale
3. Options de visualisation:
   - **Type d'arbre**: Ascendants, Descendants, ou Complet
   - **Nombre de générations**: 1 à 10
4. Cliquer sur **"Générer l'Arbre"**
5. L'arbre s'affiche avec navigation interactive

**Note**: La visualisation D3.js est prévue pour une future version.

### Authentification

#### Inscription
1. Cliquer sur l'icône utilisateur en haut à droite
2. Sélectionner **"Inscription"**
3. Remplir le formulaire:
   - Nom d'utilisateur
   - Email
   - Mot de passe (min 8 caractères)
4. Cliquer sur **"S'inscrire"**

#### Connexion
1. Cliquer sur l'icône utilisateur
2. Sélectionner **"Connexion"**
3. Entrer email et mot de passe
4. Cliquer sur **"Se connecter"**
5. Le token JWT est stocké automatiquement

#### Déconnexion
1. Cliquer sur l'icône utilisateur
2. Sélectionner **"Déconnexion"**
3. Le token est supprimé et la session est terminée

##  Sécurité

### Authentification
- Tokens JWT avec expiration automatique
- Refresh tokens pour sessions longues
- Stockage sécurisé dans localStorage

### Protection des Données
- Chiffrement des mots de passe
- HTTPS obligatoire en production
- Validation côté client et serveur
- Protection CSRF

### RGPD
- Export des données personnelles (JSON/CSV)
- Suppression complète du compte
- Gestion des consentements
- Journal d'audit

##  Tests

### Tests Manuels
1. Vérifier la connexion/déconnexion
2. Tester la recherche avec différents critères
3. Vérifier l'affichage de l'arbre
4. Contrôler les statistiques
5. Tester le responsive design

### Tests Automatisés
```javascript
// Exemple avec Cypress
describe('Authentication', () => {
  it('should login successfully', () => {
    cy.visit('http://localhost:3000')
    cy.get('#loginBtn').click()
    cy.get('#loginEmail').type('test@example.com')
    cy.get('#loginPassword').type('Password123!')
    cy.get('form#loginForm').submit()
    cy.contains('Connexion réussie')
  })
})
```

##  Déploiement

### Build de Production

1. **Minifier les assets**
```bash
# CSS
npx cssnano styles.css styles.min.css

# JavaScript
npx terser app.js -o app.min.js -c -m

# HTML
npx html-minifier index.html -o index.min.html \
  --collapse-whitespace --remove-comments
```

2. **Optimiser les images**
```bash
npx imagemin images/* --out-dir=dist/images
```

3. **Configurer le CDN**
- Héberger les fichiers statiques sur un CDN
- Configurer les headers de cache
- Activer la compression gzip

### Variables d'Environnement

Créer un fichier `.env.production`:
```
API_URL=https://api.awkward-legacy.com
ANALYTICS_ID=UA-XXXXXXXXX
SENTRY_DSN=https://xxx@sentry.io/xxx
```

##  Développement

### Structure du Code (app_complete.js)

```javascript
// Classe principale
class APIClient {
  // Méthodes pour Personnes
  async getPersons(skip, limit)
  async getPerson(id)
  async createPerson(personData)
  async updatePerson(id, personData)
  async deletePerson(id)
  async getAncestors(id, generations)
  async getDescendants(id, generations)

  // Méthodes pour Familles
  async getFamilies(skip, limit)
  async getFamily(id)
  async createFamily(familyData)

  // Méthodes de Recherche
  async search(params)
  async searchByName(firstName, lastName)

  // Méthodes pour Statistiques
  async getStatistics()
  async getSurnames(limit)
  async getCenturyDistribution()

  // Méthodes pour Consanguinité
  async calculateKinship(person1Id, person2Id)
  async calculateConsanguinity(personId)
  async getRelationshipName(person1Id, person2Id)

  // Méthodes pour Lignées
  async getConnectedComponents()
  async getComponent(personId)
  async getIsolatedPersons()
  async getComponentStatistics()

  // Méthodes GEDCOM
  async importGedcom(formData)
  async exportGedcom(options)
}

// Fonctions de chargement de pages
function loadSearchPage()         // Page de recherche avancée
function loadConsanguinityPage()  // Interface de calcul de consanguinité
function loadLineagesPage()       // Interface d'analyse de lignées
function loadStatsPage()          // Dashboard de statistiques
function loadTreePage()           // Visualisateur d'arbres
function loadImportPage()         // Interface d'import GEDCOM
function loadExportPage()         // Interface d'export GEDCOM

// Fonctions utilitaires
function navigateToPage(pageName) // Navigation entre pages
function showToast(message, type) // Notifications toast
function formatDate(dateString)   // Formatage de dates
function displaySearchResults(results) // Affichage des résultats
function displayStatistics(stats)      // Affichage des statistiques
```

### Ajouter une Nouvelle Page

1. **Ajouter le conteneur HTML dans `index_new.html`**:
```html
<div id="myNewPage" class="page">
  <!-- Contenu de la page -->
</div>
```

2. **Ajouter l'entrée de navigation**:
```html
<li class="nav-item">
  <a class="nav-link" href="#" data-page="mynew">
    <i class="bi bi-star"></i> Ma Nouvelle Page
  </a>
</li>
```

3. **Créer la fonction de chargement dans `app_complete.js`**:
```javascript
function loadMyNewPage() {
    const page = document.getElementById('myNewPage');

    page.innerHTML = `
        <div class="container">
            <h2>Ma Nouvelle Page</h2>
            <button id="myBtn" class="btn btn-primary">Action</button>
            <div id="myResults"></div>
        </div>
    `;

    // Ajouter les event listeners
    document.getElementById('myBtn').addEventListener('click', async () => {
        const data = await api.getMyData();
        displayMyResults(data);
    });
}
```

4. **Enregistrer le loader de page**:
```javascript
// Dans l'initialisation de l'application
pageLoaders['mynew'] = loadMyNewPage;
```

### API Endpoints Disponibles

#### Personnes
- `GET /api/persons?skip=0&limit=100` - Liste paginée
- `GET /api/persons/{id}` - Détail d'une personne
- `POST /api/persons` - Créer une personne
- `PUT /api/persons/{id}` - Modifier une personne
- `DELETE /api/persons/{id}` - Supprimer une personne
- `GET /api/persons/{id}/ancestors?generations=3` - Ancêtres
- `GET /api/persons/{id}/descendants?generations=3` - Descendants

#### Familles
- `GET /api/families?skip=0&limit=100` - Liste paginée
- `GET /api/families/{id}` - Détail d'une famille
- `POST /api/families` - Créer une famille
- `PUT /api/families/{id}` - Modifier une famille
- `DELETE /api/families/{id}` - Supprimer une famille

#### Recherche
- `POST /api/search` - Recherche multi-critères
  ```json
  {
    "first_name": "Jean",
    "last_name": "Dupont",
    "birth_year": 1850,
    "birth_place": "Paris",
    "sex": "M"
  }
  ```
- `GET /api/search/name?first_name=Jean&last_name=Dupont` - Recherche par nom

#### Statistiques
- `GET /api/statistics` - Statistiques générales
- `GET /api/statistics/surnames?limit=20` - Top noms de famille
- `GET /api/statistics/century-distribution` - Distribution par siècle

#### Consanguinité
- `GET /api/consanguinity/kinship?person1={id1}&person2={id2}` - Coefficient de parenté
- `GET /api/consanguinity/coefficient?person={id}` - Coefficient de consanguinité
- `GET /api/consanguinity/relationship?person1={id1}&person2={id2}` - Nom de la relation

#### Lignées (Connectivité)
- `GET /api/connectivity/components` - Toutes les composantes connexes
- `GET /api/connectivity/component/{person_id}` - Composante d'une personne
- `GET /api/connectivity/isolated` - Personnes isolées
- `GET /api/connectivity/statistics` - Statistiques des composantes

#### GEDCOM
- `POST /api/gedcom/import` - Importer un fichier GEDCOM (multipart/form-data)
- `GET /api/gedcom/export` - Exporter en GEDCOM

#### Authentification
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion
- `POST /api/auth/logout` - Déconnexion
- `GET /api/auth/profile` - Profil utilisateur

##  Débogage et Dépannage

### Console du Navigateur

Ouvrir les outils de développement (F12) et utiliser la console:

```javascript
// Tester une requête API
const api = new APIClient();
api.getPersons().then(console.log).catch(console.error);

// Vérifier les statistiques
api.getStatistics().then(console.log);

// Tester la recherche
api.search({ first_name: 'Jean' }).then(console.log);

// Voir le token JWT (si connecté)
console.log(localStorage.getItem('jwt_token'));
```

### Erreurs Communes et Solutions

#### 1. **CORS Error**
**Symptôme**: `Access to fetch at 'http://localhost:8000/api/...' has been blocked by CORS policy`

**Solution**:
- Vérifier que l'API est bien démarrée sur le port 8000
- Vérifier la configuration CORS dans `api/main.py`:
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],  # Ou spécifier les domaines
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```
- En développement, utiliser un serveur web local (pas directement le fichier)

#### 2. **404 Not Found / API Non Accessible**
**Symptôme**: `GET http://localhost:8000/api/persons 404 (Not Found)`

**Solutions**:
- Vérifier que l'API est lancée: `make run-api` ou `uvicorn api.main:app`
- Vérifier l'URL de base dans `app_complete.js`:
  ```javascript
  const API_BASE_URL = 'http://localhost:8000/api';
  ```
- Tester l'API directement: http://localhost:8000/docs

#### 3. **Charts Non Affichés**
**Symptôme**: Les graphiques ne s'affichent pas sur la page Statistiques

**Solutions**:
- Vérifier que Chart.js est bien chargé (CDN dans `index_new.html`)
- Ouvrir la console pour voir les erreurs JavaScript
- Vérifier que les données sont bien reçues de l'API
- Vérifier que les canvas ont des IDs uniques

#### 4. **Données Non Chargées**
**Symptôme**: Les listes déroulantes ou cartes sont vides

**Solutions**:
- Vérifier qu'il y a des données dans la base (importer un GEDCOM)
- Vérifier les appels API dans l'onglet Network des DevTools
- Vérifier la console JavaScript pour les erreurs
- Vérifier que l'API retourne bien des données: http://localhost:8000/api/persons

#### 5. **Navigation Ne Fonctionne Pas**
**Symptôme**: Les liens de navigation ne changent pas de page

**Solutions**:
- Vérifier que `app_complete.js` est bien chargé
- Vérifier la console pour les erreurs JavaScript
- Vérifier que les attributs `data-page` correspondent aux noms de pages
- Vérifier que les page loaders sont bien définis

#### 6. **Toast Notifications Non Affichées**
**Symptôme**: Aucune notification n'apparaît lors des actions

**Solutions**:
- Vérifier que Bootstrap 5 JS est bien chargé
- Vérifier que la fonction `showToast()` est définie dans `app_complete.js`
- Vérifier que le conteneur toast existe: `<div id="toast-container">`

### Outils de Débogage

#### Network Tab (DevTools)
Utiliser l'onglet Network pour:
- Voir toutes les requêtes API
- Vérifier les codes de statut HTTP
- Inspecter les payloads et réponses
- Mesurer les temps de réponse

#### Console Tab (DevTools)
Utiliser la console pour:
- Voir les erreurs JavaScript
- Tester les fonctions API
- Inspecter les objets retournés
- Logger les étapes d'exécution

#### Elements Tab (DevTools)
Utiliser l'onglet Elements pour:
- Vérifier que les éléments sont bien créés
- Inspecter les classes CSS appliquées
- Modifier temporairement le DOM pour tests
- Voir les event listeners attachés

### Tests de Fonctionnement

#### Checklist de Vérification

- [ ] L'API est démarrée et accessible sur http://localhost:8000
- [ ] La documentation API est visible sur http://localhost:8000/docs
- [ ] Le frontend est servi sur http://localhost:3000
- [ ] La page d'accueil affiche les statistiques
- [ ] La recherche retourne des résultats
- [ ] Les graphiques s'affichent sur la page Statistiques
- [ ] Le calcul de consanguinité fonctionne
- [ ] L'analyse de lignées affiche les composantes
- [ ] Les pages GEDCOM affichent les instructions CLI
- [ ] Aucune erreur dans la console JavaScript
- [ ] Aucune erreur CORS dans la console

##  Démarrage Rapide

Pour démarrer rapidement le frontend complet:

```bash
# Terminal 1: Lancer l'API
cd LegacyProject/modernProject
make run-api

# Terminal 2: Servir le frontend
cd LegacyProject/modernProject/frontend
python3 -m http.server 3000

# Ouvrir dans le navigateur
# http://localhost:3000/index_new.html
```

##  Technologies Utilisées

### Frontend
- **Bootstrap 5.3.0**: Framework CSS responsive
- **Bootstrap Icons 1.11.0**: Icônes vectorielles
- **Chart.js 4.4.0**: Bibliothèque de graphiques interactifs
- **Vanilla JavaScript ES6+**: Pas de frameworks JS lourds
- **CSS3 Custom Properties**: Variables CSS pour le theming

### Backend (API)
- **FastAPI**: Framework Python moderne pour API REST
- **Uvicorn**: Serveur ASGI haute performance
- **Pydantic**: Validation de données avec types Python
- **NetworkX**: Analyse de graphes pour les lignées
- **Python-GEDCOM**: Parsing de fichiers GEDCOM

### Bibliothèques CDN
Toutes les bibliothèques sont chargées via CDN pour faciliter le développement:
```html
<!-- Bootstrap CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">

<!-- Bootstrap Icons -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">

<!-- Bootstrap JS Bundle -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js">

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js">
```

##  Performance et Optimisation

### Chargement des Pages
- **Lazy Loading**: Les pages ne sont chargées que lorsqu'elles sont demandées
- **Single Page Application**: Navigation sans rechargement de page
- **Minimal Initial Load**: Seule la page d'accueil est chargée au départ

### Optimisations API
- **Pagination**: Limite de 100 résultats par défaut pour éviter les grandes réponses
- **Caching Client**: Les listes de personnes peuvent être mises en cache localement
- **Requêtes Asynchrones**: Toutes les requêtes API utilisent async/await

### Recommandations Production
1. **Minifier les fichiers**:
   ```bash
   npx terser app_complete.js -o app_complete.min.js -c -m
   ```

2. **Utiliser un CDN pour les assets statiques**

3. **Activer la compression gzip sur le serveur**

4. **Implémenter un Service Worker pour le cache offline**

5. **Utiliser HTTP/2** pour les connexions multiplexées

##  Ressources

### Documentation Officielle
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MDN Web Docs](https://developer.mozilla.org/)

### Standards et Spécifications
- [GEDCOM 5.5.1 Specification](https://www.gedcom.org/gedcom.html)
- [OpenAPI 3.0 Specification](https://swagger.io/specification/)
- [RGPD / GDPR](https://www.cnil.fr/)
- [OWASP Security Guidelines](https://owasp.org/)

### Ressources Généalogiques
- [GeneWeb Original](https://github.com/geneweb/geneweb)
- [FamilySearch GEDCOM](https://www.familysearch.org/developers/docs/guides/gedcom)

##  Fonctionnalités Futures

### Prévues pour les Prochaines Versions

#### Visualisation Avancée
- [ ] Intégration D3.js pour arbres généalogiques interactifs
- [ ] Vue chronologique (timeline) des événements
- [ ] Carte géographique des lieux de naissance/décès
- [ ] Graphe de relations familiales interactif

#### Analyses Avancées
- [ ] Recherche de cousins communs
- [ ] Analyse de l'ADN simulé
- [ ] Génération de rapports PDF
- [ ] Export en formats multiples (PDF, CSV, Excel)

#### Collaboration
- [ ] Partage de bases généalogiques entre utilisateurs
- [ ] Système de commentaires et annotations
- [ ] Suggestions de liens familiaux
- [ ] Fusion de doublons automatique

#### Interface
- [ ] Mode sombre complet
- [ ] Support multilingue (EN, FR, ES, DE)
- [ ] Application mobile (Progressive Web App)
- [ ] Accessibilité WCAG 2.1 niveau AA

##  Licence

Ce projet fait partie du système AWKWARD LEGACY.

**Licence**: GNU General Public License v2.0 (comme GeneWeb original)

Voir le fichier LICENSE principal pour plus de détails.

##  Contribution

Les contributions sont les bienvenues !

### Comment Contribuer
1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Guidelines
- Suivre les conventions de code existantes
- Ajouter des tests pour les nouvelles fonctionnalités
- Mettre à jour la documentation
- Respecter les standards d'accessibilité

##  Support

Pour toute question ou problème:

- **GitHub Issues**: [LegacyProject Issues](https://github.com/BenPali/LegacyProject/issues)
- **Documentation**: Voir les fichiers `docs/` du projet
- **API Documentation**: http://localhost:8000/docs (quand l'API est lancée)

##  Auteurs

- **Projet Original**: GeneWeb (1995-2008) - Développé en OCaml
- **Modernisation**: AWKWARD LEGACY - Python/FastAPI/Bootstrap

##  Remerciements

- L'équipe GeneWeb pour le système original
- La communauté Python pour FastAPI et les bibliothèques
- Bootstrap et Chart.js pour les outils frontend
- Tous les contributeurs du projet

---

**AWKWARD LEGACY** - *Préserver le passé, construire le futur*

*Interface Web Moderne v1.0 - Janvier 2025*