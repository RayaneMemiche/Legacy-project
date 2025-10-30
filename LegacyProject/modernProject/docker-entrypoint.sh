#!/bin/bash
# Docker entrypoint script pour AWKWARD LEGACY
set -e

echo "========================================="
echo "🚀 AWKWARD LEGACY - Starting..."
echo "========================================="

# Afficher les informations de version
echo "Python version: $(python --version)"
echo "Flask version: $(python -c 'import flask; print(flask.__version__)')"
echo "Working directory: $(pwd)"
echo "User: $(whoami)"

# Créer les répertoires nécessaires s'ils n'existent pas
mkdir -p /app/data/bases /app/data/uploads /app/logs

# Vérifier les permissions
echo "Checking permissions..."
if [ ! -w /app/logs ]; then
    echo "⚠️  Warning: /app/logs is not writable"
fi

# Charger les variables d'environnement
if [ -f .env ]; then
    echo "Loading environment variables from .env"
    export $(cat .env | grep -v '^#' | xargs)
fi

# Configuration Flask selon l'environnement
if [ "${FLASK_ENV}" = "production" ]; then
    echo "🏭 Running in PRODUCTION mode"
    export FLASK_DEBUG=0
else
    echo "🔧 Running in DEVELOPMENT mode"
    export FLASK_DEBUG=1
fi

# Attendre que la base de données soit prête (si utilisée)
if [ -n "${DATABASE_URL}" ]; then
    echo "Waiting for database to be ready..."

    # Extraire host et port de DATABASE_URL
    DB_HOST=$(echo $DATABASE_URL | sed -e 's/.*@\(.*\):.*/\1/')
    DB_PORT=$(echo $DATABASE_URL | sed -e 's/.*:\([0-9]*\)\/.*/\1/')

    MAX_TRIES=30
    COUNT=0

    while ! nc -z $DB_HOST $DB_PORT 2>/dev/null; do
        COUNT=$((COUNT + 1))
        if [ $COUNT -ge $MAX_TRIES ]; then
            echo "❌ Database not available after $MAX_TRIES attempts"
            exit 1
        fi
        echo "Waiting for database... ($COUNT/$MAX_TRIES)"
        sleep 2
    done

    echo "✅ Database is ready!"
fi

# Initialiser la base de données si nécessaire
if [ "${RUN_MIGRATIONS}" = "true" ]; then
    echo "Running database migrations..."
    python -c "from lib import database; print('Database initialized')" || echo "⚠️  Migration skipped"
fi

# Afficher la configuration
echo "========================================="
echo "Configuration:"
echo "  - Flask App: ${FLASK_APP}"
echo "  - Environment: ${FLASK_ENV}"
echo "  - Port: ${PORT:-5000}"
echo "  - Debug: ${FLASK_DEBUG}"
echo "========================================="

# Sanity check - vérifier que l'app Flask existe
if ! python -c "from lib import wserver" 2>/dev/null; then
    echo "❌ Error: Cannot import lib.wserver"
    exit 1
fi

echo "✅ All checks passed!"
echo "🚀 Starting Flask application..."
echo "========================================="

# Exécuter la commande passée en argument
exec "$@"
