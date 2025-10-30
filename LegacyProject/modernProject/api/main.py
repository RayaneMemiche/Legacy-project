"""
API REST FastAPI pour AWKWARD LEGACY
Point d'entrée principal de l'application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os
from datetime import datetime

# Ajouter le chemin des modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

from .routers import (
    persons_router,
    families_router,
    auth_router,
    search_router,
    stats_router
)

# Créer l'application FastAPI
app = FastAPI(
    title="AWKWARD LEGACY API",
    description="""
    API REST moderne pour la gestion de données généalogiques.

    Basé sur GeneWeb et implémenté en Python avec FastAPI.

    ## Fonctionnalités

    * **Personnes** - CRUD complet pour les personnes
    * **Familles** - Gestion des relations familiales
    * **Recherche** - Recherche avancée avec filtres multiples
    * **Statistiques** - Analytics sur les données généalogiques
    * **Authentification** - JWT pour sécuriser l'accès

    ## Conformité

    * RGPD compliant
    * Tests exhaustifs (80%+ coverage)
    * Documentation complète
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configuration CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(auth_router, prefix="/api")
app.include_router(persons_router, prefix="/api")
app.include_router(families_router, prefix="/api")
app.include_router(search_router, prefix="/api")
app.include_router(stats_router, prefix="/api")


# Routes de base
@app.get("/")
async def root():
    """
    Page d'accueil de l'API
    """
    return {
        "message": "Bienvenue sur l'API AWKWARD LEGACY",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/api/health"
    }


@app.get("/api/health")
async def health_check():
    """
    Endpoint de santé pour le monitoring
    """
    return {
        "status": "healthy",
        "service": "AWKWARD LEGACY API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "development")
    }


# Gestionnaire d'erreurs global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Gestionnaire d'erreurs global pour capturer toutes les exceptions
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erreur interne du serveur",
            "detail": str(exc) if os.getenv("ENVIRONMENT") == "development" else "Une erreur est survenue"
        }
    )


# Événements de démarrage/arrêt
@app.on_event("startup")
async def startup_event():
    """
    Actions à effectuer au démarrage de l'application
    """
    print("=" * 80)
    print("🚀 AWKWARD LEGACY API - Démarrage")
    print("=" * 80)
    print(f"📍 Documentation: http://localhost:8000/docs")
    print(f"🔍 ReDoc: http://localhost:8000/redoc")
    print(f"🏥 Health check: http://localhost:8000/api/health")
    print(f"📊 Version: 1.0.0")
    print("=" * 80)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions à effectuer à l'arrêt de l'application
    """
    print("\n" + "=" * 80)
    print("🛑 AWKWARD LEGACY API - Arrêt")
    print("=" * 80)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
