#!/bin/bash

# Script de lancement de tous les tests AWKWARD LEGACY
# Usage: ./run_all_tests.sh

set -e  # Arrêter en cas d'erreur

# Couleurs pour l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================"
echo "🧪 AWKWARD LEGACY - Tests Complets"
echo -e "======================================${NC}"
echo ""

# Vérifier qu'on est dans le bon dossier
if [ ! -d "lib" ]; then
    echo -e "${RED}❌ Erreur: Veuillez lancer ce script depuis le dossier modernProject${NC}"
    exit 1
fi

# Activer l'environnement virtuel si disponible
if [ -d "venv" ]; then
    echo -e "${GREEN}📦 Activation de l'environnement virtuel...${NC}"
    source venv/bin/activate
else
    echo -e "${YELLOW}⚠️  Pas d'environnement virtuel détecté${NC}"
fi

# Vérifier Python
echo -e "${BLUE}🐍 Vérification de Python...${NC}"
python3 --version

# Ajouter le chemin des modules
export PYTHONPATH="${PYTHONPATH}:$(pwd)/lib"

# Compteur de tests
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Fonction pour exécuter un test
run_test() {
    local test_name=$1
    local test_command=$2

    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}▶️  $test_name${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    if eval "$test_command"; then
        echo -e "${GREEN}✅ $test_name - PASSÉ${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}❌ $test_name - ÉCHOUÉ${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# 1. Tests des modules de base
run_test "Tests des Modules de Base" "python3 test_modules.py" || true

# 2. Tests de performance simplifiés
run_test "Tests de Performance Simplifiés" "python3 test_performance_simple.py" || true

# 3. Tests d'intégration (si pytest disponible)
if command -v pytest &> /dev/null; then
    run_test "Tests d'Intégration (Suite)" "python3 -m pytest tests/integration/test_integration_suite.py -v --tb=short" || true
    run_test "Tests d'Intégration (Complets)" "python3 -m pytest tests/integration/test_complete_integration.py -v --tb=short" || true
else
    echo -e "${YELLOW}⚠️  pytest non disponible, tests d'intégration ignorés${NC}"
fi

# 4. Tests de performance (benchmarks)
if [ -f "tests/performance/test_benchmarks.py" ]; then
    run_test "Tests de Performance (Benchmarks)" "python3 -m pytest tests/performance/test_benchmarks.py -v --tb=short" || true
fi

# 5. Tests de conformité RGPD
if [ -f "tests/compliance/rgpd_validator.py" ]; then
    run_test "Tests de Conformité RGPD" "python3 tests/compliance/rgpd_validator.py" || true
fi

# 6. Tests de sécurité
if [ -f "tests/security/security_scanner.py" ]; then
    run_test "Tests de Sécurité (Scanner OWASP)" "python3 tests/security/security_scanner.py" || true
fi

# 7. Vérification des fichiers de configuration
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📁 Vérification des Fichiers de Configuration${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

config_files=(
    ".pre-commit-config.yaml"
    ".pylintrc"
    "SECURITY.md"
    "CONTRIBUTING.md"
    "PRODUCTION_DEPLOYMENT_PLAN.md"
)

config_ok=true
for file in "${config_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}  ✅ $file${NC}"
    else
        echo -e "${RED}  ❌ $file non trouvé${NC}"
        config_ok=false
    fi
done

if $config_ok; then
    echo -e "${GREEN}✅ Fichiers de Configuration - PASSÉ${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}❌ Fichiers de Configuration - ÉCHOUÉ${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

# 8. Vérification des rapports
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📊 Vérification des Rapports${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

reports=(
    "../jour4_rapport.md"
    "../jour5_rapport.md"
    "../jour6_rapport.md"
)

reports_ok=true
for report in "${reports[@]}"; do
    if [ -f "$report" ]; then
        lines=$(wc -l < "$report")
        echo -e "${GREEN}  ✅ $report ($lines lignes)${NC}"
    else
        echo -e "${RED}  ❌ $report non trouvé${NC}"
        reports_ok=false
    fi
done

if $reports_ok; then
    echo -e "${GREEN}✅ Rapports - PASSÉ${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}❌ Rapports - ÉCHOUÉ${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

# Résumé final
echo ""
echo -e "${BLUE}======================================"
echo "📊 RÉSUMÉ DES TESTS"
echo -e "======================================${NC}"
echo ""
echo -e "Total de tests: ${BLUE}$TOTAL_TESTS${NC}"
echo -e "Tests réussis:  ${GREEN}$PASSED_TESTS${NC}"
echo -e "Tests échoués:  ${RED}$FAILED_TESTS${NC}"
echo ""

# Calcul du pourcentage
if [ $TOTAL_TESTS -gt 0 ]; then
    percentage=$((PASSED_TESTS * 100 / TOTAL_TESTS))
    echo -e "Taux de réussite: ${BLUE}$percentage%${NC}"
fi

echo ""
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}🎉 TOUS LES TESTS SONT PASSÉS!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  $FAILED_TESTS test(s) échoué(s)${NC}"
    exit 1
fi