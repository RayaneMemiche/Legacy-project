"""
Modèles Pydantic pour l'authentification
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Modèle de base pour un utilisateur"""

    email: EmailStr = Field(..., description="Email de l'utilisateur")
    full_name: Optional[str] = Field(None, max_length=100, description="Nom complet")


class UserCreate(UserBase):
    """Modèle pour la création d'un utilisateur"""

    password: str = Field(..., min_length=8, max_length=100, description="Mot de passe")


class UserLogin(BaseModel):
    """Modèle pour la connexion"""

    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Modèle de réponse pour un utilisateur"""

    id: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: Optional[str] = None


class Token(BaseModel):
    """Modèle de token JWT"""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = 86400


class TokenData(BaseModel):
    """Données contenues dans le token"""

    user_id: Optional[str] = None
    email: Optional[str] = None
