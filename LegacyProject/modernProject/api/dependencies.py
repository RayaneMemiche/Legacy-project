"""
Dépendances pour l'injection de dépendances FastAPI
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import sys
import os

# Ajouter le chemin des modules lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

try:
    from security import SecurityManager
    SECURITY_AVAILABLE = True
except ImportError:
    SECURITY_AVAILABLE = False

from database import Database

from .services import (
    PersonService,
    FamilyService,
    AuthService,
    SearchService,
    StatsService
)
from .models.auth import UserResponse

# Schéma de sécurité
security_scheme = HTTPBearer(auto_error=False)


# Instance singleton de la base de données (PARTAGÉE par tous les services)
_database = None

def get_database() -> Database:
    """Obtenir l'instance unique partagée de la base de données"""
    global _database
    if _database is None:
        _database = Database()
        print("✅ Database singleton créée et partagée par tous les services")
    return _database


# Instances singleton des services
_person_service = None
_family_service = None
_auth_service = None
_search_service = None
_stats_service = None


def get_person_service() -> PersonService:
    """Obtenir une instance du service de personnes"""
    global _person_service
    if _person_service is None:
        _person_service = PersonService(get_database())
    return _person_service


def get_family_service() -> FamilyService:
    """Obtenir une instance du service de familles"""
    global _family_service
    if _family_service is None:
        _family_service = FamilyService(get_database())
    return _family_service


def get_auth_service() -> AuthService:
    """Obtenir une instance du service d'authentification"""
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthService()
    return _auth_service


def get_search_service() -> SearchService:
    """Obtenir une instance du service de recherche"""
    global _search_service
    if _search_service is None:
        _search_service = SearchService(get_database())
    return _search_service


def get_stats_service() -> StatsService:
    """Obtenir une instance du service de statistiques"""
    global _stats_service
    if _stats_service is None:
        _stats_service = StatsService(get_database())
    return _stats_service


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    """
    Obtenir l'utilisateur actuel à partir du token JWT
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Non authentifié",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    # Vérifier et décoder le token
    if SECURITY_AVAILABLE:
        security = SecurityManager.get_instance()
        try:
            payload = security.verify_jwt(token)
            user_id = payload.get('user_id')
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token invalide",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            user = auth_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Utilisateur non trouvé",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return user
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide ou expiré",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        # Mode développement: accepter n'importe quel token
        if token.startswith("dev_token_"):
            email = token.replace("dev_token_", "")
            user = auth_service.get_user_by_email(email)
            if user:
                return user

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Vérifier que l'utilisateur actuel est actif
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Utilisateur inactif"
        )
    return current_user
