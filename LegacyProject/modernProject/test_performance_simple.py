#!/usr/bin/env python3
"""Test de performance simplifié"""

import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def simulate_request(user_id):
    """Simule une requête utilisateur"""
    start = time.time()
    # Simulation de temps de traitement
    time.sleep(random.uniform(0.01, 0.05))
    duration = time.time() - start
    return {
        'user_id': user_id,
        'duration': duration,
        'success': random.random() > 0.01  # 99% de succès
    }

def run_performance_test(num_users=100, num_requests=5):
    """Execute un test de performance"""
    print(f"\n🚀 Test de Performance - {num_users} utilisateurs, {num_requests} requêtes chacun")
    print("-" * 60)
    
    results = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        
        for user_id in range(num_users):
            for req_id in range(num_requests):
                future = executor.submit(simulate_request, f"user_{user_id}_req_{req_id}")
                futures.append(future)
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            
            if len(results) % 100 == 0:
                print(f"  Progress: {len(results)}/{num_users * num_requests} requests")
    
    total_time = time.time() - start_time
    
    # Calcul des métriques
    durations = [r['duration'] for r in results]
    successes = sum(1 for r in results if r['success'])
    
    durations.sort()
    p50 = durations[len(durations) // 2]
    p95 = durations[int(len(durations) * 0.95)]
    p99 = durations[int(len(durations) * 0.99)]
    
    print(f"\n📊 Résultats:")
    print(f"  • Total requêtes: {len(results)}")
    print(f"  • Temps total: {total_time:.2f}s")
    print(f"  • Throughput: {len(results) / total_time:.1f} req/sec")
    print(f"  • Taux de succès: {successes / len(results) * 100:.1f}%")
    print(f"  • Latence P50: {p50 * 1000:.1f}ms")
    print(f"  • Latence P95: {p95 * 1000:.1f}ms")
    print(f"  • Latence P99: {p99 * 1000:.1f}ms")
    
    return {
        'total_requests': len(results),
        'total_time': total_time,
        'throughput': len(results) / total_time,
        'success_rate': successes / len(results) * 100,
        'p50': p50 * 1000,
        'p95': p95 * 1000,
        'p99': p99 * 1000
    }

if __name__ == "__main__":
    # Test avec charge croissante
    for num_users in [10, 50, 100]:
        metrics = run_performance_test(num_users, 5)
        
        if metrics['p95'] < 100 and metrics['success_rate'] > 98:
            print(f"  ✅ Test PASSÉ pour {num_users} utilisateurs\n")
        else:
            print(f"  ❌ Test ÉCHOUÉ pour {num_users} utilisateurs\n")
