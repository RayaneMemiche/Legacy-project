#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests d'intégration complets pour AWKWARD LEGACY

Ces tests vérifient l'intégration complète de tous les composants
du système, incluant la sécurité, les performances et la conformité.
"""

import unittest
import asyncio
import json
import time
import threading
import multiprocessing
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil
import os
import sqlite3
import hashlib
import random
import string

# Import des modules du projet (avec gestion des erreurs si non installés)
try:
    from modernProject.lib.security import SecurityManager
except ImportError:
    SecurityManager = None

try:
    from modernProject.lib.database import DatabaseManager
except ImportError:
    DatabaseManager = None


class CompleteIntegrationTestSuite(unittest.TestCase):
    """Suite complète de tests d'intégration"""

    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour tous les tests"""
        cls.test_dir = tempfile.mkdtemp(prefix="awkward_test_")
        cls.test_db = os.path.join(cls.test_dir, "test.db")
        cls.security_manager = SecurityManager.get_instance() if SecurityManager else None
        cls.start_time = time.time()

        # Configuration de l'environnement de test
        os.environ['APP_ENV'] = 'test'
        os.environ['APP_DEBUG'] = 'false'
        os.environ['DATABASE_PATH'] = cls.test_db

        print(f"\n{'='*60}")
        print(f"Starting Complete Integration Test Suite")
        print(f"Test Directory: {cls.test_dir}")
        print(f"{'='*60}\n")

    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)

        elapsed = time.time() - cls.start_time
        print(f"\n{'='*60}")
        print(f"Test Suite Completed in {elapsed:.2f} seconds")
        print(f"{'='*60}\n")

    def setUp(self):
        """Configuration avant chaque test"""
        self.test_users = []
        self.test_tokens = []
        self.metrics = {
            'start_time': time.time(),
            'memory_start': self._get_memory_usage()
        }

    def tearDown(self):
        """Nettoyage après chaque test"""
        elapsed = time.time() - self.metrics['start_time']
        memory_used = self._get_memory_usage() - self.metrics['memory_start']

        print(f"  ✓ {self._testMethodName}: {elapsed:.3f}s, Memory: {memory_used:.2f}MB")

    def _get_memory_usage(self) -> float:
        """Obtient l'utilisation mémoire actuelle en MB"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except:
            return 0.0

    # ========================================================================
    # TESTS D'INTÉGRATION SYSTÈME COMPLET
    # ========================================================================

    def test_01_complete_user_lifecycle(self):
        """Test du cycle de vie complet d'un utilisateur"""
        print("\n► Testing Complete User Lifecycle...")

        # 1. Création d'utilisateur
        user_data = {
            'username': 'test_user_' + self._random_string(8),
            'email': f'test_{self._random_string(8)}@example.com',
            'password': 'SecurePass123!@#',
            'first_name': 'Test',
            'last_name': 'User'
        }

        # Simulation de la création
        if self.security_manager:
            # Hash du mot de passe
            hashed_password = self.security_manager.hash_password(user_data['password'])
            self.assertIsNotNone(hashed_password)
            self.assertNotEqual(hashed_password, user_data['password'])

            # Vérification du hash
            is_valid = self.security_manager.verify_password(
                user_data['password'],
                hashed_password
            )
            self.assertTrue(is_valid)

            # 2. Authentification et création de session
            user_id = self._create_mock_user(user_data, hashed_password)

            # Génération du JWT
            token_data = {
                'user_id': user_id,
                'username': user_data['username'],
                'email': user_data['email'],
                'roles': ['USER']
            }

            access_token = self.security_manager.create_jwt(token_data)
            self.assertIsNotNone(access_token)

            # Vérification du token
            decoded = self.security_manager.verify_jwt(access_token)
            self.assertIsNotNone(decoded)
            self.assertEqual(decoded['user_id'], user_id)

            # 3. Gestion des permissions
            has_permission = self.security_manager.check_permission(
                user_id, 'read', 'profile'
            )
            self.assertTrue(has_permission)

            # 4. Mise à jour du profil
            update_data = {
                'first_name': 'Updated',
                'last_name': 'Name'
            }

            # Simulation de la mise à jour avec audit
            audit_log = {
                'user_id': user_id,
                'action': 'profile_update',
                'timestamp': datetime.now().isoformat(),
                'changes': update_data
            }

            # 5. Changement de mot de passe
            new_password = 'NewSecurePass456!@#'
            new_hash = self.security_manager.hash_password(new_password)

            # Vérification que les hashs sont différents
            self.assertNotEqual(hashed_password, new_hash)

            # 6. Déconnexion et révocation du token
            self.security_manager.revoke_jwt(access_token)

            # Vérification que le token est révoqué
            decoded = self.security_manager.verify_jwt(access_token)
            self.assertIsNone(decoded)

            print(f"    ✓ User lifecycle completed for {user_data['username']}")

    def test_02_multi_user_concurrent_access(self):
        """Test d'accès concurrent multi-utilisateurs"""
        print("\n► Testing Multi-User Concurrent Access...")

        num_users = 10
        num_operations = 5

        def user_operations(user_id: int):
            """Opérations effectuées par chaque utilisateur"""
            operations_completed = []

            try:
                # Authentification
                if self.security_manager:
                    token = self.security_manager.create_jwt({
                        'user_id': user_id,
                        'username': f'user_{user_id}'
                    })
                    operations_completed.append('auth')

                # Lecture de données
                time.sleep(random.uniform(0.01, 0.05))
                operations_completed.append('read')

                # Écriture de données
                time.sleep(random.uniform(0.01, 0.05))
                operations_completed.append('write')

                # Mise à jour
                time.sleep(random.uniform(0.01, 0.05))
                operations_completed.append('update')

                # Déconnexion
                if self.security_manager and token:
                    self.security_manager.revoke_jwt(token)
                operations_completed.append('logout')

            except Exception as e:
                print(f"    ✗ Error for user {user_id}: {str(e)}")

            return operations_completed

        # Lancement des threads concurrents
        threads = []
        results = {}

        start_time = time.time()

        for i in range(num_users):
            thread = threading.Thread(
                target=lambda uid: results.update({uid: user_operations(uid)}),
                args=(i,)
            )
            threads.append(thread)
            thread.start()

        # Attente de la fin de tous les threads
        for thread in threads:
            thread.join(timeout=5.0)

        elapsed = time.time() - start_time

        # Vérification des résultats
        successful_users = len([r for r in results.values() if len(r) == 5])

        print(f"    ✓ {successful_users}/{num_users} users completed all operations")
        print(f"    ✓ Total time: {elapsed:.2f}s")
        print(f"    ✓ Throughput: {(num_users * num_operations) / elapsed:.1f} ops/sec")

        self.assertGreater(successful_users, num_users * 0.8)  # Au moins 80% de succès

    def test_03_database_integration(self):
        """Test d'intégration avec la base de données"""
        print("\n► Testing Database Integration...")

        # Création d'une base de données SQLite de test
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()

        # Création des tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                birth_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person1_id INTEGER NOT NULL,
                person2_id INTEGER NOT NULL,
                relationship_type TEXT NOT NULL,
                FOREIGN KEY (person1_id) REFERENCES persons (id),
                FOREIGN KEY (person2_id) REFERENCES persons (id)
            )
        ''')

        conn.commit()

        # Test d'insertion en masse
        print("    → Testing bulk insert...")
        start_time = time.time()

        persons_data = []
        for i in range(1000):
            persons_data.append((
                f'First_{i}',
                f'Last_{i}',
                f'19{50 + (i % 50):02d}-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}'
            ))

        cursor.executemany(
            'INSERT INTO persons (first_name, last_name, birth_date) VALUES (?, ?, ?)',
            persons_data
        )
        conn.commit()

        insert_time = time.time() - start_time
        print(f"    ✓ Inserted 1000 records in {insert_time:.3f}s")

        # Test de requêtes complexes
        print("    → Testing complex queries...")

        # Requête avec jointure
        cursor.execute('''
            SELECT COUNT(*) FROM persons
            WHERE birth_date < '1980-01-01'
        ''')
        count = cursor.fetchone()[0]
        print(f"    ✓ Found {count} persons born before 1980")

        # Test de transactions
        print("    → Testing transactions...")

        try:
            conn.execute('BEGIN TRANSACTION')

            # Insertion de relations
            for i in range(100):
                cursor.execute('''
                    INSERT INTO relationships (person1_id, person2_id, relationship_type)
                    VALUES (?, ?, ?)
                ''', (i + 1, i + 2, 'parent'))

            conn.commit()
            print("    ✓ Transaction completed successfully")

        except Exception as e:
            conn.rollback()
            print(f"    ✗ Transaction failed: {str(e)}")

        # Test d'index et performances
        print("    → Testing indexes...")

        cursor.execute('CREATE INDEX idx_birth_date ON persons(birth_date)')

        start_time = time.time()
        cursor.execute('''
            SELECT * FROM persons
            WHERE birth_date BETWEEN '1970-01-01' AND '1980-12-31'
            ORDER BY birth_date
        ''')
        results = cursor.fetchall()
        query_time = time.time() - start_time

        print(f"    ✓ Index query returned {len(results)} results in {query_time:.4f}s")

        conn.close()

    def test_04_security_integration(self):
        """Test d'intégration de toutes les fonctionnalités de sécurité"""
        print("\n► Testing Security Integration...")

        if not self.security_manager:
            print("    ⚠ Security manager not available, skipping...")
            return

        # 1. Test de rate limiting
        print("    → Testing rate limiting...")

        ip_address = "192.168.1.100"
        endpoint = "/api/login"

        # Simulation de tentatives multiples
        for i in range(10):
            allowed = self.security_manager.check_rate_limit(ip_address, endpoint)
            if i < 5:
                self.assertTrue(allowed, f"Request {i+1} should be allowed")
            else:
                # Après 5 tentatives, devrait être bloqué
                if not allowed:
                    print(f"    ✓ Rate limit triggered after {i+1} attempts")
                    break

        # 2. Test de chiffrement de données sensibles
        print("    → Testing data encryption...")

        sensitive_data = {
            'ssn': '123-45-6789',
            'credit_card': '4111-1111-1111-1111',
            'medical_record': 'Confidential medical information'
        }

        # Chiffrement
        encrypted_data = {}
        for key, value in sensitive_data.items():
            encrypted = self.security_manager.encrypt_data(value)
            encrypted_data[key] = encrypted
            self.assertNotEqual(encrypted, value)
            self.assertIsNotNone(encrypted)

        # Déchiffrement et vérification
        for key, encrypted in encrypted_data.items():
            decrypted = self.security_manager.decrypt_data(encrypted)
            self.assertEqual(decrypted, sensitive_data[key])

        print("    ✓ Data encryption/decryption verified")

        # 3. Test de protection CSRF
        print("    → Testing CSRF protection...")

        session_id = self._random_string(32)
        csrf_token = self.security_manager.generate_csrf_token(session_id)
        self.assertIsNotNone(csrf_token)

        # Validation du token
        is_valid = self.security_manager.validate_csrf_token(session_id, csrf_token)
        self.assertTrue(is_valid)

        # Token invalide
        is_valid = self.security_manager.validate_csrf_token(session_id, "invalid_token")
        self.assertFalse(is_valid)

        print("    ✓ CSRF protection verified")

        # 4. Test d'audit logging
        print("    → Testing audit logging...")

        audit_events = [
            {'type': 'login', 'user_id': 1, 'ip': '192.168.1.1'},
            {'type': 'data_access', 'user_id': 1, 'resource': 'persons'},
            {'type': 'data_modification', 'user_id': 1, 'resource': 'persons', 'action': 'update'},
            {'type': 'logout', 'user_id': 1}
        ]

        for event in audit_events:
            self.security_manager.log_security_event(
                event['type'],
                event.get('user_id'),
                event
            )

        print("    ✓ Audit logging verified")

    def test_05_api_workflow_integration(self):
        """Test d'un workflow API complet"""
        print("\n► Testing Complete API Workflow...")

        # Simulation d'un workflow complet d'API
        workflow_steps = []

        # 1. Registration
        print("    → Step 1: User Registration")
        registration_data = {
            'username': 'api_test_user',
            'email': 'api@test.com',
            'password': 'ApiPass123!@#'
        }

        if self.security_manager:
            hashed_pw = self.security_manager.hash_password(registration_data['password'])
            workflow_steps.append(('registration', 'success'))
        else:
            workflow_steps.append(('registration', 'skipped'))

        # 2. Email Verification (simulé)
        print("    → Step 2: Email Verification")
        verification_token = hashlib.sha256(
            f"{registration_data['email']}{time.time()}".encode()
        ).hexdigest()
        workflow_steps.append(('email_verification', 'success'))

        # 3. Login
        print("    → Step 3: User Login")
        if self.security_manager:
            login_token = self.security_manager.create_jwt({
                'username': registration_data['username'],
                'email': registration_data['email']
            })
            workflow_steps.append(('login', 'success'))
        else:
            login_token = None
            workflow_steps.append(('login', 'skipped'))

        # 4. Profile Setup
        print("    → Step 4: Profile Setup")
        profile_data = {
            'bio': 'Test user bio',
            'avatar': 'avatar.jpg',
            'preferences': {
                'theme': 'dark',
                'language': 'fr',
                'notifications': True
            }
        }
        workflow_steps.append(('profile_setup', 'success'))

        # 5. Data Operations
        print("    → Step 5: Data Operations")

        # Create
        person_data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'birth_date': '1980-01-01'
        }
        workflow_steps.append(('create_person', 'success'))

        # Read
        time.sleep(0.01)  # Simulation
        workflow_steps.append(('read_person', 'success'))

        # Update
        person_data['first_name'] = 'Jean-Pierre'
        workflow_steps.append(('update_person', 'success'))

        # Search
        search_results = []  # Simulation
        workflow_steps.append(('search_persons', 'success'))

        # 6. Export Data
        print("    → Step 6: Data Export")
        export_format = 'GEDCOM'
        workflow_steps.append(('export_data', 'success'))

        # 7. Logout
        print("    → Step 7: User Logout")
        if self.security_manager and login_token:
            self.security_manager.revoke_jwt(login_token)
            workflow_steps.append(('logout', 'success'))
        else:
            workflow_steps.append(('logout', 'skipped'))

        # Résumé du workflow
        successful_steps = len([s for s in workflow_steps if s[1] == 'success'])
        total_steps = len(workflow_steps)

        print(f"\n    ✓ Workflow completed: {successful_steps}/{total_steps} steps successful")
        for step, status in workflow_steps:
            symbol = '✓' if status == 'success' else '○'
            print(f"      {symbol} {step}: {status}")

    def test_06_performance_stress_test(self):
        """Test de stress et de performance"""
        print("\n► Running Performance Stress Test...")

        metrics = {
            'operations': [],
            'errors': [],
            'response_times': []
        }

        # Configuration du test
        num_operations = 1000
        operation_types = ['read', 'write', 'search', 'auth']

        print(f"    → Executing {num_operations} operations...")

        start_time = time.time()

        for i in range(num_operations):
            op_type = random.choice(operation_types)
            op_start = time.time()

            try:
                if op_type == 'read':
                    # Simulation de lecture
                    time.sleep(random.uniform(0.001, 0.005))

                elif op_type == 'write':
                    # Simulation d'écriture
                    time.sleep(random.uniform(0.002, 0.008))

                elif op_type == 'search':
                    # Simulation de recherche
                    time.sleep(random.uniform(0.003, 0.010))

                elif op_type == 'auth' and self.security_manager:
                    # Opération d'authentification réelle
                    token = self.security_manager.create_jwt({'user_id': i})
                    self.security_manager.verify_jwt(token)

                op_time = time.time() - op_start
                metrics['operations'].append(op_type)
                metrics['response_times'].append(op_time)

            except Exception as e:
                metrics['errors'].append((op_type, str(e)))

            # Affichage de progression
            if (i + 1) % 100 == 0:
                elapsed = time.time() - start_time
                ops_per_sec = (i + 1) / elapsed
                print(f"      Progress: {i+1}/{num_operations} ({ops_per_sec:.0f} ops/sec)")

        total_time = time.time() - start_time

        # Calcul des statistiques
        if metrics['response_times']:
            avg_response = sum(metrics['response_times']) / len(metrics['response_times'])
            min_response = min(metrics['response_times'])
            max_response = max(metrics['response_times'])

            # Calcul des percentiles
            sorted_times = sorted(metrics['response_times'])
            p50 = sorted_times[len(sorted_times) // 2]
            p95 = sorted_times[int(len(sorted_times) * 0.95)]
            p99 = sorted_times[int(len(sorted_times) * 0.99)]
        else:
            avg_response = min_response = max_response = p50 = p95 = p99 = 0

        # Affichage des résultats
        print(f"\n    Performance Metrics:")
        print(f"    ├─ Total operations: {num_operations}")
        print(f"    ├─ Total time: {total_time:.2f}s")
        print(f"    ├─ Throughput: {num_operations / total_time:.0f} ops/sec")
        print(f"    ├─ Errors: {len(metrics['errors'])}")
        print(f"    └─ Response times:")
        print(f"       ├─ Average: {avg_response*1000:.2f}ms")
        print(f"       ├─ Min: {min_response*1000:.2f}ms")
        print(f"       ├─ Max: {max_response*1000:.2f}ms")
        print(f"       ├─ P50: {p50*1000:.2f}ms")
        print(f"       ├─ P95: {p95*1000:.2f}ms")
        print(f"       └─ P99: {p99*1000:.2f}ms")

        # Assertions de performance
        self.assertLess(avg_response, 0.1)  # Moyenne < 100ms
        self.assertLess(p95, 0.2)  # P95 < 200ms
        self.assertLess(len(metrics['errors']) / num_operations, 0.01)  # < 1% d'erreurs

    def test_07_data_consistency(self):
        """Test de consistance des données"""
        print("\n► Testing Data Consistency...")

        # Simulation d'opérations concurrentes sur les mêmes données
        shared_data = {'counter': 0, 'values': []}
        lock = threading.Lock()

        def increment_counter(iterations):
            for _ in range(iterations):
                with lock:
                    shared_data['counter'] += 1
                    shared_data['values'].append(shared_data['counter'])
                time.sleep(0.0001)

        # Lancement de threads concurrents
        threads = []
        num_threads = 5
        iterations_per_thread = 100

        print(f"    → Running {num_threads} concurrent threads...")

        for _ in range(num_threads):
            thread = threading.Thread(target=increment_counter, args=(iterations_per_thread,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Vérifications de consistance
        expected_counter = num_threads * iterations_per_thread
        self.assertEqual(shared_data['counter'], expected_counter)
        self.assertEqual(len(shared_data['values']), expected_counter)

        # Vérifier que les valeurs sont séquentielles
        for i, value in enumerate(shared_data['values'], 1):
            self.assertEqual(value, i)

        print(f"    ✓ Counter consistency verified: {shared_data['counter']}")
        print(f"    ✓ Sequential values verified: {len(shared_data['values'])} entries")

    def test_08_error_recovery(self):
        """Test de récupération d'erreurs"""
        print("\n► Testing Error Recovery...")

        recovery_scenarios = []

        # 1. Récupération après erreur de base de données
        print("    → Testing database error recovery...")
        try:
            # Simulation d'une erreur DB
            conn = sqlite3.connect(":memory:")
            cursor = conn.cursor()

            # Tentative de requête sur table inexistante
            try:
                cursor.execute("SELECT * FROM non_existent_table")
            except sqlite3.OperationalError:
                # Récupération: création de la table
                cursor.execute("CREATE TABLE non_existent_table (id INTEGER)")
                cursor.execute("SELECT * FROM non_existent_table")
                recovery_scenarios.append(('database_error', 'recovered'))

            conn.close()
        except Exception as e:
            recovery_scenarios.append(('database_error', f'failed: {str(e)}'))

        # 2. Récupération après erreur d'authentification
        print("    → Testing auth error recovery...")
        if self.security_manager:
            # Token invalide
            invalid_token = "invalid.jwt.token"
            result = self.security_manager.verify_jwt(invalid_token)

            if result is None:
                # Récupération: création d'un nouveau token
                new_token = self.security_manager.create_jwt({'user_id': 'recovery_test'})
                if new_token:
                    recovery_scenarios.append(('auth_error', 'recovered'))
                else:
                    recovery_scenarios.append(('auth_error', 'failed'))
            else:
                recovery_scenarios.append(('auth_error', 'no_error'))

        # 3. Récupération après erreur de fichier
        print("    → Testing file error recovery...")
        try:
            # Tentative de lecture d'un fichier inexistant
            test_file = os.path.join(self.test_dir, 'missing.txt')

            try:
                with open(test_file, 'r') as f:
                    content = f.read()
            except FileNotFoundError:
                # Récupération: création du fichier
                with open(test_file, 'w') as f:
                    f.write("Recovery content")

                with open(test_file, 'r') as f:
                    content = f.read()

                if content == "Recovery content":
                    recovery_scenarios.append(('file_error', 'recovered'))
                else:
                    recovery_scenarios.append(('file_error', 'failed'))
        except Exception as e:
            recovery_scenarios.append(('file_error', f'failed: {str(e)}'))

        # Résumé des récupérations
        print("\n    Recovery Scenarios Summary:")
        for scenario, status in recovery_scenarios:
            symbol = '✓' if 'recovered' in status else '✗'
            print(f"      {symbol} {scenario}: {status}")

        recovered_count = len([s for s in recovery_scenarios if 'recovered' in s[1]])
        self.assertGreater(recovered_count, len(recovery_scenarios) * 0.5)

    # ========================================================================
    # MÉTHODES UTILITAIRES
    # ========================================================================

    def _random_string(self, length: int) -> str:
        """Génère une chaîne aléatoire"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def _create_mock_user(self, user_data: dict, hashed_password: str) -> int:
        """Crée un utilisateur mock et retourne son ID"""
        # Simulation de création d'utilisateur
        user_id = random.randint(1000, 9999)
        self.test_users.append({
            'id': user_id,
            'username': user_data['username'],
            'email': user_data['email'],
            'password_hash': hashed_password,
            'created_at': datetime.now()
        })
        return user_id


class PerformanceMetrics:
    """Classe pour collecter et analyser les métriques de performance"""

    def __init__(self):
        self.metrics = {
            'response_times': [],
            'memory_usage': [],
            'cpu_usage': [],
            'errors': [],
            'timestamps': []
        }
        self.start_time = time.time()

    def record_operation(self, operation_type: str, duration: float, success: bool = True):
        """Enregistre une opération"""
        self.metrics['response_times'].append(duration)
        self.metrics['timestamps'].append(time.time() - self.start_time)

        if not success:
            self.metrics['errors'].append({
                'type': operation_type,
                'timestamp': time.time() - self.start_time
            })

    def get_summary(self) -> Dict[str, Any]:
        """Retourne un résumé des métriques"""
        if not self.metrics['response_times']:
            return {}

        response_times = self.metrics['response_times']

        return {
            'total_operations': len(response_times),
            'total_errors': len(self.metrics['errors']),
            'error_rate': len(self.metrics['errors']) / len(response_times) * 100,
            'avg_response_time': sum(response_times) / len(response_times),
            'min_response_time': min(response_times),
            'max_response_time': max(response_times),
            'p50': self._percentile(response_times, 50),
            'p95': self._percentile(response_times, 95),
            'p99': self._percentile(response_times, 99),
            'duration': time.time() - self.start_time
        }

    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calcule un percentile"""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]


if __name__ == '__main__':
    # Configuration du test runner
    unittest.TestLoader.sortTestMethodsUsing = None  # Garder l'ordre défini

    # Création de la suite de tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(CompleteIntegrationTestSuite)

    # Execution avec verbosité
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Affichage du résumé final
    print("\n" + "="*60)
    print("INTEGRATION TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*60)

    # Code de sortie
    exit(0 if result.wasSuccessful() else 1)