# INDEX BLOC 6 - AWKWARD LEGACY

**Version:** 1.0
**Date:** Mars 2026
**Projet:** AWKWARD LEGACY - Modernisation de GeneWeb
**Referentiel RNCP:** Bloc 6 - EIP

---

## Table des Matieres

1. [Criteres Bloc 6 et preuves](#1-criteres-bloc-6-et-preuves)
2. [Activite A13 - Deploiement technique](#2-activite-a13---deploiement-technique)
3. [Activite A14 - Documentation et communication](#3-activite-a14---documentation-et-communication)
4. [Carte des preuves dans le code](#4-carte-des-preuves-dans-le-code)
5. [Commandes de demonstration](#5-commandes-de-demonstration)

---

## 1. Criteres Bloc 6 et preuves

| Critere | Titre | Document de reference | Preuve principale |
|---------|-------|----------------------|-------------------|
| **B6-C30.1** | Documentation hebergement | `A13_Deploiement/B6_C30_Technologies_Hebergement.md` | `LegacyProject/docs/DEPLOYMENT_GUIDE.md` |
| **B6-C30.2** | Justification des choix | `A13_Deploiement/B6_C30_Technologies_Hebergement.md` section 3 | Dockerfile multi-stage + ci.yml |
| **B6-C31.1** | Procedure detaillee | `A13_Deploiement/B6_C31_Procedure_Deploiement.md` | `ci.yml` (8 jobs) + `DEPLOYMENT_GUIDE.md` |
| **B6-C31.2** | Demonstration fonctionnelle | `A13_Deploiement/B6_C31_Procedure_Deploiement.md` section 7 | Pipeline GitHub Actions + PR #1 |
| **B6-C32.1** | Bonnes pratiques securite | `A13_Deploiement/B6_C32_Securite_Infrastructure.md` | Bandit + OWASP + Nginx headers |
| **B6-C32.2** | Implementation securisation | `A13_Deploiement/B6_C32_Securite_Infrastructure.md` section 7 | PR #1 bloquee par Bandit |
| **B6-C33.1** | Documentation technique | `A14_Documentation_Communication/B6_C33_Documentation_Technique.md` | 20+ docs, 50,000 mots |
| **B6-C33.2** | Justification perennite | `A14_Documentation_Communication/B6_C33_Documentation_Technique.md` section 4 | Python 3.12, Docker, tests 80%+ |
| **B6-C33.3** | Accessibilite docs | `A14_Documentation_Communication/B6_C33_Documentation_Technique.md` section 5 | Commit 61de763 (emojis supprimés) |
| **B6-C34.1** | Communication parties prenantes | `A14_Documentation_Communication/B6_C34_Communication.md` | Rapports journaliers + GitHub PR |
| **B6-C34.2** | Discours clair | `A14_Documentation_Communication/B6_C34_Communication.md` section 3 | GUIDE_ORAL + SCRIPT_GAMMA_PPT |
| **B6-C34.3** | Echange technique | `A14_Documentation_Communication/B6_C34_Communication.md` section 4 | Q&R techniques prepares |
| **B6-C34.4** | Accessibilite docs communication | `A14_Documentation_Communication/B6_C34_Communication.md` section 5 | Markdown structure + sans emojis |

---

## 2. Activite A13 - Deploiement technique

### C30 - Selectionner les technologies d'hebergement

**Ce que demande le jury :**
> "Le dossier contient une documentation presentant une solution d'hebergement repondant aux besoins de la solution"
> "Le candidat justifie ses choix au regard des contraintes (budget, securite, scalabilite, QoS)"

**Notre reponse :**

- **Solution** : Docker + Nginx + GitHub Actions + Let's Encrypt
- **Budget** : 100% open-source et gratuit (hors cout serveur VPS)
- **Securite** : TLS 1.3, HSTS, utilisateur non-root, Bandit, Trivy
- **Scalabilite** : multi-arch (amd64+arm64), plusieurs instances Flask possibles
- **QoS** : healthcheck 30s, restart automatique, 609 req/s mesures

**Fichier cle :** `A13_Deploiement/B6_C30_Technologies_Hebergement.md`

---

### C31 - Automatisation du deploiement

**Ce que demande le jury :**
> "Le dossier contient une procedure detaillant la mise en oeuvre des technologies"
> "Le candidat demontre que la procedure de deploiement est fonctionnelle"

**Notre reponse :**

- **Procedure** : pipeline 8 jobs GitHub Actions (entierement documente)
- **Demonstration** : `git push` = deploiement complet en ~15 min
- **Artefacts** : images Docker taguees, rapports de tests, coverage
- **Rollback** : script restore.sh + git checkout <tag>

**Fichier cle :** `A13_Deploiement/B6_C31_Procedure_Deploiement.md`

---

### C32 - Normes de securite

**Ce que demande le jury :**
> "La documentation contient les elements demontrant la prise en compte des bonnes pratiques de securite"
> "Le candidat atteste de l'implementation des solutions de securisation"

**Notre reponse :**

- **Defense en profondeur** : 7 couches (reseau, transport, app, container, code, tests, monitoring)
- **OWASP Top 10** : couvert par security_scanner.py (1240 lignes)
- **Outils** : Bandit (pre-commit + CI), detect-secrets, Safety, pip-audit, Trivy
- **Preuve concrete** : PR #1 bloquee par Bandit (7 failles detectees dans export_csv.py)

**Fichier cle :** `A13_Deploiement/B6_C32_Securite_Infrastructure.md`

---

## 3. Activite A14 - Documentation et communication

### C33 - Documentation technique

**Ce que demande le jury :**
> "Le dossier presente un ensemble documentaire detaillant les choix technologiques, d'architecture et d'implementation"
> "Le candidat argumente que ses choix garantissent la perennite de l'application"
> "Les documents respectent les recommandations d'accessibilite"

**Notre reponse :**

- **Ensemble documentaire** : 20+ fichiers, 50,000 mots, tous niveaux (operationnel, technique, soutenance)
- **Justification** : Python 3.12 (support 2028), Docker (standard), tests 80%+, architecture modulaire
- **Accessibilite** : Markdown structure, sans emojis, tables avec en-tetes, langage clair

**Fichier cle :** `A14_Documentation_Communication/B6_C33_Documentation_Technique.md`

---

### C34 - Communication

**Ce que demande le jury :**
> "Le dossier contient des elements attestant d'echanges reguliers entre les parties prenantes"
> "Le candidat presente le projet de maniere comprehensible a un auditoire non technique"
> "Le candidat engage un echange technique approfondi avec un expert"
> "Les documents respectent les recommandations d'accessibilite"

**Notre reponse :**

- **Echanges** : 6 rapports journaliers + commits conventionnels + PR #1 avec review Nicolas
- **Discours non-technique** : SCRIPT_GAMMA_PPT.md (14 slides avec fil conducteur clair)
- **Echange technique** : Q&R prepares dans B6_C34 + maitrise du Dockerfile, CI/CD, OWASP
- **Accessibilite** : documents sans emojis, Markdown structure, francais clair

**Fichier cle :** `A14_Documentation_Communication/B6_C34_Communication.md`

---

## 4. Carte des preuves dans le code

### Preuves de deploiement

```
LegacyProject/
├── modernProject/
│   ├── Dockerfile                          C30.1, C31.1, C32.1
│   ├── docker-entrypoint.sh               C31.1
│   ├── .github/workflows/ci.yml           C31.1, C31.2, C32.1
│   └── tests/performance/
│       ├── test_benchmarks.py             C30.1 (performances mesurees)
│       └── locustfile.py                  C31.2 (demo charge)
└── docs/
    └── DEPLOYMENT_GUIDE.md               C30.1, C31.1 (1547 lignes)
```

### Preuves de securite

```
LegacyProject/modernProject/
├── lib/security.py                        C32.1, C32.2 (AES-256, bcrypt, JWT)
├── lib/export_csv.py                      C32.2 (preuve: detecte par Bandit)
├── tests/
│   ├── test_security_coverage.py         C32.2 (74 tests SecurityManager)
│   ├── test_secure.py                    C32.2 (path traversal)
│   └── security/security_scanner.py     C32.1 (OWASP Top 10)
├── .pre-commit-config.yaml               C32.1 (Bandit, detect-secrets)
└── .github/workflows/ci.yml             C32.1 (Safety, pip-audit, Trivy)
```

### Preuves de documentation

```
avancement/
├── JOUR1_RAPPORT.md a jour6_rapport.md   C34.1 (rapports journaliers)
├── AUDIT_COMPLET.md                      C33.1 (audit 964 lignes)
├── RECAP_PROJET.md                       C33.1
└── coverage_reports/*.md                 C33.1 (10 rapports)

LegacyProject/docs/
├── Components.md                         C33.1 (catalogue composants)
├── DEPLOYMENT_GUIDE.md                   C33.1, C33.2
├── QA_STRATEGY.md                        C33.1
├── RGPD_COMPLIANCE.md                    C33.1
└── Disability_Standards.md              C33.3 (accessibilite)

soutenance_rncp/
├── SCRIPT_GAMMA_PPT.md                   C34.2 (discours non-technique)
├── GUIDE_ORAL_ET_SLIDES.md               C34.2, C34.3
└── Bloc6/ (ce dossier)                   C30-C34
```

### Preuves de communication

```
GitHub repository:
├── Historique commits (git log --oneline)  C34.1 (traçabilite)
├── PR #1 (feature/add-export-csv)          C34.1 (collaboration Nicolas)
├── Review "Request changes" Nicolas        C34.1 (echange technique)
└── Branch protection configuree            C34.1 (workflow defini)
```

---

## 5. Commandes de demonstration

### Pour C31.2 - Demontrer le deploiement

```bash
# Demo locale : build + run + health check
cd LegacyProject/modernProject
docker build -t awkward-legacy:demo .
docker run -d -p 5000:5000 --name demo awkward-legacy:demo
sleep 10 && curl -f http://localhost:5000/health
docker logs demo
docker stop demo && docker rm demo
```

### Pour C32.2 - Demontrer la securite

```bash
# Bandit sur le code propre (0 issues)
cd LegacyProject/modernProject
bandit -r lib/ -ll

# Bandit sur le code intentionnellement cassé (7 issues)
bandit lib/export_csv.py

# Tests de securite
pytest tests/test_security_coverage.py tests/test_secure.py -v --tb=short
```

### Pour C33.1 - Montrer la documentation

```bash
# Voir tous les documents
ls -la LegacyProject/docs/
ls -la avancement/
ls -la soutenance_rncp/Bloc6/

# Compter le contenu
wc -l LegacyProject/docs/DEPLOYMENT_GUIDE.md
wc -l LegacyProject/docs/Components.md
```

### Pour C34.1 - Montrer les echanges

```bash
# Historique des commits
git log --oneline --graph

# Voir la PR #1
gh pr view 1

# Voir la review de Nicolas
gh pr view 1 --comments
```

---

**Derniere revision :** Mars 2026
