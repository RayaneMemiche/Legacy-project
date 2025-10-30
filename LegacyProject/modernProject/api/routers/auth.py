"""
Router pour l'authentification
"""

from fastapi import APIRouter, HTTPException, status, Depends
from ..models.auth import UserCreate, UserLogin, UserResponse, Token
from ..services.auth_service import AuthService
from ..dependencies import get_auth_service, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user: UserCreate,
    service: AuthService = Depends(get_auth_service)
):
    """
    Créer un nouveau compte utilisateur
    """
    try:
        new_user = service.register(user)
        return new_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    service: AuthService = Depends(get_auth_service)
):
    """
    Se connecter et obtenir un token JWT
    """
    token = service.login(credentials.email, credentials.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """
    Obtenir les informations de l'utilisateur connecté
    """
    return current_user


@router.post("/logout")
async def logout():
    """
    Se déconnecter (côté client, supprimer le token)
    """
    return {"message": "Déconnexion réussie"}
