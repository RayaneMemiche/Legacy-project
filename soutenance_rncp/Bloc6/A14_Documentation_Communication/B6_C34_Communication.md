# Communication et Parties Prenantes - AWKWARD LEGACY

**Version:** 1.0
**Date:** Mars 2026
**Projet:** AWKWARD LEGACY - Modernisation de GeneWeb
**Referentiel RNCP:** Bloc 6 - C34.1, C34.2, C34.3, C34.4

---

## Table des Matieres

1. [Echanges reguliers entre parties prenantes](#1-echanges-reguliers-entre-parties-prenantes)
2. [Moyens de communication utilises](#2-moyens-de-communication-utilises)
3. [Preparation au discours clair et comprehensible](#3-preparation-au-discours-clair-et-comprehensible)
4. [Preparation a l'echange technique approfondi](#4-preparation-a-lechange-technique-approfondi)
5. [Accessibilite des documents de communication](#5-accessibilite-des-documents-de-communication)

---

## 1. Echanges reguliers entre parties prenantes

### 1.1 Parties prenantes du projet

| Partie prenante | Role | Mode de communication |
|----------------|------|----------------------|
| **Rayane Memiche** | Developpeur principal, auteur EIP | Commits Git, rapports journaliers |
| **Nicolas Poupon** | Collaborateur technique, reviewer code | GitHub PRs, reviews, collaboration repo |
| **Jury RNCP** | Evaluateurs Bloc 5 et Bloc 6 | Dossier de preuves, soutenance orale |
| **Ecole (Epitech)** | Commanditaire EIP | Documentation de projet, avancement |

### 1.2 Historique des echanges (preuves)

#### Rapports journaliers (avancement/)

Le projet a ete documente avec des rapports journaliers sur 6 jours consecutifs :

| Rapport | Contenu |
|---------|---------|
| `avancement/JOUR1_RAPPORT.md` | Audit initial du code OCaml, identification des composants |
| `avancement/jour2_rapport.md` | Developpement des modules Python de base |
| `avancement/jour3_rapport.md` | Integration des tests et CI/CD |
| `avancement/jour4_rapport.md` | Securite et conformite RGPD |
| `avancement/jour5_rapport.md` | Tests de performance et accessibilite |
| `avancement/jour6_rapport.md` | Finalisation et documentation |

Ces rapports constituent la trace des echanges et decisions prises a chaque etape.

#### Collaboration Git (GitHub)

La collaboration avec Nicolas est tracee via GitHub :

| Evenement | Preuve | Date |
|-----------|--------|------|
| Push initial du projet | Historique Git | Oct 2025 |
| PR #1 creee (feature/add-export-csv) | `github.com/NicolasPoupon/Legacy-project/pull/1` | Mars 2026 |
| Review "Request changes" par Nicolas | PR #1 (review soumise) | Mars 2026 |
| Configuration protection de branche | GitHub Settings | Mars 2026 |
| Droits admin accordes par Nicolas | GitHub Settings > Collaborators | Mars 2026 |

#### Commits conventionnels (traçabilite)

Tous les commits suivent le format Conventional Commits (valide par Commitizen + Gitlint) :

```
feat: Complete Bloc 5 RNCP compliance - tests, accessibility, QA docs
docs: Add presentation scripts and oral guide for RNCP Bloc 5 soutenance
fix: Enforce strict CI/CD quality gates
docs: Remove RNCP criterion codes from document titles
docs: Remove emojis from all .md files and reorganize soutenance structure
```

**Commande pour visualiser :** `git log --oneline`

---

## 2. Moyens de communication utilises

### 2.1 GitHub (principal)

**Usage :** Gestion de code, revues, issues, CI/CD

- **Commits** : chaque modification est decrite et tracee
- **Pull Requests** : interface de revue de code (PR #1 = preuve concrete)
- **Issues** : suivi des bugs et taches
- **GitHub Actions** : notifications automatiques (email) sur l'etat du pipeline
- **Branch protection** : enforcement des regles de qualite

**Justification du choix :** GitHub est la plateforme de reference pour les projets de code. Tous les developpeurs la maitrisent. La traçabilite est permanente et consultable par toutes les parties.

### 2.2 Documentation Markdown

**Usage :** Partage d'information structuree

- **Rapports journaliers** : synthese des avancees et blocages
- **Guides techniques** : DEPLOYMENT_GUIDE, QUICK_START, COMMANDES
- **Documentation de soutenance** : INDEX, GUIDE_ORAL, scripts

**Justification :** Markdown est lisible en texte brut et rendu automatiquement par GitHub. Pas de logiciel specialise requis. Versionnable avec Git.

### 2.3 CI/CD comme canal de communication automatise

Le pipeline GitHub Actions communique automatiquement :
- **Email** : notification sur l'etat du pipeline (succes / echec)
- **Slack** : webhook configure pour les notifications de deploiement production
- **GitHub Security** : rapports Trivy (vulnerabilites Docker) visibles dans l'onglet Security
- **Codecov** : rapports de couverture de tests partages automatiquement

### 2.4 Commits conventionnels comme langage commun

Le format Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`) est une forme de communication standardisee :
- N'importe qui peut comprendre le type de changement sans lire le diff
- Permet la generation automatique du CHANGELOG
- Valide automatiquement par Commitizen (echec si non respecte)

---

## 3. Preparation au discours clair et comprehensible

### 3.1 Structure de la presentation

La soutenance est organisee pour etre comprehensible par un jury non technique :

**Fil conducteur :**
1. Le probleme : GeneWeb (1995, OCaml, maintenu par personne)
2. La solution : moderniser vers Python, stack 2025
3. La methode : tests, securite, qualite, deploiement
4. Les preuves : chiffres, demonstrations, artefacts

**Analogies utilisables :**
- Le deploiement Docker = "emballage" de l'application avec tout ce qu'il faut
- Le CI/CD = "controle qualite automatique a chaque livraison"
- OWASP Top 10 = "les 10 erreurs les plus courantes en securite web"
- WCAG 2.1 = "le code de la route pour l'accessibilite web"

### 3.2 Slides de synthese (document SCRIPT_GAMMA_PPT.md)

Le script PowerPoint (14 slides) est concu pour un auditoire non technique :

| Slide | Titre | Duree |
|-------|-------|-------|
| 1 | Contexte et enjeux | 2 min |
| 2 | Documentation politique de tests | 2 min |
| 3 | Justification strategie | 2 min |
| 4 | Protocole adapte | 2 min |
| 5 | Choix d'outils | 2 min |
| 6 | Coherence protocole/code | 2 min 30 |
| 7 | Couverture des tests | 2 min |
| 8 | Strategie QA | 2 min |
| 9 | Accessibilite | 2 min 30 |
| 10 | Justification QA | 1 min 30 |
| 11 | Preuves du processus | 2 min 30 |
| 12 | Corrections appliquees | 2 min 30 |
| 13 | Synthese | 1 min |
| 14 | Conclusion | 1 min |

**Fichier :** `soutenance_rncp/SCRIPT_GAMMA_PPT.md`

### 3.3 Guide oral pour la soutenance

Le fichier `GUIDE_ORAL_ET_SLIDES.md` contient les scripts de presentation pour chaque slide, avec :
- Le discours mot pour mot
- Les points cles a ne pas oublier
- Les transitions entre slides

---

## 4. Preparation a l'echange technique approfondi

### 4.1 Questions techniques probables et reponses

**Sur le deploiement (C30-C31) :**

Q: "Pourquoi Docker plutot qu'un deploiement classique Python ?"
R: "Docker garantit que le code se comporte identiquement en dev et prod. Le Dockerfile est le contrat entre les environnements. Sans Docker, on a des problemes de versions Python, de dependances, de configuration systeme. Avec Docker, on construit une image immuable testee dans le CI."

Q: "Comment fonctionne votre pipeline CI/CD ?"
R: "8 jobs GitHub Actions s'executent sequentiellement. Le lint doit passer avant les tests, les tests avant le build Docker, et le build avant le deploiement. Si un job echoue, les suivants sont annules. C'est un principe de fail-fast : on detecte le probleme au plus tot."

**Sur la securite (C32) :**

Q: "Comment vous assurez-vous qu'aucun secret n'est commite dans le code ?"
R: "Deux mecanismes : detect-secrets dans le pre-commit (scanne le diff avant chaque commit) et un hook custom qui refuse le commit si un fichier .env est present. Les secrets de production sont dans GitHub Secrets, chiffres au repos."

Q: "Qu'est-ce que Bandit detecte concrètement ?"
R: "Bandit fait de l'analyse statique Python sans executer le code. Il detecte les appels dangereux : eval() (execution de code arbitraire), pickle.load() (deserialisation non securisee), subprocess(shell=True) (injection shell), les mots de passe en dur, les hashs MD5/SHA1 (faibles). La PR #1 en est la demonstration en temps reel."

**Sur la documentation (C33) :**

Q: "Comment garantissez-vous que la documentation reste a jour ?"
R: "Trois mecanismes : 1/ Les docstrings sont dans le code lui-meme, donc mis a jour avec le code. 2/ Le CHANGELOG est genere automatiquement par git-cliff depuis les conventional commits. 3/ Le CI echoue si les tests ne passent pas, donc la documentation des comportements (tests) est toujours synchrone avec le code reel."

Q: "Pourquoi Python plutot que de continuer en OCaml ?"
R: "GeneWeb original est en OCaml 4.x des annees 2000. Le bassin de developpeurs OCaml est tres reduit. Python est le 2eme langage mondial (TIOBE 2024), avec un ecosysteme riche (Flask, pytest, Bandit, mypy). La reprise du projet par une autre equipe est beaucoup plus probable en Python qu'en OCaml."

**Sur la communication (C34) :**

Q: "Comment avez-vous communique avec Nicolas Poupon ?"
R: "Via GitHub principalement : Pull Requests avec reviews, branch protection requiring 1 approval, conventional commits pour la comprehension immmediate des changements. La PR #1 montre une vraie collaboration : Nicolas a fait une review avec Request Changes apres avoir vu le CI echouer."

### 4.2 Points techniques a maitriser

**Savoir expliquer :**
- La difference entre `docker build` et `docker-compose up`
- Ce que fait un reverse proxy (Nginx) vs l'application (Flask)
- La difference entre TLS termination et TLS passthrough
- Ce que mesure la couverture de tests (% de lignes de code executees par les tests)
- La difference entre Bandit (analyse statique) et les tests de securite (execution)
- Ce qu'est JWT et pourquoi c'est utile (stateless, expirable)

**Savoir montrer :**
- Le pipeline CI sur GitHub Actions (onglet Actions)
- La PR #1 avec CI en echec et review Request Changes
- Un test Bandit en ligne de commande
- Le health check Docker : `curl http://localhost:5000/health`
- Le rapport de couverture : `pytest --cov=lib --cov-report=term`

---

## 5. Accessibilite des documents de communication

### 5.1 Documents sans emojis

Tous les documents de communication (rapports, guides, README) ont ete nettoyes de leurs emojis. Preuve : commit `61de763` (68 fichiers modifies).

**Pourquoi c'est important pour l'accessibilite :**
- Les lecteurs d'ecran lisent les emojis verbalement : le "thumbs up" devient "pouce leve vers le haut" ce qui brise le flux de lecture
- Certains emojis n'ont pas de description universelle
- Les documents professionnels preferent le texte clair

### 5.2 Structure des documents de communication

Chaque rapport et document du projet respecte :

- **Titre H1** unique par document (structure claire)
- **Sections H2/H3** hierarchisees (navigation lecteur d'ecran)
- **Tableaux** avec lignes d'en-tete (`**gras**` ou header Markdown)
- **Listes** structurees (pas de texte brut non structure)
- **Code en blocs** : delimite du texte narratif (triple backtick)
- **Langue identifiable** : tout en francais, consistent

### 5.3 Format et accessibilite

- **Format Markdown** : rendu HTML standard, compatible lecteurs d'ecran
- **GitHub rendering** : accessible directement dans le navigateur
- **Pas de couleurs** dans les documents texte (accessibilite daltoniens)
- **Pas de tableau uniquement visuel** : toute information en tableau est aussi lisible en texte

### 5.4 Conformite C33.3 et C34.4

Les criteres C33.3 et C34.4 demandent que les documents respectent les recommandations d'accessibilite. La conformite est assuree par :

1. **Suppression des emojis** (commit `61de763`)
2. **Structure semantique Markdown** (H1 > H2 > H3)
3. **Tables avec en-tetes explicites**
4. **Texte alternatif conceptuel** : les schemas ASCII (`+---+`) sont accompagnes d'explications textuelles
5. **Langage clair et structure** : pas de jargon sans explication

---

**Derniere revision :** Mars 2026
