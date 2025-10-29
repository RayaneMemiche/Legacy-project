# AWKWARD LEGACY - Brief Complet du Projet

## Contexte du Projet

### Entreprise et Mission
- **Entreprise** : CoinLegacy Inc. (spécialisée en reverse engineering logiciel)
- **Acquisition** : Code legacy d'une suite logicielle développée entre 1995 et 2008
- **Langage original** : OCaml
- **Référence** : https://github.com/geneweb/geneweb

### Objectif Commercial
Le logiciel contient un programme capable de révéler les origines de chaque individu. L'objectif est de découvrir les héritiers légitimes de lignées puissantes et de facturer des honoraires pour ce service.

### Votre Rôle
Vous êtes une équipe de CoinLegacy Inc. Un client majeur vous a confié ce code ancien qui pourrait "valoir son pesant d'or".

## Mission Principale

### Objectif
Rendre ce code conforme aux standards actuels tout en :
- **PRÉSERVANT** le cœur du code (pas de réécriture totale)
- **TESTANT** rigoureusement le système
- **DÉPLOYANT** de manière sécurisée
- **ÉVITANT** la destruction de l'infrastructure

### Contraintes Critiques
⚠️ **ATTENTION** : Réécrire ou détruire le code entraînera votre licenciement. C'est une pièce d'histoire à restaurer, pas à reconstruire.

## Spécifications Techniques

### Langage et Compilation
- **Langage de rendu** : Python
- **Système de compilation** : via Makefile
- **Rules Makefile requises** :
  - `re` (recompilation)
  - `clean` (nettoyage fichiers temporaires)
  - `fclean` (nettoyage complet)

### Livraison
- Inclure tous les fichiers sources nécessaires
- **EXCLURE** : binaires, fichiers temporaires, fichiers objets, et autres fichiers inutiles

## Compétences Requises

### 1. Assurance Qualité (QA)
- Développer une politique de tests documentée
- Définir des standards et processus qualité

### 2. Gestion de Projet
- Expertise technique en déploiement
- Création de documentation pour guider le déploiement

## Livrables Attendus

### Date de Défense
**Entre le 20 et 24 octobre**

### Rapport Final - Structure Obligatoire

#### A. Politique de Tests
1. **Intégration du processus qualité** tout au long du cycle de vie du projet
2. **Définition des protocoles et scénarios de tests** :
   - Tests unitaires
   - Tests fonctionnels
   - Tests d'intégration
   - Tests de performance
3. **Détection d'erreurs** et gestion des dysfonctionnements
4. **Analyse des résultats** et reporting des tests
5. **Audit de sécurité** et gestion des vulnérabilités

#### B. Standards et Processus Qualité
1. **Définition des standards de documentation**
2. **Conventions de codage**
3. **Rapports d'activité**
4. **Prise en compte de l'accessibilité** pour les personnes en situation de handicap
5. **Mise en œuvre des activités de contrôle qualité**

#### C. Expertise Technique en Déploiement
1. **Provisionnement des ressources nécessaires** :
   - Serveurs
   - Services cloud
   - Autres infrastructures
2. **Conformité aux bonnes pratiques** d'administration système et réseau :
   - Gestion des mots de passe
   - Configuration réseau et machine (prévention des vulnérabilités)
   - Gestion des clés de chiffrement

#### D. Documentation de Déploiement
1. **Sensibilisation aux bonnes pratiques de sécurité**
2. **Conformité RGPD** (Règlement Général sur la Protection des Données)
3. **Stratégie de livraison**
4. **Communication inter-départements** :
   - Ventes
   - Marketing
   - Opérations
   - Autres services
5. **Documentation des processus**
6. **Communication technique claire et intelligible**

## Points Critiques à Retenir

### Philosophie du Projet
- ✅ **RESTAURER** le code legacy
- ✅ **TESTER** exhaustivement
- ✅ **SÉCURISER** le déploiement
- ✅ **DOCUMENTER** tous les processus
- ❌ **NE PAS RÉÉCRIRE** from scratch
- ❌ **NE PAS DÉTRUIRE** l'infrastructure existante

### Priorités
1. **Qualité** : Tests rigoureux et documentation complète
2. **Sécurité** : Audit, RGPD, bonnes pratiques DevSecOps
3. **Conformité** : Standards modernes sans perdre le cœur fonctionnel
4. **Accessibilité** : Prise en compte des utilisateurs en situation de handicap

## Enjeux Business
- Découvrir des héritiers de lignées importantes
- Monétiser ce service via des honoraires
- Préserver un patrimoine logiciel historique (1995-2008)
- Démontrer l'expertise en reverse engineering de CoinLegacy Inc.

## Format de Rendu
- Rapport écrit couvrant les 4 sections (A, B, C, D)
- Code Python avec Makefile
- Documentation technique
- Politique de tests
- Guides de déploiement

---

**Remarque importante pour l'IA** : Ce projet nécessite une approche d'archéologie logicielle. Il s'agit de comprendre, tester et moderniser un système legacy OCaml (GeneWeb) sans le réécrire, tout en créant une infrastructure Python moderne autour de celui-ci. L'accent est mis sur la QA, la sécurité, et la documentation plutôt que sur le développement pur.