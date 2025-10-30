#!/usr/bin/env python3
"""
Démonstration du système de gestion de personnes inspiré de GeneWeb
Système de cache à 3 couches: PENDING → COMMITTED → BASE
"""

import sys
import os

# Importer Database directement depuis lib en utilisant importlib
from importlib import import_module
from datetime import datetime

# Ajouter lib au path et importer
lib_path = os.path.join(os.path.dirname(__file__), 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

# Importer Database du module database
database_module = import_module('database')
Database = database_module.Database

def print_separator():
    print("\n" + "="*80 + "\n")

def demo_basic_operations():
    """Démonstration des opérations de base"""
    print("🚀 DÉMONSTRATION: Opérations de Base")
    print_separator()

    # Créer une instance de la base de données
    db = Database(base_name="demo")

    print("📊 État initial:")
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"  • {key}: {value}")

    print_separator()

    # Créer quelques personnes
    print("✏️  Création de personnes...")

    person1 = db.create_person({
        'first_name': 'Jean',
        'last_name': 'Dupont',
        'birth_date': '1990-01-15',
        'birth_place': 'Paris',
        'sex': 'M',
        'notes': 'Première personne de test'
    })
    print(f"✅ Personne créée: {person1['first_name']} {person1['last_name']} (ID: {person1['id']})")

    person2 = db.create_person({
        'first_name': 'Marie',
        'last_name': 'Martin',
        'birth_date': '1992-05-20',
        'birth_place': 'Lyon',
        'sex': 'F'
    })
    print(f"✅ Personne créée: {person2['first_name']} {person2['last_name']} (ID: {person2['id']})")

    person3 = db.create_person({
        'first_name': 'Pierre',
        'last_name': 'Dupont',
        'birth_date': '2015-03-10',
        'birth_place': 'Paris',
        'sex': 'M',
        'father_id': person1['id'],
        'mother_id': person2['id']
    })
    print(f"✅ Personne créée: {person3['first_name']} {person3['last_name']} (ID: {person3['id']})")

    print_separator()

    # État après création (PENDING)
    print("📊 État après création (dans PENDING, non committé):")
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"  • {key}: {value}")

    print_separator()

    # Lister toutes les personnes
    print("📋 Liste des personnes (PENDING):")
    all_persons = db.get_all_persons()
    for person in all_persons:
        if not person.get('_deleted'):
            print(f"  • {person['id']}: {person['first_name']} {person['last_name']} "
                  f"(né(e) le {person['birth_date']})")

    return db

def demo_commit_rollback(db):
    """Démonstration du commit et rollback"""
    print_separator()
    print("🔄 DÉMONSTRATION: Commit & Rollback")
    print_separator()

    # Commiter les modifications
    print("💾 Commit des modifications PENDING → COMMITTED...")
    db.commit()

    stats = db.get_statistics()
    print(f"\n📊 Après commit:")
    for key, value in stats.items():
        print(f"  • {key}: {value}")

    print_separator()

    # Créer une nouvelle personne (qui restera en PENDING)
    print("✏️  Création d'une nouvelle personne (restera en PENDING)...")
    person4 = db.create_person({
        'first_name': 'Sophie',
        'last_name': 'Bernard',
        'birth_date': '1988-12-25',
        'sex': 'F'
    })
    print(f"✅ Personne créée: {person4['first_name']} {person4['last_name']} (ID: {person4['id']})")

    stats = db.get_statistics()
    print(f"\n📊 Avec nouvelle personne en PENDING:")
    for key, value in stats.items():
        print(f"  • {key}: {value}")

    print_separator()

    # Rollback
    print("↩️  Rollback: annulation des modifications PENDING...")
    db.rollback()

    stats = db.get_statistics()
    print(f"\n📊 Après rollback (Sophie n'existe plus):")
    for key, value in stats.items():
        print(f"  • {key}: {value}")

    print(f"\nNombre de personnes visibles: {len(db.get_all_persons())}")

    return db

def demo_search_and_update(db):
    """Démonstration de la recherche et mise à jour"""
    print_separator()
    print("🔍 DÉMONSTRATION: Recherche & Mise à Jour")
    print_separator()

    # Recherche par nom
    print("🔍 Recherche de toutes les personnes nommées 'Dupont':")
    results = db.search_persons(last_name='Dupont')
    for person in results:
        print(f"  • {person['first_name']} {person['last_name']} (ID: {person['id']})")

    print_separator()

    # Recherche par prénom
    print("🔍 Recherche de toutes les personnes prénommées 'Marie':")
    results = db.search_persons(first_name='Marie')
    for person in results:
        print(f"  • {person['first_name']} {person['last_name']} (ID: {person['id']})")

    print_separator()

    # Mise à jour
    print("✏️  Mise à jour de Marie Martin...")
    updated = db.update_person('1', {
        'death_date': '2024-01-15',
        'death_place': 'Marseille',
        'notes': 'Décédée en 2024'
    })

    if updated:
        print(f"✅ Personne mise à jour:")
        print(f"  • Nom: {updated['first_name']} {updated['last_name']}")
        print(f"  • Décès: {updated['death_date']} à {updated['death_place']}")
        print(f"  • Notes: {updated['notes']}")

    stats = db.get_statistics()
    print(f"\n📊 Après mise à jour (en PENDING):")
    for key, value in stats.items():
        print(f"  • {key}: {value}")

    return db

def demo_three_layer_system():
    """Démonstration du système à 3 couches"""
    print_separator()
    print("🎯 DÉMONSTRATION: Système à 3 Couches (BASE → COMMITTED → PENDING)")
    print_separator()

    db = Database()

    # Simuler des données en BASE (données anciennes)
    print("1️⃣  COUCHE BASE: Ajout de données 'historiques'")
    db._base_persons = [
        {
            'id': '100',
            'first_name': 'Ancien',
            'last_name': 'Record',
            'birth_date': '1950-01-01',
            'sex': 'M'
        }
    ]
    db._next_person_id = 101
    print(f"  ✅ Personne en BASE: Ancien Record (ID: 100)")

    print_separator()

    # Créer une personne et la commiter (COMMITTED)
    print("2️⃣  COUCHE COMMITTED: Ajout et commit d'une personne")
    person1 = db.create_person({
        'first_name': 'Personne',
        'last_name': 'Committée',
        'birth_date': '1980-01-01',
        'sex': 'F'
    })
    db.commit()
    print(f"  ✅ Personne committée: Personne Committée (ID: {person1['id']})")

    print_separator()

    # Créer une personne en PENDING (non committée)
    print("3️⃣  COUCHE PENDING: Ajout d'une personne (non committée)")
    person2 = db.create_person({
        'first_name': 'Personne',
        'last_name': 'Pending',
        'birth_date': '2000-01-01',
        'sex': 'M'
    })
    print(f"  ✅ Personne en PENDING: Personne Pending (ID: {person2['id']})")

    print_separator()

    # Afficher toutes les couches
    print("📊 ÉTAT DES 3 COUCHES:")
    print(f"\n  🗄️  BASE (disque):")
    for p in db._base_persons:
        print(f"      • {p['first_name']} {p['last_name']} (ID: {p['id']})")

    print(f"\n  💾 COMMITTED (mémoire, sauvegardé):")
    for pid, p in db._committed_persons.items():
        print(f"      • {p['first_name']} {p['last_name']} (ID: {p['id']})")

    print(f"\n  ⏳ PENDING (mémoire, temporaire):")
    for pid, p in db._pending_persons.items():
        print(f"      • {p['first_name']} {p['last_name']} (ID: {p['id']})")

    print_separator()

    # Afficher le résultat merged
    print("🔍 VUE MERGÉE (ce que voit l'utilisateur):")
    all_persons = db.get_all_persons()
    for p in all_persons:
        layer = "BASE" if p['id'] == '100' else ("COMMITTED" if p['id'] == '101' else "PENDING")
        print(f"  • [{layer}] {p['first_name']} {p['last_name']} (ID: {p['id']})")

    print_separator()

    # Démontrer la priorité: PENDING > COMMITTED > BASE
    print("⚡ DÉMONSTRATION DE PRIORITÉ:")
    print("  Modification de 'Personne Committée' (ID: 101) en PENDING...")

    db.update_person('101', {
        'first_name': 'Personne Modifiée',
        'notes': 'Cette version est en PENDING et override COMMITTED'
    })

    print("\n  Résultat:")
    person_101 = db.get_person_by_id('101')
    print(f"    • Nom: {person_101['first_name']} {person_101['last_name']}")
    print(f"    • Notes: {person_101['notes']}")
    print(f"    • Source: PENDING (override COMMITTED)")

    stats = db.get_statistics()
    print(f"\n📊 Statistiques finales:")
    for key, value in stats.items():
        print(f"  • {key}: {value}")

def main():
    """Fonction principale"""
    print("\n" + "🌟"*40)
    print("  DÉMONSTRATION: Système de Base de Données GeneWeb")
    print("  Pattern: Cache à 3 Couches (PENDING → COMMITTED → BASE)")
    print("🌟"*40 + "\n")

    # Démo 1: Opérations de base
    db = demo_basic_operations()

    # Démo 2: Commit et Rollback
    db = demo_commit_rollback(db)

    # Démo 3: Recherche et mise à jour
    db = demo_search_and_update(db)

    # Démo 4: Système à 3 couches
    demo_three_layer_system()

    print_separator()
    print("✅ Démonstration terminée!")
    print("\n💡 Points clés:")
    print("  1. Les modifications vont d'abord dans PENDING (temporaire)")
    print("  2. commit() déplace PENDING → COMMITTED (sauvegarde)")
    print("  3. rollback() annule les modifications PENDING")
    print("  4. Priorité: PENDING > COMMITTED > BASE")
    print("  5. IDs auto-incrémentés (comme GeneWeb)")
    print("  6. String pooling avec déduplication automatique")
    print_separator()

if __name__ == "__main__":
    main()
