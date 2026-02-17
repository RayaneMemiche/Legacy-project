# Dossier de Soutenance RNCP - Bloc 5 EIP

**Projet :** AWKWARD LEGACY - Modernisation de GeneWeb
**Candidat :** Rayane Memiche
**Date :** 17 Fevrier 2026
**Referentiel :** Certificative - Bloc 5 - EIP

---

## Structure du Dossier

### Grille de competences (source)

| Fichier | Description |
|---------|------------|
| `Certificative - bloc 5 - EIP - Francais 2 1.xlsx` | Grille de competences officielle |

---

### A11. Elaboration d'une politique de test

**Repertoire :** `B5_A11_Politique_de_test/`

| Fichier | Competences | Description |
|---------|------------|------------|
| `B5_C25-C26-C27_Politique_de_Tests.md` | C25.1, C25.2, C26.1, C26.2, C27.1, C27.2 | Politique de tests complete : strategie, justification des choix, protocoles, scenarios, outils, metriques |
| `B5_C25-C26_Methodologie_Tests.md` | C25.1, C26.1 | Methodologie des tests : pyramide de tests, repartition, workflow |
| `B5_C27_Inventaire_Composants_et_Tests.md` | C27.1, C27.2 | Inventaire detaille de tous les composants et tests du projet |

**Correspondance competences :**

- **C25.1** (Documentation des politiques de tests) : `B5_C25-C26-C27_Politique_de_Tests.md` - Document complet de 748+ lignes
- **C25.2** (Justification) : `B5_C25-C26-C27_Politique_de_Tests.md` - Section "Justification de la strategie"
- **C26.1** (Protocole adapte) : `B5_C25-C26-C27_Politique_de_Tests.md` - Section 7.1 avec justification de chaque outil
- **C26.2** (Expliquer ses choix) : `B5_C25-C26-C27_Politique_de_Tests.md` - Tableau de justification des 10 outils
- **C27.1** (Protocole et code coherents) : 1023 tests passants, `B5_C27_Inventaire_Composants_et_Tests.md`
- **C27.2** (Couverture des tests) : 81% de couverture, rapports dans `B5_Preuves_et_artefacts/`

---

### A12. Elaboration de normes et de processus qualite

**Repertoire :** `B5_A12_Normes_et_processus_QA/`

| Fichier | Competences | Description |
|---------|------------|------------|
| `B5_C28_Strategie_Assurance_Qualite.md` | C28.1, C28.2, C29.1 | Strategie QA complete : objectifs, normes, processus, accessibilite, metriques |
| `B5_C28.2_Accessibilite_WCAG.md` | C28.2 | Audit d'accessibilite WCAG 2.1 AA avec etat actuel et corrections |
| `B5_C28_Conformite_RGPD.md` | C28.1 | Documentation de conformite RGPD |
| `B5_C29_Preuves_et_Historique_QA.md` | C29.2, C29.3 | Preuves du processus QA : resultats, corrections, historique git |

**Correspondance competences :**

- **C28.1** (Documentation QA strategy) : `B5_C28_Strategie_Assurance_Qualite.md` - 10 sections couvrant toute la strategie
- **C28.2** (Accessibilite) : `B5_C28_Strategie_Assurance_Qualite.md` Section 2.2 + `B5_C28.2_Accessibilite_WCAG.md` + 39 tests d'accessibilite
- **C29.1** (Justification) : `B5_C28_Strategie_Assurance_Qualite.md` Section 1.3 et 4.3
- **C29.2** (Demonstration du processus suivi) : `B5_C29_Preuves_et_Historique_QA.md` + rapports de couverture + pipeline CI/CD
- **C29.3** (Prise en compte de la QA strategy) : `B5_C29_Preuves_et_Historique_QA.md` Section 3 - 5 corrections documentees avec commits

---

### Preuves et artefacts

**Repertoire :** `B5_Preuves_et_artefacts/`

| Fichier | Competences | Description |
|---------|------------|------------|
| `B5_C29.2_Audit_Complet.md` | C29.2 | Audit complet du projet (964 lignes) - score 85/100 |
| `B5_C29.2_Recap_Projet.md` | C29.2 | Recapitulatif du projet avec resultats |
| `B5_C29.2_Pipeline_CI_CD.yml` | C29.2 | Configuration GitHub Actions (5 jobs) |
| `B5_C29.2_Pre_Commit_Hooks.yaml` | C29.2 | 30+ hooks de qualite pre-commit |
| `B5_Presentation_Solution.md` | Support | Presentation technique de la solution |
| `B5_C27.2_Rapports_Couverture/` | C27.2 | 10 rapports de couverture (progression Oct 2025) |

---

## Resultats Cles

| Metrique | Valeur |
|----------|--------|
| Tests passants | **1023** |
| Couverture de code | **81%** |
| Tests d'accessibilite | **39/39 (100%)** |
| Fichiers de tests | **55+** |
| Lignes de tests | **~14 000** |
| Score projet global | **85/100** |
| Pre-commit hooks | **30+** |
| Jobs CI/CD | **5** |
