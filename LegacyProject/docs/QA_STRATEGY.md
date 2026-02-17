# Stratégie d'Assurance Qualité - AWKWARD LEGACY

**Version:** 2.0
**Date:** 17 Février 2026
**Projet:** AWKWARD LEGACY - Modernisation de GeneWeb
**Responsable QA:** Équipe Legacy
**Référentiel RNCP:** Bloc 5 - C28.1, C28.2, C29.1

---

## 1. Introduction et Objectifs

### 1.1 Contexte

AWKWARD LEGACY est un projet de modernisation du logiciel de généalogie GeneWeb (développé en OCaml entre 1995 et 2008) vers une architecture Python moderne. Ce projet critique manipule des données personnelles sensibles (arbres généalogiques, filiations, données biographiques) et doit garantir un niveau de qualité élevé en termes de fiabilité, sécurité, performance et accessibilité.

### 1.2 Objectifs de la stratégie QA

| Objectif | Indicateur | Cible |
|----------|-----------|-------|
| **Fiabilité fonctionnelle** | Couverture de tests | ≥ 80% |
| **Sécurité des données** | Vulnérabilités critiques | 0 |
| **Performance** | Temps de réponse API | < 500ms (p95) |
| **Accessibilité** | Conformité WCAG 2.1 AA | ≥ 75% |
| **Maintenabilité** | Score qualité code | A (pylint ≥ 8/10) |
| **Conformité RGPD** | Score conformité | ≥ 80% |

### 1.3 Justification stratégique

La stratégie QA est conçue selon 3 principes directeurs :

1. **Prévention plutôt que détection** : Les outils de linting, pre-commit hooks et revues de code empêchent les défauts d'entrer dans le code, ce qui est 10x moins coûteux que de les corriger après livraison (source : NIST Systems Sciences, "The Economic Impacts of Inadequate Infrastructure for Software Testing").

2. **Automatisation maximale** : 95% des vérifications qualité sont automatisées via CI/CD (GitHub Actions), pre-commit hooks (30+ hooks), et tests automatisés. Cela garantit la reproductibilité et élimine l'erreur humaine.

3. **Couverture multi-dimensionnelle** : La qualité ne se résume pas aux tests fonctionnels. Notre stratégie couvre 7 dimensions : fonctionnel, performance, sécurité, accessibilité, conformité RGPD, maintenabilité du code, et documentation.

---

## 2. Normes et Référentiels Appliqués

### 2.1 Normes techniques

| Norme | Application | Justification |
|-------|------------|---------------|
| **ISO 25010** | Modèle de qualité logicielle | Cadre structurant pour les 8 caractéristiques de qualité |
| **OWASP Top 10 (2021)** | Sécurité applicative | Standard industriel pour la sécurité web |
| **WCAG 2.1 AA** | Accessibilité numérique | Norme obligatoire pour l'accessibilité des personnes en situation de handicap |
| **RGPD** | Protection des données | Réglementation européenne obligatoire |
| **PEP 8 / PEP 257** | Style de code Python | Standards de la communauté Python |
| **Semantic Versioning** | Versionnage | Convention de nommage des versions |

### 2.2 Normes d'accessibilité (C28.2)

L'accessibilité numérique est **intégrée comme exigence de premier plan** dans notre stratégie QA, conformément aux obligations légales (loi n° 2005-102 du 11 février 2005, décret n° 2019-768, RGAA 4.1) et au référentiel WCAG 2.1 niveau AA.

#### Principes WCAG intégrés

| Principe | Description | Mise en œuvre |
|----------|------------|---------------|
| **Perceptible** | L'information doit être présentable de manière perceptible | Alt text, contraste ≥ 4.5:1, structure sémantique |
| **Opérable** | Les composants UI doivent être opérables | Navigation clavier complète, skip links, pas de piège clavier |
| **Compréhensible** | L'information et l'utilisation de l'UI doivent être compréhensibles | Lang="fr", labels, messages d'erreur explicites |
| **Robuste** | Le contenu doit être interprétable par les technologies d'assistance | ARIA complet, HTML5 sémantique, validation W3C |

#### Processus d'assurance accessibilité

1. **Revue de conception** : Chaque maquette est vérifiée pour les contrastes, la taille des cibles tactiles (≥ 44x44px), et la lisibilité
2. **Développement** : Checklist accessibilité obligatoire avant chaque PR (ARIA, sémantique, clavier)
3. **Tests automatisés** : Tests d'accessibilité dans la suite de tests (`tests/accessibility/`)
4. **Audit périodique** : Audit WCAG trimestriel documenté dans `Disability_Standards.md`

#### Critères d'acceptation accessibilité

- Tous les éléments interactifs sont utilisables au clavier
- Tous les formulaires ont des labels associés (`for`/`id`)
- Toutes les images/icônes ont un texte alternatif
- Les contrastes respectent le ratio 4.5:1 (texte normal) et 3:1 (grand texte)
- La navigation par skip links est disponible
- La structure HTML utilise les landmarks sémantiques (`main`, `header`, `footer`, `nav`)
- Les attributs ARIA sont utilisés pour les composants dynamiques
- `prefers-reduced-motion` est respecté pour les utilisateurs sensibles aux animations
- `prefers-contrast: high` est supporté pour les utilisateurs malvoyants

---

## 3. Processus Qualité

### 3.1 Cycle de vie du développement qualité

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Conception  │ →  │ Développement│ →  │   Revue &    │ →  │   Release    │
│              │    │              │    │   Tests      │    │              │
│ - Specs      │    │ - Code       │    │ - Code review│    │ - Tag version│
│ - Checklist  │    │ - Tests unit │    │ - CI/CD pass │    │ - CHANGELOG  │
│   accessib.  │    │ - Linting    │    │ - Coverage OK│    │ - Déploiement│
│ - Critères   │    │ - Pre-commit │    │ - Sécurité OK│    │ - Smoke tests│
│   accept.    │    │   hooks      │    │ - Accessib.OK│    │ - Monitoring │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

### 3.2 Gates de qualité (Quality Gates)

Chaque étape du développement est protégée par des portes qualité automatisées :

#### Gate 1 : Pre-commit (local)
- **Outil** : pre-commit framework (30+ hooks)
- **Vérifications** :
  - Formatage : Black, isort, Prettier
  - Linting : Flake8, Pylint (score ≥ 8/10)
  - Typage : MyPy
  - Sécurité : Bandit (failles de sécurité), detect-secrets
  - Docker : Hadolint
  - Markdown : Markdownlint
  - Commits : Commitizen (conventional commits)

#### Gate 2 : CI/CD (GitHub Actions)
- **Déclencheur** : Push et Pull Request
- **Jobs** :
  1. **Lint** : Black, Flake8, Bandit
  2. **Test** : pytest sur Python 3.10, 3.11, 3.12 avec couverture
  3. **Integration** : Tests d'intégration avec Redis
  4. **Docker** : Build de l'image conteneur
  5. **Summary** : Rapport de pipeline

#### Gate 3 : Pre-release
- Tests de performance (Locust : 100 utilisateurs simultanés)
- Scan de sécurité OWASP Top 10
- Validation RGPD
- Audit d'accessibilité WCAG

### 3.3 Revues de code

Chaque modification de code fait l'objet d'une revue selon les critères suivants :

| Critère | Vérification | Outil |
|---------|-------------|-------|
| Fonctionnel | Les tests couvrent le changement | pytest + pytest-cov |
| Style | Conforme PEP 8 | Black, Flake8 |
| Sécurité | Pas de faille introduite | Bandit, revue manuelle |
| Performance | Pas de régression | pytest-benchmark |
| Accessibilité | ARIA, sémantique, clavier | Checklist + tests auto |
| Documentation | Docstrings, CHANGELOG | Revue manuelle |

---

## 4. Pyramide de Tests

### 4.1 Architecture des tests

```
                    ╱╲
                   ╱  ╲
                  ╱ E2E╲         5% - Tests end-to-end
                 ╱──────╲
                ╱ Perf.  ╲       9% - Tests de performance/charge
               ╱──────────╲
              ╱ Intégration╲     17% - Tests inter-modules
             ╱──────────────╲
            ╱  Fonctionnels  ╲   18% - Tests de scénarios utilisateur
           ╱──────────────────╲
          ╱   Tests Unitaires  ╲  41% - Tests de modules individuels
         ╱──────────────────────╲
        ╱  Sécurité + Conformité ╲ 10% - OWASP, RGPD, Accessibilité
       ╱────────────────────────────╲
```

### 4.2 Répartition des tests

| Catégorie | Fichiers | Objectif | Framework |
|-----------|----------|----------|-----------|
| **Unitaires** | 40+ fichiers dans `tests/` | Valider chaque module isolément | pytest, unittest |
| **Fonctionnels** | 6 fichiers dans `tests/functional/` | Valider les workflows utilisateur | pytest |
| **Intégration** | 2 fichiers dans `tests/integration/` | Valider les interactions inter-modules | unittest, threading |
| **Performance** | 2 fichiers dans `tests/performance/` | Valider charge et temps de réponse | Locust, pytest-benchmark |
| **Sécurité** | `tests/security/security_scanner.py` | Scanner OWASP Top 10 | Custom Python + requests |
| **Conformité** | `tests/compliance/rgpd_validator.py` | Valider conformité RGPD | Custom Python |
| **Accessibilité** | `tests/accessibility/` | Valider conformité WCAG 2.1 AA | Custom Python |

### 4.3 Justification des choix de frameworks (C26.2)

| Outil | Justification du choix |
|-------|----------------------|
| **pytest** | Framework de test Python le plus utilisé (>80% de parts de marché dans l'écosystème Python). Syntaxe concise, discovery automatique, plugins riches (cov, benchmark), compatibilité unittest. |
| **unittest** | Bibliothèque standard Python, utilisée pour les tests d'intégration nécessitant setUp/tearDown explicites et l'isolation par TestCase. Pas de dépendance externe. |
| **Locust** | Framework de load testing en Python, permettant de définir des comportements utilisateur réalistes en code Python (plutôt que XML/YAML). Compatible avec notre stack technique. |
| **pytest-cov** | Plugin pytest pour la mesure de couverture (basé sur coverage.py). Intégré nativement au workflow pytest, génère des rapports HTML et XML pour CI/CD. |
| **pytest-benchmark** | Plugin pytest pour le benchmarking de performance. Permet de détecter les régressions de performance dans le même workflow que les tests unitaires. |
| **Bandit** | Analyseur statique de sécurité spécifique à Python. Détecte les failles courantes (injection, eval, secrets hardcodés) sans exécution du code. |
| **Black + isort + Flake8** | Trio standard de l'écosystème Python : Black pour le formatage automatique (aucun débat de style), isort pour l'ordre des imports, Flake8 pour les règles complémentaires. |
| **MyPy** | Vérificateur de types statiques pour Python. Détecte les erreurs de type sans exécution, améliorant la maintenabilité sur un projet de cette taille (~9000 LOC). |
| **Pre-commit** | Framework de hooks Git pré-commit. Permet d'exécuter automatiquement 30+ vérifications avant chaque commit, garantissant que le code non conforme ne passe pas. |

---

## 5. Métriques de Qualité et KPIs

### 5.1 Tableau de bord qualité

| Métrique | Cible | Actuel | Fréquence de mesure |
|----------|-------|--------|-------------------|
| Couverture de tests | ≥ 80% | 80%+ | Chaque commit (CI) |
| Tests passants | 100% | 100% | Chaque commit (CI) |
| Score Pylint | ≥ 8/10 | 8.5/10 | Chaque commit |
| Vulnérabilités critiques | 0 | 0 | Chaque PR |
| Temps de réponse p95 | < 500ms | ~85ms | Hebdomadaire |
| Throughput | > 500 req/s | 609 req/s | Mensuel |
| Accessibilité WCAG | ≥ 75% AA | 70%+ | Mensuel |
| Conformité RGPD | ≥ 80% | 79.3% | Trimestriel |
| Build time CI | < 5 min | ~4 min | Chaque commit |
| Uptime | 99.9% | 99.9% | Continu (Prometheus) |

### 5.2 Seuils d'alerte

| Métrique | Seuil Warning | Seuil Critique | Action |
|----------|-------------|---------------|--------|
| Couverture | < 75% | < 60% | Blocage de PR |
| Tests échoués | ≥ 1 | ≥ 3 | Blocage de merge |
| Temps de réponse | > 500ms | > 1s | Investigation |
| Taux d'erreur | > 1% | > 5% | Rollback |
| Mémoire | > 80% | > 90% | Restart automatique |

---

## 6. Gestion des Non-Conformités

### 6.1 Classification des défauts

| Sévérité | Description | SLA de résolution | Exemple |
|----------|------------|-------------------|---------|
| **Critique** | Perte de données, faille de sécurité exploitable | 4 heures | Injection SQL, corruption de base |
| **Majeur** | Fonctionnalité bloquée, régression | 24 heures | Import GEDCOM échoue, recherche cassée |
| **Mineur** | Fonctionnalité dégradée, UI | 1 semaine | Affichage incorrect, lenteur |
| **Cosmétique** | Visuel, typo | Sprint suivant | Faute d'orthographe, alignement |

### 6.2 Processus de résolution

1. **Détection** : Automatique (CI/CD, monitoring) ou manuelle (revue, test)
2. **Qualification** : Attribution d'une sévérité et d'un responsable
3. **Correction** : Branch hotfix (critique/majeur) ou branch feature (mineur/cosmétique)
4. **Validation** : Tests de non-régression + revue de code
5. **Déploiement** : Selon la sévérité (immédiat pour critique, release pour mineur)
6. **Post-mortem** : Obligatoire pour les défauts critiques et majeurs

### 6.3 Traçabilité

Chaque défaut est tracé via :
- **Git** : Commits conventionnels (`fix:`, `hotfix:`) avec référence au problème
- **Historique** : Document `QA_HISTORY.md` pour les correctifs majeurs
- **CI/CD** : Logs de pipeline conservés 90 jours

---

## 7. Amélioration Continue

### 7.1 Revues périodiques

| Fréquence | Activité | Participants |
|-----------|---------|-------------|
| **Chaque sprint** | Revue des métriques qualité | Équipe dev |
| **Mensuel** | Audit de couverture et accessibilité | Lead dev + QA |
| **Trimestriel** | Audit de sécurité OWASP | Équipe + externes |
| **Semestriel** | Revue complète de la stratégie QA | Toute l'équipe |

### 7.2 Roadmap qualité

| Période | Objectif | Statut |
|---------|---------|--------|
| Q4 2025 | Tests unitaires 80%+ coverage |  Atteint |
| Q4 2025 | Tests d'intégration |  Atteint |
| Q4 2025 | Scanner sécurité OWASP |  Atteint |
| Q1 2026 | Tests de performance/charge |  Atteint |
| Q1 2026 | Validateur RGPD |  Atteint |
| Q1 2026 | Tests d'accessibilité WCAG |  Atteint |
| Q1 2026 | Amélioration accessibilité frontend |  Atteint |
| Q2 2026 | Coverage 90% | En cours |
| Q2 2026 | Tests E2E Selenium | Planifié |

---

## 8. Outils et Infrastructure

### 8.1 Stack de qualité

```
┌─────────────────────────────────────────────────────────┐
│                    DÉVELOPPEMENT LOCAL                    │
│  Pre-commit hooks (30+) → Black, Flake8, MyPy, Bandit  │
└─────────────────────┬───────────────────────────────────┘
                      │ git push
┌─────────────────────▼───────────────────────────────────┐
│                    CI/CD (GitHub Actions)                 │
│  Lint → Test (3.10/3.11/3.12) → Integration → Docker   │
└─────────────────────┬───────────────────────────────────┘
                      │ deploy
┌─────────────────────▼───────────────────────────────────┐
│                    PRODUCTION                             │
│  Prometheus → Grafana → Alertes → Smoke Tests           │
└─────────────────────────────────────────────────────────┘
```

### 8.2 Environnements

| Environnement | Usage | Tests exécutés |
|--------------|-------|---------------|
| **Local** | Développement | Unitaires, pre-commit hooks |
| **CI** | Intégration continue | Tous les tests automatisés |
| **Staging** | Pré-production | Performance, sécurité, accessibilité |
| **Production** | Exploitation | Smoke tests, monitoring |

---

## 9. Conformité et Réglementation

### 9.1 RGPD (Règlement Général sur la Protection des Données)

La conformité RGPD est validée par le module `tests/compliance/rgpd_validator.py` qui vérifie :
- Droits des utilisateurs (articles 15-22) : accès, rectification, effacement, portabilité
- Protection des données : chiffrement AES-256-GCM, hachage bcrypt
- Gestion du consentement : retrait, journalisation
- Notification de violation : procédure 72h

### 9.2 Accessibilité numérique (C28.2)

La conformité accessibilité est intégrée à **chaque étape du processus qualité** :

1. **Standards appliqués** : WCAG 2.1 niveau AA, RGAA 4.1
2. **Tests automatisés** : Suite de tests dans `tests/accessibility/`
3. **Audit documenté** : `docs/Disability_Standards.md`
4. **Checklist développeur** : Vérification ARIA, sémantique, clavier avant chaque PR
5. **Améliorations implémentées** :
   - Skip links pour navigation clavier
   - Structure sémantique HTML5 (`<main>`, `<header>`, `<footer>`)
   - Attributs ARIA complets sur les composants interactifs
   - Support `prefers-reduced-motion` et `prefers-contrast: high`
   - Labels ARIA sur toutes les icônes
   - Navigation clavier complète

### 9.3 Sécurité (OWASP)

La sécurité est validée par le scanner `tests/security/security_scanner.py` couvrant les 10 catégories OWASP :
- A01: Broken Access Control
- A02: Cryptographic Failures
- A03: Injection (SQL, XSS, Command)
- A04: Insecure Design
- A05: Security Misconfiguration
- A06: Vulnerable Components
- A07: Authentication Failures
- A08: Data Integrity Failures
- A09: Logging Failures
- A10: SSRF

---

## 10. Conclusion

Cette stratégie d'assurance qualité garantit que le projet AWKWARD LEGACY respecte les plus hauts standards de qualité logicielle. Elle intègre de manière native :

- **La fiabilité** via une pyramide de tests complète (unitaires, fonctionnels, intégration, performance)
- **La sécurité** via des scans OWASP automatisés et un chiffrement de bout en bout
- **L'accessibilité** via des tests WCAG 2.1 AA et une intégration dans le processus de développement
- **La conformité** via la validation RGPD automatisée
- **La maintenabilité** via le linting, le typage statique, et les revues de code

Cette stratégie est un document vivant, révisé trimestriellement pour s'adapter aux évolutions du projet et aux retours d'expérience.

---

**Dernière révision :** 17 Février 2026
**Prochaine révision prévue :** Mai 2026
