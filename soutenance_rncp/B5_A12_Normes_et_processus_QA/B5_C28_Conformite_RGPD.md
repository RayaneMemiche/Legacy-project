# Conformité RGPD - AWKWARD LEGACY

**Version:** 1.0
**Date:** 17 Octobre 2025
**Projet:** Modernisation de GeneWeb
**Référence:** Règlement (UE) 2016/679 (RGPD)

---

## Table des matières

1. [Introduction](#1-introduction)
2. [Principes RGPD Appliqués](#2-principes-rgpd-appliqués)
3. [Données Personnelles Collectées](#3-données-personnelles-collectées)
4. [Base Légale du Traitement](#4-base-légale-du-traitement)
5. [Sécurité des Données](#5-sécurité-des-données)
6. [Droits des Utilisateurs](#6-droits-des-utilisateurs)
7. [Conservation des Données](#7-conservation-des-données)
8. [Transferts de Données](#8-transferts-de-données)
9. [Violations de Données](#9-violations-de-données)
10. [Conformité et Audit](#10-conformité-et-audit)

---

## 1. Introduction

AWKWARD LEGACY est une application de gestion d'arbres généalogiques qui traite des données personnelles sensibles. En tant que responsable du traitement, nous nous engageons à respecter intégralement le Règlement Général sur la Protection des Données (RGPD).

### 1.1 Périmètre d'application

Le RGPD s'applique à tous les traitements de données personnelles effectués par AWKWARD LEGACY, notamment:
- Données des utilisateurs de l'application
- Données des personnes dans les arbres généalogiques
- Données de navigation et d'utilisation

### 1.2 Responsable du traitement

**Organisation:** CoinLegacy Inc.
**DPO (Data Protection Officer):** Rayane Memiche
**Contact DPO:** dpo@awkward-legacy.com
**Adresse:** [Adresse légale de l'entreprise]

---

## 2. Principes RGPD Appliqués

### 2.1 Licéité, loyauté et transparence

**Application:**
- Informations claires sur la collecte des données
- Politique de confidentialité accessible
- Consentement explicite avant toute collecte

**Implémentation:**
```python
def collect_user_data(user_input, consent_given):
    """
    Collecte des données uniquement avec consentement explicite
    """
    if not consent_given:
        raise ConsentRequiredError("User consent is required")

    # Log du consentement
    log_consent(user_id, timestamp, consent_type="explicit")

    return process_data(user_input)
```

### 2.2 Limitation des finalités

**Finalités autorisées:**
1. Gestion des arbres généalogiques
2. Fourniture du service d'hébergement
3. Support technique
4. Amélioration du service (avec consentement)

**Finalités interdites:**
- Utilisation commerciale sans consentement
- Revente de données
- Profilage automatique

**Contrôle technique:**
```python
ALLOWED_PURPOSES = [
    "genealogy_management",
    "service_hosting",
    "technical_support",
    "service_improvement"  # Avec consentement additionnel
]

def validate_data_usage(purpose):
    if purpose not in ALLOWED_PURPOSES:
        raise UnauthorizedPurposeError(f"Purpose '{purpose}' not allowed")
```

### 2.3 Minimisation des données

**Principe:** Collecter uniquement les données strictement nécessaires

**Données obligatoires (minimum):**
- Email de l'utilisateur (pour l'authentification)
- Mot de passe (haché)

**Données optionnelles:**
- Nom/prénom de l'utilisateur
- Informations des personnes dans l'arbre (avec consentement)
- Photos (avec consentement explicite)

**Implémentation:**
```python
class PersonData:
    """Modèle de données avec minimisation"""

    # Champs obligatoires minimum
    required_fields = ['firstname', 'lastname']

    # Champs optionnels
    optional_fields = [
        'birth_date',
        'birth_place',
        'death_date',
        'death_place',
        'occupation',
        'notes',
        'photo'
    ]

    def __init__(self, **kwargs):
        # Vérifier que seuls les champs nécessaires sont fournis
        for field in kwargs:
            if field not in self.required_fields + self.optional_fields:
                raise UnnecessaryDataError(f"Field '{field}' not necessary")
```

### 2.4 Exactitude des données

**Mécanismes mis en place:**
- Validation des données à l'entrée
- Possibilité de mise à jour par l'utilisateur
- Vérification périodique de l'exactitude

```python
def validate_person_data(data):
    """Validation de l'exactitude des données"""
    errors = []

    # Vérifier les dates cohérentes
    if data.get('birth_date') and data.get('death_date'):
        if data['death_date'] < data['birth_date']:
            errors.append("Death date cannot be before birth date")

    # Vérifier les formats
    if data.get('email') and not is_valid_email(data['email']):
        errors.append("Invalid email format")

    if errors:
        raise DataValidationError(errors)

    return True
```

### 2.5 Limitation de la conservation

**Durées de conservation:**

| Type de données | Durée de conservation | Justification |
|----------------|----------------------|---------------|
| Compte utilisateur actif | Tant que le compte existe | Service actif |
| Compte inactif | 3 ans après dernière connexion | Obligation légale |
| Données généalogiques | Tant que le propriétaire le souhaite | Finalité du service |
| Logs techniques | 12 mois | Sécurité et débogage |
| Logs de sécurité | 3 ans | Obligation légale |
| Backups | 90 jours | Continuité d'activité |

**Automatisation:**
```python
from datetime import datetime, timedelta

def check_data_retention():
    """Vérification automatique de la rétention des données"""

    # Supprimer les comptes inactifs depuis 3 ans
    inactive_threshold = datetime.now() - timedelta(days=3*365)
    inactive_users = User.objects.filter(
        last_login__lt=inactive_threshold
    )

    for user in inactive_users:
        # Notification avant suppression
        send_deletion_warning(user, days_before_deletion=30)

        if user.deletion_warned_at < datetime.now() - timedelta(days=30):
            anonymize_user_data(user)
            user.delete()

    # Purger les logs anciens
    log_threshold = datetime.now() - timedelta(days=365)
    TechnicalLog.objects.filter(created_at__lt=log_threshold).delete()
```

### 2.6 Intégrité et confidentialité

**Mesures techniques:**
- Chiffrement des données au repos (AES-256)
- Chiffrement des données en transit (TLS 1.3)
- Contrôle d'accès strict (RBAC)
- Audit logs de tous les accès

```python
from cryptography.fernet import Fernet
import hashlib

class DataSecurity:
    """Gestionnaire de sécurité des données"""

    def __init__(self, encryption_key):
        self.cipher = Fernet(encryption_key)

    def encrypt_sensitive_data(self, data):
        """Chiffrement des données sensibles"""
        return self.cipher.encrypt(data.encode())

    def decrypt_sensitive_data(self, encrypted_data):
        """Déchiffrement des données"""
        return self.cipher.decrypt(encrypted_data).decode()

    def hash_password(self, password):
        """Hash sécurisé du mot de passe"""
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # iterations
        )
        return f"{salt}${pwd_hash.hex()}"
```

### 2.7 Responsabilité (Accountability)

**Documentation obligatoire:**
-  Registre des activités de traitement
-  Analyse d'impact (PIA) si nécessaire
-  Politique de confidentialité
-  Procédures de gestion des violations
-  Formation du personnel

---

## 3. Données Personnelles Collectées

### 3.1 Catégories de données

#### A. Données d'identification de l'utilisateur
**Collectées:**
- Email (obligatoire)
- Mot de passe haché (obligatoire)
- Nom, prénom (optionnel)
- Date de création du compte

**Base légale:** Contrat (nécessaire pour fournir le service)

**Durée:** Tant que le compte existe + 3 ans après inactivité

#### B. Données généalogiques
**Collectées:**
- Noms et prénoms des personnes dans l'arbre
- Dates de naissance/décès (optionnel)
- Lieux de naissance/décès (optionnel)
- Relations familiales
- Photos (optionnel, avec consentement explicite)
- Notes et commentaires (optionnel)

**Base légale:** Consentement explicite ou intérêt légitime (recherche historique)

**Particularité:** Données concernant des tiers (nécessite consentement des personnes vivantes)

#### C. Données de connexion
**Collectées:**
- Adresse IP
- Dates et heures de connexion
- Type de navigateur et système d'exploitation
- Pages visitées

**Base légale:** Intérêt légitime (sécurité du système)

**Durée:** 12 mois

#### D. Données de navigation (cookies)
**Collectées:**
- Cookies de session (essentiels)
- Cookies de préférences (avec consentement)
- Cookies analytiques (avec consentement)

**Base légale:** Consentement (sauf cookies essentiels)

**Durée:** Variable selon le type (session à 13 mois max)

### 3.2 Données sensibles

** Attention:** Les données généalogiques peuvent révéler:
- Origine ethnique
- Convictions religieuses
- Santé (dans certains cas)

**Mesures spécifiques:**
- Consentement explicite et séparé
- Chiffrement renforcé
- Accès ultra-restreint
- Logging de tous les accès

```python
class SensitiveDataHandler:
    """Gestionnaire spécial pour données sensibles"""

    @require_explicit_consent("sensitive_data_processing")
    @audit_log
    @encrypt_at_rest
    def store_sensitive_data(self, data, data_type):
        """
        Stockage de données sensibles avec protections renforcées
        """
        if not self.validate_consent(data_type):
            raise ConsentRequiredError(
                "Explicit consent required for sensitive data"
            )

        # Log de l'accès
        self.log_sensitive_access(
            user_id=get_current_user_id(),
            action="STORE",
            data_type=data_type,
            timestamp=datetime.now()
        )

        # Chiffrement renforcé
        encrypted_data = self.double_encrypt(data)

        return self.database.store(encrypted_data)
```

---

## 4. Base Légale du Traitement

### 4.1 Cartographie des traitements

| Traitement | Base légale | Justification |
|-----------|-------------|---------------|
| Création de compte | Contrat | Nécessaire pour fournir le service |
| Gestion de l'arbre | Consentement | Choix de l'utilisateur |
| Photos de personnes | Consentement explicite | Données sensibles |
| Logs de sécurité | Obligation légale | Sécurité des systèmes |
| Amélioration du service | Intérêt légitime | Optimisation (avec opt-out) |
| Newsletter | Consentement | Marketing |

### 4.2 Gestion du consentement

**Caractéristiques du consentement valide:**
-  Libre (aucune contrainte)
-  Spécifique (par finalité)
-  Éclairé (information complète)
-  Univoque (action positive)

**Implémentation:**
```python
class ConsentManager:
    """Gestionnaire de consentements RGPD"""

    CONSENT_TYPES = {
        'account_creation': {
            'required': True,
            'description': "Création et gestion de votre compte"
        },
        'genealogy_data': {
            'required': False,
            'description': "Stockage de données généalogiques"
        },
        'photos': {
            'required': False,
            'sensitive': True,
            'description': "Stockage de photographies"
        },
        'analytics': {
            'required': False,
            'description': "Analyse d'utilisation pour améliorer le service"
        },
        'newsletter': {
            'required': False,
            'description': "Réception de notre newsletter"
        }
    }

    def request_consent(self, user_id, consent_type):
        """Demander le consentement pour un traitement"""
        consent_info = self.CONSENT_TYPES.get(consent_type)

        if not consent_info:
            raise InvalidConsentTypeError(consent_type)

        # Enregistrer la demande de consentement
        ConsentRequest.objects.create(
            user_id=user_id,
            consent_type=consent_type,
            requested_at=datetime.now(),
            description=consent_info['description'],
            is_sensitive=consent_info.get('sensitive', False)
        )

    def record_consent(self, user_id, consent_type, granted):
        """Enregistrer la réponse au consentement"""
        Consent.objects.create(
            user_id=user_id,
            consent_type=consent_type,
            granted=granted,
            granted_at=datetime.now(),
            ip_address=get_client_ip(),
            user_agent=get_user_agent()
        )

        # Log pour accountability
        logger.info(f"Consent recorded: user={user_id}, "
                   f"type={consent_type}, granted={granted}")

    def withdraw_consent(self, user_id, consent_type):
        """Retrait du consentement"""
        consent = Consent.objects.get(
            user_id=user_id,
            consent_type=consent_type,
            active=True
        )

        consent.withdrawn_at = datetime.now()
        consent.active = False
        consent.save()

        # Déclencher la suppression des données associées
        self.delete_data_for_consent_type(user_id, consent_type)

        logger.info(f"Consent withdrawn: user={user_id}, type={consent_type}")
```

**Interface utilisateur:**
```html
<!-- Exemple de formulaire de consentement -->
<form id="consent-form">
    <h2>Gestion de vos consentements</h2>

    <div class="consent-item">
        <input type="checkbox" id="consent-account" checked disabled>
        <label for="consent-account">
            <strong>Création de compte</strong> (Obligatoire)
            <p>Nécessaire pour vous fournir le service.</p>
        </label>
    </div>

    <div class="consent-item">
        <input type="checkbox" id="consent-genealogy">
        <label for="consent-genealogy">
            <strong>Données généalogiques</strong>
            <p>Stockage de votre arbre généalogique et des informations associées.</p>
        </label>
    </div>

    <div class="consent-item sensitive">
        <input type="checkbox" id="consent-photos">
        <label for="consent-photos">
            <strong>Photographies</strong> (Données sensibles)
            <p>Stockage de photographies des personnes de votre arbre.</p>
        </label>
    </div>

    <div class="consent-item">
        <input type="checkbox" id="consent-analytics">
        <label for="consent-analytics">
            <strong>Analytiques</strong>
            <p>Analyse d'utilisation pour améliorer nos services.</p>
        </label>
    </div>

    <button type="submit">Enregistrer mes choix</button>
</form>
```

---

## 5. Sécurité des Données

### 5.1 Chiffrement

#### Au repos (Data at Rest)
**Méthode:** AES-256-GCM
**Portée:** Toutes les données personnelles et sensibles

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class EncryptionService:
    """Service de chiffrement des données"""

    def __init__(self, master_key):
        self.master_key = master_key
        self.aesgcm = AESGCM(master_key)

    def encrypt(self, plaintext):
        """Chiffre les données avec AES-256-GCM"""
        nonce = os.urandom(12)  # 96-bit nonce
        ciphertext = self.aesgcm.encrypt(
            nonce,
            plaintext.encode(),
            None  # No additional authenticated data
        )
        # Retourner nonce + ciphertext
        return nonce + ciphertext

    def decrypt(self, encrypted_data):
        """Déchiffre les données"""
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        plaintext = self.aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode()
```

#### En transit (Data in Transit)
**Protocole:** TLS 1.3
**Configuration:**
```nginx
# Configuration Nginx pour TLS 1.3
server {
    listen 443 ssl http2;
    server_name awkward-legacy.com;

    # Certificats SSL
    ssl_certificate /etc/ssl/certs/awkward-legacy.crt;
    ssl_certificate_key /etc/ssl/private/awkward-legacy.key;

    # Protocoles
    ssl_protocols TLSv1.3;
    ssl_prefer_server_ciphers on;

    # Ciphers sécurisés
    ssl_ciphers 'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256';

    # HSTS (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Autres headers de sécurité
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### 5.2 Authentification et contrôle d'accès

#### Hash des mots de passe
**Algorithme:** PBKDF2-SHA256 avec salt
**Itérations:** 100 000

```python
import hashlib
import secrets

def hash_password(password):
    """Hash sécurisé du mot de passe"""
    # Générer un salt aléatoire
    salt = secrets.token_hex(16)

    # Hash avec PBKDF2
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # iterations
    )

    # Retourner salt + hash
    return f"{salt}${pwd_hash.hex()}"

def verify_password(password, hash_string):
    """Vérifie un mot de passe"""
    salt, pwd_hash = hash_string.split('$')

    test_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )

    return test_hash.hex() == pwd_hash
```

#### Contrôle d'accès (RBAC)
**Rôles définis:**
- **Admin:** Accès complet au système
- **User:** Accès à ses propres données uniquement
- **Support:** Accès lecture seule pour support technique
- **Audit:** Accès aux logs uniquement

```python
from enum import Enum
from functools import wraps

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    SUPPORT = "support"
    AUDIT = "audit"

class Permission(Enum):
    READ_OWN_DATA = "read_own_data"
    WRITE_OWN_DATA = "write_own_data"
    READ_ALL_DATA = "read_all_data"
    WRITE_ALL_DATA = "write_all_data"
    READ_LOGS = "read_logs"
    DELETE_USER = "delete_user"

ROLE_PERMISSIONS = {
    Role.ADMIN: [
        Permission.READ_ALL_DATA,
        Permission.WRITE_ALL_DATA,
        Permission.READ_LOGS,
        Permission.DELETE_USER
    ],
    Role.USER: [
        Permission.READ_OWN_DATA,
        Permission.WRITE_OWN_DATA
    ],
    Role.SUPPORT: [
        Permission.READ_ALL_DATA,
        Permission.READ_LOGS
    ],
    Role.AUDIT: [
        Permission.READ_LOGS
    ]
}

def require_permission(permission):
    """Décorateur pour vérifier les permissions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            user_permissions = ROLE_PERMISSIONS.get(user.role, [])

            if permission not in user_permissions:
                raise PermissionDeniedError(
                    f"User {user.id} lacks permission: {permission.value}"
                )

            # Log de l'accès
            log_access(user.id, permission, func.__name__)

            return func(*args, **kwargs)
        return wrapper
    return decorator

# Utilisation
@require_permission(Permission.READ_ALL_DATA)
def get_all_users():
    return User.objects.all()
```

### 5.3 Audit et logging

**Événements loggés:**
- Toute création/modification/suppression de données
- Tous les accès aux données sensibles
- Toutes les tentatives d'authentification
- Tous les changements de consentement
- Toutes les erreurs de sécurité

```python
import logging
import json
from datetime import datetime

class SecurityAuditLogger:
    """Logger spécial pour l'audit de sécurité"""

    def __init__(self):
        self.logger = logging.getLogger('security_audit')
        handler = logging.FileHandler('/var/log/awkward-legacy/security-audit.log')
        formatter = logging.Formatter(
            '%(asctime)s - AUDIT - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log_data_access(self, user_id, action, resource_type, resource_id,
                       ip_address, user_agent):
        """Log d'accès aux données"""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'action': action,  # READ, WRITE, DELETE
            'resource_type': resource_type,
            'resource_id': resource_id,
            'ip_address': ip_address,
            'user_agent': user_agent
        }

        self.logger.info(json.dumps(audit_entry))

        # Stocker aussi en base pour requêtes
        AuditLog.objects.create(**audit_entry)

    def log_authentication(self, user_id, success, ip_address, reason=None):
        """Log de tentative d'authentification"""
        auth_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'AUTHENTICATION',
            'user_id': user_id,
            'success': success,
            'ip_address': ip_address,
            'reason': reason
        }

        self.logger.info(json.dumps(auth_entry))

        # Détecter les tentatives de brute force
        if not success:
            self.check_brute_force(user_id, ip_address)

    def check_brute_force(self, user_id, ip_address):
        """Détection de tentatives de brute force"""
        recent_failures = AuditLog.objects.filter(
            event_type='AUTHENTICATION',
            success=False,
            ip_address=ip_address,
            timestamp__gte=datetime.now() - timedelta(minutes=15)
        ).count()

        if recent_failures >= 5:
            # Bloquer temporairement l'IP
            self.block_ip(ip_address, duration_minutes=30)
            self.send_alert(
                f"Brute force detected from IP {ip_address}"
            )
```

### 5.4 Sauvegarde et récupération

**Politique de backup:**
- Backup quotidien automatique
- Rétention: 90 jours
- Stockage chiffré
- Test de restauration mensuel

```bash
#!/bin/bash
# Script de backup automatique

BACKUP_DIR="/var/backups/awkward-legacy"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_${DATE}.tar.gz.enc"

# Créer le backup
tar -czf - /data/awkward-legacy | \
    openssl enc -aes-256-cbc -salt -pbkdf2 \
    -out "${BACKUP_DIR}/${BACKUP_FILE}"

# Vérifier l'intégrité
if [ $? -eq 0 ]; then
    echo "Backup successful: ${BACKUP_FILE}"

    # Supprimer les backups de plus de 90 jours
    find ${BACKUP_DIR} -name "backup_*.tar.gz.enc" -mtime +90 -delete

    # Upload vers stockage distant sécurisé
    aws s3 cp "${BACKUP_DIR}/${BACKUP_FILE}" \
        s3://awkward-legacy-backups/ \
        --server-side-encryption AES256
else
    echo "Backup failed!" >&2
    exit 1
fi
```

---

## 6. Droits des Utilisateurs

### 6.1 Droit d'accès (Article 15 RGPD)

**Implémentation:**
```python
@require_authentication
def export_user_data(user_id):
    """
    Exporte toutes les données personnelles de l'utilisateur
    Délai de réponse: 30 jours max
    """
    user = User.objects.get(id=user_id)

    # Collecter toutes les données
    user_data = {
        'account': {
            'email': user.email,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat(),
        },
        'profile': {
            'firstname': user.profile.firstname,
            'lastname': user.profile.lastname,
        },
        'genealogy_trees': [],
        'consents': [],
        'access_logs': []
    }

    # Arbres généalogiques
    for tree in user.trees.all():
        tree_data = {
            'name': tree.name,
            'created_at': tree.created_at.isoformat(),
            'persons': [p.to_dict() for p in tree.persons.all()],
            'families': [f.to_dict() for f in tree.families.all()]
        }
        user_data['genealogy_trees'].append(tree_data)

    # Consentements
    for consent in user.consents.all():
        consent_data = {
            'type': consent.consent_type,
            'granted': consent.granted,
            'granted_at': consent.granted_at.isoformat()
        }
        user_data['consents'].append(consent_data)

    # Logs d'accès (6 derniers mois)
    recent_logs = AuditLog.objects.filter(
        user_id=user_id,
        timestamp__gte=datetime.now() - timedelta(days=180)
    )
    for log in recent_logs:
        log_data = {
            'timestamp': log.timestamp.isoformat(),
            'action': log.action,
            'ip_address': log.ip_address
        }
        user_data['access_logs'].append(log_data)

    # Générer un fichier JSON
    filename = f"user_data_{user_id}_{datetime.now().strftime('%Y%m%d')}.json"
    filepath = f"/tmp/{filename}"

    with open(filepath, 'w') as f:
        json.dump(user_data, f, indent=2, ensure_ascii=False)

    # Envoyer par email sécurisé ou téléchargement
    send_secure_download_link(user.email, filepath)

    # Log de la demande d'accès
    logger.info(f"Data access request fulfilled for user {user_id}")

    return filepath
```

**Endpoint API:**
```python
@app.route('/api/user/<int:user_id>/data', methods=['GET'])
@require_authentication
@require_permission(Permission.READ_OWN_DATA)
def get_user_data(user_id):
    """API pour récupérer ses données personnelles"""

    # Vérifier que l'utilisateur accède à ses propres données
    if get_current_user_id() != user_id:
        raise PermissionDeniedError("Can only access own data")

    filepath = export_user_data(user_id)

    return send_file(filepath, as_attachment=True)
```

### 6.2 Droit de rectification (Article 16 RGPD)

**Implémentation:**
```python
@app.route('/api/user/<int:user_id>/data', methods=['PUT'])
@require_authentication
@require_permission(Permission.WRITE_OWN_DATA)
def update_user_data(user_id):
    """API pour rectifier ses données personnelles"""

    if get_current_user_id() != user_id:
        raise PermissionDeniedError("Can only update own data")

    data = request.get_json()

    # Validation des données
    validate_user_data(data)

    # Mise à jour
    user = User.objects.get(id=user_id)

    # Log des modifications
    changes = []
    for field, new_value in data.items():
        old_value = getattr(user, field, None)
        if old_value != new_value:
            changes.append({
                'field': field,
                'old_value': old_value,
                'new_value': new_value
            })
            setattr(user, field, new_value)

    user.save()

    # Audit log
    logger.info(f"Data rectification for user {user_id}: {changes}")

    return {'message': 'Data updated successfully', 'changes': changes}
```

### 6.3 Droit à l'effacement / Droit à l'oubli (Article 17 RGPD)

**Implémentation:**
```python
@app.route('/api/user/<int:user_id>/gdpr', methods=['DELETE'])
@require_authentication
@require_permission(Permission.DELETE_USER)
def delete_user_gdpr(user_id):
    """
    Suppression complète des données utilisateur (droit à l'oubli)
    Délai: Immédiat (avec période de grâce de 30 jours)
    """

    user = User.objects.get(id=user_id)

    # Vérifier les exceptions au droit à l'oubli
    if has_legal_obligation_to_retain(user):
        return {
            'error': 'Cannot delete due to legal obligations',
            'reason': 'Active legal proceedings'
        }, 403

    # Marquer pour suppression (période de grâce 30 jours)
    user.deletion_requested_at = datetime.now()
    user.deletion_scheduled_for = datetime.now() + timedelta(days=30)
    user.save()

    # Envoyer email de confirmation
    send_deletion_confirmation_email(user)

    # Log
    logger.info(f"Deletion requested for user {user_id}")

    return {
        'message': 'Deletion scheduled',
        'deletion_date': user.deletion_scheduled_for.isoformat(),
        'cancellation_possible_until': user.deletion_scheduled_for.isoformat()
    }

def execute_user_deletion(user_id):
    """Exécution effective de la suppression après période de grâce"""

    user = User.objects.get(id=user_id)

    # Supprimer toutes les données associées
    user.trees.all().delete()
    user.consents.all().delete()

    # Anonymiser les logs (garder pour statistiques)
    AuditLog.objects.filter(user_id=user_id).update(
        user_id=None,
        anonymized=True
    )

    # Supprimer le compte
    user.delete()

    logger.info(f"User {user_id} deleted (GDPR right to erasure)")
```

### 6.4 Droit à la limitation du traitement (Article 18 RGPD)

**Implémentation:**
```python
@app.route('/api/user/<int:user_id>/processing/limit', methods=['POST'])
@require_authentication
def limit_data_processing(user_id):
    """Limiter le traitement des données"""

    user = User.objects.get(id=user_id)

    # Activer le mode "limitation de traitement"
    user.processing_limited = True
    user.processing_limited_since = datetime.now()
    user.processing_limited_reason = request.json.get('reason')
    user.save()

    # Les données restent stockées mais ne sont plus traitées
    # (sauf conservation, sauf consentement explicite pour cas spécifique)

    logger.info(f"Processing limited for user {user_id}")

    return {'message': 'Processing limited successfully'}
```

### 6.5 Droit à la portabilité (Article 20 RGPD)

**Implémentation:**
```python
@app.route('/api/user/<int:user_id>/export', methods=['GET'])
@require_authentication
def export_portable_data(user_id):
    """
    Export des données dans un format structuré,
    couramment utilisé et lisible par machine (JSON, CSV, GEDCOM)
    """

    format_requested = request.args.get('format', 'json')

    user = User.objects.get(id=user_id)

    if format_requested == 'json':
        data = export_user_data(user_id)  # Réutilise fonction d'accès
        return send_file(data, mimetype='application/json')

    elif format_requested == 'gedcom':
        # Export au format GEDCOM (standard généalogie)
        gedcom_file = export_to_gedcom(user.trees.all())
        return send_file(gedcom_file, mimetype='text/x-gedcom')

    elif format_requested == 'csv':
        # Export CSV pour tableur
        csv_file = export_to_csv(user.trees.all())
        return send_file(csv_file, mimetype='text/csv')

    else:
        return {'error': 'Unsupported format'}, 400
```

### 6.6 Droit d'opposition (Article 21 RGPD)

**Implémentation:**
```python
@app.route('/api/user/<int:user_id>/processing/object', methods=['POST'])
@require_authentication
def object_to_processing(user_id):
    """S'opposer à un traitement particulier"""

    processing_type = request.json.get('processing_type')

    # L'utilisateur peut s'opposer aux traitements basés sur intérêt légitime
    OBJECTABLE_PROCESSINGS = [
        'analytics',
        'service_improvement',
        'marketing'
    ]

    if processing_type not in OBJECTABLE_PROCESSINGS:
        return {
            'error': 'Cannot object to this processing',
            'reason': 'This processing is necessary for the service'
        }, 400

    # Retirer le consentement ou marquer l'opposition
    consent = Consent.objects.get(
        user_id=user_id,
        consent_type=processing_type
    )
    consent.objection_raised = True
    consent.objection_date = datetime.now()
    consent.active = False
    consent.save()

    # Arrêter le traitement concerné
    stop_processing(user_id, processing_type)

    logger.info(f"User {user_id} objected to processing: {processing_type}")

    return {'message': 'Objection registered', 'processing_stopped': True}
```

---

## 7. Conservation des Données

### 7.1 Politique de rétention

**Tableau récapitulatif:**

| Données | Durée active | Durée archive | Durée totale | Justification |
|---------|--------------|---------------|--------------|---------------|
| Compte actif | Illimitée | - | Tant que compte existe | Service actif |
| Compte inactif | 3 ans | - | 3 ans après dernière connexion | CNIL recommandation |
| Données généalogiques | Illimitée* | - | Tant que propriétaire veut | Finalité service |
| Logs techniques | 12 mois | - | 12 mois | Maintenance |
| Logs sécurité | 3 ans | - | 3 ans | Obligation légale |
| Logs audit | 5 ans | - | 5 ans | Compliance |
| Backups | 90 jours | - | 90 jours | Continuité activité |
| Données supprimées | - | 0 jour | Suppression immédiate | RGPD |

*Avec consentement explicite renouvelé périodiquement

### 7.2 Automatisation de la purge

**Script de purge automatique:**
```python
from celery import Celery
from datetime import datetime, timedelta

app = Celery('tasks')

@app.task
def daily_data_retention_check():
    """Tâche quotidienne de vérification de la rétention"""

    today = datetime.now()

    # 1. Comptes inactifs depuis 3 ans
    inactive_threshold = today - timedelta(days=3*365)
    inactive_users = User.objects.filter(
        last_login__lt=inactive_threshold,
        deletion_warned=False
    )

    for user in inactive_users:
        # Avertir l'utilisateur
        send_inactivity_warning(user)
        user.deletion_warned = True
        user.deletion_warning_sent_at = today
        user.save()

    # 2. Comptes avertis il y a 30 jours (période de grâce)
    deletion_threshold = today - timedelta(days=30)
    users_to_delete = User.objects.filter(
        deletion_warned=True,
        deletion_warning_sent_at__lt=deletion_threshold
    )

    for user in users_to_delete:
        anonymize_and_delete_user(user)

    # 3. Purger les logs techniques > 12 mois
    log_threshold = today - timedelta(days=365)
    TechnicalLog.objects.filter(created_at__lt=log_threshold).delete()

    # 4. Purger les backups > 90 jours
    backup_threshold = today - timedelta(days=90)
    old_backups = Backup.objects.filter(created_at__lt=backup_threshold)
    for backup in old_backups:
        delete_backup_file(backup)
        backup.delete()

    # 5. Anonymiser les données personnelles dans les logs > 3 ans
    anonymization_threshold = today - timedelta(days=3*365)
    AuditLog.objects.filter(
        timestamp__lt=anonymization_threshold,
        anonymized=False
    ).update(
        user_id=None,
        ip_address='0.0.0.0',
        anonymized=True
    )

    logger.info("Data retention check completed")

def anonymize_and_delete_user(user):
    """Anonymisation puis suppression d'un compte inactif"""

    # Anonymiser avant suppression (pour historique)
    user.email = f"deleted_{user.id}@anonymized.local"
    user.firstname = "[DELETED]"
    user.lastname = "[DELETED]"
    user.anonymized_at = datetime.now()
    user.save()

    # Attendre 30 jours supplémentaires avant suppression définitive
    # pour permettre réclamation
    user.scheduled_deletion_at = datetime.now() + timedelta(days=30)
    user.save()
```

**Configuration Cron:**
```bash
# Crontab pour exécution quotidienne à 2h du matin
0 2 * * * /usr/bin/python /app/scripts/data_retention.py
```

---

## 8. Transferts de Données

### 8.1 Transferts hors UE

**Politique:** Minimiser les transferts hors UE

**Si transfert nécessaire:**
-  Clauses contractuelles types (CCT) de la Commission Européenne
-  Garanties appropriées (Privacy Shield si applicable)
-  Consentement explicite de l'utilisateur
-  Évaluation des risques (TIA - Transfer Impact Assessment)

**Implémentation:**
```python
class DataTransferManager:
    """Gestionnaire des transferts de données"""

    EU_COUNTRIES = ['FR', 'DE', 'IT', 'ES', 'BE', 'NL', 'etc.']
    ADEQUATE_COUNTRIES = ['CH', 'CA', 'JP', 'GB', 'etc.']  # Décisions d'adéquation

    def can_transfer_to_country(self, country_code):
        """Vérifie si un transfert vers un pays est autorisé"""

        # UE: Toujours OK
        if country_code in self.EU_COUNTRIES:
            return True, "EU country"

        # Pays avec décision d'adéquation
        if country_code in self.ADEQUATE_COUNTRIES:
            return True, "Adequacy decision"

        # Autres pays: nécessite garanties
        return False, "Requires safeguards (SCC, consent, etc.)"

    def transfer_with_safeguards(self, data, destination_country, user_consent=False):
        """Transfert avec garanties appropriées"""

        can_transfer, reason = self.can_transfer_to_country(destination_country)

        if not can_transfer:
            if not user_consent:
                raise TransferNotAllowedError(
                    f"Transfer to {destination_country} requires explicit consent"
                )

            # Vérifier que le consentement est valide
            if not self.verify_transfer_consent(data.user_id, destination_country):
                raise InvalidConsentError("Valid consent not found")

        # Log du transfert
        self.log_data_transfer(
            user_id=data.user_id,
            destination_country=destination_country,
            data_type=data.type,
            reason=reason,
            consent_given=user_consent
        )

        # Effectuer le transfert avec chiffrement
        encrypted_data = self.encrypt_for_transfer(data)
        return self.send_data(encrypted_data, destination_country)
```

### 8.2 Sous-traitants

**Liste des sous-traitants:**

| Sous-traitant | Service | Localisation | Garanties |
|---------------|---------|--------------|-----------|
| AWS | Hébergement | UE (Ireland) | DPA + CCT |
| SendGrid | Emails | USA | Privacy Shield + CCT |
| Stripe | Paiements | USA | Privacy Shield + PCI-DSS |

**Contrat de sous-traitance (DPA):**
```markdown
# Data Processing Agreement (DPA)

Entre:
- Responsable du traitement: CoinLegacy Inc.
- Sous-traitant: [Nom du sous-traitant]

Article 1: Objet
Le sous-traitant s'engage à traiter les données personnelles uniquement
pour le compte du responsable du traitement.

Article 2: Durée
La durée du contrat correspond à celle du contrat principal.

Article 3: Obligations du sous-traitant
- Traiter les données uniquement sur instruction documentée
- Garantir la confidentialité
- Assurer la sécurité des données
- Assister le responsable pour les droits des personnes
- Notifier les violations de données sous 24h
- Supprimer ou restituer les données à la fin du contrat

Article 4: Sous-traitance ultérieure
Le sous-traitant ne peut recourir à un autre sous-traitant qu'avec
l'accord écrit préalable du responsable du traitement.

Article 5: Audits
Le responsable peut auditer le sous-traitant à tout moment.
```

---

## 9. Violations de Données

### 9.1 Procédure de notification

**Délais RGPD:**
- ⏰ 72 heures max pour notifier la CNIL
- ⏰ Sans délai pour notifier les personnes concernées (si risque élevé)

**Workflow:**
```python
class DataBreachManager:
    """Gestionnaire des violations de données"""

    def detect_breach(self, breach_type, affected_data, affected_users):
        """Détection et enregistrement d'une violation"""

        breach = DataBreach.objects.create(
            detected_at=datetime.now(),
            breach_type=breach_type,
            affected_data_types=affected_data,
            affected_user_count=len(affected_users),
            status='DETECTED'
        )

        # Alerte immédiate
        self.send_immediate_alert(breach)

        # Lancer la procédure de gestion
        self.handle_breach(breach, affected_users)

        return breach

    def handle_breach(self, breach, affected_users):
        """Gestion d'une violation de données"""

        # Étape 1: Contenir la violation
        self.contain_breach(breach)
        breach.status = 'CONTAINED'
        breach.contained_at = datetime.now()
        breach.save()

        # Étape 2: Évaluer la gravité
        severity = self.assess_breach_severity(breach)
        breach.severity = severity
        breach.save()

        # Étape 3: Notifier si nécessaire
        if severity in ['HIGH', 'CRITICAL']:
            # Notifier la CNIL sous 72h
            self.notify_cnil(breach)
            breach.cnil_notified_at = datetime.now()

            # Notifier les personnes concernées si risque élevé
            if severity == 'CRITICAL':
                self.notify_affected_users(breach, affected_users)
                breach.users_notified_at = datetime.now()

        breach.save()

        # Étape 4: Documenter
        self.document_breach(breach)

    def assess_breach_severity(self, breach):
        """Évaluation de la gravité de la violation"""

        # Critères d'évaluation
        criteria = {
            'data_sensitivity': 0,  # 0-3
            'number_of_people': 0,  # 0-3
            'ease_of_identification': 0,  # 0-3
            'consequences_severity': 0,  # 0-3
            'special_categories': 0  # 0-3
        }

        # Données sensibles?
        if 'passwords' in breach.affected_data_types:
            criteria['data_sensitivity'] = 3
        elif 'financial' in breach.affected_data_types:
            criteria['data_sensitivity'] = 2
        elif 'email' in breach.affected_data_types:
            criteria['data_sensitivity'] = 1

        # Nombre de personnes
        if breach.affected_user_count > 10000:
            criteria['number_of_people'] = 3
        elif breach.affected_user_count > 1000:
            criteria['number_of_people'] = 2
        elif breach.affected_user_count > 100:
            criteria['number_of_people'] = 1

        # Score total
        total_score = sum(criteria.values())

        if total_score >= 12:
            return 'CRITICAL'
        elif total_score >= 8:
            return 'HIGH'
        elif total_score >= 4:
            return 'MEDIUM'
        else:
            return 'LOW'

    def notify_cnil(self, breach):
        """Notification à la CNIL"""

        notification = {
            'controller': {
                'name': 'CoinLegacy Inc.',
                'contact': 'dpo@awkward-legacy.com'
            },
            'breach': {
                'detected_at': breach.detected_at.isoformat(),
                'type': breach.breach_type,
                'affected_data': breach.affected_data_types,
                'affected_count': breach.affected_user_count,
                'severity': breach.severity
            },
            'measures': {
                'containment': 'Immediate system isolation',
                'mitigation': 'Password reset for all affected users',
                'prevention': 'Security audit and patches'
            }
        }

        # Envoyer via le formulaire en ligne de la CNIL
        # https://www.cnil.fr/fr/notifier-une-violation-de-donnees-personnelles

        logger.critical(f"CNIL notification sent for breach {breach.id}")

    def notify_affected_users(self, breach, affected_users):
        """Notification aux personnes concernées"""

        for user in affected_users:
            email_content = f"""
            Objet: Notification importante - Sécurité de vos données

            Madame, Monsieur,

            Nous vous informons qu'un incident de sécurité a affecté vos données
            personnelles le {breach.detected_at.strftime('%d/%m/%Y')}.

            Données concernées: {', '.join(breach.affected_data_types)}

            Mesures prises:
            - Violation contenue immédiatement
            - Réinitialisation de votre mot de passe
            - Renforcement de notre sécurité

            Actions recommandées:
            - Changez votre mot de passe immédiatement
            - Surveillez vos comptes
            - Activez l'authentification à deux facteurs

            Nous restons à votre disposition: support@awkward-legacy.com

            Cordialement,
            L'équipe AWKWARD LEGACY
            """

            send_email(user.email, "Notification de sécurité", email_content)

        logger.critical(f"Notified {len(affected_users)} users for breach {breach.id}")
```

### 9.2 Registre des violations

**Format du registre:**
```python
class DataBreach(models.Model):
    """Modèle pour le registre des violations"""

    # Identification
    id = models.AutoField(primary_key=True)
    detected_at = models.DateTimeField()
    breach_type = models.CharField(max_length=100)

    # Description
    description = models.TextField()
    affected_data_types = models.JSONField()
    affected_user_count = models.IntegerField()

    # Évaluation
    severity = models.CharField(
        max_length=20,
        choices=[
            ('LOW', 'Faible'),
            ('MEDIUM', 'Moyen'),
            ('HIGH', 'Élevé'),
            ('CRITICAL', 'Critique')
        ]
    )

    # Gestion
    status = models.CharField(
        max_length=20,
        choices=[
            ('DETECTED', 'Détectée'),
            ('CONTAINED', 'Contenue'),
            ('RESOLVED', 'Résolue')
        ]
    )
    contained_at = models.DateTimeField(null=True)
    resolved_at = models.DateTimeField(null=True)

    # Notifications
    cnil_notified_at = models.DateTimeField(null=True)
    users_notified_at = models.DateTimeField(null=True)

    # Mesures
    containment_measures = models.TextField()
    mitigation_measures = models.TextField()
    prevention_measures = models.TextField()

    # Documentation
    post_mortem_url = models.URLField(null=True)
```

---

## 10. Conformité et Audit

### 10.1 Registre des activités de traitement

**Obligation RGPD Article 30:**

**Registre des traitements:**
```markdown
# REGISTRE DES ACTIVITÉS DE TRAITEMENT

## Traitement 1: Gestion des comptes utilisateurs

**Responsable:** CoinLegacy Inc.
**Contact DPO:** dpo@awkward-legacy.com

**Finalités:**
- Création et gestion de compte
- Authentification
- Support technique

**Catégories de personnes concernées:**
- Utilisateurs de l'application

**Catégories de données:**
- Email, mot de passe (haché)
- Date de création, dernière connexion
- Logs d'authentification

**Catégories de destinataires:**
- Équipe support (accès limité)
- Sous-traitant hébergement (AWS)

**Transferts hors UE:**
- Aucun

**Délais d'effacement:**
- 3 ans après dernière connexion

**Mesures de sécurité:**
- Chiffrement AES-256
- Hash PBKDF2-SHA256
- TLS 1.3
- Authentification à 2 facteurs

---

## Traitement 2: Gestion des arbres généalogiques

**Responsable:** CoinLegacy Inc.

**Finalités:**
- Stockage des données généalogiques
- Calcul de consanguinité
- Export GEDCOM

**Catégories de personnes concernées:**
- Personnes mentionnées dans les arbres généalogiques

**Catégories de données:**
- Noms, prénoms, dates de naissance/décès
- Relations familiales
- Lieux de naissance/décès
- Photos (optionnel)

**Base légale:**
- Consentement explicite (personnes vivantes)
- Intérêt légitime (recherche historique pour personnes décédées)

**Catégories de destinataires:**
- Propriétaire de l'arbre uniquement
- Personnes autorisées par le propriétaire

**Transferts hors UE:**
- Aucun

**Délais d'effacement:**
- À la demande du propriétaire
- 3 ans après suppression du compte

**Mesures de sécurité:**
- Chiffrement AES-256
- Contrôle d'accès strict (RBAC)
- Audit logs de tous les accès
- Consentement explicite pour photos
```

### 10.2 Analyse d'impact (PIA/DPIA)

**Quand réaliser une PIA:**
-  Traitement de données sensibles à grande échelle
-  Profilage automatisé
-  Surveillance systématique
-  Nouvelles technologies

**Template PIA:**
```markdown
# Privacy Impact Assessment (PIA)

**Traitement évalué:** [Nom du traitement]
**Date:** [Date de l'évaluation]
**Évaluateur:** [Nom du DPO ou responsable]

## 1. Description du traitement

**Finalités:**
[Description des finalités]

**Données traitées:**
[Liste des données]

**Personnes concernées:**
[Catégories de personnes]

## 2. Nécessité et proportionnalité

**Nécessité:**
- Le traitement est-il nécessaire? Oui/Non
- Existe-t-il des alternatives moins intrusives? Oui/Non

**Proportionnalité:**
- Les données collectées sont-elles limitées au strict nécessaire? Oui/Non
- La durée de conservation est-elle appropriée? Oui/Non

## 3. Risques identifiés

| Risque | Probabilité | Impact | Gravité | Mesures |
|--------|-------------|--------|---------|---------|
| Accès non autorisé | Moyenne | Élevé | ÉLEVÉ | Authentification renforcée |
| Perte de données | Faible | Élevé | MOYEN | Backups quotidiens |
| etc. | | | | |

## 4. Mesures de sécurité

**Mesures techniques:**
- Chiffrement AES-256
- TLS 1.3
- Authentification à 2 facteurs

**Mesures organisationnelles:**
- Formation du personnel
- Politique de sécurité
- Audits réguliers

## 5. Conclusion

**Risque résiduel:** FAIBLE/MOYEN/ÉLEVÉ

**Recommandations:**
[Liste des recommandations]

**Validation DPO:**  Approuvé  Rejeté
**Date:** [Date]
**Signature:**
```

### 10.3 Audits et contrôles

**Programme d'audit:**

| Fréquence | Type d'audit | Responsable |
|-----------|--------------|-------------|
| Trimestriel | Audit de conformité RGPD | DPO |
| Semestriel | Audit de sécurité | RSSI |
| Annuel | Audit externe | Auditeur certifié |
| Continu | Monitoring automatique | DevOps |

**Checklist d'audit RGPD:**
```markdown
# CHECKLIST AUDIT RGPD

## Principes fondamentaux

- [ ] Licéité des traitements vérifiée
- [ ] Finalités définies et légitimes
- [ ] Minimisation des données respectée
- [ ] Exactitude des données assurée
- [ ] Limitation de conservation documentée
- [ ] Sécurité appropriée implémentée
- [ ] Accountability démontrée

## Documentation

- [ ] Registre des traitements à jour
- [ ] PIA réalisées si nécessaire
- [ ] Politique de confidentialité accessible
- [ ] Mentions légales conformes
- [ ] DPA avec sous-traitants signés

## Droits des personnes

- [ ] Procédure d'exercice des droits en place
- [ ] Délais de réponse respectés (30 jours)
- [ ] Droit d'accès fonctionnel
- [ ] Droit de rectification fonctionnel
- [ ] Droit à l'effacement fonctionnel
- [ ] Droit à la portabilité fonctionnel

## Sécurité

- [ ] Chiffrement au repos et en transit
- [ ] Contrôle d'accès strict
- [ ] Audit logs activés
- [ ] Procédure de gestion des violations
- [ ] Backups réguliers et testés
- [ ] Plan de continuité d'activité

## Sous-traitance

- [ ] Liste des sous-traitants à jour
- [ ] DPA signés avec tous les sous-traitants
- [ ] Audits des sous-traitants réalisés
- [ ] Garanties appropriées pour transferts hors UE

## Formation et sensibilisation

- [ ] Personnel formé au RGPD
- [ ] Politique de sécurité communiquée
- [ ] Sensibilisation régulière

## Violations de données

- [ ] Procédure de notification en place
- [ ] Registre des violations tenu
- [ ] Délais de notification respectés

## Score total: ____ / 30

**Niveau de conformité:**
- 25-30: Excellent
- 20-24: Bon
- 15-19: Moyen (améliorations nécessaires)
- < 15: Insuffisant (actions urgentes requises)
```

---

## 11. Contacts et Ressources

### 11.1 Contacts internes

**Data Protection Officer (DPO):**
- Email: dpo@awkward-legacy.com
- Téléphone: +33 6 XX XX XX XX
- Disponibilité: Lun-Ven 9h-17h

**Support utilisateurs:**
- Email: support@awkward-legacy.com
- Formulaire: https://awkward-legacy.com/support

### 11.2 Autorités de contrôle

**CNIL (France):**
- Site: https://www.cnil.fr
- Téléphone: 01 53 73 22 22
- Adresse: 3 Place de Fontenoy, 75007 Paris

**Plaintes:**
https://www.cnil.fr/fr/plaintes

### 11.3 Ressources utiles

**Documentation RGPD:**
- Texte officiel: https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32016R0679
- Guide CNIL: https://www.cnil.fr/fr/reglement-europeen-protection-donnees

**Outils:**
- Registre des traitements: https://www.cnil.fr/fr/modele-de-registre
- PIA: https://www.cnil.fr/fr/outil-pia-telechargez-et-installez-le-logiciel-de-la-cnil

---

## 12. Historique des révisions

| Version | Date | Auteur | Modifications |
|---------|------|--------|---------------|
| 1.0 | 17/10/2025 | [DPO] | Version initiale |

---

**Dernière mise à jour:** 17 Octobre 2025
**Prochaine révision:** Janvier 2026
**Approuvé par:** Rayane Memiche (DPO)