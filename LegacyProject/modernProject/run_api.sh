#!/bin/bash

# Script de démarrage de l'API REST AWKWARD LEGACY

echo "=========================================="
echo " AWKWARD LEGACY - Démarrage de l'API"
echo "=========================================="

# Vérifier si le venv existe
if [ ! -d "venv" ]; then
    echo "❌ Environnement virtuel non trouvé"
    echo "🔧 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer le venv
echo "🔌 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances si nécessaire
echo "📦 Vérification des dépendances..."
pip install -q -r ../requirements.txt

# Démarrer l'API
echo "🚀 Démarrage de l'API sur http://localhost:8000"
echo ""
echo "📖 Documentation disponible sur:"
echo "   - Swagger UI: http://localhost:8000/docs"
echo "   - ReDoc: http://localhost:8000/redoc"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo "=========================================="
echo ""

# Lancer uvicorn
cd api
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
