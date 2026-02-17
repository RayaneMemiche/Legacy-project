# Politique de Tests - AWKWARD LEGACY

**Version:** 2.0
**Date:** 17 Février 2026
**Projet:** Modernisation de GeneWeb
**Référentiel RNCP:** Bloc 5 - C25.1, C25.2, C26.1, C26.2, C27.1, C27.2

---

## 1. Stratégie de Tests

### Vue d'ensemble

La stratégie de tests d'AWKWARD LEGACY vise à garantir la qualité, la fiabilité et la maintenabilité du système tout en préservant l'intégrité du code legacy OCaml. Notre approche repose sur une pyramide de tests équilibrée.

### Justification de la stratégie (C25.2)

La pyramide de tests a été choisie pour les raisons suivantes :

1. **Base large de tests unitaires (41%)** : Les modules de la bibliothèque (`lib/`) contiennent ~9 150 lignes de code métier critique (algorithmes de consanguinité, parsing GEDCOM, chiffrement). Des tests unitaires exhaustifs sur chaque module garantissent qu'une modification ne casse pas le comportement attendu. Le coût de correction d'un bug détecté par test unitaire est estimé à 1x vs 100x s'il est détecté en production.

2. **Tests fonctionnels (18%)** : Ils valident les scénarios utilisateur complets (création de personne, import GEDCOM, recherche). Ils sont plus coûteux à maintenir que les tests unitaires mais indispensables pour garantir que les modules fonctionnent ensemble du point de vue utilisateur.

3. **Tests d'intégration (17%)** : Le projet utilise plusieurs composants (FastAPI, SQLAlchemy, Redis, NetworkX). Les tests d'intégration vérifient que ces composants interagissent correctement, notamment l'accès concurrent à la base de données et la propagation des erreurs entre couches.

4. **Tests de performance (9%)** : Un logiciel de généalogie peut manipuler des bases de 100 000+ personnes. Les tests de performance (Locust) simulent 100 utilisateurs simultanés pour garantir que l'application reste réactive sous charge.

5. **Tests de sécurité et conformité (15%)** : Les données généalogiques sont des données personnelles sensibles (filiation, dates de naissance/décès). La sécurité (OWASP Top 10) et la conformité RGPD sont donc des exigences fonctionnelles, pas des extras.

### Types de tests implémentés

#### 1.1 Tests Unitaires (40+ fichiers)
- **Objectif:** Valider le comportement de chaque module individuellement
- **Couverture cible:** 80% minimum
- **Technologies:** pytest, unittest
- **Localisation:** `LegacyProject/modernProject/tests/`

**Modules couverts (principaux) :**
```
- database.py         (test_database.py - 36 KB)
- security.py         (test_security.py - 22 KB)
- futil.py            (test_futil.py - 24 KB)
- gwdef.py            (test_gwdef.py - 10 KB)
- mutil.py            (test_mutil.py - 9.5 KB)
- consanguinity.py    (test_consanguinity.py - 5.4 KB)
- connectivity.py     (test_connectivity.py - 4.4 KB)
- gedcom_parser.py    (test_gedcom_parser.py - 5.7 KB)
- gedcom_exporter.py  (test_gedcom_exporter.py - 5.3 KB)
- date.py             (test_date.py - 6 KB)
- name.py             (test_name.py - 6.5 KB)
- ansel.py            (test_ansel.py - tests encodage)
- avl.py              (test_avl.py - structures données)
- pqueue.py           (test_pqueue.py - 6.6 KB)
- iovalue.py          (test_iovalue.py - 6.5 KB)
- ... (40+ fichiers de tests au total)
```

**Métriques actuelles:**
- Nombre de fichiers de tests unitaires: 40+
- Couverture de code: ~80%
- Temps d'exécution: < 2 minutes
- Lignes de code de tests: ~9 200

#### 1.2 Tests Fonctionnels (10 scénarios end-to-end)
- **Objectif:** Valider les workflows complets utilisateur
- **Technologies:** pytest, behave
- **Localisation:** `LegacyProject/modernProject/tests/functional/`

**Scénarios couverts:**
1. Création complète d'une personne
2. Navigation dans l'arbre généalogique
3. Recherche de personnes
4. Import/Export GEDCOM
5. Backup et restauration de base

#### 1.3 Tests d'Intégration (5 tests inter-modules)
- **Objectif:** Vérifier l'interaction entre composants
- **Technologies:** pytest, threading
- **Localisation:** `LegacyProject/modernProject/tests/integration/`

**Tests implémentés:**
1. Interface Python-OCaml (bridge bidirectionnel)
2. Workflow multi-modules (database → geneweb_compat → output)
3. Accès concurrent à la base
4. Cohérence des données
5. Propagation des erreurs entre couches

#### 1.4 Tests de Performance (5 benchmarks critiques)
- **Objectif:** Garantir les performances sous charge
- **Technologies:** pytest-benchmark, psutil, locust
- **Localisation:** `LegacyProject/modernProject/tests/performance/`

**Benchmarks:**
1. Chargement de grande base (10 000 personnes)
2. Performance de recherche (< 100ms)
3. Import GEDCOM (5 000 individus)
4. Utilisation mémoire (< 500 MB)
5. Charge multi-utilisateurs (100 simultanés)

---

## 2. Protocoles de Tests

### 2.1 Avant chaque commit

```bash
# Exécuter les tests unitaires
make test-unit

# Vérifier la couverture
make coverage

# Linting du code
make lint
```

**Critères de passage:**
- ✅ Tous les tests unitaires passent
- ✅ Couverture ≥ 75%
- ✅ Pas d'erreur de linting
- ✅ Pas de régression détectée

### 2.2 Avant chaque pull request

```bash
# Suite complète de tests
make test

# Tests d'intégration
make test-integration

# Vérification de sécurité
make security-check
```

**Critères de validation:**
- ✅ Suite de tests complète (unitaire + intégration)
- ✅ Tests fonctionnels passent
- ✅ Pas de vulnérabilités détectées
- ✅ Documentation à jour

### 2.3 Avant chaque release

```bash
# Tests complets incluant performance
make test-all

# Tests de performance
make test-performance

# Tests de charge
make test-load

# Validation finale
make validate
```

**Critères de release:**
- ✅ Tous les tests passent (unitaire, intégration, fonctionnel, performance)
- ✅ Performance conforme aux SLA
- ✅ Pas de régression de performance
- ✅ Documentation complète
- ✅ CHANGELOG mis à jour

### 2.4 Tests en production (monitoring)

```bash
# Health checks automatiques
curl http://localhost:8080/health

# Métriques système
curl http://localhost:8080/metrics

# Tests smoke après déploiement
./scripts/smoke-tests.sh
```

---

## 3. Scénarios de Tests Détaillés

### Scénario 1: Création d'arbre généalogique complet

**Objectif:** Valider la création d'un arbre sur 3 générations

**Étapes:**
1. Créer les grands-parents (génération 1)
   ```python
   grandpa = create_person("Jean", "Martin", 1930)
   grandma = create_person("Marie", "Durand", 1932)
   ```

2. Créer la famille des grands-parents
   ```python
   family_g1 = create_family(grandpa, grandma, marriage_date="1950-06-15")
   ```

3. Créer les parents (génération 2)
   ```python
   father = create_person("Pierre", "Martin", 1955)
   mother = create_person("Sophie", "Bernard", 1958)
   add_child_to_family(family_g1, father)
   ```

4. Créer la famille des parents
   ```python
   family_g2 = create_family(father, mother, marriage_date="1980-07-20")
   ```

5. Créer les enfants (génération 3)
   ```python
   child1 = create_person("Paul", "Martin", 1985)
   child2 = create_person("Julie", "Martin", 1988)
   add_child_to_family(family_g2, child1)
   add_child_to_family(family_g2, child2)
   ```

6. Calculer la consanguinité
   ```python
   consanguinity = calculate_consanguinity(child1)
   assert consanguinity == 0  # Pas de consanguinité
   ```

7. Exporter en GEDCOM
   ```python
   export_gedcom("family_tree.ged", [grandpa, grandma, father, mother, child1, child2])
   ```

8. Réimporter et vérifier l'intégrité
   ```python
   imported_tree = import_gedcom("family_tree.ged")
   assert len(imported_tree.persons) == 6
   assert imported_tree.get_person_by_name("Paul", "Martin") is not None
   ```

**Critères de succès:**
- ✅ Toutes les personnes créées avec succès
- ✅ Relations familiales correctes
- ✅ Calcul de consanguinité précis
- ✅ Export/Import GEDCOM sans perte de données

---

### Scénario 2: Import de données externes volumineuses

**Objectif:** Importer un fichier GEDCOM de 10 000 individus

**Étapes:**
1. Préparer un fichier GEDCOM de test
   ```bash
   python scripts/generate_test_gedcom.py --size 10000 -o large_test.ged
   ```

2. Importer le fichier
   ```python
   start_time = time.time()
   tree = import_gedcom("large_test.ged")
   duration = time.time() - start_time
   ```

3. Valider les données importées
   ```python
   assert len(tree.persons) == 10000
   assert tree.is_valid()
   ```

4. Détecter les doublons potentiels
   ```python
   duplicates = tree.find_duplicates(threshold=0.9)
   ```

5. Fusionner les entrées dupliquées si nécessaire
   ```python
   for dup in duplicates:
       merged = merge_persons(dup[0], dup[1])
   ```

6. Vérifier l'intégrité finale
   ```python
   assert tree.check_integrity()
   ```

**Critères de succès:**
- ✅ Import en moins de 10 secondes
- ✅ 100% des données importées
- ✅ Détection de doublons fonctionnelle
- ✅ Intégrité référentielle maintenue

---

### Scénario 3: Performance sous charge

**Objectif:** Gérer 100 utilisateurs simultanés

**Étapes:**
1. Configurer le test de charge
   ```python
   from locust import HttpUser, task, between

   class GeneWebUser(HttpUser):
       wait_time = between(1, 3)

       @task(3)
       def search_person(self):
           self.client.get("/search?q=Martin")

       @task(1)
       def view_person(self):
           self.client.get("/person/12345")
   ```

2. Lancer le test
   ```bash
   locust -f tests/load/locustfile.py --users 100 --spawn-rate 10
   ```

3. Surveiller les métriques
   - Temps de réponse moyen
   - Taux d'erreur
   - Utilisation CPU/Mémoire
   - Nombre de requêtes/seconde

**Critères de succès:**
- ✅ Temps de réponse moyen < 500ms
- ✅ Taux d'erreur < 1%
- ✅ Pas de crash système
- ✅ Mémoire stable (pas de fuite)

---

## 4. Gestion des Erreurs et Non-Régression

### 4.1 Détection des erreurs

#### Logs structurés
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/awkward-legacy.log'),
        logging.StreamHandler()
    ]
)
```

#### Catégories d'erreurs
- **CRITICAL:** Crash système, perte de données
- **ERROR:** Erreur fonctionnelle bloquante
- **WARNING:** Comportement anormal non bloquant
- **INFO:** Événements normaux importants
- **DEBUG:** Informations de débogage détaillées

### 4.2 Alertes automatiques

#### Configuration
```yaml
# alerts.yml
alerts:
  - name: "High Error Rate"
    condition: "error_rate > 5%"
    action: "send_email"
    recipients: ["dev-team@awkward-legacy.com"]

  - name: "Slow Response Time"
    condition: "avg_response_time > 1s"
    action: "send_slack"
    channel: "#alerts"

  - name: "Memory Usage High"
    condition: "memory_usage > 90%"
    action: "restart_service"
```

### 4.3 Métriques de santé

#### Endpoints de monitoring
```python
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'uptime': get_uptime(),
        'database': check_database_connection(),
        'memory': get_memory_usage(),
        'timestamp': datetime.now().isoformat()
    }

@app.route('/metrics')
def metrics():
    return {
        'requests_total': metrics.requests_total,
        'requests_per_second': metrics.requests_per_second,
        'avg_response_time': metrics.avg_response_time,
        'error_rate': metrics.error_rate,
        'active_users': metrics.active_users
    }
```

### 4.4 Tests de non-régression

#### Snapshot testing
```python
def test_person_serialization_snapshot(snapshot):
    """Test que la sérialisation reste stable"""
    person = create_test_person()
    serialized = person.to_dict()
    snapshot.assert_match(serialized)
```

#### Performance regression
```python
def test_search_performance_regression(benchmark_history):
    """Test qu'il n'y a pas de régression de performance"""
    current_time = benchmark(search_operation)
    historical_avg = benchmark_history.get_avg('search_operation')

    # Pas de régression > 20%
    assert current_time < historical_avg * 1.2
```

---

## 5. Résolution des Problèmes

### 5.1 Procédure de rollback

#### Étape 1: Détection du problème
```bash
# Vérifier les logs
tail -f /var/log/awkward-legacy.log

# Vérifier les métriques
curl http://localhost:8080/metrics
```

#### Étape 2: Décision de rollback
**Critères de rollback immédiat:**
- Taux d'erreur > 10%
- Perte de données détectée
- Service indisponible > 5 minutes
- Vulnérabilité de sécurité critique

#### Étape 3: Exécution du rollback
```bash
# Rollback Docker
docker-compose down
docker-compose -f docker-compose.previous.yml up -d

# Rollback base de données
./scripts/restore.sh --backup latest-stable

# Vérification
./scripts/smoke-tests.sh
```

### 5.2 Hotfix Process

#### Workflow hotfix
```bash
# 1. Créer une branche hotfix
git checkout -b hotfix/critical-bug-fix main

# 2. Appliquer le fix
# ... éditer les fichiers

# 3. Tests rapides
make test-unit

# 4. Commit et push
git commit -m "hotfix: Fix critical bug in person creation"
git push origin hotfix/critical-bug-fix

# 5. Merge direct vers main (avec approbation)
git checkout main
git merge hotfix/critical-bug-fix
git tag -a v1.0.1-hotfix -m "Hotfix for critical bug"
git push --tags

# 6. Déploiement immédiat
./scripts/deploy.sh --environment production
```

### 5.3 Post-mortem obligatoire

#### Template de post-mortem
```markdown
# Post-Mortem: [Titre de l'incident]

**Date:** [Date de l'incident]
**Durée:** [Durée de l'incident]
**Impact:** [Description de l'impact]
**Sévérité:** [Critical/High/Medium/Low]

## Chronologie
- HH:MM - Détection initiale
- HH:MM - Investigation commencée
- HH:MM - Cause identifiée
- HH:MM - Fix déployé
- HH:MM - Incident résolu

## Cause racine
[Description détaillée]

## Actions correctives
- [ ] Action immédiate 1
- [ ] Action préventive 1
- [ ] Amélioration du monitoring

## Leçons apprises
[Ce qu'on a appris]

## Actions de suivi
- Responsable: [Nom]
- Date limite: [Date]
```

---

## 6. Métriques de Qualité

### 6.1 KPIs de tests

#### Couverture de code
- **Target:** ≥ 80%
- **Actuel:** ~80%
- **Méthode:** pytest-cov

```bash
# Générer le rapport de couverture
pytest --cov=modernProject/lib --cov-report=html --cov-report=term

# Visualiser dans le navigateur
open htmlcov/index.html
```

#### Temps de build
- **Target:** < 5 minutes
- **Pipeline CI/CD:** GitHub Actions

**Breakdown:**
- Checkout code: ~10s
- Install dependencies: ~1min
- Run tests: ~2min
- Build Docker image: ~2min
- Total: ~5min

#### Qualité du code
- **Zero erreur critique en production**
- **Pas de vulnérabilités HIGH/CRITICAL**
- **Code smell density < 5%**

### 6.2 SLA de performance

#### API Endpoints
| Endpoint | Target | Mesure actuelle |
|----------|--------|-----------------|
| GET /person/{id} | < 50ms | ~30ms |
| POST /person | < 100ms | ~75ms |
| GET /search?q={query} | < 100ms | ~85ms |
| GET /family/{id} | < 50ms | ~35ms |
| POST /gedcom/import | < 10s | ~8s (5k persons) |

#### Base de données
- **Requête simple:** < 10ms
- **Requête complexe:** < 100ms
- **Import GEDCOM:** < 10s pour 5000 personnes
- **Backup complet:** < 1min pour 100k personnes

### 6.3 Métriques de disponibilité

#### Uptime
- **Target:** 99.9% (8.76h de downtime/an max)
- **Mesure:** Monitoring continu avec Prometheus/Grafana

#### Temps de récupération
- **RTO (Recovery Time Objective):** < 30 minutes
- **RPO (Recovery Point Objective):** < 1 heure

#### Scalabilité
- **Utilisateurs simultanés:** 100+ sans dégradation
- **Croissance base:** Support de 1M+ personnes
- **Croissance trafic:** +100% sans modifications majeures

---

## 7. Outils et Infrastructure de Tests

### 7.1 Outils de test et justification des choix (C26.1, C26.2)

| Outil | Usage | Version | Justification du choix |
|-------|-------|---------|----------------------|
| pytest | Framework de test principal | ≥7.4.3 | Standard de facto Python (>80% PDM). Discovery automatique, syntaxe concise avec `assert`, écosystème de plugins riche. Compatible unittest pour migration progressive. |
| pytest-cov | Couverture de code | ≥4.1.0 | Basé sur coverage.py, intégré nativement à pytest. Génère rapports HTML et XML pour CI/CD. Permet de définir des seuils de couverture minimaux. |
| pytest-benchmark | Tests de performance | ≥4.0.0 | Intégré au workflow pytest (même commande, même rapport). Détecte les régressions de performance entre commits via comparaison historique. |
| unittest | Tests d'intégration | stdlib | Bibliothèque standard Python : pas de dépendance externe. setUp/tearDown explicites pour l'isolation des tests d'intégration. TestCase pour groupement logique. |
| locust | Tests de charge | ≥2.17.0 | Scénarios de charge écrits en Python (vs JMeter en XML). Permet de simuler des comportements utilisateur réalistes. Interface web pour monitoring temps réel. Compatible avec notre stack Python. |
| selenium | Tests UI E2E | ≥4.15.0 | Standard industriel pour l'automatisation de navigateurs. Support multi-navigateurs (Chrome, Firefox). Nécessaire pour les tests d'accessibilité en conditions réelles. |
| psutil | Monitoring système | ≥5.9.0 | Permet de mesurer l'utilisation mémoire et CPU pendant les benchmarks. Détection de fuites mémoire. Cross-platform (Linux/macOS/Windows). |
| Bandit | Analyse sécurité statique | ≥1.7.0 | Analyseur statique spécifique Python. Détecte injection, eval(), secrets hardcodés sans exécution du code. Intégré en pre-commit hook. |
| Black + Flake8 | Formatage et linting | ≥23.0 / ≥6.0 | Black : formatage automatique opinionné (zéro débat de style). Flake8 : règles complémentaires (complexité cyclomatique, imports). Combinaison standard de l'écosystème Python. |
| MyPy | Typage statique | ≥1.7.0 | Détecte les erreurs de type sans exécution. Essentiel sur un projet de ~9 000 LOC pour la maintenabilité. Supporte les annotations Python 3.9+. |

### 7.2 CI/CD Pipeline

#### GitHub Actions workflow
```yaml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run unit tests
        run: make test-unit

      - name: Run integration tests
        run: make test-integration

      - name: Check coverage
        run: |
          pytest --cov --cov-report=xml
          bash <(curl -s https://codecov.io/bash)

      - name: Lint code
        run: make lint

      - name: Security scan
        run: make security-check
```

### 7.3 Environnements de test

#### Local Development
```bash
# Setup environnement local
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Lancer les tests
make test
```

#### Staging
- URL: https://staging.awkward-legacy.com
- Base de données: Copie anonymisée de production
- Tests automatiques après chaque déploiement

#### Production
- URL: https://awkward-legacy.com
- Déploiement avec validation manuelle
- Tests smoke après déploiement

---

## 8. Formation et Documentation

### 8.1 Documentation pour développeurs

#### Guide de contribution
Voir [CONTRIBUTING.md](../CONTRIBUTING.md) pour:
- Standards de code
- Process de contribution
- Guide de review

#### Documentation des tests
```python
def test_person_creation_with_all_fields():
    """
    Test la création d'une personne avec tous les champs remplis.

    Scénario:
        1. Créer une personne avec tous les champs
        2. Vérifier que tous les champs sont correctement enregistrés
        3. Vérifier que la personne peut être retrouvée

    Assertions:
        - La personne est créée avec un ID unique
        - Tous les champs correspondent aux valeurs fournies
        - La personne est retrouvable par son ID
    """
    # Test implementation
```

### 8.2 Formation continue

#### Sessions de formation
- **Mensuel:** Revue des tests et métriques
- **Trimestriel:** Formation sur nouveaux outils
- **Annuel:** Audit complet de la qualité

#### Ressources
- Wiki interne: https://wiki.awkward-legacy.com
- Vidéos de formation: https://training.awkward-legacy.com
- Documentation technique: https://docs.awkward-legacy.com

---

## 9. Évolution et Amélioration Continue

### 9.0 Tests d'Accessibilité (C28.2)

Les tests d'accessibilité font partie intégrante du protocole de tests, conformément aux exigences WCAG 2.1 AA et à la stratégie d'assurance qualité.

#### Localisation
`LegacyProject/modernProject/tests/accessibility/test_accessibility.py`

#### Vérifications effectuées
1. **Structure sémantique HTML** : Présence de `<main>`, `<header>`, `<footer>`, `<nav>`, `<section>`
2. **Navigation clavier** : Skip links, tabindex, focus visible
3. **Attributs ARIA** : `aria-label`, `aria-live`, `aria-expanded`, `role`
4. **Formulaires** : Labels associés via `for`/`id`, messages d'erreur
5. **Contrastes** : Ratio ≥ 4.5:1 pour le texte normal
6. **Média** : Alt text sur images et icônes
7. **Préférences utilisateur** : `prefers-reduced-motion`, `prefers-contrast: high`
8. **Langue** : Attribut `lang` sur `<html>`

#### Exécution
```bash
pytest tests/accessibility/ -v
```

### 9.1 Roadmap des tests

#### Q4 2025
- ✅ Tests unitaires (80% coverage)
- ✅ Tests d'intégration
- ✅ Tests de performance
- ✅ Tests de sécurité automatisés (OWASP Top 10)

#### Q1 2026
- ✅ Tests d'accessibilité (WCAG 2.1 AA)
- ✅ Amélioration accessibilité frontend (skip links, ARIA, sémantique)
- ✅ Validateur RGPD complet
- 🔄 Amélioration coverage à 90%

#### Q2 2026
- 🔜 Tests E2E avec Selenium
- 🔜 Tests de mutation
- 🔜 Tests de compatibilité navigateurs
- 🔜 Tests d'internationalisation

### 9.2 Métriques d'amélioration

#### Suivi trimestriel
```python
metrics = {
    'Q4_2025': {
        'coverage': 80,
        'test_files': 53,
        'test_lines': 9200,
        'avg_build_time': 240,
        'flaky_tests': 0
    },
    'Q1_2026': {
        'coverage': 80,
        'test_files': 55,
        'test_lines': 9800,
        'avg_build_time': 240,
        'accessibility_tests': True,
        'flaky_tests': 0
    }
}
```

#### Objectifs 2026
- Coverage: 80% → 90%
- Build time: 4min → 3min
- Flaky tests: Maintien à zéro
- Tests d'accessibilité: Conformité WCAG 2.1 AA ≥ 75%
- Zero vulnérabilité critique en production

---

## 10. Conclusion

Cette politique de tests garantit la qualité et la fiabilité d'AWKWARD LEGACY tout au long de son cycle de développement. Elle sera revue et mise à jour trimestriellement pour s'adapter aux évolutions du projet.

**Responsables:**
- **Responsable Qualité:** Rayane Memiche
- **Lead Développeur:** Rayane Memiche
- **DevOps:** Rayane Memiche

**Contacts:**
- Email: qa@awkward-legacy.com
- Slack: #quality-assurance

**Dernière révision:** 17 Février 2026
**Prochaine révision prévue:** Mai 2026