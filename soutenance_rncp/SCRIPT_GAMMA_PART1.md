# Script Gamma - Soutenance RNCP Bloc 5 EIP (Partie 1 : Slides 1-10)

Cree une presentation PowerPoint professionnelle de 10 slides pour une soutenance de certification RNCP. Le projet s'appelle "AWKWARD LEGACY" et consiste a moderniser le logiciel de genealogie GeneWeb (OCaml) en Python. Candidat : Rayane Memiche. Date : 17 Fevrier 2026. Utilise un design sobre, moderne et professionnel avec des couleurs bleu fonce / blanc / gris. Chaque slide doit etre claire, visuelle et structuree avec des icones, des tableaux ou des schemas quand c'est pertinent.

---

## Slide 1 : Page de titre

**Titre :** AWKWARD LEGACY - Modernisation de GeneWeb
**Sous-titre :** Soutenance RNCP - Bloc 5 : Elaboration de politiques de test et de normes qualite
**Candidat :** Rayane Memiche
**Date :** 17 Fevrier 2026
**Referentiel :** Certificative - Bloc 5 - EIP

Ajoute le contexte en bas : "Projet de modernisation d'un logiciel de genealogie open-source (OCaml vers Python)"

---

## Slide 2 : Documentation de la politique de tests

**Titre :** Documentation complete de la politique de tests
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

## Slide 3 : Justification de la strategie de tests

**Titre :** Justification des choix de la politique de tests
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

## Slide 4 : Protocole de test adapte

**Titre :** Protocole de test multi-niveaux
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

## Slide 5 : Justification des choix d'outils

**Titre :** 10 outils selectionnes et justifies
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

## Slide 6 : Coherence protocole et code

**Titre :** 1023 tests passants couvrant tout le protocole
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

## Slide 7 : Couverture exhaustive des tests

**Titre :** 81% de couverture de code
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

## Slide 8 : Strategie d'assurance qualite

**Titre :** Strategie QA multi-dimensionnelle
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

## Slide 9 : Accessibilite numerique

**Titre :** Conformite WCAG 2.1 AA : 39/39 tests
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

## Slide 10 : Justification de la strategie QA

**Titre :** Pertinence de la strategie d'assurance qualite
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
