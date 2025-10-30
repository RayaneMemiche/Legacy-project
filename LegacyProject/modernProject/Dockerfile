# Multi-stage Dockerfile pour AWKWARD LEGACY
# Optimisé pour production avec image légère

# ============================================
# Stage 1: Builder - Installation dépendances
# ============================================
FROM python:3.12-slim as builder

LABEL maintainer="CoinLegacy Inc. <contact@coinlegacy.com>"
LABEL description="AWKWARD LEGACY - Modernisation GeneWeb"
LABEL version="1.0"

# Variables d'environnement pour le build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libc-dev \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Créer et activer environnement virtuel
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copier requirements
WORKDIR /build
COPY requirements.txt .

# Installer dépendances Python
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# ============================================
# Stage 2: Runtime - Image finale légère
# ============================================
FROM python:3.12-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    FLASK_APP=lib.wserver \
    FLASK_ENV=production \
    PORT=5000

# Installer runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Créer utilisateur non-root pour sécurité
RUN useradd -m -u 1000 -s /bin/bash awkward && \
    mkdir -p /app /app/data /app/logs && \
    chown -R awkward:awkward /app

# Copier le venv depuis builder
COPY --from=builder /opt/venv /opt/venv

# Définir workdir
WORKDIR /app

# Copier le code source
COPY --chown=awkward:awkward lib/ ./lib/
COPY --chown=awkward:awkward tests/ ./tests/
COPY --chown=awkward:awkward *.py ./
COPY --chown=awkward:awkward *.md ./
COPY --chown=awkward:awkward .env.example ./.env

# Créer les répertoires nécessaires
RUN mkdir -p /app/data/bases \
    /app/data/uploads \
    /app/logs \
    /app/static \
    /app/templates && \
    chown -R awkward:awkward /app

# Passer à l'utilisateur non-root
USER awkward

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Exposer le port
EXPOSE ${PORT}

# Script d'entrée
COPY --chown=awkward:awkward docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
