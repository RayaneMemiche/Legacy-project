#!/usr/bin/env python3
"""Test des modules créés"""

import sys
import os
sys.path.append('LegacyProject/modernProject/lib')

def test_security_module():
    """Test du module de sécurité"""
    print("\n🔒 Test du Module Security")
    print("-" * 40)
    
    try:
        from security import SecurityManager
        
        security = SecurityManager.get_instance()
        print("  ✅ Module importé avec succès")
        
        # Test hashage
        password = "TestPassword123!"
        hashed = security.hash_password(password)
        is_valid = security.verify_password(password, hashed)
        
        if is_valid:
            print("  ✅ Hashage/Vérification de mot de passe OK")
        else:
            print("  ❌ Erreur dans hashage/vérification")
            
        # Test JWT
        token = security.create_jwt({"user_id": 123})
        decoded = security.verify_jwt(token)
        
        if decoded and decoded.get("user_id") == 123:
            print("  ✅ JWT création/vérification OK")
        else:
            print("  ❌ Erreur dans JWT")
            
        # Test chiffrement
        data = "Données sensibles"
        encrypted = security.encrypt_data(data)
        decrypted = security.decrypt_data(encrypted)
        
        if decrypted == data:
            print("  ✅ Chiffrement/Déchiffrement OK")
        else:
            print("  ❌ Erreur dans chiffrement")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def test_config_files():
    """Test de la présence des fichiers de configuration"""
    print("\n📁 Test des Fichiers de Configuration")
    print("-" * 40)
    
    files = [
        '.pre-commit-config.yaml',
        '.pylintrc',
        'SECURITY.md',
        'CONTRIBUTING.md',
        'PRODUCTION_DEPLOYMENT_PLAN.md',
        'presentation_slides.md'
    ]
    
    all_present = True
    for file in files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} non trouvé")
            all_present = False
            
    return all_present

def test_reports():
    """Test de la présence des rapports"""
    print("\n📊 Test des Rapports")
    print("-" * 40)
    
    reports = [
        'jour4_rapport.md',
        'jour5_rapport.md',
        'jour6_rapport.md'
    ]
    
    all_present = True
    for report in reports:
        if os.path.exists(report):
            # Compte les lignes
            with open(report, 'r') as f:
                lines = len(f.readlines())
            print(f"  ✅ {report} ({lines} lignes)")
        else:
            print(f"  ❌ {report} non trouvé")
            all_present = False
            
    return all_present

def main():
    print("=" * 50)
    print("TEST GLOBAL DES MODULES AWKWARD LEGACY")
    print("=" * 50)
    
    results = []
    
    # Tests
    results.append(("Security Module", test_security_module()))
    results.append(("Configuration Files", test_config_files()))
    results.append(("Reports", test_reports()))
    
    # Résumé
    print("\n" + "=" * 50)
    print("RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"  {name}: {status}")
    
    print(f"\nScore Global: {passed}/{total} ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
    else:
        print(f"\n⚠️  {total - passed} test(s) échoué(s)")

if __name__ == "__main__":
    main()
