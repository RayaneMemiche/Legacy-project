# Script Gamma - Soutenance RNCP Bloc 5 EIP

Cree une presentation PowerPoint professionnelle de 14 slides pour une soutenance de certification RNCP. Le projet s'appelle "AWKWARD LEGACY" et consiste a moderniser le logiciel de genealogie GeneWeb (OCaml) en Python. Candidat : Rayane Memiche. Date : 17 Fevrier 2026. Utilise un design sobre, moderne et professionnel avec des couleurs bleu fonce / blanc / gris. Chaque slide doit etre claire, visuelle et structuree avec des icones, des tableaux ou des schemas quand c'est pertinent.

---

## Slide 1 : Page de titre

**Titre :** AWKWARD LEGACY - Modernisation de GeneWeb
**Sous-titre :** Soutenance RNCP - Bloc 5 : Elaboration de politiques de test et de normes qualite
**Candidat :** Rayane Memiche
**Date :** 17 Fevrier 2026
**Referentiel :** Certificative - Bloc 5 - EIP

Ajoute le contexte en bas : "Projet de modernisation d'un logiciel de genealogie open-source (OCaml vers Python)"

---

## Slide 2 : C25.1 - Documentation de la politique de tests

**Titre :** C25.1 - Documentation complete de la politique de tests
**Critere RNCP :** "Le dossier du candidat presente une documentation complete presentant la politique de test mise en oeuvre en coherence avec les attendus lies au projet"

**Contenu :**
- Document principal : Politique de Tests (805 lignes, v2.0)
- Document complementaire : Methodologie des Tests (435 lignes)
- Inventaire composants/tests : 1431 lignes detaillant chaque module et son test

**Tableau :**
| Document | Lignes | Contenu |
|----------|--------|---------|
| Politique de Tests | 805 | Strategie, protocoles, scenarios, metriques |
| Methodologie des Tests | 435 | Pyramide de tests, repartition, workflow |
| Inventaire Composants | 1431 | Mapping module-par-module (48 modules) |

**Chiffre cle :** 2671 lignes de documentation de politique de tests

---

## Slide 3 : C25.2 - Justification de la strategie de tests

**Titre :** C25.2 - Justification des choix de la politique de tests
**Critere RNCP :** "Le candidat est capable de defendre les choix realises au cours de la definition de sa politique de test"

**Contenu - Pyramide de tests justifiee :**

Schema d'une pyramide de tests avec 5 niveaux :
1. Tests unitaires (41%) - Base large, cout de correction 1x, detection precoce des bugs
2. Tests fonctionnels (18%) - Scenarios utilisateur de bout en bout
3. Tests d'integration (17%) - Verification des interactions entre composants
4. Tests de performance (9%) - Capacite a gerer 100 000+ personnes
5. Tests securite/conformite (15%) - Protection des donnees genealogiques sensibles (RGPD, OWASP)

**Argument economique :** Reference etude NIST - Le cout de correction d'un bug augmente de x1 (tests unitaires) a x100 (production). Notre strategie privilege la detection au plus tot.

**Justification domaine :** Les donnees genealogiques sont des donnees personnelles sensibles (filiation, dates de naissance/deces) necessitant une couverture securite et conformite renforcee.

---

## Slide 4 : C26.1 - Protocole de test adapte

**Titre :** C26.1 - Protocole de test multi-niveaux
**Critere RNCP :** "Le protocole de test fait appel a des composants existants adaptes aux cas d'usage et repondant aux exigences definies dans la politique de test"

**Contenu - 4 niveaux de verification :**

Schema en 4 colonnes :

| Niveau | Declencheur | Outils | Criteres de passage |
|--------|-------------|--------|---------------------|
| Pre-commit | Chaque commit local | 41 hooks pre-commit (Black, Flake8, Bandit, MyPy, isort) | Zero erreur lint, format OK |
| Pre-PR | Push vers branche | Pipeline CI/CD GitHub Actions (5 jobs) | Tous tests passent, couverture >= 75% |
| Pre-release | Merge vers main | Tests complets + audit securite + tests performance | Zero regression, audit OK |
| Production | Deploiement | Monitoring, health checks, logs | Disponibilite > 99%, temps reponse < 500ms |

**Artefacts :** Pipeline CI/CD reel (ci.yml) avec 5 jobs : lint, test (Python 3.10/3.11/3.12), integration, docker, summary

---

## Slide 5 : C26.2 - Justification des choix d'outils

**Titre :** C26.2 - 10 outils selectionnes et justifies
**Critere RNCP :** "Le candidat est en mesure d'argumenter de la pertinence des choix de composants existants"

**Tableau des 10 outils avec justification :**

| Outil | Usage | Justification |
|-------|-------|---------------|
| pytest | Tests unitaires/fonctionnels | Standard Python (>80% PDM), discovery auto, plugins riches |
| pytest-cov | Couverture de code | Integration native pytest, rapports HTML/XML |
| pytest-benchmark | Tests de performance | Mesures statistiques, comparaison entre versions |
| unittest | Tests de base | Bibliotheque standard, zero dependance |
| Locust | Tests de charge | Scenarios en Python (vs XML JMeter), interface web |
| Bandit | Securite statique | Analyse AST Python, detection OWASP automatique |
| Black + Flake8 | Formatage + linting | Formatage deterministe + regles PEP 8 |
| MyPy | Typage statique | Detection d'erreurs de type avant execution |
| pre-commit | Hooks automatiques | 41 hooks, execution avant chaque commit |
| GitHub Actions | CI/CD | Integration native GitHub, matrices multi-version |

---

## Slide 6 : C27.1 - Coherence protocole et code

**Titre :** C27.1 - 1023 tests passants couvrant tout le protocole
**Critere RNCP :** "Le code de la solution contient l'ensemble des tests correspondant au protocole decrit"

**Contenu :**

**Tableau de resultats :**
| Categorie | Tests | Passes | Echoues | Skippes |
|-----------|-------|--------|---------|---------|
| Tests unitaires (40+ fichiers) | ~950 | 950 | 0 | 15 |
| Tests fonctionnels | 35 | 35 | 0 | 0 |
| Tests d'integration | 13 | 12 | 1 | 0 |
| Tests de performance | 5 | 5 | 0 | 3 |
| Tests d'accessibilite | 39 | 39 | 0 | 0 |
| **Total** | **1042** | **1023** | **1** | **18** |

**Chiffres cles en gros :**
- 55 fichiers de tests
- ~14 000 lignes de code de test
- Execution en 6.78 secondes
- 1 seul echec : test de concurrence SQLite (passe en PostgreSQL de production)

---

## Slide 7 : C27.2 - Couverture exhaustive des tests

**Titre :** C27.2 - 81% de couverture de code
**Critere RNCP :** "L'implementation des tests couvre de maniere exhaustive les scenarios qu'ils decrivent"

**Contenu :**

Graphique en barres horizontales montrant la couverture par module :
- gwdef.py : 100%
- dbdisk.py : 100%
- dutil.py : 100%
- output.py : 100%
- buff.py : 100%
- collection.py : 100%
- logs.py : 99%
- adef.py : 98%
- pqueue.py : 98%
- name.py : 96%
- my_gzip.py : 95%
- mutil.py : 94%
- futil.py : 93%
- iovalue.py : 88%
- gwcalendar.py : 87%
- avl.py : 87%
- outbase.py : 85%
- secure.py : 85%

**Progression documentee :** 10 rapports de couverture (1er octobre au 25 octobre 2025) montrant la progression continue du projet.

**Couverture globale : 81% sur 44 modules (5821 lignes de code)**

---

## Slide 8 : C28.1 - Strategie d'assurance qualite

**Titre :** C28.1 - Strategie QA multi-dimensionnelle
**Critere RNCP :** "Le dossier contient une reference documentaire decrivant une strategie d'assurance qualite coherente"

**Contenu :**

Document de strategie QA (372 lignes, 10 sections) base sur 5 normes :

Schema en etoile ou en cercle avec 5 branches :
1. **ISO 25010** - 8 caracteristiques qualite logicielle
2. **OWASP Top 10** - Securite applicative (95% de conformite)
3. **WCAG 2.1 AA** - Accessibilite numerique (39 tests)
4. **RGPD** - Protection des donnees personnelles (79% conformite)
5. **PEP 8/257** - Standards de code Python

**3 principes fondateurs :**
- Prevention > Detection (reference NIST : reduction cout x10)
- Automatisation maximale (95% des verifications automatisees)
- Couverture multi-dimensionnelle (7 dimensions qualite)

**KPIs definis :** Couverture > 80%, tests passants > 99%, accessibilite > 75% AA, temps de reponse < 500ms

---

## Slide 9 : C28.2 - Accessibilite numerique

**Titre :** C28.2 - Conformite WCAG 2.1 AA : 39/39 tests
**Critere RNCP :** "La strategie d'assurance qualite integre les normes d'accessibilite numerique pour les personnes en situation de handicap"

**Contenu :**

**Avant / Apres :**
| Critere | Avant (Oct 2025) | Apres (Fev 2026) |
|---------|-------------------|-------------------|
| Skip links | Absent | Implementes |
| Structure HTML5 semantique | Absent | <header>, <main>, <footer>, <nav> |
| Attributs ARIA | Partiels | Complets (aria-label, aria-expanded, aria-live) |
| Support prefers-reduced-motion | Absent | Implemente |
| Support prefers-contrast: high | Absent | Implemente |
| Focus visible clavier | Absent | :focus-visible implemente |
| Icones decoratives aria-hidden | Absent | Toutes les icones decoratives masquees |
| Role search sur formulaire | Absent | role="search" + label cache |
| Score global | 45-50% | 100% sur criteres testes |

**9 corrections appliquees** documentees avec preuves dans le code (index_new.html + styles.css)
**39 tests d'accessibilite** repartis en 9 classes de test couvrant les 4 principes WCAG (Perceptible, Operable, Comprehensible, Robuste)

---

## Slide 10 : C29.1 - Justification de la strategie QA

**Titre :** C29.1 - Pertinence de la strategie d'assurance qualite
**Critere RNCP :** "Le candidat est capable d'exposer la pertinence de la strategie d'assurance qualite qu'il a elabore"

**Contenu :**

**3 arguments de pertinence :**

1. **Argument economique**
   - Etude NIST : un bug detecte en production coute 100x plus cher qu'en test unitaire
   - Notre strategie : 95% de detection automatisee avant merge
   - Resultat : 0 bug critique en production

2. **Argument domaine**
   - Donnees genealogiques = donnees personnelles sensibles (filiation, dates, lieux)
   - Obligation RGPD : protection renforcee des donnees de sante/filiation
   - Notre reponse : tests de conformite RGPD + securite OWASP integres au pipeline

3. **Argument technique**
   - Migration OCaml vers Python = risque de regression majeur
   - Notre reponse : couverture de test a 81% + tests fonctionnels end-to-end
   - Validation : 1023 tests passants sur 1042 collectes

---

## Slide 11 : C29.2 - Preuves du processus QA

**Titre :** C29.2 - Preuves tangibles du processus qualite
**Critere RNCP :** "Le dossier contient les preuves prouvant les actions mettant en oeuvre la strategie decrite"

**Contenu :**

**5 categories de preuves :**

| Type de preuve | Artefact | Detail |
|----------------|----------|--------|
| Resultats de tests | Execution pytest | 1023 passes, 1 echec, 18 skippes |
| Rapports de couverture | 10 rapports | Progression Oct 2025 (baseline -> 81%) |
| Audit complet | Document 964 lignes | Score global : 85/100 |
| Pipeline CI/CD | ci.yml (GitHub Actions) | 5 jobs, 3 versions Python, Docker |
| Pre-commit hooks | .pre-commit-config.yaml | 41 hooks (format, lint, securite, types) |

**Schema du pipeline CI/CD :**
```
Push -> Lint (Black, Flake8, Bandit) -> Tests (Python 3.10/3.11/3.12 + coverage) -> Integration (Redis) -> Docker Build -> Summary Report
```

**Chiffre cle :** Score d'audit global du projet : **85/100**

---

## Slide 12 : C29.3 - Corrections issues du processus QA

**Titre :** C29.3 - 5 corrections tracees par le processus qualite
**Critere RNCP :** "Le candidat est capable de montrer que les correctifs exiges par l'application de la strategie d'assurance qualite ont ete mis en oeuvre"

**Contenu :**

**Timeline des 5 corrections :**

1. **Oct 2025 - Erreurs d'import** (commit c1a6255)
   - Detecte par : CI/CD (GitHub Actions)
   - Impact : Bloquant - Pipeline en echec
   - Correction : Ajout imports manquants (Optional de typing)

2. **Oct 2025 - Tests de consanguinite** (commit 2510abe)
   - Detecte par : Suite pytest
   - Impact : Tests bloquants
   - Correction : Skip avec documentation + planification implementation Q2 2026

3. **Oct 2025 - Positionnement CI/CD** (commit 96b066b)
   - Detecte par : Revue de code
   - Impact : Pipeline non fonctionnel
   - Correction : Deplacement workflow vers .github/workflows/

4. **Oct 2025 - Probleme submodules Git** (commit 8ff8d43)
   - Detecte par : Tests d'integration
   - Impact : Bloquant - Build impossible
   - Correction : Conversion submodules en repertoires reguliers

5. **Fev 2026 - Accessibilite frontend** (9 problemes WCAG)
   - Detecte par : Audit d'accessibilite
   - Impact : Score initial 45-50%
   - Correction : 9 corrections (skip links, ARIA, semantique HTML, contrast, motion)
   - Resultat : 39/39 tests d'accessibilite passants

**Boucle qualite demontree :** Detection -> Classification -> Correction -> Verification

---

## Slide 13 : Synthese - Matrice de conformite

**Titre :** Synthese : 11/11 criteres CONFORMES
**Sous-titre :** Matrice de conformite Bloc 5

**Grand tableau de synthese :**

| Critere | Description | Statut | Preuve principale |
|---------|-------------|--------|-------------------|
| C25.1 | Documentation politique de tests | CONFORME | 2671 lignes de documentation |
| C25.2 | Justification strategie | CONFORME | Pyramide justifiee + ref. NIST |
| C26.1 | Protocole adapte | CONFORME | 4 niveaux + 41 hooks + CI/CD |
| C26.2 | Choix d'outils | CONFORME | 10 outils justifies |
| C27.1 | Coherence protocole/code | CONFORME | 1023/1042 tests passants |
| C27.2 | Couverture des tests | CONFORME | 81% couverture, 10 rapports |
| C28.1 | Strategie QA | CONFORME | 5 normes, 10 sections |
| C28.2 | Accessibilite | CONFORME | 39/39 tests WCAG 2.1 AA |
| C29.1 | Justification QA | CONFORME | 3 arguments (eco, domaine, tech) |
| C29.2 | Preuves du processus | CONFORME | 5 types d'artefacts |
| C29.3 | Corrections appliquees | CONFORME | 5 corrections tracees (git) |

Mettre tous les statuts en vert avec une coche.

---

## Slide 14 : Resultats cles et conclusion

**Titre :** AWKWARD LEGACY - Resultats cles

**Chiffres en grand, visuellement impactants :**

- **1023** tests passants
- **81%** de couverture de code
- **39/39** tests d'accessibilite (100%)
- **55** fichiers de tests
- **~14 000** lignes de code de test
- **41** hooks pre-commit
- **85/100** score d'audit global
- **5** jobs CI/CD
- **11/11** criteres RNCP conformes

**Message de conclusion :**
"AWKWARD LEGACY demontre une demarche qualite complete et documentee, de la definition de la politique de tests a sa mise en oeuvre effective, en passant par l'accessibilite et la conformite aux normes. Chaque critere du Bloc 5 est couvert par des preuves tangibles et verifiables."

**Merci - Questions ?**
