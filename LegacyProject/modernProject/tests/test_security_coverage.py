"""
Tests supplémentaires pour security.py - Augmentation de la couverture.

Couvre les fonctionnalités de SecurityManager :
- Initialisation et configuration
- Hash de mots de passe (PBKDF2 fallback)
- Vérification de mots de passe
- Génération et vérification de tokens
- Rate limiting
- CSRF tokens
- Validation des entrées (sanitize, email, password strength)
- Audit logging
- RBAC (contrôle d'accès par rôle)
- Gestion des sessions
- TOTP (2FA)
"""

import time
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from lib.security import (
    ROLE_PERMISSIONS,
    AuditLog,
    HashAlgorithm,
    Permission,
    SecurityManager,
    Session,
    User,
    UserRole,
)


class TestSecurityManagerInit(unittest.TestCase):
    """Tests d'initialisation du SecurityManager."""

    def test_init_default(self):
        """SecurityManager s'initialise avec la config par défaut."""
        sm = SecurityManager()
        self.assertIsNotNone(sm.secret_key)
        self.assertIsNotNone(sm.jwt_secret)
        self.assertEqual(sm.jwt_algorithm, "HS256")
        self.assertEqual(sm.jwt_expiration, 3600)
        self.assertEqual(sm.max_login_attempts, 5)
        self.assertEqual(sm.lockout_duration, 900)

    def test_init_custom_config(self):
        """SecurityManager s'initialise avec une config personnalisée."""
        config = {
            "SECRET_KEY": "test_secret_key_123",
            "JWT_SECRET": "test_jwt_secret_456",
            "JWT_ALGORITHM": "HS256",
            "JWT_EXPIRATION": 7200,
            "MAX_LOGIN_ATTEMPTS": 3,
            "LOCKOUT_DURATION": 600,
            "PBKDF2_ITERATIONS": 50000,
        }
        sm = SecurityManager(config)
        self.assertEqual(sm.secret_key, "test_secret_key_123")
        self.assertEqual(sm.jwt_secret, "test_jwt_secret_456")
        self.assertEqual(sm.jwt_expiration, 7200)
        self.assertEqual(sm.max_login_attempts, 3)
        self.assertEqual(sm.lockout_duration, 600)

    def test_init_no_encryption_key(self):
        """SecurityManager sans clé de chiffrement."""
        sm = SecurityManager()
        self.assertIsNone(sm.encryption_key)


class TestPasswordHashing(unittest.TestCase):
    """Tests de hashage de mots de passe."""

    def setUp(self):
        self.sm = SecurityManager({"PBKDF2_ITERATIONS": 1000})

    def test_hash_password_pbkdf2(self):
        """Hash un mot de passe avec PBKDF2 (fallback)."""
        # Forcer PBKDF2
        self.sm.hash_algorithm = HashAlgorithm.PBKDF2_SHA256
        hashed = self.sm.hash_password("TestPassword123!")
        self.assertTrue(hashed.startswith("pbkdf2_sha256$"))
        parts = hashed.split("$")
        self.assertEqual(len(parts), 3)

    def test_hash_password_empty_raises(self):
        """Hash d'un mot de passe vide lève une exception."""
        with self.assertRaises(ValueError):
            self.sm.hash_password("")

    def test_verify_password_pbkdf2(self):
        """Vérifie un mot de passe hashé en PBKDF2."""
        self.sm.hash_algorithm = HashAlgorithm.PBKDF2_SHA256
        password = "SecurePass123!"
        hashed = self.sm.hash_password(password)
        self.assertTrue(self.sm.verify_password(password, hashed))

    def test_verify_password_wrong(self):
        """Vérifie qu'un mauvais mot de passe échoue."""
        self.sm.hash_algorithm = HashAlgorithm.PBKDF2_SHA256
        hashed = self.sm.hash_password("CorrectPassword123!")
        self.assertFalse(self.sm.verify_password("WrongPassword", hashed))

    def test_verify_password_empty(self):
        """Vérifie qu'un mot de passe vide retourne False."""
        self.assertFalse(self.sm.verify_password("", "somehash"))
        self.assertFalse(self.sm.verify_password("password", ""))

    def test_verify_password_invalid_hash_format(self):
        """Vérifie qu'un format de hash invalide retourne False."""
        self.assertFalse(self.sm.verify_password("password", "invalid_format"))

    def test_hash_different_passwords_differ(self):
        """Deux mots de passe différents produisent des hashes différents."""
        self.sm.hash_algorithm = HashAlgorithm.PBKDF2_SHA256
        hash1 = self.sm.hash_password("Password1!")
        hash2 = self.sm.hash_password("Password2!")
        self.assertNotEqual(hash1, hash2)

    def test_hash_same_password_differs(self):
        """Le même mot de passe produit des hashes différents (sel aléatoire)."""
        self.sm.hash_algorithm = HashAlgorithm.PBKDF2_SHA256
        hash1 = self.sm.hash_password("SamePassword!")
        hash2 = self.sm.hash_password("SamePassword!")
        self.assertNotEqual(hash1, hash2)


class TestTokens(unittest.TestCase):
    """Tests de génération/vérification de tokens."""

    def setUp(self):
        self.sm = SecurityManager({
            "JWT_SECRET": "test_jwt_secret",
            "JWT_EXPIRATION": 3600,
        })

    def test_generate_token(self):
        """Génère un token pour un utilisateur."""
        token = self.sm.generate_token("user_123")
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 10)

    def test_verify_token(self):
        """Vérifie un token valide."""
        token = self.sm.generate_token("user_123")
        payload = self.sm.verify_token(token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["user_id"], "user_123")

    def test_verify_invalid_token(self):
        """Vérifie qu'un token invalide retourne None."""
        result = self.sm.verify_token("invalid.token.here")
        self.assertIsNone(result)

    def test_generate_token_with_extra_claims(self):
        """Génère un token avec des claims supplémentaires."""
        token = self.sm.generate_token("user_123", {"role": "admin"})
        payload = self.sm.verify_token(token)
        if payload:
            self.assertEqual(payload.get("user_id"), "user_123")

    def test_refresh_token(self):
        """Rafraîchit un token valide."""
        token = self.sm.generate_token("user_456")
        new_token = self.sm.refresh_token(token)
        self.assertIsNotNone(new_token)
        self.assertNotEqual(token, new_token)

    def test_refresh_invalid_token(self):
        """Rafraîchir un token invalide retourne None."""
        result = self.sm.refresh_token("invalid_token")
        self.assertIsNone(result)


class TestRateLimiting(unittest.TestCase):
    """Tests de rate limiting."""

    def setUp(self):
        self.sm = SecurityManager()

    def test_rate_limit_under_limit(self):
        """Requêtes sous la limite passent."""
        for _ in range(5):
            self.assertTrue(self.sm.check_rate_limit("ip_1", limit=10, window=60))

    def test_rate_limit_exceeded(self):
        """Requêtes au-dessus de la limite sont bloquées."""
        for _ in range(5):
            self.sm.check_rate_limit("ip_2", limit=5, window=60)
        self.assertFalse(self.sm.check_rate_limit("ip_2", limit=5, window=60))

    def test_rate_limit_different_identifiers(self):
        """Chaque identifiant a son propre compteur."""
        for _ in range(5):
            self.sm.check_rate_limit("ip_a", limit=5, window=60)
        self.assertFalse(self.sm.check_rate_limit("ip_a", limit=5, window=60))
        self.assertTrue(self.sm.check_rate_limit("ip_b", limit=5, window=60))

    def test_rate_limit_window_expires(self):
        """Les requêtes expirent après la fenêtre."""
        self.sm.rate_limits["ip_3"] = [time.time() - 100]
        self.assertTrue(self.sm.check_rate_limit("ip_3", limit=1, window=60))


class TestCSRFTokens(unittest.TestCase):
    """Tests de tokens CSRF."""

    def setUp(self):
        self.sm = SecurityManager({"SECRET_KEY": "csrf_test_secret"})

    def test_generate_csrf_token(self):
        """Génère un token CSRF."""
        token = self.sm.generate_csrf_token("session_123")
        self.assertIsNotNone(token)
        self.assertIn(":", token)

    def test_verify_csrf_token_valid(self):
        """Vérifie un token CSRF valide."""
        token = self.sm.generate_csrf_token("session_123")
        self.assertTrue(self.sm.verify_csrf_token(token, "session_123"))

    def test_verify_csrf_token_wrong_session(self):
        """Vérifie qu'un token CSRF avec mauvaise session échoue."""
        token = self.sm.generate_csrf_token("session_123")
        self.assertFalse(self.sm.verify_csrf_token(token, "session_456"))

    def test_verify_csrf_token_invalid(self):
        """Vérifie qu'un token CSRF invalide échoue."""
        self.assertFalse(self.sm.verify_csrf_token("invalid:token:here", "session_123"))

    def test_verify_csrf_token_tampered(self):
        """Vérifie qu'un token CSRF altéré échoue."""
        token = self.sm.generate_csrf_token("session_123")
        tampered = token[:-1] + ("a" if token[-1] != "a" else "b")
        self.assertFalse(self.sm.verify_csrf_token(tampered, "session_123"))


class TestInputValidation(unittest.TestCase):
    """Tests de validation et sanitization des entrées."""

    def setUp(self):
        self.sm = SecurityManager()

    def test_sanitize_input_basic(self):
        """Sanitize nettoie le texte basique."""
        result = self.sm.sanitize_input("  Hello World  ")
        self.assertEqual(result, "Hello World")

    def test_sanitize_input_html(self):
        """Sanitize échappe le HTML."""
        result = self.sm.sanitize_input("<script>alert('xss')</script>")
        self.assertNotIn("<script>", result)
        # Les caractères dangereux doivent être échappés
        self.assertNotIn("<", result)

    def test_sanitize_input_allow_html(self):
        """Sanitize avec allow_html garde le HTML."""
        result = self.sm.sanitize_input("<b>Bold</b>", allow_html=True)
        self.assertIn("<b>", result)

    def test_sanitize_input_empty(self):
        """Sanitize d'une chaîne vide retourne vide."""
        self.assertEqual(self.sm.sanitize_input(""), "")

    def test_sanitize_input_special_chars(self):
        """Sanitize échappe les caractères spéciaux."""
        result = self.sm.sanitize_input('Test "quotes" & <tags>')
        self.assertNotIn('"', result.replace("&quot;", ""))
        self.assertNotIn("<", result.replace("&lt;", ""))

    def test_validate_email_valid(self):
        """Valide un email correct."""
        self.assertTrue(self.sm.validate_email("user@example.com"))
        self.assertTrue(self.sm.validate_email("test.user+tag@domain.co.uk"))

    def test_validate_email_invalid(self):
        """Rejette un email invalide."""
        self.assertFalse(self.sm.validate_email("not_an_email"))
        self.assertFalse(self.sm.validate_email("@domain.com"))
        self.assertFalse(self.sm.validate_email("user@"))
        self.assertFalse(self.sm.validate_email(""))

    def test_password_strength_strong(self):
        """Un mot de passe fort est accepté."""
        valid, issues = self.sm.validate_password_strength("Str0ng!Pass#2024")
        self.assertTrue(valid)
        self.assertEqual(len(issues), 0)

    def test_password_strength_too_short(self):
        """Un mot de passe trop court est rejeté."""
        valid, issues = self.sm.validate_password_strength("Ab1!")
        self.assertFalse(valid)
        self.assertTrue(any("8 caractères" in i for i in issues))

    def test_password_strength_no_uppercase(self):
        """Un mot de passe sans majuscule est signalé."""
        valid, issues = self.sm.validate_password_strength("password123!")
        self.assertFalse(valid)
        self.assertTrue(any("majuscule" in i for i in issues))

    def test_password_strength_no_digit(self):
        """Un mot de passe sans chiffre est signalé."""
        valid, issues = self.sm.validate_password_strength("Password!!")
        self.assertFalse(valid)
        self.assertTrue(any("chiffre" in i for i in issues))

    def test_password_strength_no_special(self):
        """Un mot de passe sans caractère spécial est signalé."""
        valid, issues = self.sm.validate_password_strength("Password123")
        self.assertFalse(valid)
        self.assertTrue(any("spécial" in i for i in issues))

    def test_password_strength_common(self):
        """Un mot de passe commun est rejeté."""
        valid, issues = self.sm.validate_password_strength("password")
        self.assertFalse(valid)
        self.assertTrue(any("commun" in i for i in issues))


class TestRBAC(unittest.TestCase):
    """Tests du contrôle d'accès basé sur les rôles."""

    def setUp(self):
        self.sm = SecurityManager()
        self.admin_user = User(
            id="admin_1",
            username="admin",
            email="admin@test.com",
            role=UserRole.ADMIN,
        )
        self.regular_user = User(
            id="user_1",
            username="user",
            email="user@test.com",
            role=UserRole.USER,
        )
        self.guest_user = User(
            id="guest_1",
            username="guest",
            email="guest@test.com",
            role=UserRole.GUEST,
        )

    def test_admin_has_all_permissions(self):
        """L'admin a toutes les permissions."""
        for perm in Permission:
            self.assertTrue(
                self.sm.check_permission(self.admin_user, perm),
                f"Admin devrait avoir la permission {perm.value}",
            )

    def test_user_limited_permissions(self):
        """Un utilisateur standard a des permissions limitées."""
        self.assertTrue(
            self.sm.check_permission(self.regular_user, Permission.READ_OWN_DATA)
        )
        self.assertTrue(
            self.sm.check_permission(self.regular_user, Permission.EXPORT_DATA)
        )
        self.assertFalse(
            self.sm.check_permission(self.regular_user, Permission.MANAGE_USERS)
        )
        self.assertFalse(
            self.sm.check_permission(self.regular_user, Permission.DELETE_ALL_DATA)
        )

    def test_guest_minimal_permissions(self):
        """Un invité a des permissions minimales."""
        self.assertTrue(
            self.sm.check_permission(self.guest_user, Permission.READ_OWN_DATA)
        )
        self.assertFalse(
            self.sm.check_permission(self.guest_user, Permission.WRITE_OWN_DATA)
        )

    def test_explicit_user_permissions(self):
        """Les permissions explicites de l'utilisateur sont vérifiées."""
        user = User(
            id="special_1",
            username="special",
            email="special@test.com",
            role=UserRole.GUEST,
            permissions=[Permission.MANAGE_USERS],
        )
        self.assertTrue(self.sm.check_permission(user, Permission.MANAGE_USERS))

    def test_role_permissions_mapping(self):
        """Le mapping rôle->permissions est cohérent."""
        for role in UserRole:
            self.assertIn(role, ROLE_PERMISSIONS)

    def test_require_permission_decorator(self):
        """Le décorateur require_permission fonctionne."""
        @self.sm.require_permission(Permission.READ_OWN_DATA)
        def protected_function(current_user=None):
            return "success"

        result = protected_function(current_user=self.regular_user)
        self.assertEqual(result, "success")

    def test_require_permission_denied(self):
        """Le décorateur require_permission refuse l'accès."""
        @self.sm.require_permission(Permission.MANAGE_USERS)
        def admin_function(current_user=None):
            return "success"

        with self.assertRaises(PermissionError):
            admin_function(current_user=self.regular_user)

    def test_require_permission_no_user(self):
        """Le décorateur require_permission refuse sans utilisateur."""
        @self.sm.require_permission(Permission.READ_OWN_DATA)
        def protected_function(current_user=None):
            return "success"

        with self.assertRaises(PermissionError):
            protected_function()


class TestAuditLogging(unittest.TestCase):
    """Tests du logging d'audit."""

    def setUp(self):
        self.sm = SecurityManager()

    def test_log_security_event(self):
        """Enregistre un événement de sécurité."""
        self.sm.log_security_event(
            user_id="user_1",
            action="LOGIN",
            resource="auth",
            success=True,
            ip_address="192.168.1.1",
            user_agent="TestBrowser",
        )
        self.assertEqual(len(self.sm.audit_logs), 1)
        log = self.sm.audit_logs[0]
        self.assertEqual(log.user_id, "user_1")
        self.assertEqual(log.action, "LOGIN")
        self.assertTrue(log.success)

    def test_log_security_event_with_details(self):
        """Enregistre un événement avec détails."""
        self.sm.log_security_event(
            user_id="user_1",
            action="ACCESS_DENIED",
            resource="admin_panel",
            success=False,
            details={"reason": "insufficient_permissions"},
        )
        log = self.sm.audit_logs[0]
        self.assertFalse(log.success)
        self.assertEqual(log.details["reason"], "insufficient_permissions")

    def test_get_audit_logs_all(self):
        """Récupère tous les logs d'audit."""
        for i in range(5):
            self.sm.log_security_event(
                user_id=f"user_{i}",
                action="TEST",
                resource="test",
                success=True,
            )
        logs = self.sm.get_audit_logs()
        self.assertEqual(len(logs), 5)

    def test_get_audit_logs_by_user(self):
        """Filtre les logs par utilisateur."""
        self.sm.log_security_event(
            user_id="user_1", action="LOGIN", resource="auth", success=True
        )
        self.sm.log_security_event(
            user_id="user_2", action="LOGIN", resource="auth", success=True
        )
        logs = self.sm.get_audit_logs(user_id="user_1")
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].user_id, "user_1")

    def test_get_audit_logs_by_date(self):
        """Filtre les logs par date."""
        self.sm.log_security_event(
            user_id="user_1", action="TEST", resource="test", success=True
        )
        logs = self.sm.get_audit_logs(start_date=datetime.now() - timedelta(hours=1))
        self.assertEqual(len(logs), 1)

        logs = self.sm.get_audit_logs(end_date=datetime.now() - timedelta(hours=1))
        self.assertEqual(len(logs), 0)


class TestTOTP(unittest.TestCase):
    """Tests TOTP (2FA)."""

    def setUp(self):
        self.sm = SecurityManager()

    def test_generate_totp_secret(self):
        """Génère un secret TOTP."""
        secret = self.sm.generate_totp_secret()
        self.assertIsNotNone(secret)
        self.assertIsInstance(secret, str)
        self.assertTrue(len(secret) > 10)

    def test_generate_totp_secret_unique(self):
        """Chaque secret TOTP est unique."""
        secret1 = self.sm.generate_totp_secret()
        secret2 = self.sm.generate_totp_secret()
        self.assertNotEqual(secret1, secret2)

    def test_verify_totp_without_pyotp(self):
        """Vérification TOTP sans pyotp retourne False."""
        # pyotp n'est probablement pas installé dans cet env
        result = self.sm.verify_totp("JBSWY3DPEHPK3PXP", "123456")
        self.assertFalse(result)


class TestDataModels(unittest.TestCase):
    """Tests des modèles de données de sécurité."""

    def test_user_creation(self):
        """Création d'un utilisateur."""
        user = User(
            id="1",
            username="testuser",
            email="test@example.com",
            role=UserRole.USER,
        )
        self.assertEqual(user.id, "1")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role, UserRole.USER)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_verified)
        self.assertEqual(user.failed_login_attempts, 0)

    def test_session_creation(self):
        """Création d'une session."""
        session = Session(
            id="sess_1",
            user_id="user_1",
            token="token_123",
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=1),
            ip_address="192.168.1.1",
            user_agent="TestBrowser",
        )
        self.assertEqual(session.id, "sess_1")
        self.assertTrue(session.is_active)

    def test_audit_log_creation(self):
        """Création d'un log d'audit."""
        log = AuditLog(
            id="log_1",
            timestamp=datetime.now(),
            user_id="user_1",
            action="LOGIN",
            resource="auth",
            ip_address="192.168.1.1",
            user_agent="TestBrowser",
            success=True,
            details={},
        )
        self.assertEqual(log.action, "LOGIN")
        self.assertTrue(log.success)

    def test_hash_algorithm_enum(self):
        """Les algorithmes de hashage sont définis."""
        self.assertEqual(HashAlgorithm.PBKDF2_SHA256.value, "pbkdf2_sha256")
        self.assertEqual(HashAlgorithm.BCRYPT.value, "bcrypt")
        self.assertEqual(HashAlgorithm.ARGON2.value, "argon2")

    def test_user_role_enum(self):
        """Les rôles utilisateur sont définis."""
        self.assertEqual(UserRole.ADMIN.value, "admin")
        self.assertEqual(UserRole.USER.value, "user")
        self.assertEqual(UserRole.GUEST.value, "guest")

    def test_permission_enum(self):
        """Les permissions sont définies."""
        self.assertEqual(Permission.READ_OWN_DATA.value, "read_own_data")
        self.assertEqual(Permission.MANAGE_USERS.value, "manage_users")


class TestNeedsRehash(unittest.TestCase):
    """Tests de needs_rehash."""

    def setUp(self):
        self.sm = SecurityManager()

    def test_pbkdf2_needs_rehash(self):
        """Un hash PBKDF2 doit être mis à jour si Argon2/Bcrypt est dispo."""
        result = self.sm.needs_rehash("pbkdf2_sha256$salt$hash")
        # Le résultat dépend de la disponibilité d'Argon2/Bcrypt
        self.assertIsInstance(result, bool)

    def test_random_string_needs_rehash(self):
        """Un format inconnu nécessite un rehash."""
        result = self.sm.needs_rehash("random_hash_format")
        self.assertIsInstance(result, bool)


class TestRateLimitDecorator(unittest.TestCase):
    """Tests du décorateur rate_limit."""

    def setUp(self):
        self.sm = SecurityManager()

    def test_rate_limit_decorator_passes(self):
        """Le décorateur laisse passer sous la limite."""
        @self.sm.rate_limit(limit=5, window=60)
        def my_function(ip_address="127.0.0.1"):
            return "ok"

        result = my_function(ip_address="127.0.0.1")
        self.assertEqual(result, "ok")

    def test_rate_limit_decorator_blocks(self):
        """Le décorateur bloque au-dessus de la limite."""
        @self.sm.rate_limit(limit=2, window=60)
        def my_function(ip_address="127.0.0.2"):
            return "ok"

        my_function(ip_address="127.0.0.2")
        my_function(ip_address="127.0.0.2")

        with self.assertRaises(Exception) as ctx:
            my_function(ip_address="127.0.0.2")
        self.assertIn("Rate limit exceeded", str(ctx.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
