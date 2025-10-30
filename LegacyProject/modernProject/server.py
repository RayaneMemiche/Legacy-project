#!/usr/bin/env python3
"""
Serveur API Flask pour AWKWARD LEGACY
Serveur de développement pour tester le frontend
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
from datetime import datetime, timedelta

# Ajouter le chemin des modules
sys.path.append('lib')

try:
    from security import SecurityManager
    security = SecurityManager.get_instance()
    SECURITY_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Module security non disponible: {e}")
    SECURITY_AVAILABLE = False

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])

# Base de données simulée pour le développement
USERS_DB = {}
PERSONS_DB = [
    {
        'id': '1',
        'firstName': 'Jean',
        'lastName': 'Martin',
        'birthDate': '1950-05-15',
        'birthPlace': 'Paris',
        'birthYear': 1950,
        'deathDate': None,
        'deathPlace': None,
        'deathYear': None,
        'father': None,
        'mother': None,
        'spouse': {'name': 'Marie Bernard'}
    },
    {
        'id': '2',
        'firstName': 'Marie',
        'lastName': 'Bernard',
        'birthDate': '1948-08-20',
        'birthPlace': 'Lyon',
        'birthYear': 1948,
        'deathDate': '2020-03-10',
        'deathPlace': 'Lyon',
        'deathYear': 2020,
        'father': None,
        'mother': None,
        'spouse': {'name': 'Jean Martin'}
    },
    {
        'id': '3',
        'firstName': 'Pierre',
        'lastName': 'Martin',
        'birthDate': '1975-03-12',
        'birthPlace': 'Paris',
        'birthYear': 1975,
        'deathDate': None,
        'deathPlace': None,
        'deathYear': None,
        'father': {'name': 'Jean Martin'},
        'mother': {'name': 'Marie Bernard'},
        'spouse': None
    },
    {
        'id': '4',
        'firstName': 'Sophie',
        'lastName': 'Martin',
        'birthDate': '1978-11-25',
        'birthPlace': 'Lyon',
        'birthYear': 1978,
        'deathDate': None,
        'deathPlace': None,
        'deathYear': None,
        'father': {'name': 'Jean Martin'},
        'mother': {'name': 'Marie Bernard'},
        'spouse': None
    },
    {
        'id': '5',
        'firstName': 'Jacques',
        'lastName': 'Dubois',
        'birthDate': '1920-01-10',
        'birthPlace': 'Marseille',
        'birthYear': 1920,
        'deathDate': '1995-06-20',
        'deathPlace': 'Marseille',
        'deathYear': 1995,
        'father': None,
        'mother': None,
        'spouse': None
    }
]

FAMILIES_DB = [
    {
        'id': '1',
        'father': 'Jean Martin',
        'mother': 'Marie Bernard',
        'children': ['Pierre Martin', 'Sophie Martin'],
        'marriageDate': '1972-06-15'
    }
]

# Routes de base
@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de la santé de l'API"""
    return jsonify({
        'status': 'healthy',
        'service': 'AWKWARD LEGACY API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'security_module': SECURITY_AVAILABLE
    })

# Routes d'authentification
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Connexion utilisateur"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email et mot de passe requis'}), 400

    # Simulation pour le développement
    if SECURITY_AVAILABLE:
        token = security.create_jwt({
            'user_id': 1,
            'email': email,
            'exp': (datetime.now() + timedelta(hours=24)).timestamp()
        })
    else:
        token = 'dev_token_' + email

    user_data = {
        'id': 1,
        'name': email.split('@')[0].title(),
        'email': email
    }

    # Sauvegarder l'utilisateur
    USERS_DB[email] = {
        'password': password,
        'data': user_data
    }

    return jsonify({
        'success': True,
        'token': token,
        'user': user_data
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Inscription utilisateur"""
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Tous les champs sont requis'}), 400

    # Vérifier si l'utilisateur existe déjà
    if email in USERS_DB:
        return jsonify({'error': 'Utilisateur déjà existant'}), 409

    # Hash du mot de passe
    if SECURITY_AVAILABLE:
        hashed = security.hash_password(password)
    else:
        hashed = password  # En développement uniquement !

    USERS_DB[email] = {
        'name': name,
        'email': email,
        'password': hashed
    }

    return jsonify({
        'success': True,
        'message': 'Utilisateur créé avec succès'
    })

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Déconnexion utilisateur"""
    return jsonify({
        'success': True,
        'message': 'Déconnexion réussie'
    })

@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    """Obtenir l'utilisateur actuel"""
    # Simuler l'authentification
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Non authentifié'}), 401

    return jsonify({
        'user': {
            'id': 1,
            'name': 'Test User',
            'email': 'test@example.com'
        }
    })

# Routes pour les personnes
@app.route('/api/persons', methods=['GET'])
def get_persons():
    """Liste de toutes les personnes"""
    return jsonify(PERSONS_DB)

@app.route('/api/persons/<person_id>', methods=['GET'])
def get_person(person_id):
    """Détails d'une personne"""
    person = next((p for p in PERSONS_DB if p['id'] == person_id), None)
    if not person:
        return jsonify({'error': 'Personne non trouvée'}), 404
    return jsonify(person)

@app.route('/api/persons/search', methods=['GET'])
def search_persons():
    """Recherche de personnes"""
    query = request.args.get('query', '').lower()
    first_name = request.args.get('firstName', '').lower()
    last_name = request.args.get('lastName', '').lower()
    birth_year = request.args.get('birthYear', '')
    death_year = request.args.get('deathYear', '')
    place = request.args.get('place', '').lower()

    results = PERSONS_DB

    # Filtrer par requête générale
    if query:
        results = [p for p in results if
                   query in p['firstName'].lower() or
                   query in p['lastName'].lower()]

    # Filtrer par prénom
    if first_name:
        results = [p for p in results if first_name in p['firstName'].lower()]

    # Filtrer par nom
    if last_name:
        results = [p for p in results if last_name in p['lastName'].lower()]

    # Filtrer par année de naissance
    if birth_year:
        results = [p for p in results if str(p.get('birthYear', '')) == birth_year]

    # Filtrer par année de décès
    if death_year:
        results = [p for p in results if str(p.get('deathYear', '')) == death_year]

    # Filtrer par lieu
    if place:
        results = [p for p in results if
                   (p.get('birthPlace') and place in p['birthPlace'].lower()) or
                   (p.get('deathPlace') and place in p['deathPlace'].lower())]

    return jsonify(results)

@app.route('/api/persons', methods=['POST'])
def create_person():
    """Créer une nouvelle personne"""
    data = request.get_json()
    new_id = str(len(PERSONS_DB) + 1)

    person = {
        'id': new_id,
        'firstName': data.get('firstName'),
        'lastName': data.get('lastName'),
        'birthDate': data.get('birthDate'),
        'birthPlace': data.get('birthPlace'),
        'birthYear': int(data.get('birthDate', '2000-01-01').split('-')[0]),
        'deathDate': data.get('deathDate'),
        'deathPlace': data.get('deathPlace'),
        'deathYear': int(data.get('deathDate').split('-')[0]) if data.get('deathDate') else None,
        'father': data.get('father'),
        'mother': data.get('mother'),
        'spouse': data.get('spouse')
    }

    PERSONS_DB.append(person)
    return jsonify(person), 201

# Routes pour les familles
@app.route('/api/families', methods=['GET'])
def get_families():
    """Liste de toutes les familles"""
    return jsonify(FAMILIES_DB)

@app.route('/api/families/<family_id>', methods=['GET'])
def get_family(family_id):
    """Détails d'une famille"""
    family = next((f for f in FAMILIES_DB if f['id'] == family_id), None)
    if not family:
        return jsonify({'error': 'Famille non trouvée'}), 404
    return jsonify(family)

# Routes pour l'arbre généalogique
@app.route('/api/tree/<person_id>', methods=['GET'])
def get_tree(person_id):
    """Générer l'arbre généalogique"""
    tree_type = request.args.get('type', 'full')
    generations = int(request.args.get('generations', 4))

    person = next((p for p in PERSONS_DB if p['id'] == person_id), None)
    if not person:
        return jsonify({'error': 'Personne non trouvée'}), 404

    # Simuler un arbre simple
    tree_data = {
        'root': person,
        'type': tree_type,
        'generations': generations,
        'ancestors': [],
        'descendants': []
    }

    return jsonify(tree_data)

# Routes pour les statistiques
@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Statistiques générales"""
    total_persons = len(PERSONS_DB)
    total_families = len(FAMILIES_DB)

    # Calculer les statistiques
    birth_years = [p['birthYear'] for p in PERSONS_DB if p['birthYear']]
    death_years = [p['deathYear'] for p in PERSONS_DB if p['deathYear']]

    century_distribution = {}
    for year in birth_years:
        century = f"{(year // 100) + 1}ème"
        century_distribution[century] = century_distribution.get(century, 0) + 1

    # Top noms de famille
    surname_counts = {}
    for person in PERSONS_DB:
        surname = person['lastName']
        surname_counts[surname] = surname_counts.get(surname, 0) + 1

    top_surnames = dict(sorted(surname_counts.items(), key=lambda x: x[1], reverse=True)[:10])

    return jsonify({
        'totalPersons': total_persons,
        'totalFamilies': total_families,
        'avgChildren': 2.0 if total_families > 0 else 0,
        'maxGenerations': 4,
        'lastUpdate': datetime.now().isoformat(),
        'centuryDistribution': century_distribution,
        'topSurnames': top_surnames
    })

# Routes pour l'activité
@app.route('/api/activity/recent', methods=['GET'])
def get_recent_activity():
    """Activité récente"""
    activities = [
        {
            'type': 'create',
            'description': 'Nouvelle personne ajoutée: Jean Martin',
            'timestamp': (datetime.now() - timedelta(hours=2)).isoformat()
        },
        {
            'type': 'update',
            'description': 'Modification de Marie Bernard',
            'timestamp': (datetime.now() - timedelta(hours=5)).isoformat()
        },
        {
            'type': 'view',
            'description': 'Consultation de l\'arbre de Pierre Martin',
            'timestamp': (datetime.now() - timedelta(hours=8)).isoformat()
        }
    ]

    return jsonify(activities)

# Routes RGPD
@app.route('/api/rgpd/export', methods=['POST'])
def export_user_data():
    """Exporter les données utilisateur"""
    return jsonify({
        'success': True,
        'data': {
            'user': {'id': 1, 'name': 'Test User'},
            'persons': PERSONS_DB,
            'families': FAMILIES_DB
        },
        'exportDate': datetime.now().isoformat()
    })

@app.route('/api/rgpd/delete', methods=['DELETE'])
def delete_user_data():
    """Supprimer les données utilisateur"""
    return jsonify({
        'success': True,
        'message': 'Données supprimées avec succès'
    })

# Gestion des erreurs
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Route non trouvée'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erreur serveur interne'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Démarrage du serveur API AWKWARD LEGACY")
    print("=" * 60)
    print(f"📍 API disponible sur: http://localhost:8000")
    print(f"🔗 Frontend à lancer sur: http://localhost:3000")
    print(f"🔒 Module Security: {'✅ Actif' if SECURITY_AVAILABLE else '⚠️  Non disponible'}")
    print(f"📊 Données de test: {len(PERSONS_DB)} personnes, {len(FAMILIES_DB)} familles")
    print("=" * 60)
    print("\nEndpoints disponibles:")
    print("  - GET  /api/health")
    print("  - POST /api/auth/login")
    print("  - POST /api/auth/register")
    print("  - GET  /api/persons")
    print("  - GET  /api/persons/search")
    print("  - GET  /api/families")
    print("  - GET  /api/tree/<id>")
    print("  - GET  /api/statistics")
    print("  - GET  /api/activity/recent")
    print("=" * 60)
    print("\nAppuyez sur Ctrl+C pour arrêter le serveur\n")

    app.run(host='0.0.0.0', port=8000, debug=True)