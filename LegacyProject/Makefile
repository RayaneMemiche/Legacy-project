.PHONY: all test test-modern coverage clean fclean re help install run-api run-flask test-api

help:
	@echo "=========================================="
	@echo "AWKWARD LEGACY - Available Makefile targets"
	@echo "=========================================="
	@echo ""
	@echo "🏗️  Build & Installation:"
	@echo "  install       - Install all dependencies"
	@echo ""
	@echo "🚀 Server Commands:"
	@echo "  run-api       - Start FastAPI server (port 8000)"
	@echo "  run-flask     - Start Flask dev server (port 8000)"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  all           - Default target, runs tests"
	@echo "  test          - Run all modernProject tests"
	@echo "  test-modern   - Run all modernProject tests"
	@echo "  test-api      - Run API-specific tests"
	@echo "  coverage      - Run tests with coverage report"
	@echo ""
	@echo "🧹 Cleanup:"
	@echo "  clean         - Remove test artifacts"
	@echo "  fclean        - Remove all generated files"
	@echo "  re            - Clean and run all tests"
	@echo ""
	@echo "=========================================="

all: test

test: test-modern coverage

test-modern:
	@echo "Running modernProject tests..."
	@PYTHONPATH=modernProject python -m pytest modernProject/tests/ -v

coverage:
	@if ! python3 -c "import pytest_cov" 2>/dev/null; then \
		echo "ERROR: pytest-cov not installed"; \
		echo "Install: sudo pacman -S python-pytest-cov"; \
		exit 1; \
	fi
	@echo "Running tests with coverage..."
	@PYTHONPATH=modernProject python -m pytest modernProject/tests/ -q --cov=modernProject/lib --cov-report=html:modernProject/htmlcov --cov-report=xml:coverage.xml --cov-report=term | grep -E "^(modernProject/lib/|TOTAL|passed|skipped|failed)"
	@echo ""
	@echo "HTML report: modernProject/htmlcov/index.html"

clean:
	@echo "Cleaning test artifacts..."
	-find . -type d -name __pycache__ -exec rm -rf {} +
	-find . -type f -name "*.pyc" -delete
	-rm -f modernProject/coverage.xml modernProject/.coverage
	-rm -rf modernProject/htmlcov/

fclean: clean
	@echo "Deep cleaning..."
	-find . -type d -name "*.egg-info" -exec rm -rf {} +
	-find . -type d -name ".pytest_cache" -exec rm -rf {} +
	-rm -rf htmlcov/

re: fclean all

# Installation des dépendances
install:
	@echo "📦 Installation des dépendances..."
	@if [ ! -d "modernProject/venv" ]; then \
		echo "🔧 Création de l'environnement virtuel..."; \
		python3 -m venv modernProject/venv; \
	fi
	@echo "📥 Installation des packages Python..."
	@modernProject/venv/bin/pip install -q --upgrade pip
	@modernProject/venv/bin/pip install -q -r requirements.txt
	@echo "✅ Installation terminée!"

# Démarrer l'API FastAPI
run-api:
	@echo "🚀 Démarrage de l'API FastAPI..."
	@if [ ! -d "modernProject/venv" ]; then \
		echo "❌ Environnement virtuel non trouvé. Exécutez 'make install' d'abord."; \
		exit 1; \
	fi
	@echo "📍 API disponible sur: http://localhost:8000"
	@echo "📖 Documentation: http://localhost:8000/docs"
	@echo ""
	@cd modernProject && venv/bin/python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Démarrer le serveur Flask (legacy)
run-flask:
	@echo "🚀 Démarrage du serveur Flask (dev)..."
	@if [ ! -d "modernProject/venv" ]; then \
		echo "❌ Environnement virtuel non trouvé. Exécutez 'make install' d'abord."; \
		exit 1; \
	fi
	@echo "📍 API disponible sur: http://localhost:8000"
	@cd modernProject && venv/bin/python server.py

# Tests spécifiques à l'API
test-api:
	@echo "🧪 Running API tests..."
	@if [ -d "modernProject/tests/api" ]; then \
		PYTHONPATH=modernProject python -m pytest modernProject/tests/api/ -v; \
	else \
		echo "⚠️  No API tests found yet"; \
	fi
