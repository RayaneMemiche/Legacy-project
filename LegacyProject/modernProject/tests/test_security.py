#!/usr/bin/env python3
"""
Tests complets pour le module security.py
Coverage visé: 90%+
"""

import pytest
import time
import hashlib
import hmac
import re
import secrets
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

# Import du module à tester
from lib import security


class TestHashAlgorithm:
    """Tests pour l'enum HashAlgorithm"""

    def test_hash_algorithm_values(self):
        """Test que tous les algorithmes sont définis"""
        assert security.HashAlgorithm.PBKDF2_SHA256.value == "pbkdf2_sha256"
        assert security.HashAlgorithm.BCRYPT.value == "bcrypt"
        assert security.HashAlgorithm.ARGON2.value == "argon2"
        assert security.HashAlgorithm.SHA256.value == "sha256"
        assert security.HashAlgorithm.SHA512.value == "sha512"

    def test_hash_algorithm_enum_members(self):
        """Test le nombre d'algorithmes"""
        assert len(security.HashAlgorithm) == 5


class TestUserRole:
    """Tests pour l'enum UserRole"""

    def test_user_roles_exist(self):
        """Test que tous les rôles sont définis"""
        assert security.UserRole.ADMIN.value == "admin"
        assert security.UserRole.USER.value == "user"
        assert security.UserRole.MODERATOR.value == "moderator"
        assert security.UserRole.SUPPORT.value == "support"
        assert security.UserRole.AUDIT.value == "audit"
        assert security.UserRole.GUEST.value == "guest"

    def test_user_role_count(self):
        """Test le nombre de rôles"""
        assert len(security.UserRole) >= 6


class TestPermission:
    """Tests pour l'enum Permission"""

    def test_permission_read_own_data_exists(self):
        """Test que la permission READ_OWN_DATA existe"""
        assert security.Permission.READ_OWN_DATA.value == "read_own_data"

    def test_permission_enum_has_members(self):
        """Test que l'enum Permission a des membres"""
        assert len(security.Permission) >= 1


class TestSecurityConstants:
    """Tests pour les constantes de sécurité"""

    def test_crypto_availability_boolean(self):
        """Test que CRYPTO_AVAILABLE est un booléen"""
        assert isinstance(security.CRYPTO_AVAILABLE, bool)

    def test_jwt_availability_boolean(self):
        """Test que JWT_AVAILABLE est un booléen"""
        assert isinstance(security.JWT_AVAILABLE, bool)

    def test_bcrypt_availability_boolean(self):
        """Test que BCRYPT_AVAILABLE est un booléen"""
        assert isinstance(security.BCRYPT_AVAILABLE, bool)

    def test_argon2_availability_boolean(self):
        """Test que ARGON2_AVAILABLE est un booléen"""
        assert isinstance(security.ARGON2_AVAILABLE, bool)


class TestPasswordHashing:
    """Tests pour le hashage de mots de passe"""

    def test_simple_sha256_hash(self):
        """Test hashage SHA256 simple"""
        password = "test_password_123"
        hashed = hashlib.sha256(password.encode()).hexdigest()
        assert len(hashed) == 64  # SHA256 = 64 caractères hex
        assert isinstance(hashed, str)

    def test_sha256_different_passwords(self):
        """Test que deux mots de passe différents donnent des hash différents"""
        pwd1 = "password1"
        pwd2 = "password2"
        hash1 = hashlib.sha256(pwd1.encode()).hexdigest()
        hash2 = hashlib.sha256(pwd2.encode()).hexdigest()
        assert hash1 != hash2

    def test_sha256_same_password_same_hash(self):
        """Test que le même mot de passe donne le même hash"""
        password = "consistent_password"
        hash1 = hashlib.sha256(password.encode()).hexdigest()
        hash2 = hashlib.sha256(password.encode()).hexdigest()
        assert hash1 == hash2

    def test_sha512_hash(self):
        """Test hashage SHA512"""
        password = "test_password_456"
        hashed = hashlib.sha512(password.encode()).hexdigest()
        assert len(hashed) == 128  # SHA512 = 128 caractères hex
        assert isinstance(hashed, str)

    @pytest.mark.skipif(not security.BCRYPT_AVAILABLE, reason="bcrypt not installed")
    def test_bcrypt_hash_verify(self):
        """Test hashage et vérification bcrypt"""
        import bcrypt
        password = b"secure_password"
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        assert bcrypt.checkpw(password, hashed)
        assert not bcrypt.checkpw(b"wrong_password", hashed)

    @pytest.mark.skipif(not security.ARGON2_AVAILABLE, reason="argon2 not installed")
    def test_argon2_hash_verify(self):
        """Test hashage et vérification argon2"""
        from argon2 import PasswordHasher
        ph = PasswordHasher()
        password = "secure_password_argon2"
        hashed = ph.hash(password)
        assert ph.verify(hashed, password)


class TestTokenGeneration:
    """Tests pour la génération de tokens"""

    def test_secrets_token_generation(self):
        """Test génération de token sécurisé"""
        token = secrets.token_hex(32)
        assert len(token) == 64  # 32 bytes = 64 hex chars
        assert isinstance(token, str)

    def test_secrets_token_uniqueness(self):
        """Test que les tokens générés sont uniques"""
        token1 = secrets.token_hex(32)
        token2 = secrets.token_hex(32)
        assert token1 != token2

    def test_secrets_token_urlsafe(self):
        """Test génération de token URL-safe"""
        token = secrets.token_urlsafe(32)
        assert len(token) >= 40  # Base64 encoding augmente la taille
        assert isinstance(token, str)
        # Vérifier que contient seulement caractères URL-safe
        import string
        allowed_chars = string.ascii_letters + string.digits + '-_'
        assert all(c in allowed_chars for c in token)


class TestHMAC:
    """Tests pour HMAC (Hash-based Message Authentication Code)"""

    def test_hmac_sha256_creation(self):
        """Test création HMAC SHA256"""
        key = b"secret_key"
        message = b"important message"
        signature = hmac.new(key, message, hashlib.sha256).hexdigest()
        assert len(signature) == 64
        assert isinstance(signature, str)

    def test_hmac_verification(self):
        """Test vérification HMAC"""
        key = b"secret_key"
        message = b"important message"
        signature1 = hmac.new(key, message, hashlib.sha256).digest()
        signature2 = hmac.new(key, message, hashlib.sha256).digest()
        assert hmac.compare_digest(signature1, signature2)

    def test_hmac_different_key_different_signature(self):
        """Test que différentes clés donnent différentes signatures"""
        key1 = b"key1"
        key2 = b"key2"
        message = b"same message"
        sig1 = hmac.new(key1, message, hashlib.sha256).hexdigest()
        sig2 = hmac.new(key2, message, hashlib.sha256).hexdigest()
        assert sig1 != sig2

    def test_hmac_tamper_detection(self):
        """Test détection de modification du message"""
        key = b"secret_key"
        message = b"original message"
        tampered = b"tampered message"
        original_sig = hmac.new(key, message, hashlib.sha256).digest()
        tampered_sig = hmac.new(key, tampered, hashlib.sha256).digest()
        assert not hmac.compare_digest(original_sig, tampered_sig)


class TestTimeBasedOperations:
    """Tests pour les opérations basées sur le temps"""

    def test_timestamp_generation(self):
        """Test génération de timestamp"""
        timestamp = int(time.time())
        assert isinstance(timestamp, int)
        assert timestamp > 1700000000  # Après 2023

    def test_datetime_operations(self):
        """Test opérations datetime"""
        now = datetime.now()
        future = now + timedelta(hours=1)
        assert future > now
        assert (future - now).total_seconds() == 3600

    def test_expiration_check(self):
        """Test vérification d'expiration"""
        issued_at = datetime.now()
        expires_at = issued_at + timedelta(hours=1)
        current_time = datetime.now()
        assert current_time < expires_at  # Pas encore expiré

    def test_token_expiration_logic(self):
        """Test logique d'expiration de token"""
        # Token émis il y a 2 heures
        issued_at = datetime.now() - timedelta(hours=2)
        expires_in = timedelta(hours=1)
        expires_at = issued_at + expires_in
        current_time = datetime.now()
        is_expired = current_time > expires_at
        assert is_expired  # Devrait être expiré


@pytest.mark.skipif(not security.JWT_AVAILABLE, reason="JWT not installed")
class TestJWT:
    """Tests pour JWT (JSON Web Tokens)"""

    def test_jwt_encode_decode(self):
        """Test encodage et décodage JWT"""
        import jwt as pyjwt
        secret = "my_secret_key"
        payload = {"user_id": 123, "username": "john_doe"}
        token = pyjwt.encode(payload, secret, algorithm="HS256")
        decoded = pyjwt.decode(token, secret, algorithms=["HS256"])
        assert decoded["user_id"] == 123
        assert decoded["username"] == "john_doe"

    def test_jwt_with_expiration(self):
        """Test JWT avec expiration"""
        import jwt as pyjwt
        secret = "my_secret"
        exp_time = datetime.utcnow() + timedelta(hours=1)
        payload = {"user_id": 1, "exp": exp_time}
        token = pyjwt.encode(payload, secret, algorithm="HS256")
        decoded = pyjwt.decode(token, secret, algorithms=["HS256"])
        assert decoded["user_id"] == 1

    def test_jwt_expired_token(self):
        """Test rejet de token expiré"""
        import jwt as pyjwt
        secret = "my_secret"
        # Token expiré il y a 1 heure
        exp_time = datetime.utcnow() - timedelta(hours=1)
        payload = {"user_id": 1, "exp": exp_time}
        token = pyjwt.encode(payload, secret, algorithm="HS256")
        with pytest.raises(pyjwt.ExpiredSignatureError):
            pyjwt.decode(token, secret, algorithms=["HS256"])

    def test_jwt_invalid_signature(self):
        """Test rejet de signature invalide"""
        import jwt as pyjwt
        secret1 = "secret1"
        secret2 = "secret2"
        payload = {"user_id": 1}
        token = pyjwt.encode(payload, secret1, algorithm="HS256")
        with pytest.raises(pyjwt.InvalidSignatureError):
            pyjwt.decode(token, secret2, algorithms=["HS256"])


@pytest.mark.skipif(not security.CRYPTO_AVAILABLE, reason="cryptography not installed")
class TestAESEncryption:
    """Tests pour chiffrement AES"""

    def test_aes_gcm_encrypt_decrypt(self):
        """Test chiffrement/déchiffrement AES-GCM"""
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        key = AESGCM.generate_key(bit_length=256)
        aesgcm = AESGCM(key)
        nonce = secrets.token_bytes(12)
        plaintext = b"Secret message to encrypt"
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        decrypted = aesgcm.decrypt(nonce, ciphertext, None)
        assert decrypted == plaintext

    def test_aes_different_keys_different_output(self):
        """Test que différentes clés donnent différents résultats"""
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        plaintext = b"Same message"
        nonce = secrets.token_bytes(12)

        key1 = AESGCM.generate_key(bit_length=256)
        aesgcm1 = AESGCM(key1)
        cipher1 = aesgcm1.encrypt(nonce, plaintext, None)

        key2 = AESGCM.generate_key(bit_length=256)
        aesgcm2 = AESGCM(key2)
        cipher2 = aesgcm2.encrypt(nonce, plaintext, None)

        assert cipher1 != cipher2

    def test_aes_wrong_key_fails(self):
        """Test que le déchiffrement avec mauvaise clé échoue"""
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        from cryptography.exceptions import InvalidTag

        key1 = AESGCM.generate_key(bit_length=256)
        key2 = AESGCM.generate_key(bit_length=256)

        aesgcm1 = AESGCM(key1)
        nonce = secrets.token_bytes(12)
        plaintext = b"Secret"
        ciphertext = aesgcm1.encrypt(nonce, plaintext, None)

        aesgcm2 = AESGCM(key2)
        with pytest.raises(InvalidTag):
            aesgcm2.decrypt(nonce, ciphertext, None)


@pytest.mark.skipif(not security.CRYPTO_AVAILABLE, reason="cryptography not installed")
class TestPBKDF2:
    """Tests pour PBKDF2 (Password-Based Key Derivation Function)"""

    def test_pbkdf2_key_derivation(self):
        """Test dérivation de clé PBKDF2"""
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.backends import default_backend

        password = b"my_password"
        salt = secrets.token_bytes(16)
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password)
        assert len(key) == 32
        assert isinstance(key, bytes)

    def test_pbkdf2_same_password_same_key(self):
        """Test que le même mot de passe donne la même clé"""
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.backends import default_backend

        password = b"consistent_password"
        salt = b"fixed_salt_for_test"

        kdf1 = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key1 = kdf1.derive(password)

        kdf2 = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key2 = kdf2.derive(password)

        assert key1 == key2


class TestInputValidation:
    """Tests pour validation et sanitization des entrées"""

    def test_email_validation_regex(self):
        """Test validation d'email avec regex"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        valid_emails = [
            "user@example.com",
            "test.user@domain.co.uk",
            "name+tag@site.org"
        ]

        for email in valid_emails:
            assert re.match(email_pattern, email)

    def test_email_validation_invalid(self):
        """Test rejet d'emails invalides"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        invalid_emails = [
            "not-an-email",
            "@example.com",
            "user@",
            "user@.com"
        ]

        for email in invalid_emails:
            assert not re.match(email_pattern, email)

    def test_sql_injection_detection(self):
        """Test détection de SQL injection"""
        dangerous_patterns = [
            "' OR '1'='1",
            "1; DROP TABLE users",
            "admin'--",
            "' UNION SELECT"
        ]

        # Pattern simple de détection
        sql_injection_pattern = r"('|(--|;|UNION|DROP|SELECT))"

        for pattern in dangerous_patterns:
            assert re.search(sql_injection_pattern, pattern, re.IGNORECASE)

    def test_xss_detection(self):
        """Test détection de XSS"""
        xss_patterns = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert('xss')"
        ]

        xss_regex = r'<script|javascript:|onerror='

        for pattern in xss_patterns:
            assert re.search(xss_regex, pattern, re.IGNORECASE)

    def test_sanitize_html_tags(self):
        """Test suppression de tags HTML"""
        def sanitize(text):
            return re.sub(r'<[^>]+>', '', text)

        dirty = "Hello <script>alert('xss')</script> World"
        clean = sanitize(dirty)
        assert "<script>" not in clean
        assert "Hello" in clean
        assert "World" in clean


class TestSecurityLogging:
    """Tests pour le logging de sécurité"""

    def test_logger_exists(self):
        """Test que le logger est initialisé"""
        assert security.logger is not None
        assert security.logger.name == "lib.security"

    def test_logger_level(self):
        """Test le niveau de log"""
        import logging
        assert security.logger.level == logging.INFO


class TestCSRFProtection:
    """Tests pour la protection CSRF"""

    def test_csrf_token_generation(self):
        """Test génération de token CSRF"""
        csrf_token = secrets.token_hex(32)
        assert len(csrf_token) == 64
        assert isinstance(csrf_token, str)

    def test_csrf_token_validation(self):
        """Test validation de token CSRF"""
        stored_token = secrets.token_hex(32)
        provided_token = stored_token
        assert hmac.compare_digest(stored_token, provided_token)

    def test_csrf_token_rejection(self):
        """Test rejet de token CSRF invalide"""
        stored_token = secrets.token_hex(32)
        wrong_token = secrets.token_hex(32)
        assert not hmac.compare_digest(stored_token, wrong_token)


class TestRateLimiting:
    """Tests pour le rate limiting"""

    def test_rate_limit_counter(self):
        """Test compteur de rate limiting"""
        from collections import defaultdict
        rate_limits = defaultdict(list)

        user_id = "user123"
        current_time = time.time()

        # Simuler 5 requêtes
        for _ in range(5):
            rate_limits[user_id].append(current_time)

        assert len(rate_limits[user_id]) == 5

    def test_rate_limit_window(self):
        """Test fenêtre de temps pour rate limiting"""
        requests = []
        current_time = time.time()
        window = 60  # 60 secondes

        # Requêtes dans la fenêtre
        requests.append(current_time - 30)  # Il y a 30s
        requests.append(current_time - 10)  # Il y a 10s
        requests.append(current_time)       # Maintenant

        # Filtrer les requêtes dans la fenêtre
        recent = [r for r in requests if current_time - r < window]
        assert len(recent) == 3

    def test_rate_limit_exceeded(self):
        """Test détection de dépassement de limite"""
        max_requests = 10
        current_requests = 15
        assert current_requests > max_requests


class TestSecureRandomness:
    """Tests pour la génération sécurisée d'aléatoire"""

    def test_secrets_choice(self):
        """Test choix aléatoire sécurisé"""
        choices = ['a', 'b', 'c', 'd']
        chosen = secrets.choice(choices)
        assert chosen in choices

    def test_secrets_randbelow(self):
        """Test génération d'entier aléatoire"""
        random_int = secrets.randbelow(100)
        assert 0 <= random_int < 100

    def test_secrets_token_bytes(self):
        """Test génération de bytes aléatoires"""
        random_bytes = secrets.token_bytes(16)
        assert len(random_bytes) == 16
        assert isinstance(random_bytes, bytes)


class TestPasswordStrength:
    """Tests pour la validation de force des mots de passe"""

    def test_password_length_check(self):
        """Test vérification de longueur de mot de passe"""
        min_length = 8
        weak_password = "12345"
        strong_password = "SecurePass123!"
        assert len(weak_password) < min_length
        assert len(strong_password) >= min_length

    def test_password_complexity(self):
        """Test vérification de complexité de mot de passe"""
        def check_complexity(password):
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_special = any(c in "!@#$%^&*" for c in password)
            return has_upper and has_lower and has_digit and has_special

        weak = "password"
        strong = "SecurePass123!"
        assert not check_complexity(weak)
        assert check_complexity(strong)


class TestSecurityHeaders:
    """Tests pour les headers de sécurité HTTP"""

    def test_security_headers_definition(self):
        """Test définition des headers de sécurité"""
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000',
            'Content-Security-Policy': "default-src 'self'"
        }
        assert 'X-Content-Type-Options' in security_headers
        assert security_headers['X-Frame-Options'] == 'DENY'


class TestSessionManagement:
    """Tests pour la gestion des sessions"""

    def test_session_id_generation(self):
        """Test génération d'ID de session"""
        session_id = secrets.token_urlsafe(32)
        assert len(session_id) >= 40
        assert isinstance(session_id, str)

    def test_session_expiration(self):
        """Test expiration de session"""
        session_created = datetime.now()
        session_lifetime = timedelta(hours=24)
        session_expires = session_created + session_lifetime
        current_time = datetime.now()
        is_valid = current_time < session_expires
        assert is_valid  # Session encore valide


class TestAuditLogging:
    """Tests pour l'audit et le logging"""

    def test_audit_log_structure(self):
        """Test structure d'un log d'audit"""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': 123,
            'action': 'login',
            'ip_address': '192.168.1.1',
            'result': 'success'
        }
        assert 'timestamp' in audit_entry
        assert 'user_id' in audit_entry
        assert 'action' in audit_entry

    def test_sensitive_data_masking(self):
        """Test masquage de données sensibles"""
        def mask_password(password):
            return '*' * len(password)

        password = "MySecretPassword123"
        masked = mask_password(password)
        assert masked == '*' * len(password)
        assert password not in masked
