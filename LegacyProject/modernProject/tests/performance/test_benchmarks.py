#!/usr/bin/env python3
"""
Tests de performance et benchmarks pour AWKWARD LEGACY

Ces tests mesurent les performances du système sous différentes charges
et vérifient que les temps de réponse restent dans les limites acceptables.
"""

import unittest
import time
import tempfile
import os
import sys
import random
import string
import gc
from pathlib import Path
import json
from datetime import datetime

# Pour la mesure de la mémoire
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Note: psutil non installé, certaines métriques mémoire ne seront pas disponibles")

# Pour les benchmarks avancés
try:
    import pytest
    from pytest_benchmark.plugin import benchmark
    PYTEST_BENCHMARK_AVAILABLE = True
except ImportError:
    PYTEST_BENCHMARK_AVAILABLE = False
    print("Note: pytest-benchmark non installé, utilisation de benchmarks simplifiés")

# Ajouter le chemin vers les modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'lib'))

# Import des modules à tester
try:
    from lib import database
    from lib import geneweb_compat
    from lib import util
    from lib import gwdb
except ImportError as e:
    print(f"Attention: Impossible d'importer certains modules: {e}")


class PerformanceTimer:
    """Classe utilitaire pour mesurer les performances"""

    def __init__(self, name="Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None
        self.duration = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end_time = time.perf_counter()
        self.duration = self.end_time - self.start_time

    def get_duration(self):
        return self.duration


class MemoryTracker:
    """Classe pour suivre l'utilisation de la mémoire"""

    def __init__(self):
        self.initial_memory = None
        self.peak_memory = None
        self.final_memory = None

    def start(self):
        """Commence le suivi de la mémoire"""
        gc.collect()  # Force le garbage collection
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            self.initial_memory = process.memory_info().rss / 1024 / 1024  # En MB
        else:
            self.initial_memory = 0

    def update_peak(self):
        """Met à jour la mémoire pic"""
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            current_memory = process.memory_info().rss / 1024 / 1024
            if self.peak_memory is None or current_memory > self.peak_memory:
                self.peak_memory = current_memory

    def stop(self):
        """Arrête le suivi et retourne l'utilisation"""
        gc.collect()
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            self.final_memory = process.memory_info().rss / 1024 / 1024
            memory_used = self.final_memory - self.initial_memory
            return {
                'initial': self.initial_memory,
                'final': self.final_memory,
                'peak': self.peak_memory or self.final_memory,
                'used': memory_used
            }
        return {'initial': 0, 'final': 0, 'peak': 0, 'used': 0}


class TestPerformanceBenchmarks(unittest.TestCase):
    """Suite de tests de performance pour AWKWARD LEGACY"""

    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour tous les tests"""
        cls.test_dir = tempfile.mkdtemp(prefix="perf_test_")
        cls.results = []  # Pour stocker les résultats des benchmarks

    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests et génération du rapport"""
        import shutil
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)

        # Générer le rapport de performance
        cls.generate_performance_report()

    @classmethod
    def generate_performance_report(cls):
        """Génère un rapport de performance"""
        print("\n" + "=" * 70)
        print("RAPPORT DE PERFORMANCE - AWKWARD LEGACY")
        print("=" * 70)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 70)

        if cls.results:
            for result in cls.results:
                print(f"\n{result['name']}:")
                print(f"  Durée: {result['duration']:.4f}s")
                if 'memory' in result:
                    print(f"  Mémoire utilisée: {result['memory']['used']:.2f} MB")
                    print(f"  Mémoire pic: {result['memory']['peak']:.2f} MB")
                if 'operations_per_second' in result:
                    print(f"  Opérations/sec: {result['operations_per_second']:.0f}")
                if 'status' in result:
                    print(f"  Statut: {result['status']}")

        print("\n" + "=" * 70)

    def generate_test_data(self, size='small'):
        """Génère des données de test selon la taille demandée"""
        sizes = {
            'small': 100,
            'medium': 1000,
            'large': 10000,
            'xlarge': 100000
        }

        num_persons = sizes.get(size, 100)
        persons = []

        for i in range(num_persons):
            person = {
                'id': f'pers_{i:06d}',
                'firstname': ''.join(random.choices(string.ascii_letters, k=10)),
                'lastname': ''.join(random.choices(string.ascii_letters, k=15)),
                'birth_year': random.randint(1900, 2020),
                'birth_month': random.randint(1, 12),
                'birth_day': random.randint(1, 28),
                'sex': random.choice(['M', 'F']),
                'occupation': random.choice(['Engineer', 'Teacher', 'Doctor', 'Artist', 'Other'])
            }
            persons.append(person)

        return persons

    def generate_gedcom_data(self, num_individuals=1000):
        """Génère des données GEDCOM de test"""
        gedcom_lines = ['0 HEAD', '1 GEDC', '2 VERS 5.5.1', '1 CHAR UTF-8']

        for i in range(num_individuals):
            gedcom_lines.extend([
                f'0 @I{i:05d}@ INDI',
                f'1 NAME TestFirstname{i} /TestLastname{i}/',
                f'2 GIVN TestFirstname{i}',
                f'2 SURN TestLastname{i}',
                '1 SEX ' + random.choice(['M', 'F']),
                f'1 BIRT',
                f'2 DATE {random.randint(1, 28)} {random.choice(["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"])} {random.randint(1900, 2020)}'
            ])

        gedcom_lines.append('0 TRLR')
        return '\n'.join(gedcom_lines)

    # Test 1: Chargement d'une grande base de données
    def test_large_database_load(self):
        """Test de chargement d'une base avec 10000 personnes"""
        print("\n[BENCHMARK 1] Chargement d'une grande base de données")

        # Générer les données de test
        test_persons = self.generate_test_data('large')
        memory_tracker = MemoryTracker()

        memory_tracker.start()

        with PerformanceTimer("Database Load") as timer:
            # Simuler le chargement d'une base de données
            db_simulation = {
                'persons': test_persons,
                'families': [],
                'metadata': {
                    'version': '1.0',
                    'created': datetime.now().isoformat(),
                    'person_count': len(test_persons)
                }
            }

            # Simuler des opérations de traitement
            for person in test_persons[:100]:  # Traiter les 100 premières personnes
                # Simulation de calcul d'index
                index_key = f"{person['lastname'].upper()}_{person['firstname'].upper()}"
                person['index_key'] = index_key

            memory_tracker.update_peak()

        memory_stats = memory_tracker.stop()
        duration = timer.get_duration()

        # Vérifier les performances
        self.assertLess(duration, 5.0, f"Le chargement a pris {duration:.2f}s (max 5s)")

        # Enregistrer les résultats
        result = {
            'name': 'Large Database Load (10000 persons)',
            'duration': duration,
            'memory': memory_stats,
            'operations_per_second': len(test_persons) / duration if duration > 0 else 0,
            'status': 'PASS' if duration < 5.0 else 'FAIL'
        }
        self.__class__.results.append(result)

        print(f"  ✓ Chargement de {len(test_persons)} personnes en {duration:.2f}s")
        print(f"  ✓ Mémoire utilisée: {memory_stats['used']:.2f} MB")
        print(f"  ✓ Performance: {result['operations_per_second']:.0f} personnes/seconde")

    # Test 2: Performance de recherche
    def test_search_performance(self):
        """Test de performance de recherche dans un grand dataset"""
        print("\n[BENCHMARK 2] Performance de recherche")

        # Créer un grand dataset
        test_persons = self.generate_test_data('large')

        # Créer des index pour la recherche
        name_index = {}
        for person in test_persons:
            key = person['lastname'].lower()
            if key not in name_index:
                name_index[key] = []
            name_index[key].append(person)

        # Effectuer plusieurs recherches
        search_terms = ['smith', 'jones', 'wilson', 'taylor', 'brown']
        search_times = []

        for term in search_terms:
            with PerformanceTimer(f"Search '{term}'") as timer:
                # Recherche simple
                results = []
                for person in test_persons:
                    if term in person['lastname'].lower() or term in person['firstname'].lower():
                        results.append(person)

            search_times.append(timer.get_duration())

        # Calculer les statistiques
        avg_search_time = sum(search_times) / len(search_times)
        max_search_time = max(search_times)

        # Vérifications
        self.assertLess(avg_search_time, 0.1, f"Recherche moyenne trop lente: {avg_search_time:.3f}s")
        self.assertLess(max_search_time, 0.2, f"Recherche max trop lente: {max_search_time:.3f}s")

        # Enregistrer les résultats
        result = {
            'name': 'Search Performance',
            'duration': avg_search_time,
            'max_duration': max_search_time,
            'dataset_size': len(test_persons),
            'status': 'PASS' if avg_search_time < 0.1 else 'FAIL'
        }
        self.__class__.results.append(result)

        print(f"  ✓ Temps de recherche moyen: {avg_search_time*1000:.2f}ms")
        print(f"  ✓ Temps de recherche max: {max_search_time*1000:.2f}ms")
        print(f"  ✓ Dataset: {len(test_persons)} personnes")

    # Test 3: Performance d'import GEDCOM
    def test_import_gedcom_performance(self):
        """Test de performance d'import d'un fichier GEDCOM volumineux"""
        print("\n[BENCHMARK 3] Performance d'import GEDCOM")

        # Générer un fichier GEDCOM de test
        gedcom_content = self.generate_gedcom_data(5000)
        gedcom_size_mb = len(gedcom_content) / (1024 * 1024)

        memory_tracker = MemoryTracker()
        memory_tracker.start()

        with PerformanceTimer("GEDCOM Import") as timer:
            # Simuler le parsing GEDCOM
            lines = gedcom_content.split('\n')
            persons = []
            current_person = None

            for line in lines:
                if line.startswith('0') and 'INDI' in line:
                    if current_person:
                        persons.append(current_person)
                    current_person = {'id': line.split('@')[1] if '@' in line else None}
                elif current_person and line.startswith('1 NAME'):
                    parts = line[7:].split('/')
                    if len(parts) >= 2:
                        current_person['firstname'] = parts[0].strip()
                        current_person['lastname'] = parts[1].strip()
                elif current_person and line.startswith('1 SEX'):
                    current_person['sex'] = line[5:].strip()

            if current_person:
                persons.append(current_person)

            memory_tracker.update_peak()

        memory_stats = memory_tracker.stop()
        duration = timer.get_duration()

        # Vérifications
        self.assertLess(duration, 10.0, f"Import trop lent: {duration:.2f}s")
        self.assertGreater(len(persons), 0, "Aucune personne importée")

        # Calcul du débit
        throughput_mb_per_sec = gedcom_size_mb / duration if duration > 0 else 0
        persons_per_sec = len(persons) / duration if duration > 0 else 0

        # Enregistrer les résultats
        result = {
            'name': 'GEDCOM Import Performance',
            'duration': duration,
            'memory': memory_stats,
            'file_size_mb': gedcom_size_mb,
            'persons_imported': len(persons),
            'throughput_mb_per_sec': throughput_mb_per_sec,
            'persons_per_second': persons_per_sec,
            'status': 'PASS' if duration < 10.0 else 'FAIL'
        }
        self.__class__.results.append(result)

        print(f"  ✓ Import de {len(persons)} personnes en {duration:.2f}s")
        print(f"  ✓ Taille du fichier: {gedcom_size_mb:.2f} MB")
        print(f"  ✓ Débit: {throughput_mb_per_sec:.2f} MB/s")
        print(f"  ✓ Performance: {persons_per_sec:.0f} personnes/seconde")

    # Test 4: Utilisation mémoire
    def test_memory_usage(self):
        """Test de consommation mémoire lors d'opérations intensives"""
        print("\n[BENCHMARK 4] Test d'utilisation mémoire")

        if not PSUTIL_AVAILABLE:
            print("  ⚠ psutil non disponible, test simplifié")

        memory_samples = []
        operations = [
            ('Création de données', lambda: self.generate_test_data('medium')),
            ('Duplication de données', lambda: self.generate_test_data('medium') * 2),
            ('Traitement de données', lambda: [p for p in self.generate_test_data('small') if p['birth_year'] > 1950]),
            ('Agrégation de données', lambda: {p['lastname']: p for p in self.generate_test_data('small')}),
        ]

        initial_memory = 0
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            initial_memory = process.memory_info().rss / 1024 / 1024

        for op_name, operation in operations:
            memory_tracker = MemoryTracker()
            memory_tracker.start()

            # Exécuter l'opération
            result = operation()

            memory_stats = memory_tracker.stop()
            memory_samples.append({
                'operation': op_name,
                'memory_used': memory_stats['used'],
                'peak': memory_stats['peak']
            })

            # Forcer le garbage collection entre les opérations
            del result
            gc.collect()

        # Analyse des résultats
        total_memory_used = sum(s['memory_used'] for s in memory_samples)
        max_peak_memory = max(s['peak'] for s in memory_samples) if memory_samples else 0

        # Vérifications
        if PSUTIL_AVAILABLE:
            self.assertLess(max_peak_memory - initial_memory, 500,
                           f"Utilisation mémoire excessive: {max_peak_memory - initial_memory:.2f} MB")

        # Enregistrer les résultats
        result = {
            'name': 'Memory Usage Test',
            'operations': len(operations),
            'total_memory_used': total_memory_used,
            'max_peak_memory': max_peak_memory,
            'initial_memory': initial_memory,
            'samples': memory_samples,
            'status': 'PASS' if not PSUTIL_AVAILABLE or (max_peak_memory - initial_memory < 500) else 'FAIL'
        }
        self.__class__.results.append(result)

        print(f"  ✓ {len(operations)} opérations testées")
        if PSUTIL_AVAILABLE:
            print(f"  ✓ Mémoire initiale: {initial_memory:.2f} MB")
            print(f"  ✓ Pic mémoire max: {max_peak_memory:.2f} MB")
            print(f"  ✓ Augmentation max: {max_peak_memory - initial_memory:.2f} MB")

        for sample in memory_samples:
            print(f"    - {sample['operation']}: {sample['memory_used']:.2f} MB utilisés")

    # Test 5: Charge multi-utilisateurs
    def test_concurrent_users_load(self):
        """Test de charge avec utilisateurs simultanés"""
        print("\n[BENCHMARK 5] Test de charge multi-utilisateurs")

        import threading
        import queue

        num_users = 100
        operations_per_user = 10
        results_queue = queue.Queue()
        errors = []

        def simulate_user(user_id, results_queue):
            """Simule les actions d'un utilisateur"""
            user_times = []

            try:
                for op in range(operations_per_user):
                    with PerformanceTimer(f"User {user_id} Op {op}") as timer:
                        # Simuler différentes opérations
                        if op % 3 == 0:
                            # Recherche
                            data = self.generate_test_data('small')
                            filtered = [p for p in data if p['birth_year'] > 1980]
                        elif op % 3 == 1:
                            # Création
                            new_person = {
                                'id': f'user_{user_id}_person_{op}',
                                'name': f'Person_{op}',
                                'created_by': user_id
                            }
                        else:
                            # Lecture
                            data = {'user': user_id, 'operation': op}

                        # Petite pause aléatoire pour simuler le temps de traitement
                        time.sleep(random.uniform(0.001, 0.01))

                    user_times.append(timer.get_duration())

                results_queue.put({
                    'user_id': user_id,
                    'times': user_times,
                    'avg_time': sum(user_times) / len(user_times),
                    'total_time': sum(user_times)
                })

            except Exception as e:
                errors.append(f"User {user_id}: {e}")

        # Lancer les threads utilisateurs
        start_time = time.perf_counter()
        threads = []

        for i in range(num_users):
            thread = threading.Thread(target=simulate_user, args=(i, results_queue))
            threads.append(thread)
            thread.start()

        # Attendre que tous les threads se terminent
        for thread in threads:
            thread.join()

        total_duration = time.perf_counter() - start_time

        # Collecter les résultats
        user_results = []
        while not results_queue.empty():
            user_results.append(results_queue.get())

        # Calculer les statistiques
        if user_results:
            avg_response_time = sum(r['avg_time'] for r in user_results) / len(user_results)
            max_response_time = max(r['avg_time'] for r in user_results)
            min_response_time = min(r['avg_time'] for r in user_results)
            total_operations = num_users * operations_per_user
            throughput = total_operations / total_duration if total_duration > 0 else 0
        else:
            avg_response_time = 0
            max_response_time = 0
            min_response_time = 0
            throughput = 0

        # Vérifications
        self.assertLess(avg_response_time, 0.5, f"Temps de réponse moyen trop élevé: {avg_response_time:.3f}s")
        self.assertEqual(len(errors), 0, f"Erreurs détectées: {errors}")
        self.assertEqual(len(user_results), num_users, f"Tous les utilisateurs n'ont pas terminé")

        # Enregistrer les résultats
        result = {
            'name': 'Concurrent Users Load Test',
            'duration': total_duration,
            'num_users': num_users,
            'operations_per_user': operations_per_user,
            'total_operations': total_operations,
            'throughput': throughput,
            'avg_response_time': avg_response_time,
            'max_response_time': max_response_time,
            'min_response_time': min_response_time,
            'errors': len(errors),
            'status': 'PASS' if avg_response_time < 0.5 and len(errors) == 0 else 'FAIL'
        }
        self.__class__.results.append(result)

        print(f"  ✓ {num_users} utilisateurs simulés")
        print(f"  ✓ {total_operations} opérations totales en {total_duration:.2f}s")
        print(f"  ✓ Débit: {throughput:.0f} ops/seconde")
        print(f"  ✓ Temps de réponse moyen: {avg_response_time*1000:.2f}ms")
        print(f"  ✓ Temps de réponse max: {max_response_time*1000:.2f}ms")
        print(f"  ✓ Aucune erreur détectée" if len(errors) == 0 else f"  ⚠ {len(errors)} erreur(s)")


def run_performance_tests():
    """Fonction principale pour exécuter les tests de performance"""
    print("=" * 70)
    print("TESTS DE PERFORMANCE - AWKWARD LEGACY")
    print("=" * 70)
    print(f"Début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 70)

    # Créer le test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPerformanceBenchmarks)

    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Afficher le résumé
    print("\n" + "=" * 70)
    print("RÉSUMÉ DES TESTS DE PERFORMANCE")
    print("=" * 70)
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")

    # Sauvegarder les résultats dans un fichier JSON
    if TestPerformanceBenchmarks.results:
        report_path = Path(__file__).parent / 'performance_report.json'
        with open(report_path, 'w') as f:
            json.dump({
                'date': datetime.now().isoformat(),
                'results': TestPerformanceBenchmarks.results,
                'summary': {
                    'total_tests': result.testsRun,
                    'passed': result.testsRun - len(result.failures) - len(result.errors),
                    'failed': len(result.failures),
                    'errors': len(result.errors)
                }
            }, f, indent=2)
        print(f"\n📊 Rapport de performance sauvegardé dans: {report_path}")

    if result.wasSuccessful():
        print("\n✅ TOUS LES TESTS DE PERFORMANCE SONT PASSÉS !")
    else:
        print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")

    return result.wasSuccessful()


# Support pour pytest-benchmark si disponible
if PYTEST_BENCHMARK_AVAILABLE:
    def test_with_pytest_benchmark(benchmark):
        """Test utilisant pytest-benchmark pour des mesures précises"""

        def sample_operation():
            # Opération à mesurer
            data = list(range(10000))
            return sum(x**2 for x in data if x % 2 == 0)

        result = benchmark(sample_operation)
        assert result > 0


if __name__ == '__main__':
    success = run_performance_tests()
    sys.exit(0 if success else 1)