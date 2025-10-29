#!/bin/bash
# =================================================================
# AWKWARD LEGACY - Script de Déploiement Production
# =================================================================
# Description: Script complet de déploiement avec vérifications et rollback
# Version: 2.0
# Date: 17 Octobre 2025
# Usage: ./deploy.sh [options]
# =================================================================

set -e  # Exit on error
set -u  # Exit on undefined variable

# =================================================================
# CONFIGURATION
# =================================================================

# Couleurs pour output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

# Configuration du projet
readonly PROJECT_NAME="AWKWARD LEGACY"
readonly DOCKER_COMPOSE_FILE="docker-compose.yml"
readonly ENV_FILE=".env"
readonly BACKUP_DIR="./backups"
readonly LOG_DIR="./logs"
readonly MAX_HEALTH_CHECKS=30
readonly HEALTH_CHECK_INTERVAL=2
readonly DEPLOYMENT_TIMEOUT=300

# Timestamp pour logs et backups
readonly TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
readonly LOG_FILE="${LOG_DIR}/deploy_${TIMESTAMP}.log"

# =================================================================
# FONCTIONS UTILITAIRES
# =================================================================

# Logger avec horodatage
log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    case $level in
        ERROR)
            echo -e "${RED}[ERROR] ${timestamp}: ${message}${NC}" | tee -a "$LOG_FILE"
            ;;
        SUCCESS)
            echo -e "${GREEN}[SUCCESS] ${timestamp}: ${message}${NC}" | tee -a "$LOG_FILE"
            ;;
        WARNING)
            echo -e "${YELLOW}[WARNING] ${timestamp}: ${message}${NC}" | tee -a "$LOG_FILE"
            ;;
        INFO)
            echo -e "${CYAN}[INFO] ${timestamp}: ${message}${NC}" | tee -a "$LOG_FILE"
            ;;
        *)
            echo "[${timestamp}] ${message}" | tee -a "$LOG_FILE"
            ;;
    esac
}

# Vérifier le code de retour
check_result() {
    if [ $? -eq 0 ]; then
        log SUCCESS "$1"
        return 0
    else
        log ERROR "$2"
        return 1
    fi
}

# Fonction d'erreur avec cleanup
error_exit() {
    log ERROR "$1"
    cleanup_on_error
    exit 1
}

# Nettoyage en cas d'erreur
cleanup_on_error() {
    log WARNING "Nettoyage après erreur..."
    # Conserver les logs même en cas d'erreur
    if [ -f "$LOG_FILE" ]; then
        log INFO "Logs conservés dans: $LOG_FILE"
    fi
}

# Créer les répertoires nécessaires
create_directories() {
    log INFO "Création des répertoires..."
    mkdir -p "$BACKUP_DIR" "$LOG_DIR"
    check_result "Répertoires créés" "Échec création répertoires"
}

# =================================================================
# VÉRIFICATIONS PRÉ-DÉPLOIEMENT
# =================================================================

check_prerequisites() {
    log INFO "=== Vérification des prérequis ==="

    # Vérifier Docker
    if ! command -v docker &> /dev/null; then
        error_exit "Docker n'est pas installé"
    fi
    log SUCCESS "Docker: $(docker --version)"

    # Vérifier Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        if ! docker compose version &> /dev/null; then
            error_exit "Docker Compose n'est pas installé"
        fi
        COMPOSE_CMD="docker compose"
    else
        COMPOSE_CMD="docker-compose"
    fi
    log SUCCESS "Docker Compose: OK"

    # Vérifier les fichiers requis
    local required_files=("$DOCKER_COMPOSE_FILE" "$ENV_FILE" "nginx.conf")
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            error_exit "Fichier requis manquant: $file"
        fi
    done
    log SUCCESS "Tous les fichiers requis sont présents"

    # Vérifier l'espace disque
    local available_space=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "$available_space" -lt 5 ]; then
        log WARNING "Espace disque faible: ${available_space}GB disponible"
    else
        log SUCCESS "Espace disque: ${available_space}GB disponible"
    fi

    # Vérifier les ports
    local ports=(80 443 8080)
    for port in "${ports[@]}"; do
        if lsof -i :$port &> /dev/null; then
            log WARNING "Port $port déjà utilisé"
        fi
    done

    log SUCCESS "Prérequis vérifiés"
}

# =================================================================
# BACKUP
# =================================================================

perform_backup() {
    log INFO "=== Création du backup ==="

    local backup_file="${BACKUP_DIR}/backup_${TIMESTAMP}.tar.gz"

    # Identifier les volumes Docker à sauvegarder
    local volumes=$(docker volume ls --filter name=awkward -q)

    if [ -n "$volumes" ]; then
        log INFO "Sauvegarde des volumes Docker..."

        for volume in $volumes; do
            log INFO "Sauvegarde du volume: $volume"
            docker run --rm \
                -v "$volume":/data \
                -v "$(pwd)/$BACKUP_DIR":/backup \
                alpine tar czf "/backup/${volume}_${TIMESTAMP}.tar.gz" /data 2>> "$LOG_FILE"
        done

        log SUCCESS "Volumes sauvegardés"
    else
        log WARNING "Aucun volume à sauvegarder"
    fi

    # Sauvegarder la configuration
    log INFO "Sauvegarde de la configuration..."
    tar czf "${backup_file}" \
        --exclude='./backups' \
        --exclude='./logs' \
        --exclude='.git' \
        .env nginx.conf docker-compose.yml 2>> "$LOG_FILE"

    check_result "Configuration sauvegardée: $backup_file" "Échec de la sauvegarde"

    # Nettoyer les anciens backups (garder les 5 derniers)
    log INFO "Nettoyage des anciens backups..."
    ls -t1 "$BACKUP_DIR"/backup_*.tar.gz 2>/dev/null | tail -n +6 | xargs -r rm -f

    return 0
}

# =================================================================
# DÉPLOIEMENT
# =================================================================

pull_latest_code() {
    log INFO "=== Récupération du code ==="

    if [ -d ".git" ]; then
        log INFO "Pull des dernières modifications..."
        git fetch --all >> "$LOG_FILE" 2>&1
        git pull origin main >> "$LOG_FILE" 2>&1
        check_result "Code mis à jour" "Échec de la mise à jour du code"
    else
        log WARNING "Pas de repository Git détecté"
    fi
}

build_containers() {
    log INFO "=== Construction des conteneurs ==="

    log INFO "Construction des images Docker..."
    $COMPOSE_CMD build --no-cache --pull >> "$LOG_FILE" 2>&1
    check_result "Images construites avec succès" "Échec de la construction"

    # Tagguer l'image avec la version
    docker tag awkward-legacy:latest "awkward-legacy:${TIMESTAMP}" 2>> "$LOG_FILE"
    log SUCCESS "Image taguée: awkward-legacy:${TIMESTAMP}"
}

stop_old_containers() {
    log INFO "=== Arrêt des anciens conteneurs ==="

    if $COMPOSE_CMD ps | grep -q "Up"; then
        log INFO "Arrêt gracieux des conteneurs..."
        $COMPOSE_CMD down --timeout 30 >> "$LOG_FILE" 2>&1
        check_result "Conteneurs arrêtés" "Erreur lors de l'arrêt"
    else
        log INFO "Aucun conteneur en cours d'exécution"
    fi
}

start_new_containers() {
    log INFO "=== Démarrage des nouveaux conteneurs ==="

    log INFO "Démarrage des services..."
    $COMPOSE_CMD up -d >> "$LOG_FILE" 2>&1
    check_result "Services démarrés" "Échec du démarrage"

    # Attendre que les conteneurs soient prêts
    log INFO "Attente du démarrage complet..."
    sleep 5
}

# =================================================================
# HEALTH CHECKS
# =================================================================

perform_health_checks() {
    log INFO "=== Vérification de santé ==="

    local health_url="http://localhost:8080/health"
    local attempts=0

    log INFO "Vérification de l'endpoint de santé..."

    while [ $attempts -lt $MAX_HEALTH_CHECKS ]; do
        attempts=$((attempts + 1))

        if curl -sf "$health_url" > /dev/null 2>&1; then
            log SUCCESS "Application opérationnelle (tentative $attempts/$MAX_HEALTH_CHECKS)"

            # Vérifier le statut détaillé
            local health_status=$(curl -sf "$health_url" 2>/dev/null)
            log INFO "Statut de santé: $health_status"

            return 0
        fi

        log INFO "Tentative $attempts/$MAX_HEALTH_CHECKS..."
        sleep $HEALTH_CHECK_INTERVAL
    done

    log ERROR "L'application n'a pas démarré après $MAX_HEALTH_CHECKS tentatives"
    return 1
}

verify_deployment() {
    log INFO "=== Vérification du déploiement ==="

    # Vérifier que tous les conteneurs sont en cours d'exécution
    local expected_services=("web" "nginx" "redis" "postgres")
    local all_running=true

    for service in "${expected_services[@]}"; do
        if $COMPOSE_CMD ps | grep -q "${service}.*Up"; then
            log SUCCESS "Service $service: En cours d'exécution"
        else
            log ERROR "Service $service: Non démarré"
            all_running=false
        fi
    done

    if [ "$all_running" = false ]; then
        return 1
    fi

    # Vérifier les logs pour des erreurs
    log INFO "Vérification des logs pour erreurs..."
    if $COMPOSE_CMD logs --tail=50 2>&1 | grep -i "error\|critical\|fatal" > /dev/null; then
        log WARNING "Des erreurs ont été détectées dans les logs"
    else
        log SUCCESS "Aucune erreur critique dans les logs"
    fi

    return 0
}

# =================================================================
# ROLLBACK
# =================================================================

rollback_deployment() {
    log ERROR "=== Rollback du déploiement ==="

    # Arrêter les conteneurs défaillants
    log INFO "Arrêt des conteneurs actuels..."
    $COMPOSE_CMD down >> "$LOG_FILE" 2>&1

    # Restaurer l'image précédente si elle existe
    local previous_image=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep "awkward-legacy:" | grep -v "latest\|${TIMESTAMP}" | head -n1)

    if [ -n "$previous_image" ]; then
        log INFO "Restauration de l'image précédente: $previous_image"
        docker tag "$previous_image" awkward-legacy:latest

        # Redémarrer avec l'ancienne image
        log INFO "Redémarrage avec l'image précédente..."
        $COMPOSE_CMD up -d >> "$LOG_FILE" 2>&1

        if perform_health_checks; then
            log SUCCESS "Rollback réussi"
        else
            log ERROR "Rollback échoué - intervention manuelle requise"
        fi
    else
        log ERROR "Aucune image précédente disponible pour rollback"
    fi
}

# =================================================================
# NETTOYAGE POST-DÉPLOIEMENT
# =================================================================

cleanup_post_deployment() {
    log INFO "=== Nettoyage post-déploiement ==="

    # Nettoyer les images Docker non utilisées
    log INFO "Nettoyage des images non utilisées..."
    docker image prune -f >> "$LOG_FILE" 2>&1

    # Nettoyer les volumes non utilisés
    log INFO "Nettoyage des volumes non utilisés..."
    docker volume prune -f >> "$LOG_FILE" 2>&1

    # Garder seulement les 3 dernières images taguées
    log INFO "Nettoyage des anciennes images..."
    docker images --format "{{.Repository}}:{{.Tag}}" | \
        grep "awkward-legacy:" | \
        grep -v "latest" | \
        sort -r | \
        tail -n +4 | \
        xargs -r docker rmi 2>> "$LOG_FILE" || true

    log SUCCESS "Nettoyage terminé"
}

# =================================================================
# NOTIFICATIONS
# =================================================================

send_notification() {
    local status=$1
    local message=$2

    log INFO "Envoi de notification: $status"

    # Slack (si configuré)
    if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
        curl -X POST "$SLACK_WEBHOOK_URL" \
            -H 'Content-Type: application/json' \
            -d "{\"text\":\"${PROJECT_NAME} - Déploiement ${status}: ${message}\"}" \
            2>> "$LOG_FILE" || true
    fi

    # Email (si configuré)
    if [ -n "${NOTIFICATION_EMAIL:-}" ]; then
        echo "$message" | mail -s "${PROJECT_NAME} - Déploiement ${status}" "$NOTIFICATION_EMAIL" 2>> "$LOG_FILE" || true
    fi
}

# =================================================================
# AFFICHAGE DU STATUT
# =================================================================

display_status() {
    log INFO "=== Statut du déploiement ==="

    echo -e "\n${BLUE}╔════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}   ${GREEN}DÉPLOIEMENT TERMINÉ AVEC SUCCÈS${NC}         ${BLUE}║${NC}"
    echo -e "${BLUE}╠════════════════════════════════════════════╣${NC}"
    echo -e "${BLUE}║${NC} Timestamp: ${TIMESTAMP}                      ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC} Durée: ${SECONDS}s                           ${BLUE}║${NC}"
    echo -e "${BLUE}╠════════════════════════════════════════════╣${NC}"
    echo -e "${BLUE}║${NC} Services déployés:                         ${BLUE}║${NC}"

    $COMPOSE_CMD ps --format "table {{.Name}}\t{{.Status}}" | while read line; do
        echo -e "${BLUE}║${NC}  $line"
    done

    echo -e "${BLUE}╠════════════════════════════════════════════╣${NC}"
    echo -e "${BLUE}║${NC} URLs d'accès:                              ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}  - Application: https://awkward-legacy.com ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}  - Monitoring: http://localhost:9090       ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}  - Grafana: http://localhost:3000          ${BLUE}║${NC}"
    echo -e "${BLUE}╠════════════════════════════════════════════╣${NC}"
    echo -e "${BLUE}║${NC} Logs: $LOG_FILE                            ${BLUE}║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
}

# =================================================================
# FONCTION PRINCIPALE
# =================================================================

main() {
    local start_time=$(date +%s)

    echo -e "${CYAN}╔════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║     🚀 DÉPLOIEMENT ${PROJECT_NAME}          ║${NC}"
    echo -e "${CYAN}║        Version: 2.0                        ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════╝${NC}\n"

    # Créer les répertoires
    create_directories

    # Démarrer le logging
    log INFO "Début du déploiement: ${TIMESTAMP}"

    # Étapes du déploiement
    check_prerequisites || error_exit "Prérequis non satisfaits"
    perform_backup || log WARNING "Backup incomplet"
    pull_latest_code
    build_containers || error_exit "Construction échouée"
    stop_old_containers
    start_new_containers || error_exit "Démarrage échoué"

    # Vérifications
    if perform_health_checks; then
        if verify_deployment; then
            cleanup_post_deployment

            # Calculer la durée
            local end_time=$(date +%s)
            local duration=$((end_time - start_time))

            log SUCCESS "Déploiement réussi en ${duration} secondes"
            send_notification "SUCCESS" "Déploiement réussi en ${duration}s"
            display_status

            exit 0
        else
            log ERROR "Vérification du déploiement échouée"
        fi
    else
        log ERROR "Health checks échoués"
    fi

    # Si on arrive ici, le déploiement a échoué
    rollback_deployment
    send_notification "FAILED" "Déploiement échoué - Rollback effectué"
    error_exit "Déploiement échoué"
}

# =================================================================
# GESTION DES ARGUMENTS
# =================================================================

show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Script de déploiement pour ${PROJECT_NAME}

OPTIONS:
    -h, --help          Afficher cette aide
    -b, --backup-only   Effectuer uniquement un backup
    -s, --skip-backup   Ignorer l'étape de backup
    -f, --force         Forcer le déploiement sans confirmations
    -r, --rollback      Effectuer un rollback au déploiement précédent
    -c, --check         Vérifier les prérequis uniquement
    -v, --verbose       Mode verbose

EXEMPLES:
    $0                  # Déploiement standard
    $0 --backup-only    # Backup uniquement
    $0 --skip-backup    # Déploiement sans backup
    $0 --rollback       # Rollback au déploiement précédent

EOF
}

# Parser les arguments
SKIP_BACKUP=false
BACKUP_ONLY=false
FORCE_DEPLOY=false
ROLLBACK_ONLY=false
CHECK_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -b|--backup-only)
            BACKUP_ONLY=true
            shift
            ;;
        -s|--skip-backup)
            SKIP_BACKUP=true
            shift
            ;;
        -f|--force)
            FORCE_DEPLOY=true
            shift
            ;;
        -r|--rollback)
            ROLLBACK_ONLY=true
            shift
            ;;
        -c|--check)
            CHECK_ONLY=true
            shift
            ;;
        -v|--verbose)
            set -x
            shift
            ;;
        *)
            echo "Option inconnue: $1"
            show_help
            exit 1
            ;;
    esac
done

# =================================================================
# EXÉCUTION
# =================================================================

# Trap pour cleanup en cas d'interruption
trap cleanup_on_error EXIT

# Exécuter selon les options
if [ "$CHECK_ONLY" = true ]; then
    create_directories
    check_prerequisites
    exit $?
elif [ "$BACKUP_ONLY" = true ]; then
    create_directories
    perform_backup
    exit $?
elif [ "$ROLLBACK_ONLY" = true ]; then
    create_directories
    rollback_deployment
    exit $?
else
    # Demander confirmation si pas en mode force
    if [ "$FORCE_DEPLOY" = false ]; then
        echo -e "${YELLOW}Êtes-vous sûr de vouloir déployer? (yes/no)${NC}"
        read -r confirmation
        if [ "$confirmation" != "yes" ]; then
            echo "Déploiement annulé"
            exit 0
        fi
    fi

    main
fi