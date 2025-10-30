#!/bin/bash
# Script de démonstration de l'API pour l'ajout de personnes

echo "=================================="
echo "  DÉMONSTRATION API - Ajout de Personnes"
echo "=================================="
echo ""

# Couleurs
GREEN='\033[0.32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

API_URL="http://localhost:8000/api"

echo "🔍 1. Vérifier l'état de l'API..."
echo ""
curl -s "${API_URL}/health" | python3 -m json.tool
echo ""

echo "=================================="
echo "📊 2. Statistiques initiales"
echo "=================================="
echo ""
curl -s "${API_URL}/statistics/" | python3 -m json.tool
echo ""

echo "=================================="
echo "✏️  3. Créer une première personne (Jean Dupont)"
echo "=================================="
echo ""
curl -X POST "${API_URL}/persons/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jean",
    "last_name": "Dupont",
    "birth_date": "1990-01-15",
    "birth_place": "Paris",
    "sex": "M"
  }' | python3 -m json.tool
echo ""

echo "=================================="
echo "✏️  4. Créer une deuxième personne (Marie Martin)"
echo "=================================="
echo ""
curl -X POST "${API_URL}/persons/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Marie",
    "last_name": "Martin",
    "birth_date": "1992-05-20",
    "birth_place": "Lyon",
    "sex": "F"
  }' | python3 -m json.tool
echo ""

echo "=================================="
echo "✏️  5. Créer une troisième personne (Pierre Dupont, enfant)"
echo "=================================="
echo ""
curl -X POST "${API_URL}/persons/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Pierre",
    "last_name": "Dupont",
    "birth_date": "2015-03-10",
    "birth_place": "Paris",
    "sex": "M",
    "father_id": "0",
    "mother_id": "1"
  }' | python3 -m json.tool
echo ""

echo "=================================="
echo "📋 6. Lister toutes les personnes"
echo "=================================="
echo ""
curl -s "${API_URL}/persons/" | python3 -m json.tool
echo ""

echo "=================================="
echo "🔍 7. Rechercher les personnes nommées 'Dupont'"
echo "=================================="
echo ""
curl -s "${API_URL}/search/?last_name=Dupont" | python3 -m json.tool
echo ""

echo "=================================="
echo "📊 8. Statistiques après ajout"
echo "=================================="
echo ""
curl -s "${API_URL}/statistics/" | python3 -m json.tool
echo ""

echo "=================================="
echo "✅ Démonstration terminée!"
echo "=================================="
echo ""
echo "💡 Points clés:"
echo "  • IDs auto-incrémentés: 0, 1, 2, ..."
echo "  • Système 3 couches: PENDING → COMMITTED → BASE"
echo "  • Les personnes sont en PENDING (non committées)"
echo ""
echo "📖 Pour commiter les changements:"
echo "  db.commit()  # En Python"
echo ""
