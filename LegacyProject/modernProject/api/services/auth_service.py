"""
Service pour l'authentification
"""

import sys
import os
from typing import Optional
from datetime import datetime, timedelta

# Ajouter le chemin des modules lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

try:
    from security import SecurityManager
    SECURITY_AVAILABLE = True
except ImportError:
    SECURITY_AVAILABLE = False
    print("⚠️ Module security non disponible")

from ..models.auth import UserCreate, UserResponse, Token


class AuthService:
    """Service pour l'authentification"""

    def __init__(self):
        self.users = {}  # email -> user data
        self.next_id = 1
        if SECURITY_AVAILABLE:
            self.security = SecurityManager.get_instance()

    def register(self, user: UserCreate) -> UserResponse:
        """Créer un nouveau compte utilisateur"""
        if user.email in self.users:
            raise ValueError("Un utilisateur avec cet email existe déjà")

        # Hasher le mot de passe
        if SECURITY_AVAILABLE:
            hashed_password = self.security.hash_password(user.password)
        else:
            hashed_password = user.password  # Dev uniquement

        user_id = str(self.next_id)
        self.next_id += 1

        user_data = {
            'id': user_id,
            'email': user.email,
            'full_name': user.full_name,
            'hashed_password': hashed_password,
            'is_active': True,
            'is_superuser': False,
            'created_at': datetime.now().isoformat()
        }

        self.users[user.email] = user_data

        return UserResponse(
            id=user_id,
            email=user.email,
            full_name=user.full_name,
            is_active=True,
            is_superuser=False,
            created_at=user_data['created_at']
        )

    def login(self, email: str, password: str) -> Optional[Token]:
        """Se connecter et obtenir un token"""
        user = self.users.get(email)
        if not user:
            return None

        # Vérifier le mot de passe
        if SECURITY_AVAILABLE:
            if not self.security.verify_password(password, user['hashed_password']):
                return None
        else:
            if password != user['hashed_password']:
                return None

        # Créer un token JWT
        if SECURITY_AVAILABLE:
            token_data = {
                'user_id': user['id'],
                'email': user['email'],
                'exp': (datetime.now() + timedelta(hours=24)).timestamp()
            }
            access_token = self.security.create_jwt(token_data)
        else:
            access_token = f"dev_token_{user['email']}"

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=86400
        )

    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Récupérer un utilisateur par son email"""
        user = self.users.get(email)
        if not user:
            return None

        return UserResponse(
            id=user['id'],
            email=user['email'],
            full_name=user.get('full_name'),
            is_active=user.get('is_active', True),
            is_superuser=user.get('is_superuser', False),
            created_at=user.get('created_at')
        )

    def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Récupérer un utilisateur par son ID"""
        for user_data in self.users.values():
            if user_data['id'] == user_id:
                return UserResponse(
                    id=user_data['id'],
                    email=user_data['email'],
                    full_name=user_data.get('full_name'),
                    is_active=user_data.get('is_active', True),
                    is_superuser=user_data.get('is_superuser', False),
                    created_at=user_data.get('created_at')
                )
        return None
