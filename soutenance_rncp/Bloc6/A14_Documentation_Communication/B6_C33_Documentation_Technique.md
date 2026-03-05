# Documentation Technique - AWKWARD LEGACY

**Version:** 1.0
**Date:** Mars 2026
**Projet:** AWKWARD LEGACY - Modernisation de GeneWeb
**Referentiel RNCP:** Bloc 6 - C33.1, C33.2, C33.3

---

## Table des Matieres

1. [Ensemble documentaire du projet](#1-ensemble-documentaire-du-projet)
2. [Choix technologiques et justifications](#2-choix-technologiques-et-justifications)
3. [Architecture et implementation](#3-architecture-et-implementation)
4. [Perennite de la solution](#4-perennite-de-la-solution)
5. [Accessibilite de la documentation](#5-accessibilite-de-la-documentation)

---

## 1. Ensemble documentaire du projet

### 1.1 Carte des documents

Le projet AWKWARD LEGACY produit **20+ documents** couvrant tous les aspects du projet.

#### Documentation technique (LegacyProject/docs/)

| Document | Lignes | Contenu |
|----------|--------|---------|
| `DEPLOYMENT_GUIDE.md` | 1547 | Guide complet de deploiement : prerequis, installation, Docker, Nginx, SSL, monitoring, backup, rollback |
| `Components.md` | 300+ | Catalogue complet des composants : 132 fichiers Python, 48 modules lib/, 60+ fichiers de tests, metriques |
| `QA_STRATEGY.md` | 372 | Strategie d'assurance qualite : normes, KPIs, pyramide de tests, processus |
| `TEST_POLICY.md` | 400+ | Politique de tests : methodologie, pyramide, protocoles, scenarios |
| `RGPD_COMPLIANCE.md` | 200+ | Documentation conformite RGPD : droits utilisateurs, chiffrement, consentement |
| `Disability_Standards.md` | 150+ | Standards d'accessibilite : WCAG 2.1 AA, RGAA 4.1, corrections appliquees |
| `Solution_Presentation.md` | 268 | Presentation de la solution : contexte, architecture, resultats |

#### Documentation operationnelle (MD/)

| Document | Contenu |
|----------|---------|
| `GUIDE_LANCEMENT.md` | Guide de demarrage complet |
| `QUICK_START.md` | Demarrage rapide (5 minutes) |
| `COMMANDES.md` | Reference des commandes courantes |
| `DOCKER_CI_GUIDE.md` | Guide Docker et CI/CD |
| `SECURITY.md` | Guide de securite |
| `METHODOLOGIE_TESTS.md` | Methodologie de tests |

#### Documentation d'avancement (avancement/)

| Document | Contenu |
|----------|---------|
| `JOUR1_RAPPORT.md` | Rapport journalier J1 |
| `jour2_rapport.md` a `jour6_rapport.md` | Rapports journaliers J2-J6 |
| `AUDIT_COMPLET.md` | Audit complet du projet (964 lignes, score 85/100) |
| `COMPARAISON_FONCTIONNELLE.md` | Comparaison OCaml vs Python |
| `RECAP_PROJET.md` | Recapitulatif projet |
| `coverage_reports/` | 10 rapports de couverture de tests (Oct 2025) |

#### Documentation soutenance (soutenance_rncp/)

| Document | Contenu |
|----------|---------|
| Bloc5 (A11, A12, Preuves) | 15+ documents pour Bloc 5 |
| Bloc6 (A13, A14) | Documents Bloc 6 (ce dossier) |
| `GUIDE_ORAL_ET_SLIDES.md` | Guide oral de soutenance |
| `SCRIPT_GAMMA_PPT.md` | Script PowerPoint 14 slides |
| `INDEX.md` | Index de tous les documents |

### 1.2 Statistiques globales de documentation

| Metrique | Valeur |
|----------|--------|
| Fichiers de documentation | 20+ fichiers .md |
| Mots total | ~50,000 mots |
| Langues | Francais (principal) |
| Formats | Markdown (compatible GitHub, renderable) |
| Documentation code | Docstrings Python (PEP 257) sur tous les modules |
| README | Fichier README.md a chaque niveau |

---

## 2. Choix technologiques et justifications

### 2.1 Backend : Python 3.12

**Choix :** Python 3.12 (au lieu de continuer en OCaml)

**Justification :**
- OCaml original date de 1995-2008, peu de developpeurs disponibles sur le marche
- Python : 2eme langage le plus utilise mondialement (TIOBE 2024), ecosysteme riche
- Python 3.12 : derniere version stable, support jusqu'en 2028
- Librairies de genealogie disponibles en Python (dateutil, etc.)
- Maintenabilite : une equipe Python peut reprendre le projet facilement

**Fichiers :** `LegacyProject/modernProject/lib/*.py` (48 modules), `requirements.txt`

### 2.2 Framework API : Flask + FastAPI

**Choix :** Flask pour le serveur de developpement, FastAPI reference pour les APIs

**Justification :**
- Flask : leger, simple, idéal pour un projet de taille moyenne
- FastAPI : validation automatique avec Pydantic, documentation OpenAPI auto-generee
- Les deux sont en Python pur, pas de couplage fort
- Facilement remplacable si les besoins evoluent (le code metier est dans `lib/`)

### 2.3 Conteneurisation : Docker

**Choix :** Docker + Docker Compose

**Justification :**
- Portabilite : meme comportement partout
- Isolation : l'application ne depend pas de l'environnement systeme
- Versionnage des images (tag SHA, semver)
- Standard industriel : toutes les equipes DevOps maitrisent Docker
- Image multi-stage pour minimiser la taille et la surface d'attaque

**Fichier :** `LegacyProject/modernProject/Dockerfile`

### 2.4 CI/CD : GitHub Actions

**Choix :** GitHub Actions (au lieu de Jenkins, GitLab CI, CircleCI)

**Justification :**
- Integre nativement a GitHub (meme plateforme que le code)
- Gratuit pour les repos publics et plans GitHub standard
- Matrix builds : teste Python 3.10/3.11/3.12 en parallele sans configuration supplementaire
- Marketplace de 10,000+ actions pre-construites
- Secrets management integre

**Fichier :** `LegacyProject/modernProject/.github/workflows/ci.yml`

### 2.5 Tests : pytest + ecosystem

**Choix :** pytest comme framework principal

**Justification :**
- >80% de parts de marche dans l'ecosysteme Python
- Discovery automatique, syntaxe concise
- Plugins riches : pytest-cov (couverture), pytest-benchmark (performance)
- Compatible unittest (retro-compatibilite)
- Integration CI/CD via JUnit XML output

### 2.6 Frontend : HTML5 / CSS3 / JavaScript Vanilla + Bootstrap

**Choix :** Pas de framework JS lourd (pas de React, Vue, Angular)

**Justification :**
- Genealogie = donnees relationnelles simples, pas besoin de SPA complexe
- Maintenance facilitee : tout developpeur comprend HTML/CSS/JS de base
- Bootstrap 5.3 : composants UI accessibles par defaut
- Pas de build step (webpack, etc.) = deploiement plus simple
- Performance : moins de JS a charger pour l'utilisateur

### 2.7 Securite : Bandit + OWASP + AES-256

**Choix :** Analyse statique Bandit + chiffrement AES-256-GCM + bcrypt

**Justification :**
- Bandit : specifique Python, detects les failles sans execution du code
- AES-256-GCM : standard NIST recommande pour le chiffrement authentifie
- bcrypt : algorithme de hachage adaptatif (cout augmente avec le temps), recommande par OWASP
- OWASP Top 10 : referentiel industriel pour la securite web

---

## 3. Architecture et implementation

### 3.1 Architecture en couches

```
+-----------------------------+
|      Interface Frontend     |  HTML5 + CSS3 + JS Vanilla + Bootstrap 5
+-----------------------------+
|         API REST            |  Flask / FastAPI (Python 3.12)
+-----------------------------+
|      Modules Metier         |  lib/ (48 modules Python)
+-----------------------------+
|     Securite Transverse     |  lib/security.py (JWT, AES-256, bcrypt)
+-----------------------------+
|    Base de donnees          |  Fichiers .gwb (format GeneWeb natif)
+-----------------------------+
```

### 3.2 Structure du code

```
LegacyProject/modernProject/
├── lib/                    # 48 modules metier Python
│   ├── database.py         # Acces aux donnees GeneWeb
│   ├── security.py         # Securite (JWT, crypto, OWASP)
│   ├── wserver.py          # Serveur Flask
│   └── ...                 # 45 autres modules
├── api/                    # 20 fichiers d'API REST
├── frontend/               # Interface web (HTML/CSS/JS)
├── tests/                  # 60+ fichiers de tests (13,000+ lignes)
│   ├── test_*.py           # Tests unitaires (1023 tests)
│   ├── functional/         # Tests fonctionnels
│   ├── integration/        # Tests d'integration
│   ├── performance/        # Tests de charge (Locust)
│   ├── security/           # Scanner OWASP
│   ├── compliance/         # Validateur RGPD
│   └── accessibility/      # Tests WCAG 2.1
├── Dockerfile              # Image multi-stage
├── docker-entrypoint.sh    # Script d'entree Docker
└── requirements.txt        # Dependances Python
```

**Statistiques :**
- 132+ fichiers Python
- ~28,314 lignes de code Python
- 286 fichiers frontend
- 60+ fichiers de tests

**Fichier :** `LegacyProject/docs/Components.md` (catalogue complet)

---

## 4. Perennite de la solution

### 4.1 Arguments de perennite

**1. Choix de technologies stables et maintenues**

| Technologie | Fin de support | Raison du choix |
|-------------|---------------|-----------------|
| Python 3.12 | Octobre 2028 | LTS, ecosysteme stable |
| Docker CE | Sans limite | Projet open-source actif |
| GitHub Actions | Sans limite | Integre a GitHub |
| Bootstrap 5.3 | Maintenu | Majorite des sites web |
| Nginx | Sans limite | Projet open-source actif |

**2. Architecture modulaire**
- Les 48 modules `lib/` sont independants les uns des autres
- Chaque module peut etre mis a jour ou remplace sans impacter les autres
- Separation stricte entre code metier (`lib/`) et infrastructure (`api/`, Dockerfile)

**3. Documentation exhaustive**
- Guide de deploiement detaille (1547 lignes) : une equipe inconnue peut reprendre en autonomie
- Rapports d'avancement journaliers : historique des decisions
- Docstrings Python (PEP 257) : le code se documente lui-meme
- CHANGELOG genere automatiquement (git-cliff) : historique des versions

**4. Tests comme filet de securite**
- 80%+ de couverture de code : les regressions sont detectees immediatement
- Tests d'integration : les interactions entre modules sont verifiees
- Pipeline CI/CD : chaque modification est validee automatiquement

**5. Semantic Versioning**
- Versionnage MAJOR.MINOR.PATCH : les changements incompatibles sont identifies
- Tags Git pour chaque release : retour a toute version passee possible
- Images Docker taguees : rollback en 30 secondes

**6. RGPD et conformite legale**
- La conformite est documentee et testee automatiquement (`rgpd_validator.py`)
- Pas de dette technique legale : les obligations sont integrees dans le code

### 4.2 Reprise par une autre equipe

Une equipe qui reprend le projet peut :

1. Lire `MD/QUICK_START.md` pour demarrer en 5 minutes
2. Lire `LegacyProject/docs/Components.md` pour comprendre l'architecture
3. Lire `LegacyProject/docs/DEPLOYMENT_GUIDE.md` pour deployer en production
4. Lancer le CI/CD (`git push`) : les tests valident que tout fonctionne
5. Consulter les rapports d'avancement (`avancement/`) pour l'historique

---

## 5. Accessibilite de la documentation

### 5.1 Recommandations WCAG pour la documentation

Tous les fichiers de documentation du projet respectent les recommandations WCAG 2.1 pour l'accessibilite des documents :

**Structure semantique :**
- Titres hierarchiques (`# H1`, `## H2`, `### H3`) : structure de navigation claire
- Tables avec en-tetes : lisibles par les lecteurs d'ecran
- Listes ordonnees/non-ordonnees : structure logique
- Code en blocs : distingue du texte narratif

**Lisibilite :**
- Texte en francais clair et structure (pas de jargon non explique)
- Abreviations explicitees a la premiere utilisation
- Tableaux de synthese pour les informations comparatives
- Table des matieres au debut de chaque document long

**Format Markdown :**
- Compatible avec tous les lecteurs d'ecran (rendu HTML standard)
- Visualisable sur GitHub sans outil supplementaire
- Convertible en HTML, PDF pour accessibilite elargie

### 5.2 Conformite des documents

| Document | Structure OK | Tables | Code blocs | TDM |
|----------|-------------|--------|------------|-----|
| `DEPLOYMENT_GUIDE.md` | Oui | Oui | Oui | Oui |
| `Components.md` | Oui | Oui | Oui | Oui |
| `QA_STRATEGY.md` | Oui | Oui | Oui | Oui |
| `B6_C30_Technologies_Hebergement.md` | Oui | Oui | Oui | Oui |
| `B6_C31_Procedure_Deploiement.md` | Oui | Oui | Oui | Oui |
| `B6_C32_Securite_Infrastructure.md` | Oui | Oui | Oui | Oui |

### 5.3 Absence d'emojis

Tous les fichiers .md du projet ont ete nettoyes de leurs emojis pour :
- Compatibilite avec les lecteurs d'ecran (les emojis sont annonces verbalement par les AT)
- Presentation professionnelle
- Conformite avec les recommandations WCAG sur les elements non textuels

**Preuve :** Commit `61de763` - "docs: Remove emojis from all .md files and reorganize soutenance structure" (68 fichiers modifies)

---

**Derniere revision :** Mars 2026
