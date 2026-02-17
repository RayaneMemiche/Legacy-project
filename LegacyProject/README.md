# AWKWARD LEGACY

[![CI](https://github.com/BenPali/LegacyProject/actions/workflows/ci.yml/badge.svg)](https://github.com/BenPali/LegacyProject/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/BenPali/LegacyProject/branch/main/graph/badge.svg)](https://codecov.io/gh/BenPali/LegacyProject)

**Projet de modernisation de GeneWeb** - Système de gestion généalogique professionnel

Modernisation d'un système généalogique legacy (GeneWeb, développé en OCaml 1995-2008) vers une architecture Python moderne, tout en préservant le cœur fonctionnel original.

---

##  Table des Matières

1. [Vue d'ensemble](#-vue-densemble)
2. [Fonctionnalités](#-fonctionnalités)
3. [Installation](#-installation)
4. [Utilisation](#-utilisation)
5. [API REST](#-api-rest)
6. [Outils CLI](#-outils-cli)
7. [Tests](#-tests)
8. [Documentation](#-documentation)
9. [Architecture](#-architecture)
10. [Conformité](#-conformité)

---

##  Vue d'ensemble

### Objectif

Rendre le code legacy GeneWeb conforme aux standards actuels tout en:
-  **PRÉSERVANT** le cœur du code (architecture hybride OCaml-Python)
-  **TESTANT** rigoureusement le système (80%+ coverage)
-  **DÉPLOYANT** de manière sécurisée (Docker, CI/CD)
-  **DOCUMENTANT** complètement (RGPD, déploiement, tests)

### Caractéristiques Clés

- **API REST moderne** (FastAPI) avec documentation OpenAPI
- **Outils CLI** pour import/export GEDCOM
- **Calculs généalogiques avancés** (consanguinité, lignées)
- **Sécurité renforcée** (JWT, RBAC, encryption AES-256-GCM)
- **Tests exhaustifs** (48 fichiers, 80%+ coverage)
- **CI/CD automatisé** (GitHub Actions, Codecov)
- **Containerisation** (Docker multi-stage)

---

##  Fonctionnalités

### Gestion des Données

- **Personnes**: CRUD complet avec relations familiales
- **Familles**: Mariages, enfants, divorces
- **Événements**: Naissances, décès, mariages
- **Lieux**: Gestion des localisations
- **Notes**: Annotations et commentaires

### Fonctionnalités Avancées

####  Calcul de Consanguinité
Calcule les coefficients de parenté et de consanguinité entre individus.

```python
from lib.consanguinity import ConsanguinityCalculator

calc = ConsanguinityCalculator(persons)
kinship = calc.calculate_kinship('person1_id', 'person2_id')
consang = calc.calculate_consanguinity('person_id')
relationship = calc.get_relationship_name('person1_id', 'person2_id')
```

####  Analyse de Connectivité
Identifie les composantes connexes (lignées distinctes) dans la base.

####  Import/Export GEDCOM
Support complet du format GEDCOM 5.5.1 pour interopérabilité.

####  Recherche Avancée
Recherche multi-critères avec filtres.

####  Statistiques
Analytics détaillées sur les données généalogiques.

---

##  Installation

### Prérequis

- **Python 3.9+**
- **OCaml 4.14+** (pour compilation GeneWeb)
- **Docker** (optionnel, recommandé)

### Installation Locale

```bash
# Cloner le repository
git clone https://github.com/BenPali/LegacyProject.git
cd LegacyProject

# Installer les dépendances
make install

# Lancer l'API
make run-api
```

---

##  Utilisation

### Démarrer l'API

```bash
make run-api
```

**Accès:**
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Outils CLI

```bash
# Import GEDCOM
./modernProject/bin/ged2gwb.py input.ged output_dir --verbose

# Export GEDCOM
./modernProject/bin/gwb2ged.py input_dir output.ged --verbose
```

---

##  Tests

```bash
# Tous les tests
make test

# Tests avec coverage
make coverage
```

**Coverage actuel**: 80%+

---

##  Documentation

- `docs/DEPLOYMENT_GUIDE.md` - Guide de déploiement (33 KB)
- `docs/RGPD_COMPLIANCE.md` - Conformité RGPD (52 KB)
- `docs/TEST_POLICY.md` - Stratégie de tests (17 KB)
- `AUDIT_COMPLET.md` - Audit détaillé du projet

---

##  License

GNU General Public License v2.0 (comme GeneWeb original)

---

##  Liens

- **Repository**: https://github.com/BenPali/LegacyProject
- **GeneWeb original**: https://github.com/geneweb/geneweb
- **Documentation**: http://localhost:8000/docs (après démarrage)

---

**AWKWARD LEGACY** - *Préserver le passé, construire le futur*
