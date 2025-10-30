#!/usr/bin/env python3
"""
Module de Sécurité - AWKWARD LEGACY

Ce module fournit toutes les fonctionnalités de sécurité pour l'application :
- Authentification (JWT)
- Hashage des mots de passe (PBKDF2/Bcrypt/Argon2)
- Chiffrement des données (AES-256-GCM)
- Contrôle d'accès (RBAC)
- Protection CSRF
- Rate limiting
- Audit et logging de sécurité
- Validation et sanitization des entrées

Version: 1.0
Date: 17 Octobre 2025
"""

import hashlib
import secrets
import hmac
import time
import json
import logging
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from functools import wraps
from enum import Enum
from dataclasses import dataclass, field
import threading
from collections import defaultdict

# Imports cryptographiques
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    from cryptography.hazmat.backends import default_backend
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("Warning: cryptography package not installed, some features will be limited")

# JWT
try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    print("Warning: PyJWT not installed, JWT features disabled")

# Bcrypt pour hashage de mots de passe
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False

# Argon2 (plus sécurisé que bcrypt)
try:
    from argon2 import PasswordHasher, VerifyMismatchError
    from argon2.exceptions import VerificationError, InvalidHash
    ARGON2_AVAILABLE = True
except ImportError:
    ARGON2_AVAILABLE = False

# Configuration du logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# =================================================================
# CONSTANTES DE SÉCURITÉ
# =================================================================

# Algorithmes de hashage
class HashAlgorithm(Enum):
    """Algorithmes de hashage supportés"""
    PBKDF2_SHA256 = "pbkdf2_sha256"
    BCRYPT = "bcrypt"
    ARGON2 = "argon2"
    SHA256 = "sha256"
    SHA512 = "sha512"

# Rôles utilisateur
class UserRole(Enum):
    """Rôles utilisateur pour RBAC"""
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"
    SUPPORT = "support"
    AUDIT = "audit"
    GUEST = "guest"

# Permissions
class Permission(Enum):
    """Permissions système"""
    # Données personnelles
    READ_OWN_DATA = "read_own_data"
    WRITE_OWN_DATA = "write_own_data"
    DELETE_OWN_DATA = "delete_own_data"

    # Données globales
    READ_ALL_DATA = "read_all_data"
    WRITE_ALL_DATA = "write_all_data"
    DELETE_ALL_DATA = "delete_all_data"

    # Administration
    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"
    VIEW_LOGS = "view_logs"
    SYSTEM_CONFIG = "system_config"

    # Actions spécifiques
    EXPORT_DATA = "export_data"
    IMPORT_DATA = "import_data"
    BACKUP_DATA = "backup_data"

# Mapping rôles -> permissions
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [p for p in Permission],  # Toutes les permissions
    UserRole.USER: [
        Permission.READ_OWN_DATA,
        Permission.WRITE_OWN_DATA,
        Permission.DELETE_OWN_DATA,
        Permission.EXPORT_DATA,
    ],
    UserRole.MODERATOR: [
        Permission.READ_OWN_DATA,
        Permission.WRITE_OWN_DATA,
        Permission.READ_ALL_DATA,
        Permission.WRITE_ALL_DATA,
    ],
    UserRole.SUPPORT: [
        Permission.READ_ALL_DATA,
        Permission.VIEW_LOGS,
    ],
    UserRole.AUDIT: [
        Permission.READ_ALL_DATA,
        Permission.VIEW_LOGS,
    ],
    UserRole.GUEST: [
        Permission.READ_OWN_DATA,
    ],
}

# =================================================================
# CLASSES DE DONNÉES
# =================================================================

@dataclass
class User:
    """Modèle utilisateur pour la sécurité"""
    id: str
    username: str
    email: str
    role: UserRole
    permissions: List[Permission] = field(default_factory=list)
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    two_factor_enabled: bool = False
    two_factor_secret: Optional[str] = None

@dataclass
class Session:
    """Modèle de session utilisateur"""
    id: str
    user_id: str
    token: str
    created_at: datetime
    expires_at: datetime
    ip_address: str
    user_agent: str
    is_active: bool = True

@dataclass
class AuditLog:
    """Modèle de log d'audit"""
    id: str
    timestamp: datetime
    user_id: Optional[str]
    action: str
    resource: str
    ip_address: str
    user_agent: str
    success: bool
    details: Dict[str, Any]

# =================================================================
# GESTIONNAIRE DE SÉCURITÉ PRINCIPAL
# =================================================================

class SecurityManager:
    """
    Gestionnaire principal de sécurité pour AWKWARD LEGACY
    Centralise toutes les fonctionnalités de sécurité
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialise le gestionnaire de sécurité

        Args:
            config: Configuration de sécurité
        """
        self.config = config or {}

        # Clés secrètes
        self.secret_key = self.config.get('SECRET_KEY', secrets.token_hex(32))
        self.jwt_secret = self.config.get('JWT_SECRET', secrets.token_hex(32))
        self.encryption_key = self.config.get('ENCRYPTION_KEY')

        # Configuration
        self.jwt_algorithm = self.config.get('JWT_ALGORITHM', 'HS256')
        self.jwt_expiration = self.config.get('JWT_EXPIRATION', 3600)  # 1 heure
        self.bcrypt_rounds = self.config.get('BCRYPT_ROUNDS', 12)
        self.pbkdf2_iterations = self.config.get('PBKDF2_ITERATIONS', 100000)

        # Rate limiting
        self.max_login_attempts = self.config.get('MAX_LOGIN_ATTEMPTS', 5)
        self.lockout_duration = self.config.get('LOCKOUT_DURATION', 900)  # 15 minutes

        # Stockage en mémoire (à remplacer par une vraie DB)
        self.sessions = {}
        self.users = {}
        self.audit_logs = []
        self.rate_limits = defaultdict(list)

        # Initialiser les composants
        self._init_password_hasher()
        self._init_encryptor()

        logger.info("SecurityManager initialized")

    def _init_password_hasher(self):
        """Initialise le hasheur de mots de passe"""
        if ARGON2_AVAILABLE:
            self.password_hasher = PasswordHasher(
                time_cost=2,
                memory_cost=65536,
                parallelism=1,
                hash_len=32,
                salt_len=16
            )
            self.hash_algorithm = HashAlgorithm.ARGON2
        elif BCRYPT_AVAILABLE:
            self.hash_algorithm = HashAlgorithm.BCRYPT
        else:
            self.hash_algorithm = HashAlgorithm.PBKDF2_SHA256

    def _init_encryptor(self):
        """Initialise le système de chiffrement"""
        if CRYPTO_AVAILABLE and self.encryption_key:
            if len(self.encryption_key) == 44:  # Fernet key
                self.fernet = Fernet(self.encryption_key.encode())
            else:
                # AES-GCM
                self.aes_key = hashlib.sha256(self.encryption_key.encode()).digest()
                self.aesgcm = AESGCM(self.aes_key)
        else:
            self.fernet = None
            self.aesgcm = None

    # =================================================================
    # HASHAGE DE MOTS DE PASSE
    # =================================================================

    def hash_password(self, password: str) -> str:
        """
        Hash un mot de passe avec l'algorithme le plus sécurisé disponible

        Args:
            password: Mot de passe en clair

        Returns:
            Hash du mot de passe
        """
        if not password:
            raise ValueError("Password cannot be empty")

        if self.hash_algorithm == HashAlgorithm.ARGON2 and ARGON2_AVAILABLE:
            return self.password_hasher.hash(password)

        elif self.hash_algorithm == HashAlgorithm.BCRYPT and BCRYPT_AVAILABLE:
            salt = bcrypt.gensalt(rounds=self.bcrypt_rounds)
            return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

        else:  # PBKDF2_SHA256 (fallback)
            salt = secrets.token_hex(16)
            pwd_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                self.pbkdf2_iterations
            )
            return f"pbkdf2_sha256${salt}${pwd_hash.hex()}"

    def verify_password(self, password: str, hash_string: str) -> bool:
        """
        Vérifie un mot de passe contre son hash

        Args:
            password: Mot de passe en clair
            hash_string: Hash stocké

        Returns:
            True si le mot de passe est correct
        """
        if not password or not hash_string:
            return False

        try:
            # Argon2
            if ARGON2_AVAILABLE and hash_string.startswith('$argon2'):
                try:
                    self.password_hasher.verify(hash_string, password)
                    return True
                except (VerifyMismatchError, VerificationError, InvalidHash):
                    return False

            # Bcrypt
            elif BCRYPT_AVAILABLE and hash_string.startswith('$2'):
                return bcrypt.checkpw(password.encode('utf-8'), hash_string.encode('utf-8'))

            # PBKDF2
            elif 'pbkdf2_sha256$' in hash_string:
                algorithm, salt, pwd_hash = hash_string.split('$')
                test_hash = hashlib.pbkdf2_hmac(
                    'sha256',
                    password.encode('utf-8'),
                    salt.encode('utf-8'),
                    self.pbkdf2_iterations
                )
                return hmac.compare_digest(test_hash.hex(), pwd_hash)

            return False

        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False

    def needs_rehash(self, hash_string: str) -> bool:
        """
        Vérifie si un hash doit être mis à jour

        Args:
            hash_string: Hash à vérifier

        Returns:
            True si le hash doit être mis à jour
        """
        # Préférer Argon2
        if ARGON2_AVAILABLE and not hash_string.startswith('$argon2'):
            return True

        # Sinon Bcrypt
        if BCRYPT_AVAILABLE and not hash_string.startswith('$2'):
            return True

        return False

    # =================================================================
    # JWT / TOKENS
    # =================================================================

    def generate_token(self, user_id: str, extra_claims: Optional[Dict] = None) -> str:
        """
        Génère un JWT token

        Args:
            user_id: ID de l'utilisateur
            extra_claims: Claims additionnels

        Returns:
            JWT token
        """
        if not JWT_AVAILABLE:
            # Fallback: token simple
            token = secrets.token_urlsafe(32)
            self.sessions[token] = {
                'user_id': user_id,
                'created_at': datetime.now(),
                'expires_at': datetime.now() + timedelta(seconds=self.jwt_expiration)
            }
            return token

        payload = {
            'user_id': user_id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=self.jwt_expiration),
            'jti': secrets.token_hex(16),  # JWT ID unique
        }

        if extra_claims:
            payload.update(extra_claims)

        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Vérifie et décode un JWT token

        Args:
            token: JWT token

        Returns:
            Payload du token si valide, None sinon
        """
        if not JWT_AVAILABLE:
            # Fallback: vérification simple
            session = self.sessions.get(token)
            if session and session['expires_at'] > datetime.now():
                return {'user_id': session['user_id']}
            return None

        try:
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None

    def refresh_token(self, token: str) -> Optional[str]:
        """
        Rafraîchit un token expiré

        Args:
            token: Token à rafraîchir

        Returns:
            Nouveau token si succès
        """
        payload = self.verify_token(token)
        if payload:
            return self.generate_token(payload['user_id'])
        return None

    # =================================================================
    # CHIFFREMENT
    # =================================================================

    def encrypt(self, data: Union[str, bytes]) -> bytes:
        """
        Chiffre des données avec AES-256-GCM ou Fernet

        Args:
            data: Données à chiffrer

        Returns:
            Données chiffrées
        """
        if not CRYPTO_AVAILABLE:
            raise RuntimeError("Cryptography package not installed")

        if isinstance(data, str):
            data = data.encode('utf-8')

        if self.fernet:
            return self.fernet.encrypt(data)

        elif self.aesgcm:
            nonce = secrets.token_bytes(12)  # 96-bit nonce pour GCM
            ciphertext = self.aesgcm.encrypt(nonce, data, None)
            return nonce + ciphertext

        else:
            raise RuntimeError("No encryption key configured")

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """
        Déchiffre des données

        Args:
            encrypted_data: Données chiffrées

        Returns:
            Données déchiffrées
        """
        if not CRYPTO_AVAILABLE:
            raise RuntimeError("Cryptography package not installed")

        if self.fernet:
            return self.fernet.decrypt(encrypted_data)

        elif self.aesgcm:
            nonce = encrypted_data[:12]
            ciphertext = encrypted_data[12:]
            return self.aesgcm.decrypt(nonce, ciphertext, None)

        else:
            raise RuntimeError("No encryption key configured")

    # =================================================================
    # RBAC (Role-Based Access Control)
    # =================================================================

    def check_permission(self, user: User, permission: Permission) -> bool:
        """
        Vérifie si un utilisateur a une permission

        Args:
            user: Utilisateur
            permission: Permission à vérifier

        Returns:
            True si l'utilisateur a la permission
        """
        # Permissions explicites de l'utilisateur
        if permission in user.permissions:
            return True

        # Permissions du rôle
        role_perms = ROLE_PERMISSIONS.get(user.role, [])
        return permission in role_perms

    def require_permission(self, permission: Permission):
        """
        Décorateur pour protéger une fonction avec une permission

        Args:
            permission: Permission requise
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Récupérer l'utilisateur du contexte (à implémenter)
                user = kwargs.get('current_user')
                if not user:
                    raise PermissionError("No user in context")

                if not self.check_permission(user, permission):
                    self.log_security_event(
                        user_id=user.id,
                        action=f"PERMISSION_DENIED",
                        resource=func.__name__,
                        success=False,
                        details={'required_permission': permission.value}
                    )
                    raise PermissionError(f"Permission denied: {permission.value}")

                return func(*args, **kwargs)
            return wrapper
        return decorator

    # =================================================================
    # RATE LIMITING
    # =================================================================

    def check_rate_limit(self, identifier: str, limit: int = 60, window: int = 60) -> bool:
        """
        Vérifie le rate limiting

        Args:
            identifier: Identifiant (IP, user_id, etc.)
            limit: Nombre max de requêtes
            window: Fenêtre de temps en secondes

        Returns:
            True si dans les limites
        """
        now = time.time()

        # Nettoyer les anciennes entrées
        self.rate_limits[identifier] = [
            t for t in self.rate_limits[identifier]
            if now - t < window
        ]

        # Vérifier la limite
        if len(self.rate_limits[identifier]) >= limit:
            return False

        # Ajouter la nouvelle requête
        self.rate_limits[identifier].append(now)
        return True

    def rate_limit(self, limit: int = 60, window: int = 60):
        """
        Décorateur pour rate limiting

        Args:
            limit: Nombre max de requêtes
            window: Fenêtre de temps en secondes
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Identifier par IP ou user_id
                identifier = kwargs.get('ip_address', 'unknown')

                if not self.check_rate_limit(identifier, limit, window):
                    raise Exception(f"Rate limit exceeded: {limit} requests per {window} seconds")

                return func(*args, **kwargs)
            return wrapper
        return decorator

    # =================================================================
    # PROTECTION CSRF
    # =================================================================

    def generate_csrf_token(self, session_id: str) -> str:
        """
        Génère un token CSRF

        Args:
            session_id: ID de session

        Returns:
            Token CSRF
        """
        token_data = f"{session_id}:{time.time()}"
        signature = hmac.new(
            self.secret_key.encode(),
            token_data.encode(),
            hashlib.sha256
        ).hexdigest()

        return f"{token_data}:{signature}"

    def verify_csrf_token(self, token: str, session_id: str, max_age: int = 3600) -> bool:
        """
        Vérifie un token CSRF

        Args:
            token: Token CSRF
            session_id: ID de session
            max_age: Âge max du token en secondes

        Returns:
            True si valide
        """
        try:
            token_data, signature = token.rsplit(':', 1)
            expected_signature = hmac.new(
                self.secret_key.encode(),
                token_data.encode(),
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(signature, expected_signature):
                return False

            session, timestamp = token_data.split(':')
            if session != session_id:
                return False

            if time.time() - float(timestamp) > max_age:
                return False

            return True

        except Exception as e:
            logger.warning(f"CSRF token verification failed: {e}")
            return False

    # =================================================================
    # VALIDATION ET SANITIZATION
    # =================================================================

    def sanitize_input(self, data: str, allow_html: bool = False) -> str:
        """
        Nettoie les entrées utilisateur

        Args:
            data: Données à nettoyer
            allow_html: Autoriser le HTML

        Returns:
            Données nettoyées
        """
        if not data:
            return ""

        # Supprimer les caractères de contrôle
        data = ''.join(char for char in data if ord(char) >= 32 or char == '\n')

        if not allow_html:
            # Échapper les caractères HTML
            replacements = {
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#x27;',
                '&': '&amp;',
                '/': '&#x2F;',
            }
            for char, replacement in replacements.items():
                data = data.replace(char, replacement)

        # Supprimer les espaces en début/fin
        data = data.strip()

        return data

    def validate_email(self, email: str) -> bool:
        """
        Valide une adresse email

        Args:
            email: Email à valider

        Returns:
            True si valide
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def validate_password_strength(self, password: str) -> Tuple[bool, List[str]]:
        """
        Vérifie la force d'un mot de passe

        Args:
            password: Mot de passe à vérifier

        Returns:
            (valide, liste des problèmes)
        """
        issues = []

        if len(password) < 8:
            issues.append("Le mot de passe doit contenir au moins 8 caractères")

        if not re.search(r'[A-Z]', password):
            issues.append("Le mot de passe doit contenir au moins une majuscule")

        if not re.search(r'[a-z]', password):
            issues.append("Le mot de passe doit contenir au moins une minuscule")

        if not re.search(r'[0-9]', password):
            issues.append("Le mot de passe doit contenir au moins un chiffre")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            issues.append("Le mot de passe doit contenir au moins un caractère spécial")

        # Vérifier les mots de passe communs
        common_passwords = ['password', '123456', 'admin', 'qwerty', 'letmein']
        if password.lower() in common_passwords:
            issues.append("Ce mot de passe est trop commun")

        return len(issues) == 0, issues

    # =================================================================
    # AUDIT ET LOGGING
    # =================================================================

    def log_security_event(self, user_id: Optional[str], action: str, resource: str,
                          success: bool, ip_address: str = "unknown",
                          user_agent: str = "unknown", details: Optional[Dict] = None):
        """
        Enregistre un événement de sécurité

        Args:
            user_id: ID de l'utilisateur
            action: Action effectuée
            resource: Ressource concernée
            success: Succès ou échec
            ip_address: Adresse IP
            user_agent: User agent
            details: Détails additionnels
        """
        audit_log = AuditLog(
            id=secrets.token_hex(16),
            timestamp=datetime.now(),
            user_id=user_id,
            action=action,
            resource=resource,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            details=details or {}
        )

        self.audit_logs.append(audit_log)

        # Log aussi dans le système de logging
        log_level = logging.INFO if success else logging.WARNING
        logger.log(log_level, f"Security event: {action} on {resource} by {user_id} from {ip_address}")

    def get_audit_logs(self, user_id: Optional[str] = None,
                       start_date: Optional[datetime] = None,
                       end_date: Optional[datetime] = None) -> List[AuditLog]:
        """
        Récupère les logs d'audit

        Args:
            user_id: Filtrer par utilisateur
            start_date: Date de début
            end_date: Date de fin

        Returns:
            Liste des logs d'audit
        """
        logs = self.audit_logs

        if user_id:
            logs = [log for log in logs if log.user_id == user_id]

        if start_date:
            logs = [log for log in logs if log.timestamp >= start_date]

        if end_date:
            logs = [log for log in logs if log.timestamp <= end_date]

        return logs

    # =================================================================
    # AUTHENTIFICATION À DEUX FACTEURS (2FA)
    # =================================================================

    def generate_totp_secret(self) -> str:
        """
        Génère un secret pour l'authentification TOTP

        Returns:
            Secret TOTP en base32
        """
        import base64
        secret_bytes = secrets.token_bytes(20)
        return base64.b32encode(secret_bytes).decode('utf-8')

    def verify_totp(self, secret: str, token: str, window: int = 1) -> bool:
        """
        Vérifie un token TOTP

        Args:
            secret: Secret TOTP
            token: Token à vérifier
            window: Fenêtre de tolérance

        Returns:
            True si valide
        """
        try:
            import pyotp
            totp = pyotp.TOTP(secret)
            return totp.verify(token, valid_window=window)
        except ImportError:
            logger.warning("pyotp not installed, 2FA disabled")
            return False
        except Exception as e:
            logger.error(f"TOTP verification error: {e}")
            return False

    # =================================================================
    # GESTION DES SESSIONS
    # =================================================================

    def create_session(self, user_id: str, ip_address: str, user_agent: str) -> Session:
        """
        Crée une nouvelle session

        Args:
            user_id: ID de l'utilisateur
            ip_address: Adresse IP
            user_agent: User agent

        Returns:
            Session créée
        """
        session = Session(
            id=secrets.token_hex(16),
            user_id=user_id,
            token=self.generate_token(user_id),
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(seconds=self.jwt_expiration),
            ip_address=ip_address,
            user_agent=user_agent
        )

        self.sessions[session.id] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Récupère une session

        Args:
            session_id: ID de session

        Returns:
            Session si trouvée
        """
        session = self.sessions.get(session_id)
        if session and session.expires_at > datetime.now() and session.is_active:
            return session
        return None

    def invalidate_session(self, session_id: str):
        """
        Invalide une session

        Args:
            session_id: ID de session
        """
        if session_id in self.sessions:
            self.sessions[session_id].is_active = False

    def cleanup_expired_sessions(self):
        """Nettoie les sessions expirées"""
        now = datetime.now()
        expired = [
            sid for sid, session in self.sessions.items()
            if session.expires_at < now
        ]
        for sid in expired:
            del self.sessions[sid]


# =================================================================
# FONCTIONS UTILITAIRES
# =================================================================

def generate_secure_password(length: int = 16) -> str:
    """
    Génère un mot de passe sécurisé

    Args:
        length: Longueur du mot de passe

    Returns:
        Mot de passe généré
    """
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))

    # S'assurer qu'il y a au moins un de chaque type
    if not any(c.isupper() for c in password):
        password = password[:-1] + secrets.choice(string.ascii_uppercase)
    if not any(c.islower() for c in password):
        password = password[:-1] + secrets.choice(string.ascii_lowercase)
    if not any(c.isdigit() for c in password):
        password = password[:-1] + secrets.choice(string.digits)
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        password = password[:-1] + secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")

    return password


def constant_time_compare(val1: str, val2: str) -> bool:
    """
    Comparaison en temps constant pour éviter les timing attacks

    Args:
        val1: Première valeur
        val2: Deuxième valeur

    Returns:
        True si égales
    """
    return hmac.compare_digest(val1, val2)


# =================================================================
# EXEMPLE D'UTILISATION
# =================================================================

if __name__ == "__main__":
    import string

    # Créer le gestionnaire de sécurité
    config = {
        'SECRET_KEY': secrets.token_hex(32),
        'JWT_SECRET': secrets.token_hex(32),
        'ENCRYPTION_KEY': Fernet.generate_key().decode() if CRYPTO_AVAILABLE else None,
    }

    security = SecurityManager(config)

    # Test de hashage de mot de passe
    password = "MySecurePassword123!"
    hashed = security.hash_password(password)
    print(f"Password hash: {hashed[:50]}...")
    print(f"Password valid: {security.verify_password(password, hashed)}")
    print(f"Wrong password: {security.verify_password('wrong', hashed)}")

    # Test de JWT
    if JWT_AVAILABLE:
        token = security.generate_token("user123")
        print(f"\nJWT Token: {token[:50]}...")
        payload = security.verify_token(token)
        print(f"Token payload: {payload}")

    # Test de chiffrement
    if CRYPTO_AVAILABLE and security.encryption_key:
        secret_data = "Sensitive information"
        encrypted = security.encrypt(secret_data)
        print(f"\nEncrypted: {encrypted[:50]}...")
        decrypted = security.decrypt(encrypted)
        print(f"Decrypted: {decrypted.decode()}")

    # Test de validation
    email = "test@example.com"
    print(f"\nEmail valid: {security.validate_email(email)}")

    password_check = "Weak"
    valid, issues = security.validate_password_strength(password_check)
    print(f"Password '{password_check}' valid: {valid}")
    if not valid:
        print(f"Issues: {issues}")

    # Test de génération de mot de passe
    generated_pwd = generate_secure_password()
    print(f"\nGenerated password: {generated_pwd}")

    # Test de RBAC
    test_user = User(
        id="user1",
        username="testuser",
        email="test@example.com",
        role=UserRole.USER
    )

    print(f"\nUser can read own data: {security.check_permission(test_user, Permission.READ_OWN_DATA)}")
    print(f"User can read all data: {security.check_permission(test_user, Permission.READ_ALL_DATA)}")

    print("\n✅ Security module tests completed!")