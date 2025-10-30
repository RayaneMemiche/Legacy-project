#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests de charge avec Locust pour AWKWARD LEGACY

Ce fichier contient les scénarios de test de charge pour vérifier
la scalabilité et les performances sous forte charge.

Usage:
    locust -f locustfile.py --host=http://localhost:8000
    locust -f locustfile.py --host=http://localhost:8000 --headless -u 100 -r 10 -t 5m
"""

from locust import HttpUser, TaskSet, task, between, constant, constant_pacing
from locust import events
from locust.exception import RescheduleTask
import json
import random
import string
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserBehavior(TaskSet):
    """Comportements utilisateur pour les tests de charge"""

    def on_start(self):
        """Initialisation avant le début des tests"""
        # Génération d'un utilisateur unique
        self.username = f"user_{self._random_string(8)}"
        self.email = f"{self.username}@test.com"
        self.password = "TestPass123!@#"
        self.token = None
        self.user_id = None
        self.persons = []

        # Tentative d'inscription et connexion
        self.register_and_login()

    def on_stop(self):
        """Nettoyage à la fin des tests"""
        if self.token:
            self.logout()

    def _random_string(self, length: int) -> str:
        """Génère une chaîne aléatoire"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def register_and_login(self):
        """Inscription et connexion de l'utilisateur"""
        # Inscription
        with self.client.post(
            "/api/register",
            json={
                "username": self.username,
                "email": self.email,
                "password": self.password,
                "first_name": "Test",
                "last_name": "User"
            },
            catch_response=True
        ) as response:
            if response.status_code == 201:
                response.success()
                data = response.json()
                self.user_id = data.get("user_id")
                logger.info(f"User {self.username} registered successfully")
            else:
                # L'utilisateur existe peut-être déjà, on essaye de se connecter
                response.success()

        # Connexion
        with self.client.post(
            "/api/login",
            json={
                "username": self.username,
                "password": self.password
            },
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
                data = response.json()
                self.token = data.get("access_token")
                if not self.user_id:
                    self.user_id = data.get("user_id")
                logger.info(f"User {self.username} logged in successfully")
            else:
                response.failure(f"Login failed: {response.status_code}")
                raise RescheduleTask()

    def logout(self):
        """Déconnexion de l'utilisateur"""
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            with self.client.post(
                "/api/logout",
                headers=headers,
                catch_response=True
            ) as response:
                if response.status_code == 200:
                    response.success()
                    self.token = None
                else:
                    response.failure(f"Logout failed: {response.status_code}")

    # ========================================================================
    # TÂCHES DE TEST
    # ========================================================================

    @task(10)
    def view_dashboard(self):
        """Consultation du dashboard (tâche fréquente)"""
        if not self.token:
            self.register_and_login()
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        with self.client.get(
            "/api/dashboard",
            headers=headers,
            catch_response=True,
            name="/api/dashboard"
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                # Token expiré, reconnexion
                self.register_and_login()
                response.failure("Token expired")
            else:
                response.failure(f"Dashboard failed: {response.status_code}")

    @task(8)
    def search_persons(self):
        """Recherche de personnes"""
        if not self.token:
            self.register_and_login()
            return

        # Génération d'une requête de recherche aléatoire
        search_queries = [
            "Jean", "Marie", "Dupont", "Martin", "Bernard",
            "Durand", "Thomas", "Robert", "Richard", "Petit"
        ]
        query = random.choice(search_queries)

        headers = {"Authorization": f"Bearer {self.token}"}
        with self.client.get(
            f"/api/persons/search?q={query}",
            headers=headers,
            catch_response=True,
            name="/api/persons/search"
        ) as response:
            if response.status_code == 200:
                response.success()
                data = response.json()
                # Stocker quelques résultats pour d'autres opérations
                if data.get("results"):
                    self.persons = data["results"][:5]
            else:
                response.failure(f"Search failed: {response.status_code}")

    @task(6)
    def create_person(self):
        """Création d'une nouvelle personne"""
        if not self.token:
            self.register_and_login()
            return

        person_data = {
            "first_name": f"Prénom_{self._random_string(5)}",
            "last_name": f"Nom_{self._random_string(5)}",
            "birth_date": f"{random.randint(1920, 2020)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            "birth_place": random.choice(["Paris", "Lyon", "Marseille", "Toulouse", "Nice"]),
            "gender": random.choice(["M", "F"]),
            "occupation": random.choice(["Ingénieur", "Médecin", "Professeur", "Artisan", "Commerçant"])
        }

        headers = {"Authorization": f"Bearer {self.token}"}
        with self.client.post(
            "/api/persons",
            json=person_data,
            headers=headers,
            catch_response=True,
            name="/api/persons [POST]"
        ) as response:
            if response.status_code == 201:
                response.success()
                data = response.json()
                if data.get("id"):
                    self.persons.append(data)
            else:
                response.failure(f"Create person failed: {response.status_code}")

    @task(5)
    def view_person_details(self):
        """Consultation des détails d'une personne"""
        if not self.token:
            self.register_and_login()
            return

        if not self.persons:
            # Pas de personnes disponibles, on fait une recherche d'abord
            self.search_persons()
            return

        person = random.choice(self.persons)
        person_id = person.get("id", random.randint(1, 100))

        headers = {"Authorization": f"Bearer {self.token}"}
        with self.client.get(
            f"/api/persons/{person_id}",
            headers=headers,
            catch_response=True,
            name="/api/persons/[id]"
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()  # 404 est acceptable si la personne n'existe pas
            else:
                response.failure(f"View person failed: {response.status_code}")

    @task(4)
    def update_person(self):
        """Mise à jour des informations d'une personne"""
        if not self.token:
            self.register_and_login()
            return

        if not self.persons:
            return

        person = random.choice(self.persons)
        person_id = person.get("id", random.randint(1, 100))

        update_data = {
            "occupation": random.choice(["Retraité", "Ingénieur", "Médecin", "Professeur"]),
            "notes": f"Mise à jour le {datetime.now().isoformat()}"
        }

        headers = {"Authorization": f"Bearer {self.token}"}
        with self.client.patch(
            f"/api/persons/{person_id}",
            json=update_data,
            headers=headers,
            catch_response=True,
            name="/api/persons/[id] [PATCH]"
        ) as response:
            if response.status_code in [200, 204]:
                response.success()
            elif response.status_code == 404:
                response.success()  # 404 acceptable
            else:
                response.failure(f"Update person failed: {response.status_code}")

    @task(3)
    def create_relationship(self):
        """Création d'une relation entre deux personnes"""
        if not self.token:
            self.register_and_login()
            return

        if len(self.persons) < 2:
            return

        person1 = random.choice(self.persons)
        person2 = random.choice([p for p in self.persons if p != person1])

        relationship_data = {
            "person1_id": person1.get("id", 1),
            "person2_id": person2.get("id", 2),
            "relationship_type": random.choice(["parent", "child", "spouse", "sibling"])
        }

        headers = {"Authorization": f"Bearer {self.token}"}
        with self.client.post(
            "/api/relationships",
            json=relationship_data,
            headers=headers,
            catch_response=True,
            name="/api/relationships [POST]"
        ) as response:
            if response.status_code in [201, 200]:
                response.success()
            elif response.status_code == 409:
                response.success()  # Relation déjà existante
            else:
                response.failure(f"Create relationship failed: {response.status_code}")

    @task(3)
    def view_family_tree(self):
        """Consultation de l'arbre généalogique"""
        if not self.token:
            self.register_and_login()
            return

        if not self.persons:
            return

        person = random.choice(self.persons)
        person_id = person.get("id", 1)

        headers = {"Authorization": f"Bearer {self.token}"}
        with self.client.get(
            f"/api/persons/{person_id}/family-tree?depth=3",
            headers=headers,
            catch_response=True,
            name="/api/persons/[id]/family-tree"
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()
            else:
                response.failure(f"View family tree failed: {response.status_code}")

    @task(2)
    def export_gedcom(self):
        """Export au format GEDCOM (opération lourde)"""
        if not self.token:
            self.register_and_login()
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        with self.client.get(
            "/api/export/gedcom",
            headers=headers,
            catch_response=True,
            name="/api/export/gedcom",
            timeout=30  # Timeout plus long pour l'export
        ) as response:
            if response.status_code == 200:
                response.success()
                # Vérifier que le contenu ressemble à du GEDCOM
                content = response.text
                if content.startswith("0 HEAD"):
                    logger.info("GEDCOM export successful")
            else:
                response.failure(f"Export GEDCOM failed: {response.status_code}")

    @task(2)
    def import_gedcom(self):
        """Import d'un fichier GEDCOM (opération lourde)"""
        if not self.token:
            self.register_and_login()
            return

        # Génération d'un petit fichier GEDCOM de test
        gedcom_content = """0 HEAD
1 SOUR AWKWARD_LEGACY
2 VERS 1.0
1 GEDC
2 VERS 5.5.1
2 FORM LINEAGE-LINKED
1 CHAR UTF-8
0 @I1@ INDI
1 NAME Test /User/
1 SEX M
1 BIRT
2 DATE 1 JAN 1980
2 PLAC Paris, France
0 @I2@ INDI
1 NAME Test /Wife/
1 SEX F
1 BIRT
2 DATE 15 MAR 1982
2 PLAC Lyon, France
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
0 TRLR"""

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "text/plain"
        }

        with self.client.post(
            "/api/import/gedcom",
            data=gedcom_content,
            headers=headers,
            catch_response=True,
            name="/api/import/gedcom",
            timeout=30
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
                logger.info("GEDCOM import successful")
            else:
                response.failure(f"Import GEDCOM failed: {response.status_code}")

    @task(1)
    def generate_statistics(self):
        """Génération de statistiques (opération analytique)"""
        if not self.token:
            self.register_and_login()
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        with self.client.get(
            "/api/statistics",
            headers=headers,
            catch_response=True,
            name="/api/statistics"
        ) as response:
            if response.status_code == 200:
                response.success()
                data = response.json()
                logger.debug(f"Statistics: {data}")
            else:
                response.failure(f"Generate statistics failed: {response.status_code}")

    @task(1)
    def backup_data(self):
        """Demande de backup des données"""
        if not self.token:
            self.register_and_login()
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        with self.client.post(
            "/api/backup",
            headers=headers,
            catch_response=True,
            name="/api/backup",
            timeout=60
        ) as response:
            if response.status_code in [200, 202]:
                response.success()
                logger.info("Backup initiated successfully")
            else:
                response.failure(f"Backup failed: {response.status_code}")


class WebsiteUser(HttpUser):
    """Utilisateur simulé pour les tests de charge"""

    tasks = [UserBehavior]

    # Temps d'attente entre les requêtes (simule un comportement humain)
    wait_time = between(1, 3)  # Entre 1 et 3 secondes

    # Configuration de base
    host = "http://localhost:8000"  # Peut être overridé en ligne de commande


class MobileUser(HttpUser):
    """Utilisateur mobile avec comportement différent"""

    tasks = [UserBehavior]

    # Les utilisateurs mobiles font moins de requêtes
    wait_time = between(3, 7)

    # Headers spécifiques mobile
    def on_start(self):
        self.client.headers.update({
            "User-Agent": "AWKWARD-Mobile/1.0 (iOS 14.0)"
        })


class APIUser(HttpUser):
    """Utilisateur API avec requêtes plus fréquentes"""

    tasks = [UserBehavior]

    # Les clients API font des requêtes plus fréquentes
    wait_time = constant(0.5)  # Toutes les 0.5 secondes

    # Headers spécifiques API
    def on_start(self):
        self.client.headers.update({
            "User-Agent": "AWKWARD-API-Client/1.0",
            "Accept": "application/json"
        })


class AdminUser(HttpUser):
    """Utilisateur administrateur avec tâches spécifiques"""

    wait_time = between(2, 5)

    def on_start(self):
        """Connexion en tant qu'admin"""
        self.token = None
        self.login_as_admin()

    def login_as_admin(self):
        """Connexion avec des privilèges admin"""
        with self.client.post(
            "/api/login",
            json={
                "username": "admin",
                "password": "AdminPass123!@#"
            },
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
                data = response.json()
                self.token = data.get("access_token")
            else:
                response.failure(f"Admin login failed: {response.status_code}")

    @task(5)
    def view_admin_dashboard(self):
        """Consultation du dashboard admin"""
        if not self.token:
            self.login_as_admin()
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/api/admin/dashboard", headers=headers)

    @task(3)
    def view_system_logs(self):
        """Consultation des logs système"""
        if not self.token:
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/api/admin/logs", headers=headers)

    @task(2)
    def manage_users(self):
        """Gestion des utilisateurs"""
        if not self.token:
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/api/admin/users", headers=headers)

    @task(1)
    def system_health_check(self):
        """Vérification de la santé du système"""
        if not self.token:
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/api/admin/health", headers=headers)


# ============================================================================
# EVENT HANDLERS pour collecter des métriques personnalisées
# ============================================================================

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Handler au démarrage des tests"""
    logger.info("="*60)
    logger.info("Starting AWKWARD LEGACY Load Tests")
    logger.info(f"Target host: {environment.host}")
    logger.info(f"Total users: {environment.parsed_options.num_users if environment.parsed_options else 'N/A'}")
    logger.info("="*60)


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Handler à l'arrêt des tests"""
    logger.info("="*60)
    logger.info("Load Tests Completed")

    # Affichage des statistiques finales
    if environment.stats:
        logger.info(f"Total requests: {environment.stats.total.num_requests}")
        logger.info(f"Failure rate: {environment.stats.total.fail_ratio:.2%}")
        logger.info(f"Avg response time: {environment.stats.total.avg_response_time:.0f}ms")
        logger.info(f"RPS: {environment.stats.total.current_rps:.1f}")

    logger.info("="*60)


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """Handler pour chaque requête (pour métriques personnalisées)"""
    if exception:
        logger.error(f"Request failed: {name} - {exception}")

    # Alertes pour les requêtes lentes
    if response_time > 5000:  # Plus de 5 secondes
        logger.warning(f"Slow request detected: {name} took {response_time}ms")


# ============================================================================
# SCÉNARIOS DE TEST AVANCÉS
# ============================================================================

class StressTestScenario(TaskSet):
    """Scénario de stress test avec montée en charge progressive"""

    def on_start(self):
        self.intensity_level = 1

    @task
    def escalating_load(self):
        """Augmentation progressive de la charge"""
        # Simuler une charge croissante
        for _ in range(self.intensity_level):
            self.client.get("/api/health")

        # Augmenter l'intensité toutes les 10 requêtes
        if random.random() < 0.1:
            self.intensity_level = min(self.intensity_level + 1, 10)
            logger.info(f"Intensity level increased to {self.intensity_level}")


class SpikeTestScenario(TaskSet):
    """Scénario de test de pic de charge"""

    @task
    def normal_load(self):
        """Charge normale"""
        self.client.get("/api/dashboard")
        time.sleep(random.uniform(1, 3))

    @task
    def spike_load(self):
        """Pic de charge soudain"""
        if random.random() < 0.05:  # 5% de chance de déclencher un pic
            logger.info("Spike load triggered!")
            for _ in range(50):  # 50 requêtes rapides
                self.client.get("/api/search?q=test", name="/api/search [spike]")
                time.sleep(0.01)


if __name__ == "__main__":
    # Si exécuté directement, afficher les instructions
    print("="*60)
    print("AWKWARD LEGACY - Load Testing with Locust")
    print("="*60)
    print("\nUsage:")
    print("  Web UI:     locust -f locustfile.py --host=http://localhost:8000")
    print("  Headless:   locust -f locustfile.py --host=http://localhost:8000 --headless -u 100 -r 10 -t 5m")
    print("\nScenarios available:")
    print("  - WebsiteUser: Regular web users")
    print("  - MobileUser: Mobile app users")
    print("  - APIUser: API clients")
    print("  - AdminUser: Admin users")
    print("="*60)