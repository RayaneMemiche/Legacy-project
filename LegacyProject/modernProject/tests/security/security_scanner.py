#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scanner de sécurité pour AWKWARD LEGACY

Ce script effectue un audit de sécurité complet de l'application
en vérifiant les vulnérabilités OWASP Top 10 et autres failles.

Usage:
    python security_scanner.py [--full] [--report]
"""

import os
import sys
import re
import json
import time
import hashlib
import subprocess
import socket
import ssl
import urllib.parse
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
from enum import Enum
import argparse
import requests
from pathlib import Path


class SeverityLevel(Enum):
    """Niveaux de sévérité des vulnérabilités"""
    CRITICAL = "🔴 CRITIQUE"
    HIGH = "🟠 ÉLEVÉ"
    MEDIUM = "🟡 MOYEN"
    LOW = "🟢 FAIBLE"
    INFO = "ℹ️  INFO"


class VulnerabilityType(Enum):
    """Types de vulnérabilités (OWASP Top 10 2021)"""
    A01_BROKEN_ACCESS_CONTROL = "Contrôle d'accès défaillant"
    A02_CRYPTOGRAPHIC_FAILURES = "Défaillances cryptographiques"
    A03_INJECTION = "Injection"
    A04_INSECURE_DESIGN = "Conception non sécurisée"
    A05_SECURITY_MISCONFIGURATION = "Mauvaise configuration de sécurité"
    A06_VULNERABLE_COMPONENTS = "Composants vulnérables"
    A07_AUTH_FAILURES = "Défaillances d'authentification"
    A08_DATA_INTEGRITY_FAILURES = "Défaillances d'intégrité des données"
    A09_LOGGING_FAILURES = "Défaillances de journalisation"
    A10_SSRF = "Server-Side Request Forgery"


class SecurityScanner:
    """Scanner de sécurité principal"""

    def __init__(self, target_url: str = "http://localhost:8000", verbose: bool = False):
        self.target_url = target_url
        self.verbose = verbose
        self.vulnerabilities = []
        self.scan_results = {}
        self.start_time = None
        self.session = requests.Session()

        # Configuration des headers par défaut
        self.session.headers.update({
            'User-Agent': 'AWKWARD-Security-Scanner/1.0'
        })

        print("="*70)
        print("AWKWARD LEGACY - SCANNER DE SÉCURITÉ")
        print("="*70)
        print(f"Cible: {self.target_url}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")

    def run_full_scan(self) -> Dict[str, Any]:
        """Execute un scan de sécurité complet"""
        self.start_time = time.time()

        print("🔍 Démarrage du scan de sécurité...\n")

        # Phase 1: Reconnaissance
        self._phase_reconnaissance()

        # Phase 2: Tests OWASP Top 10
        self._phase_owasp_tests()

        # Phase 3: Tests d'infrastructure
        self._phase_infrastructure_tests()

        # Phase 4: Tests de configuration
        self._phase_configuration_tests()

        # Phase 5: Tests de code
        self._phase_code_analysis()

        # Génération du rapport
        elapsed_time = time.time() - self.start_time
        report = self._generate_report(elapsed_time)

        return report

    # ========================================================================
    # PHASE 1: RECONNAISSANCE
    # ========================================================================

    def _phase_reconnaissance(self):
        """Phase de reconnaissance et collecte d'informations"""
        print("📡 PHASE 1: Reconnaissance")
        print("-" * 50)

        # Détection de technologies
        self._detect_technologies()

        # Énumération des endpoints
        self._enumerate_endpoints()

        # Détection des headers de sécurité
        self._check_security_headers()

        # Scan des ports
        self._scan_ports()

        print()

    def _detect_technologies(self):
        """Détecte les technologies utilisées"""
        print("  → Détection des technologies...")

        try:
            response = self.session.get(self.target_url, timeout=5)

            # Analyse des headers
            server = response.headers.get('Server', 'Unknown')
            powered_by = response.headers.get('X-Powered-By', 'Unknown')

            # Analyse du contenu
            technologies = []

            if 'django' in response.text.lower() or 'csrftoken' in response.cookies:
                technologies.append('Django')

            if 'flask' in response.text.lower():
                technologies.append('Flask')

            if 'react' in response.text.lower():
                technologies.append('React')

            if 'vue' in response.text.lower():
                technologies.append('Vue.js')

            self.scan_results['technologies'] = {
                'server': server,
                'powered_by': powered_by,
                'detected': technologies
            }

            print(f"    ✓ Server: {server}")
            print(f"    ✓ Technologies détectées: {', '.join(technologies) if technologies else 'N/A'}")

        except Exception as e:
            print(f"    ✗ Erreur: {str(e)}")

    def _enumerate_endpoints(self):
        """Énumère les endpoints disponibles"""
        print("  → Énumération des endpoints...")

        common_endpoints = [
            '/api', '/api/docs', '/api/swagger',
            '/admin', '/login', '/register',
            '/dashboard', '/profile', '/settings',
            '/health', '/metrics', '/status',
            '/.git', '/.env', '/robots.txt',
            '/sitemap.xml', '/wp-admin', '/phpmyadmin'
        ]

        discovered = []

        for endpoint in common_endpoints:
            try:
                url = self.target_url + endpoint
                response = self.session.head(url, timeout=2, allow_redirects=False)

                if response.status_code < 400:
                    discovered.append({
                        'endpoint': endpoint,
                        'status': response.status_code,
                        'size': response.headers.get('Content-Length', 'N/A')
                    })

                    # Vulnérabilité si endpoints sensibles accessibles
                    if endpoint in ['/.git', '/.env', '/phpmyadmin']:
                        self._add_vulnerability(
                            VulnerabilityType.A05_SECURITY_MISCONFIGURATION,
                            SeverityLevel.HIGH,
                            f"Endpoint sensible accessible: {endpoint}",
                            f"L'endpoint {endpoint} est accessible publiquement"
                        )

            except:
                pass

        self.scan_results['endpoints'] = discovered
        print(f"    ✓ {len(discovered)} endpoints découverts")

    def _check_security_headers(self):
        """Vérifie les headers de sécurité"""
        print("  → Vérification des headers de sécurité...")

        try:
            response = self.session.get(self.target_url, timeout=5)

            security_headers = {
                'Strict-Transport-Security': 'HSTS',
                'X-Frame-Options': 'Clickjacking Protection',
                'X-Content-Type-Options': 'MIME Sniffing Protection',
                'X-XSS-Protection': 'XSS Protection',
                'Content-Security-Policy': 'CSP',
                'Referrer-Policy': 'Referrer Policy',
                'Permissions-Policy': 'Permissions Policy'
            }

            missing_headers = []

            for header, description in security_headers.items():
                if header not in response.headers:
                    missing_headers.append(header)

            if missing_headers:
                self._add_vulnerability(
                    VulnerabilityType.A05_SECURITY_MISCONFIGURATION,
                    SeverityLevel.MEDIUM,
                    f"Headers de sécurité manquants",
                    f"Headers manquants: {', '.join(missing_headers)}"
                )

            print(f"    ✓ {len(security_headers) - len(missing_headers)}/{len(security_headers)} headers présents")

        except Exception as e:
            print(f"    ✗ Erreur: {str(e)}")

    def _scan_ports(self):
        """Scan des ports ouverts"""
        print("  → Scan des ports...")

        common_ports = [
            (21, 'FTP'),
            (22, 'SSH'),
            (23, 'Telnet'),
            (25, 'SMTP'),
            (80, 'HTTP'),
            (443, 'HTTPS'),
            (3306, 'MySQL'),
            (5432, 'PostgreSQL'),
            (6379, 'Redis'),
            (8080, 'HTTP Alt'),
            (9200, 'Elasticsearch')
        ]

        open_ports = []
        host = urllib.parse.urlparse(self.target_url).hostname or 'localhost'

        for port, service in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)

            result = sock.connect_ex((host, port))
            sock.close()

            if result == 0:
                open_ports.append((port, service))

                # Vulnérabilité si services sensibles exposés
                if port in [21, 23, 3306, 5432, 6379, 9200]:
                    self._add_vulnerability(
                        VulnerabilityType.A05_SECURITY_MISCONFIGURATION,
                        SeverityLevel.HIGH,
                        f"Service sensible exposé: {service}",
                        f"Port {port} ({service}) accessible depuis l'extérieur"
                    )

        self.scan_results['open_ports'] = open_ports
        print(f"    ✓ {len(open_ports)} ports ouverts détectés")

    # ========================================================================
    # PHASE 2: TESTS OWASP TOP 10
    # ========================================================================

    def _phase_owasp_tests(self):
        """Tests des vulnérabilités OWASP Top 10"""
        print("🛡️  PHASE 2: Tests OWASP Top 10")
        print("-" * 50)

        # A01: Broken Access Control
        self._test_broken_access_control()

        # A02: Cryptographic Failures
        self._test_cryptographic_failures()

        # A03: Injection
        self._test_injection_vulnerabilities()

        # A04: Insecure Design
        self._test_insecure_design()

        # A05: Security Misconfiguration
        self._test_security_misconfiguration()

        # A06: Vulnerable Components
        self._test_vulnerable_components()

        # A07: Authentication Failures
        self._test_authentication_failures()

        # A08: Data Integrity Failures
        self._test_data_integrity_failures()

        # A09: Logging Failures
        self._test_logging_failures()

        # A10: SSRF
        self._test_ssrf()

        print()

    def _test_broken_access_control(self):
        """Test A01: Contrôle d'accès défaillant"""
        print("  → A01: Test du contrôle d'accès...")

        # Test IDOR (Insecure Direct Object Reference)
        test_urls = [
            '/api/users/1',
            '/api/users/2',
            '/api/admin/users',
            '/api/profile/1/edit'
        ]

        for url in test_urls:
            try:
                response = self.session.get(self.target_url + url, timeout=3)

                if response.status_code == 200:
                    self._add_vulnerability(
                        VulnerabilityType.A01_BROKEN_ACCESS_CONTROL,
                        SeverityLevel.HIGH,
                        f"IDOR potentiel détecté",
                        f"Accès non autorisé possible à: {url}"
                    )

            except:
                pass

        # Test de bypass d'authentification
        admin_endpoints = ['/admin', '/api/admin', '/dashboard/admin']

        for endpoint in admin_endpoints:
            try:
                response = self.session.get(self.target_url + endpoint, timeout=3, allow_redirects=False)

                if response.status_code == 200:
                    self._add_vulnerability(
                        VulnerabilityType.A01_BROKEN_ACCESS_CONTROL,
                        SeverityLevel.CRITICAL,
                        "Bypass d'authentification",
                        f"Accès administrateur sans authentification: {endpoint}"
                    )

            except:
                pass

        print("    ✓ Tests de contrôle d'accès complétés")

    def _test_cryptographic_failures(self):
        """Test A02: Défaillances cryptographiques"""
        print("  → A02: Test cryptographique...")

        # Vérification SSL/TLS
        if self.target_url.startswith('http://'):
            self._add_vulnerability(
                VulnerabilityType.A02_CRYPTOGRAPHIC_FAILURES,
                SeverityLevel.HIGH,
                "Pas de chiffrement HTTPS",
                "Le site n'utilise pas HTTPS pour les communications"
            )

        # Test de cookies non sécurisés
        try:
            response = self.session.get(self.target_url, timeout=5)

            for cookie in response.cookies:
                if not cookie.secure and 'session' in cookie.name.lower():
                    self._add_vulnerability(
                        VulnerabilityType.A02_CRYPTOGRAPHIC_FAILURES,
                        SeverityLevel.MEDIUM,
                        "Cookie de session non sécurisé",
                        f"Le cookie '{cookie.name}' n'a pas le flag 'Secure'"
                    )

                if not cookie.has_nonstandard_attr('HttpOnly'):
                    self._add_vulnerability(
                        VulnerabilityType.A02_CRYPTOGRAPHIC_FAILURES,
                        SeverityLevel.MEDIUM,
                        "Cookie sans HttpOnly",
                        f"Le cookie '{cookie.name}' n'a pas le flag 'HttpOnly'"
                    )

        except:
            pass

        print("    ✓ Tests cryptographiques complétés")

    def _test_injection_vulnerabilities(self):
        """Test A03: Vulnérabilités d'injection"""
        print("  → A03: Test d'injection...")

        # Payloads d'injection
        sql_payloads = [
            "' OR '1'='1",
            "1; DROP TABLE users--",
            "' UNION SELECT * FROM users--"
        ]

        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>"
        ]

        command_payloads = [
            "; ls -la",
            "| whoami",
            "`cat /etc/passwd`"
        ]

        # Test SQL Injection
        for payload in sql_payloads:
            try:
                response = self.session.get(
                    f"{self.target_url}/api/search",
                    params={'q': payload},
                    timeout=3
                )

                if 'error' in response.text.lower() and ('sql' in response.text.lower() or 'database' in response.text.lower()):
                    self._add_vulnerability(
                        VulnerabilityType.A03_INJECTION,
                        SeverityLevel.CRITICAL,
                        "SQL Injection détectée",
                        f"Injection SQL possible avec le payload: {payload[:30]}..."
                    )

            except:
                pass

        # Test XSS
        for payload in xss_payloads:
            try:
                response = self.session.post(
                    f"{self.target_url}/api/comment",
                    data={'comment': payload},
                    timeout=3
                )

                if payload in response.text:
                    self._add_vulnerability(
                        VulnerabilityType.A03_INJECTION,
                        SeverityLevel.HIGH,
                        "XSS détecté",
                        f"XSS possible avec le payload: {payload[:30]}..."
                    )

            except:
                pass

        print("    ✓ Tests d'injection complétés")

    def _test_insecure_design(self):
        """Test A04: Conception non sécurisée"""
        print("  → A04: Test de conception...")

        # Test de rate limiting
        login_endpoint = f"{self.target_url}/api/login"
        attempts = 0

        for i in range(10):
            try:
                response = self.session.post(
                    login_endpoint,
                    json={'username': 'test', 'password': 'wrong'},
                    timeout=1
                )
                attempts += 1

            except:
                break

        if attempts >= 10:
            self._add_vulnerability(
                VulnerabilityType.A04_INSECURE_DESIGN,
                SeverityLevel.HIGH,
                "Pas de rate limiting",
                "Attaques par force brute possibles sur l'authentification"
            )

        # Test de validation côté client uniquement
        # (Simulé car nécessite analyse du code JavaScript)

        print("    ✓ Tests de conception complétés")

    def _test_security_misconfiguration(self):
        """Test A05: Mauvaise configuration de sécurité"""
        print("  → A05: Test de configuration...")

        # Test de messages d'erreur verbeux
        try:
            response = self.session.get(f"{self.target_url}/api/error_test", timeout=3)

            if response.status_code >= 400:
                if 'traceback' in response.text.lower() or 'stack trace' in response.text.lower():
                    self._add_vulnerability(
                        VulnerabilityType.A05_SECURITY_MISCONFIGURATION,
                        SeverityLevel.MEDIUM,
                        "Messages d'erreur verbeux",
                        "Stack traces exposées dans les erreurs"
                    )

        except:
            pass

        # Test de configuration par défaut
        default_creds = [
            ('admin', 'admin'),
            ('admin', 'password'),
            ('root', 'root'),
            ('test', 'test')
        ]

        for username, password in default_creds:
            try:
                response = self.session.post(
                    f"{self.target_url}/api/login",
                    json={'username': username, 'password': password},
                    timeout=3
                )

                if response.status_code == 200:
                    self._add_vulnerability(
                        VulnerabilityType.A05_SECURITY_MISCONFIGURATION,
                        SeverityLevel.CRITICAL,
                        "Identifiants par défaut",
                        f"Connexion possible avec {username}:{password}"
                    )

            except:
                pass

        print("    ✓ Tests de configuration complétés")

    def _test_vulnerable_components(self):
        """Test A06: Composants vulnérables"""
        print("  → A06: Test des composants...")

        # Vérification des versions exposées
        try:
            response = self.session.get(self.target_url, timeout=5)

            # Recherche de versions dans les headers et le contenu
            version_patterns = [
                r'jquery[/-](\d+\.\d+\.\d+)',
                r'bootstrap[/-](\d+\.\d+\.\d+)',
                r'angular[/-](\d+\.\d+\.\d+)',
                r'react[/-](\d+\.\d+\.\d+)'
            ]

            for pattern in version_patterns:
                matches = re.findall(pattern, response.text.lower())
                if matches:
                    for version in matches:
                        # Vérification simplifiée de versions obsolètes
                        major_version = int(version.split('.')[0])

                        if 'jquery' in pattern and major_version < 3:
                            self._add_vulnerability(
                                VulnerabilityType.A06_VULNERABLE_COMPONENTS,
                                SeverityLevel.MEDIUM,
                                "jQuery obsolète",
                                f"Version jQuery {version} avec vulnérabilités connues"
                            )

        except:
            pass

        print("    ✓ Tests des composants complétés")

    def _test_authentication_failures(self):
        """Test A07: Défaillances d'authentification"""
        print("  → A07: Test d'authentification...")

        # Test de politique de mot de passe faible
        weak_passwords = ['123456', 'password', 'admin', 'test']

        for pwd in weak_passwords:
            try:
                response = self.session.post(
                    f"{self.target_url}/api/register",
                    json={'username': 'testuser', 'password': pwd},
                    timeout=3
                )

                if response.status_code == 201:
                    self._add_vulnerability(
                        VulnerabilityType.A07_AUTH_FAILURES,
                        SeverityLevel.HIGH,
                        "Politique de mot de passe faible",
                        f"Mot de passe faible accepté: {pwd}"
                    )

            except:
                pass

        # Test de session fixation
        # (Simulé car nécessite interaction complexe)

        print("    ✓ Tests d'authentification complétés")

    def _test_data_integrity_failures(self):
        """Test A08: Défaillances d'intégrité des données"""
        print("  → A08: Test d'intégrité...")

        # Test de désérialisation non sécurisée
        # (Simulé car dépend de l'implémentation)

        # Test d'absence de vérification d'intégrité
        try:
            response = self.session.get(f"{self.target_url}/api/data", timeout=3)

            if 'integrity' not in response.headers and 'etag' not in response.headers:
                self._add_vulnerability(
                    VulnerabilityType.A08_DATA_INTEGRITY_FAILURES,
                    SeverityLevel.LOW,
                    "Pas de vérification d'intégrité",
                    "Les données ne sont pas signées ou vérifiées"
                )

        except:
            pass

        print("    ✓ Tests d'intégrité complétés")

    def _test_logging_failures(self):
        """Test A09: Défaillances de journalisation"""
        print("  → A09: Test de journalisation...")

        # Test si les événements de sécurité sont loggés
        # (Simulé car nécessite accès aux logs)

        # Test de tentatives de connexion
        for i in range(3):
            try:
                self.session.post(
                    f"{self.target_url}/api/login",
                    json={'username': 'hacker', 'password': 'hack'},
                    timeout=3
                )
            except:
                pass

        # Vérification si un mécanisme de monitoring existe
        monitoring_endpoints = ['/metrics', '/health', '/monitoring']

        monitoring_found = False
        for endpoint in monitoring_endpoints:
            try:
                response = self.session.get(self.target_url + endpoint, timeout=3)
                if response.status_code < 400:
                    monitoring_found = True
                    break
            except:
                pass

        if not monitoring_found:
            self._add_vulnerability(
                VulnerabilityType.A09_LOGGING_FAILURES,
                SeverityLevel.MEDIUM,
                "Monitoring insuffisant",
                "Pas d'endpoint de monitoring détecté"
            )

        print("    ✓ Tests de journalisation complétés")

    def _test_ssrf(self):
        """Test A10: Server-Side Request Forgery"""
        print("  → A10: Test SSRF...")

        # Payloads SSRF
        ssrf_payloads = [
            'http://localhost',
            'http://127.0.0.1',
            'http://169.254.169.254',  # AWS metadata
            'file:///etc/passwd'
        ]

        for payload in ssrf_payloads:
            try:
                response = self.session.post(
                    f"{self.target_url}/api/fetch",
                    json={'url': payload},
                    timeout=3
                )

                if response.status_code == 200:
                    if 'root:' in response.text or 'ami-id' in response.text:
                        self._add_vulnerability(
                            VulnerabilityType.A10_SSRF,
                            SeverityLevel.CRITICAL,
                            "SSRF détecté",
                            f"Accès interne possible via: {payload}"
                        )

            except:
                pass

        print("    ✓ Tests SSRF complétés")

    # ========================================================================
    # PHASE 3: TESTS D'INFRASTRUCTURE
    # ========================================================================

    def _phase_infrastructure_tests(self):
        """Tests de l'infrastructure"""
        print("🏗️  PHASE 3: Tests d'Infrastructure")
        print("-" * 50)

        # Test SSL/TLS
        self._test_ssl_configuration()

        # Test DNS
        self._test_dns_configuration()

        # Test de la configuration serveur
        self._test_server_configuration()

        print()

    def _test_ssl_configuration(self):
        """Test de la configuration SSL/TLS"""
        print("  → Test SSL/TLS...")

        if not self.target_url.startswith('https://'):
            print("    ⚠️  Pas de HTTPS activé")
            return

        try:
            hostname = urllib.parse.urlparse(self.target_url).hostname
            port = 443

            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    protocol = ssock.version()

                    # Vérification du protocole
                    if protocol in ['TLSv1', 'TLSv1.1']:
                        self._add_vulnerability(
                            VulnerabilityType.A02_CRYPTOGRAPHIC_FAILURES,
                            SeverityLevel.HIGH,
                            "Protocole TLS obsolète",
                            f"Le serveur utilise {protocol} qui est obsolète"
                        )

                    # Vérification de la date d'expiration
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (not_after - datetime.now()).days

                    if days_until_expiry < 30:
                        self._add_vulnerability(
                            VulnerabilityType.A05_SECURITY_MISCONFIGURATION,
                            SeverityLevel.MEDIUM,
                            "Certificat SSL proche de l'expiration",
                            f"Le certificat expire dans {days_until_expiry} jours"
                        )

                    print(f"    ✓ SSL/TLS configuré ({protocol})")

        except Exception as e:
            print(f"    ✗ Erreur SSL: {str(e)}")

    def _test_dns_configuration(self):
        """Test de la configuration DNS"""
        print("  → Test DNS...")

        try:
            hostname = urllib.parse.urlparse(self.target_url).hostname

            # Résolution DNS
            ip = socket.gethostbyname(hostname)
            print(f"    ✓ Résolution DNS: {hostname} → {ip}")

            # Vérification si IP privée exposée
            if ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.'):
                self._add_vulnerability(
                    VulnerabilityType.A05_SECURITY_MISCONFIGURATION,
                    SeverityLevel.LOW,
                    "IP privée exposée",
                    f"Le domaine résout vers une IP privée: {ip}"
                )

        except Exception as e:
            print(f"    ✗ Erreur DNS: {str(e)}")

    def _test_server_configuration(self):
        """Test de la configuration serveur"""
        print("  → Test de configuration serveur...")

        try:
            response = self.session.options(self.target_url, timeout=5)

            # Vérification des méthodes HTTP autorisées
            allowed_methods = response.headers.get('Allow', '').split(',')

            dangerous_methods = ['PUT', 'DELETE', 'TRACE', 'CONNECT']
            for method in dangerous_methods:
                if method in allowed_methods:
                    self._add_vulnerability(
                        VulnerabilityType.A05_SECURITY_MISCONFIGURATION,
                        SeverityLevel.MEDIUM,
                        f"Méthode HTTP dangereuse: {method}",
                        f"La méthode {method} est autorisée sur le serveur"
                    )

            print(f"    ✓ Méthodes autorisées: {', '.join(allowed_methods) if allowed_methods else 'N/A'}")

        except:
            pass

    # ========================================================================
    # PHASE 4: TESTS DE CONFIGURATION
    # ========================================================================

    def _phase_configuration_tests(self):
        """Tests de configuration"""
        print("⚙️  PHASE 4: Tests de Configuration")
        print("-" * 50)

        # Test des fichiers sensibles
        self._test_sensitive_files()

        # Test de la configuration des cookies
        self._test_cookie_configuration()

        # Test CORS
        self._test_cors_configuration()

        print()

    def _test_sensitive_files(self):
        """Test d'accès aux fichiers sensibles"""
        print("  → Test des fichiers sensibles...")

        sensitive_files = [
            '/.git/config',
            '/.env',
            '/.env.local',
            '/config.php',
            '/wp-config.php',
            '/web.config',
            '/.htaccess',
            '/backup.sql',
            '/dump.sql',
            '/database.sql'
        ]

        for file in sensitive_files:
            try:
                response = self.session.get(self.target_url + file, timeout=3)

                if response.status_code == 200:
                    self._add_vulnerability(
                        VulnerabilityType.A05_SECURITY_MISCONFIGURATION,
                        SeverityLevel.CRITICAL,
                        f"Fichier sensible accessible",
                        f"Le fichier {file} est accessible publiquement"
                    )

            except:
                pass

        print("    ✓ Tests des fichiers sensibles complétés")

    def _test_cookie_configuration(self):
        """Test de la configuration des cookies"""
        print("  → Test des cookies...")

        try:
            response = self.session.get(self.target_url, timeout=5)

            for cookie in response.cookies:
                issues = []

                if not cookie.secure:
                    issues.append('Secure flag manquant')

                if not cookie.has_nonstandard_attr('HttpOnly'):
                    issues.append('HttpOnly flag manquant')

                if not cookie.has_nonstandard_attr('SameSite'):
                    issues.append('SameSite flag manquant')

                if issues and ('session' in cookie.name.lower() or 'token' in cookie.name.lower()):
                    self._add_vulnerability(
                        VulnerabilityType.A05_SECURITY_MISCONFIGURATION,
                        SeverityLevel.MEDIUM,
                        f"Configuration cookie non sécurisée: {cookie.name}",
                        f"Problèmes: {', '.join(issues)}"
                    )

            print("    ✓ Configuration des cookies vérifiée")

        except:
            pass

    def _test_cors_configuration(self):
        """Test de la configuration CORS"""
        print("  → Test CORS...")

        try:
            headers = {'Origin': 'http://evil.com'}
            response = self.session.get(self.target_url, headers=headers, timeout=5)

            cors_header = response.headers.get('Access-Control-Allow-Origin')

            if cors_header == '*':
                self._add_vulnerability(
                    VulnerabilityType.A05_SECURITY_MISCONFIGURATION,
                    SeverityLevel.MEDIUM,
                    "CORS trop permissif",
                    "Access-Control-Allow-Origin configuré à '*'"
                )

            elif cors_header == 'http://evil.com':
                self._add_vulnerability(
                    VulnerabilityType.A05_SECURITY_MISCONFIGURATION,
                    SeverityLevel.HIGH,
                    "CORS mal configuré",
                    "Le serveur accepte n'importe quelle origine"
                )

            print("    ✓ Configuration CORS vérifiée")

        except:
            pass

    # ========================================================================
    # PHASE 5: ANALYSE DE CODE
    # ========================================================================

    def _phase_code_analysis(self):
        """Analyse statique du code (si accessible)"""
        print("📝 PHASE 5: Analyse de Code")
        print("-" * 50)

        # Recherche de patterns dangereux dans le JavaScript
        self._analyze_javascript()

        # Recherche d'informations sensibles
        self._search_sensitive_data()

        print()

    def _analyze_javascript(self):
        """Analyse du JavaScript côté client"""
        print("  → Analyse JavaScript...")

        try:
            response = self.session.get(self.target_url, timeout=5)

            # Patterns dangereux
            dangerous_patterns = {
                r'eval\(': 'Utilisation de eval()',
                r'innerHTML\s*=': 'Utilisation de innerHTML',
                r'document\.write': 'Utilisation de document.write',
                r'localStorage\.setItem.*password': 'Mot de passe dans localStorage',
                r'console\.log.*api[_-]?key': 'API key dans console.log'
            }

            for pattern, description in dangerous_patterns.items():
                if re.search(pattern, response.text, re.IGNORECASE):
                    self._add_vulnerability(
                        VulnerabilityType.A04_INSECURE_DESIGN,
                        SeverityLevel.MEDIUM,
                        f"Pattern dangereux: {description}",
                        f"Le code JavaScript contient: {description}"
                    )

            print("    ✓ Analyse JavaScript complétée")

        except:
            pass

    def _search_sensitive_data(self):
        """Recherche de données sensibles exposées"""
        print("  → Recherche de données sensibles...")

        try:
            response = self.session.get(self.target_url, timeout=5)

            # Patterns de données sensibles
            sensitive_patterns = {
                r'api[_-]?key\s*[:=]\s*["\'][\w\-]+["\']': 'API Key',
                r'secret[_-]?key\s*[:=]\s*["\'][\w\-]+["\']': 'Secret Key',
                r'password\s*[:=]\s*["\'][\w\-]+["\']': 'Mot de passe',
                r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}': 'Email',
                r'\b(?:\d{4}[-\s]?){3}\d{4}\b': 'Numéro de carte bancaire'
            }

            for pattern, data_type in sensitive_patterns.items():
                matches = re.findall(pattern, response.text)
                if matches:
                    # Filtrer les faux positifs
                    if data_type != 'Email' or len(matches) > 10:
                        self._add_vulnerability(
                            VulnerabilityType.A02_CRYPTOGRAPHIC_FAILURES,
                            SeverityLevel.HIGH if data_type != 'Email' else SeverityLevel.LOW,
                            f"Données sensibles exposées: {data_type}",
                            f"{len(matches)} instance(s) de {data_type} trouvée(s)"
                        )

            print("    ✓ Recherche de données sensibles complétée")

        except:
            pass

    # ========================================================================
    # MÉTHODES UTILITAIRES
    # ========================================================================

    def _add_vulnerability(self, vuln_type: VulnerabilityType, severity: SeverityLevel,
                          title: str, description: str):
        """Ajoute une vulnérabilité à la liste"""
        self.vulnerabilities.append({
            'type': vuln_type,
            'severity': severity,
            'title': title,
            'description': description,
            'timestamp': datetime.now().isoformat()
        })

        if self.verbose:
            print(f"      {severity.value} {title}")

    def _generate_report(self, elapsed_time: float) -> Dict[str, Any]:
        """Génère le rapport de sécurité"""
        print("="*70)
        print("RAPPORT DE SCAN DE SÉCURITÉ")
        print("="*70 + "\n")

        # Comptage par sévérité
        severity_counts = {
            SeverityLevel.CRITICAL: 0,
            SeverityLevel.HIGH: 0,
            SeverityLevel.MEDIUM: 0,
            SeverityLevel.LOW: 0,
            SeverityLevel.INFO: 0
        }

        for vuln in self.vulnerabilities:
            severity_counts[vuln['severity']] += 1

        # Affichage du résumé
        print("📊 RÉSUMÉ DES VULNÉRABILITÉS")
        print("-" * 50)

        total_vulns = len(self.vulnerabilities)
        print(f"Total: {total_vulns} vulnérabilité(s) détectée(s)\n")

        for severity, count in severity_counts.items():
            if count > 0:
                print(f"  {severity.value}: {count}")

        print()

        # Score de sécurité
        score = self._calculate_security_score(severity_counts)

        if score >= 80:
            score_color = "🟢"
        elif score >= 60:
            score_color = "🟡"
        elif score >= 40:
            score_color = "🟠"
        else:
            score_color = "🔴"

        print(f"Score de Sécurité: {score_color} {score}/100")
        print()

        # Vulnérabilités critiques et élevées
        critical_high = [v for v in self.vulnerabilities
                         if v['severity'] in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]]

        if critical_high:
            print("⚠️  VULNÉRABILITÉS CRITIQUES ET ÉLEVÉES")
            print("-" * 50)

            for vuln in critical_high[:10]:  # Top 10
                print(f"\n{vuln['severity'].value} {vuln['title']}")
                print(f"  Type: {vuln['type'].value}")
                print(f"  Description: {vuln['description']}")

        # Recommandations
        print("\n💡 RECOMMANDATIONS PRIORITAIRES")
        print("-" * 50)

        recommendations = self._generate_recommendations(severity_counts)
        for i, rec in enumerate(recommendations[:10], 1):
            print(f"{i}. {rec}")

        # Statistiques du scan
        print(f"\n📈 STATISTIQUES DU SCAN")
        print("-" * 50)
        print(f"Durée du scan: {elapsed_time:.2f} secondes")
        print(f"Endpoints testés: {len(self.scan_results.get('endpoints', []))}")
        print(f"Technologies détectées: {', '.join(self.scan_results.get('technologies', {}).get('detected', []))}")

        return {
            'score': score,
            'total_vulnerabilities': total_vulns,
            'severity_counts': {k.name: v for k, v in severity_counts.items()},
            'vulnerabilities': [
                {
                    'type': v['type'].name,
                    'severity': v['severity'].name,
                    'title': v['title'],
                    'description': v['description']
                }
                for v in self.vulnerabilities
            ],
            'scan_results': self.scan_results,
            'recommendations': recommendations,
            'elapsed_time': elapsed_time,
            'timestamp': datetime.now().isoformat()
        }

    def _calculate_security_score(self, severity_counts: Dict[SeverityLevel, int]) -> int:
        """Calcule le score de sécurité"""
        # Pondération des vulnérabilités
        weights = {
            SeverityLevel.CRITICAL: 25,
            SeverityLevel.HIGH: 15,
            SeverityLevel.MEDIUM: 8,
            SeverityLevel.LOW: 3,
            SeverityLevel.INFO: 1
        }

        total_penalty = 0
        for severity, count in severity_counts.items():
            total_penalty += count * weights.get(severity, 0)

        # Score sur 100
        score = max(0, 100 - total_penalty)

        return score

    def _generate_recommendations(self, severity_counts: Dict[SeverityLevel, int]) -> List[str]:
        """Génère des recommandations basées sur les vulnérabilités"""
        recommendations = []

        if severity_counts[SeverityLevel.CRITICAL] > 0:
            recommendations.append("🔴 Corriger immédiatement les vulnérabilités CRITIQUES")

        if severity_counts[SeverityLevel.HIGH] > 0:
            recommendations.append("🟠 Traiter les vulnérabilités ÉLEVÉES dans les 48h")

        # Recommandations spécifiques basées sur les types de vulnérabilités
        vuln_types = set(v['type'] for v in self.vulnerabilities)

        if VulnerabilityType.A01_BROKEN_ACCESS_CONTROL in vuln_types:
            recommendations.append("Implémenter un contrôle d'accès robuste (RBAC)")

        if VulnerabilityType.A02_CRYPTOGRAPHIC_FAILURES in vuln_types:
            recommendations.append("Activer HTTPS et utiliser TLS 1.3 minimum")

        if VulnerabilityType.A03_INJECTION in vuln_types:
            recommendations.append("Utiliser des requêtes paramétrées et valider toutes les entrées")

        if VulnerabilityType.A05_SECURITY_MISCONFIGURATION in vuln_types:
            recommendations.append("Réviser la configuration de sécurité et activer tous les headers")

        if VulnerabilityType.A07_AUTH_FAILURES in vuln_types:
            recommendations.append("Renforcer la politique de mots de passe et implémenter le 2FA")

        # Recommandations générales
        recommendations.extend([
            "Effectuer des audits de sécurité réguliers (trimestriels)",
            "Maintenir toutes les dépendances à jour",
            "Implémenter un WAF (Web Application Firewall)",
            "Mettre en place un système de monitoring et d'alertes",
            "Former l'équipe aux bonnes pratiques de sécurité"
        ])

        return recommendations

    def export_report(self, report: Dict[str, Any], filename: str = "security_scan_report.json"):
        """Exporte le rapport en JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        print(f"\n✓ Rapport exporté vers {filename}")


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Scanner de sécurité AWKWARD LEGACY")
    parser.add_argument('--target', '-t', default='http://localhost:8000', help='URL cible')
    parser.add_argument('--full', '-f', action='store_true', help='Scan complet')
    parser.add_argument('--verbose', '-v', action='store_true', help='Mode verbeux')
    parser.add_argument('--report', '-r', action='store_true', help='Exporter le rapport')
    parser.add_argument('--output', '-o', default='security_report.json', help='Fichier de sortie')

    args = parser.parse_args()

    # Création du scanner
    scanner = SecurityScanner(target_url=args.target, verbose=args.verbose)

    # Exécution du scan
    report = scanner.run_full_scan()

    # Export si demandé
    if args.report:
        scanner.export_report(report, args.output)

    # Code de sortie basé sur le score
    exit_code = 0 if report['score'] >= 60 else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()