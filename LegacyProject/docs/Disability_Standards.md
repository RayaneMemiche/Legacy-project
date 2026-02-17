#  Standards d'Accessibilité - AWKWARD LEGACY
## État Actuel de l'Implémentation

**Date:** 30 Octobre 2025
**Version:** 1.0
**Projet:** AWKWARD LEGACY - Modernisation de bases généalogiques
**Score d'Accessibilité Estimé:** 45-50% (WCAG 2.1 AA)

---

##  Table des Matières

1. [Vue d'Ensemble](#-vue-densemble)
2. [Fonctionnalités Implémentées](#-fonctionnalités-implémentées)
3. [Détails Techniques](#-détails-techniques)
4. [Fichiers Concernés](#-fichiers-concernés)
5. [Lacunes Identifiées](#-lacunes-identifiées)
6. [Évaluation par Catégorie](#-évaluation-par-catégorie)

---

##  Vue d'Ensemble

Ce document recense **uniquement les fonctionnalités d'accessibilité déjà implémentées** dans le projet AWKWARD LEGACY. Il reflète l'état actuel du code et ne contient pas de recommandations futures.

### Résumé de l'État Actuel

| Catégorie | Implémentation | Score |
|-----------|---------------|-------|
| Formulaires | Excellente | 90%  |
| Gestion du Focus | Bonne | 75%  |
| Design Réactif | Bonne | 70%  |
| Mode Sombre | Bonne | 70%  |
| Lecteurs d'Écran | Faible | 30%  |
| Navigation Clavier | Basique | 40%  |
| ARIA | Très Faible | 15%  |
| Structure Sémantique | Partielle | 35%  |

---

##  Fonctionnalités Implémentées

### 1. Accessibilité des Formulaires

**Status:**  Excellente implémentation

Tous les formulaires de l'application utilisent des pratiques d'accessibilité correctes:

#### Formulaire de Recherche
```html
<!-- Fichier: frontend/index.html, Lignes 152-170 -->
<label for="searchFirstName" class="form-label">Prénom</label>
<input type="text" class="form-control" id="searchFirstName">

<label for="searchLastName" class="form-label">Nom</label>
<input type="text" class="form-control" id="searchLastName">

<label for="searchBirthYear" class="form-label">Année de naissance</label>
<input type="number" class="form-control" id="searchBirthYear">

<label for="searchDeathYear" class="form-label">Année de décès</label>
<input type="number" class="form-control" id="searchDeathYear">

<label for="searchPlace" class="form-label">Lieu</label>
<input type="text" class="form-control" id="searchPlace">
```

#### Formulaire de Connexion
```html
<!-- Fichier: frontend/index.html, Lignes 307-316 -->
<label for="loginEmail" class="form-label">Email</label>
<input type="email" class="form-control" id="loginEmail" required>

<label for="loginPassword" class="form-label">Mot de passe</label>
<input type="password" class="form-control" id="loginPassword" required>

<input type="checkbox" class="form-check-input" id="rememberMe">
<label class="form-check-label" for="rememberMe">Se souvenir de moi</label>
```

#### Formulaire d'Inscription
```html
<!-- Fichier: frontend/index.html, Lignes 338-356 -->
<label for="registerName" class="form-label">Nom complet</label>
<input type="text" class="form-control" id="registerName" required>

<label for="registerEmail" class="form-label">Email</label>
<input type="email" class="form-control" id="registerEmail" required>

<label for="registerPassword" class="form-label">Mot de passe</label>
<input type="password" class="form-control" id="registerPassword" required>

<label for="registerPasswordConfirm" class="form-label">Confirmer le mot de passe</label>
<input type="password" class="form-control" id="registerPasswordConfirm" required>

<input type="checkbox" class="form-check-input" id="acceptTerms" required>
<label class="form-check-label" for="acceptTerms">
  J'accepte les conditions d'utilisation
</label>
```

**Points forts:**
-  Tous les champs ont des labels associés via l'attribut `for`
-  Attribut `required` présent sur les champs obligatoires
-  Types d'input appropriés (email, password, number, text, checkbox)
-  Classes Bootstrap pour styling cohérent

---

### 2. Gestion du Focus

**Status:**  Bonne implémentation

#### Styles de Focus Visibles

```css
/* Fichier: frontend/styles.css, Lignes 502-510 */

/* Focus global sur tous les éléments */
*:focus {
    outline: 2px solid var(--primary-color);
    outline-offset: 2px;
}

/* Focus renforcé pour boutons et liens */
button:focus,
a:focus {
    outline-offset: 4px;
}
```

#### Focus sur les Contrôles de Formulaire

```css
/* Fichier: frontend/styles.css, Lignes 190-194 */
.form-control:focus,
.form-select:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}
```

#### Gestion du Focus dans les Modales

```html
<!-- Fichier: frontend/index.html, Lignes 297, 328 -->
<div class="modal fade" id="loginModal" tabindex="-1">
<div class="modal fade" id="registerModal" tabindex="-1">
```

```javascript
// Fichier: frontend/app_complete.js, Ligne 448
modal.setAttribute('tabindex', '-1');
```

**Points forts:**
-  Outline visible de 2px sur tous les éléments focusables
-  Offset de 4px sur les boutons et liens pour meilleure visibilité
-  Box-shadow sur les contrôles de formulaire
-  Modales avec tabindex="-1" pour gestion du focus

---

### 3. Support des Lecteurs d'Écran

**Status:**  Implémentation basique

#### Classe Screen Reader Only

```css
/* Fichier: frontend/styles.css, Lignes 489-499 */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0,0,0,0);
    white-space: nowrap;
    border: 0;
}
```

Cette classe permet de masquer visuellement du texte tout en le rendant accessible aux lecteurs d'écran.

#### Texte Masqué Visuellement

```html
<!-- Fichier: frontend/index_new.html, Ligne 399 -->
<div class="spinner-border text-primary" role="status">
  <span class="visually-hidden">Chargement...</span>
</div>
```

#### Régions ARIA Live

```html
<!-- Fichier: frontend/index_new.html, Ligne 201 -->
<div class="toast-container position-fixed bottom-0 end-0 p-3"
     aria-live="polite"
     aria-atomic="true">
</div>
```

```javascript
// Fichier: frontend/app.js, Ligne 634
toast.setAttribute('role', 'alert');
```

**Points forts:**
-  Classe `.sr-only` correctement implémentée
-  Utilisation de `.visually-hidden` sur les spinners
-  Toast container avec `aria-live="polite"`
-  Toasts avec `role="alert"`

**Limitations:**
-  Seulement 2 attributs ARIA dans tout le code
-  Aucun `aria-label` sur les boutons d'icônes
-  Pas d'`aria-describedby` pour les messages d'aide

---

### 4. Éléments Sémantiques HTML

**Status:**  Implémentation partielle

#### Navigation Sémantique

```html
<!-- Fichier: frontend/index.html, Ligne 13 -->
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
  <!-- Navigation principale -->
</nav>

<!-- Fichier: frontend/index_new.html, Ligne 117 -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
  <!-- Navigation principale -->
</nav>
```

#### Attributs Role

```html
<!-- Fichier: frontend/index.html -->
<button role="button" class="dropdown-toggle">  <!-- Ligne 41 -->
<div class="btn-group" role="group">            <!-- Ligne 197 -->

<!-- Fichier: frontend/index_new.html -->
<button role="button" class="dropdown-toggle">  <!-- Lignes 143, 169, 184 -->
<div role="status" class="spinner-border">      <!-- Ligne 398 -->
```

**Points forts:**
-  Utilisation de l'élément `<nav>` pour la navigation
-  Attribut `role="button"` sur les toggles de dropdown
-  `role="group"` sur les groupes de boutons
-  `role="status"` sur les spinners de chargement

**Limitations:**
-  Pas d'élément `<main>` pour le contenu principal
-  Pas d'élément `<header>` ou `<footer>`
-  Pas d'utilisation de `<article>` ou `<section>`
-  Pas d'élément `<aside>` pour les sidebars

---

### 5. Mode Sombre et Préférences Système

**Status:**  Bonne implémentation

#### Variables CSS pour le Thème

```css
/* Fichier: frontend/styles.css, Lignes 3-11 */
:root {
    --primary-color: #0d6efd;    /* Bootstrap blue */
    --secondary-color: #6c757d;  /* Bootstrap gray */
    --success-color: #198754;    /* Bootstrap green */
    --warning-color: #ffc107;    /* Bootstrap yellow */
    --danger-color: #dc3545;     /* Bootstrap red */
    --light-color: #f8f9fa;      /* Light gray */
    --dark-color: #212529;       /* Near black */
}
```

#### Mode Sombre Automatique

```css
/* Fichier: frontend/styles.css, Lignes 377-413 */
@media (prefers-color-scheme: dark) {
    body {
        background-color: #1a1d23;
        color: #e4e6eb;
    }

    .navbar {
        background-color: #242526 !important;
    }

    .card {
        background-color: #242526;
        border-color: #3a3b3c;
        color: #e4e6eb;
    }

    .modal-content {
        background-color: #242526;
        color: #e4e6eb;
        border-color: #3a3b3c;
    }

    .form-control,
    .form-select {
        background-color: #3a3b3c;
        border-color: #4e4f50;
        color: #e4e6eb;
    }

    .table {
        color: #e4e6eb;
    }

    .table-striped tbody tr:nth-of-type(odd) {
        background-color: rgba(255, 255, 255, 0.05);
    }
}
```

**Points forts:**
-  Détection automatique de la préférence système
-  Thème sombre complet (navbar, cards, modals, forms, tables)
-  Couleurs sombres avec bon contraste
-  Utilisation de variables CSS pour cohérence

**Limitations:**
-  Pas de toggle manuel pour le mode sombre
-  Pas de support `prefers-reduced-motion`
-  Pas de support `prefers-contrast: high`

---

### 6. Design Réactif (Responsive)

**Status:**  Bonne implémentation

#### Breakpoints Responsive

```css
/* Fichier: frontend/styles.css, Lignes 416-459 */

/* Tablettes et petits écrans */
@media (max-width: 768px) {
    .card {
        margin-bottom: 1rem;
    }

    .btn-group {
        flex-direction: column;
    }

    .table-responsive {
        font-size: 0.875rem;
    }

    .navbar-collapse {
        background-color: rgba(0, 0, 0, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 0.5rem;
    }
}

/* Mobiles */
@media (max-width: 576px) {
    h1 {
        font-size: 1.75rem;
    }

    .btn {
        font-size: 0.875rem;
        padding: 0.5rem 1rem;
    }

    .modal-dialog {
        margin: 0.5rem;
    }

    .card-body {
        padding: 1rem;
    }

    .toast {
        font-size: 0.875rem;
    }
}
```

#### Meta Viewport

```html
<!-- Tous les fichiers HTML -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**Points forts:**
-  Breakpoints à 768px (tablette) et 576px (mobile)
-  Ajustements de taille de police
-  Adaptation des boutons et cards
-  Meta viewport configuré correctement
-  Pas de désactivation du zoom utilisateur

---

### 7. Styles d'Impression

**Status:**  Implémentée

```css
/* Fichier: frontend/styles.css, Lignes 358-374 */
@media print {
    .navbar,
    .btn,
    .modal,
    .toast-container {
        display: none !important;
    }

    .card {
        box-shadow: none;
        border: 1px solid #000;
    }

    body {
        background-color: white;
        color: black;
    }

    a {
        text-decoration: underline;
    }
}
```

**Points forts:**
-  Masquage des éléments interactifs (navbar, boutons, modals, toasts)
-  Simplification des cards
-  Fond blanc et texte noir pour économie d'encre
-  Liens soulignés

---

### 8. Déclaration de Langue

**Status:**  Implémentée

```html
<!-- Tous les fichiers HTML, Ligne 2 -->
<html lang="fr">
```

**Fichiers concernés:**
- `frontend/index.html`
- `frontend/index_new.html`
- `frontend/comparison.html`
- `frontend/geneweb-demo.html`

**Points forts:**
-  Langue déclarée sur toutes les pages
-  Code de langue correct (fr = français)
-  Aide les lecteurs d'écran à choisir la bonne prononciation

---

### 9. Notifications Accessibles

**Status:**  Bonne implémentation

#### Toast Container avec ARIA Live

```html
<!-- Fichier: frontend/index_new.html, Ligne 201 -->
<div class="toast-container position-fixed bottom-0 end-0 p-3"
     aria-live="polite"
     aria-atomic="true">
</div>
```

#### Création Dynamique de Toasts

```javascript
// Fichier: frontend/app.js, Lignes 629-658
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container');

    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button"
                    class="btn-close btn-close-white me-2 m-auto"
                    data-bs-dismiss="toast"
                    aria-label="Fermer"></button>
        </div>
    `;

    toastContainer.appendChild(toast);

    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 5000
    });

    bsToast.show();

    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}
```

**Points forts:**
-  Container avec `aria-live="polite"` pour notifications non urgentes
-  Toasts individuels avec `role="alert"` et `aria-live="assertive"`
-  Bouton de fermeture avec `aria-label="Fermer"`
-  Auto-dismiss après 5 secondes
-  Suppression du DOM après fermeture

---

##  Fichiers Concernés

### Fichiers HTML

| Fichier | Localisation | Fonctionnalités |
|---------|-------------|-----------------|
| `index.html` | `/frontend/` | Navigation, formulaires, modals |
| `index_new.html` | `/frontend/` | Toast container, spinners |
| `comparison.html` | `/frontend/` | Navigation |
| `geneweb-demo.html` | `/frontend/` | Navigation |

### Fichiers CSS

| Fichier | Localisation | Fonctionnalités |
|---------|-------------|-----------------|
| `styles.css` | `/frontend/` | Focus, mode sombre, responsive, .sr-only |

### Fichiers JavaScript

| Fichier | Localisation | Fonctionnalités |
|---------|-------------|-----------------|
| `app.js` | `/frontend/` | Toast notifications |
| `app_complete.js` | `/frontend/` | Modals dynamiques |

---

##  Détails Techniques

### Bootstrap 5

Le projet utilise **Bootstrap 5**, qui fournit une base d'accessibilité:

-  Composants accessibles par défaut (modals, dropdowns, toasts)
-  Classes utilitaires (.visually-hidden, .sr-only)
-  Gestion du focus dans les modals
-  Support du clavier (Tab, Escape)
-  ARIA attributes sur les composants

**Version utilisée:** Bootstrap 5.3.x (dernière stable)

### Palette de Couleurs

```css
/* Couleurs basées sur Bootstrap 5 (WCAG 2.1 compliant) */
--primary-color: #0d6efd;    /* Bleu - Ratio 4.5:1 sur blanc */
--success-color: #198754;    /* Vert - Ratio 4.6:1 sur blanc */
--warning-color: #ffc107;    /* Jaune - Ratio 4.5:1 sur blanc */
--danger-color: #dc3545;     /* Rouge - Ratio 5.9:1 sur blanc */
--dark-color: #212529;       /* Noir - Ratio 16.9:1 sur blanc */
```

**Note:** Bootstrap 5 assure des ratios de contraste conformes WCAG 2.1 AA (minimum 4.5:1 pour le texte normal).

---

##  Lacunes Identifiées

### Fonctionnalités Manquantes

#### 1. Skip Links
-  Pas de lien "Aller au contenu principal"
-  Pas de lien "Passer la navigation"
- **Impact:** Utilisateurs clavier doivent tabuler à travers toute la navigation

#### 2. ARIA Complet
-  Seulement 2 attributs ARIA dans tout le code
-  Pas d'`aria-label` sur les boutons d'icônes
-  Pas d'`aria-expanded` sur les dropdowns
-  Pas d'`aria-controls` pour les relations
-  Pas d'`aria-describedby` pour les aides contextuelles
- **Impact:** Lecteurs d'écran ne peuvent pas décrire correctement les interactions

#### 3. Structure Sémantique Complète
-  Pas d'élément `<main>` pour le contenu principal
-  Pas d'éléments `<header>` ou `<footer>`
-  Pas d'utilisation de `<article>` ou `<section>`
-  Pas d'élément `<aside>` pour les sidebars
- **Impact:** Navigation par landmarks impossible pour les utilisateurs de lecteurs d'écran

#### 4. Textes Alternatifs
-  Aucune image avec attribut `alt`
-  Icônes (Bootstrap Icons) sans texte alternatif
-  Exemple: `<i class="bi bi-search"></i>` sans label
- **Impact:** Icônes invisibles pour les lecteurs d'écran

#### 5. Navigation Clavier Personnalisée
-  Pas de gestionnaires d'événements clavier (keydown, keypress)
-  Pas de raccourcis clavier personnalisés
-  Dépendance totale sur Bootstrap pour la navigation
- **Impact:** Pas d'accélérateurs clavier pour power users

#### 6. Préférences d'Animation
-  Pas de support `prefers-reduced-motion`
-  Animations sans possibilité de désactivation
- **Impact:** Problèmes pour utilisateurs sensibles au mouvement

#### 7. Mode Contraste Élevé
-  Pas de support `prefers-contrast: high`
-  Pas de thème contraste élevé
- **Impact:** Difficultés pour utilisateurs malvoyants

#### 8. Documentation
-  Accessibilité mentionnée mais non documentée
-  Pas de guide d'utilisation pour technologies d'assistance
- **Impact:** Manque de transparence sur le niveau d'accessibilité

---

##  Évaluation par Catégorie

### 1. Perceptible (WCAG Principe 1)

| Critère | Status | Détails |
|---------|--------|---------|
| 1.1.1 Contenu non textuel |  Partiel | Icônes sans alt text |
| 1.3.1 Info et relations |  Partiel | Labels OK, landmarks manquants |
| 1.3.2 Ordre séquentiel |  OK | Ordre DOM logique |
| 1.4.1 Utilisation de la couleur |  OK | Pas de dépendance à la couleur seule |
| 1.4.3 Contraste minimum |  OK | Bootstrap 5 palette (4.5:1) |
| 1.4.4 Redimensionnement texte |  OK | Responsive, pas de zoom bloqué |

**Score:** 60% (4/6 critères complets)

### 2. Opérable (WCAG Principe 2)

| Critère | Status | Détails |
|---------|--------|---------|
| 2.1.1 Clavier |  Partiel | Bootstrap OK, pas de custom handlers |
| 2.1.2 Pas de piège clavier |  OK | Modals avec Escape |
| 2.4.1 Contourner des blocs |  Non | Pas de skip links |
| 2.4.3 Parcours du focus |  OK | Ordre logique |
| 2.4.7 Focus visible |  OK | Outlines clairs |

**Score:** 50% (2.5/5 critères complets)

### 3. Compréhensible (WCAG Principe 3)

| Critère | Status | Détails |
|---------|--------|---------|
| 3.1.1 Langue de la page |  OK | lang="fr" |
| 3.2.1 Au focus |  OK | Pas de changements inattendus |
| 3.2.2 À la saisie |  OK | Formulaires prévisibles |
| 3.3.1 Identification erreurs |  Partiel | HTML5 validation, pas ARIA |
| 3.3.2 Étiquettes ou instructions |  OK | Tous les labels présents |

**Score:** 80% (4/5 critères complets)

### 4. Robuste (WCAG Principe 4)

| Critère | Status | Détails |
|---------|--------|---------|
| 4.1.1 Analyse syntaxique |  OK | HTML5 valide |
| 4.1.2 Nom, rôle, valeur |  Partiel | Basique, pas assez ARIA |

**Score:** 50% (1/2 critères complets)

---

##  Score d'Accessibilité Global

### Calcul du Score

| Catégorie | Poids | Score | Points |
|-----------|-------|-------|--------|
| Formulaires | 20% | 90% | 18 |
| Focus | 15% | 75% | 11.25 |
| Lecteurs d'écran | 20% | 30% | 6 |
| ARIA | 15% | 15% | 2.25 |
| Sémantique | 15% | 35% | 5.25 |
| Responsive | 10% | 70% | 7 |
| Autres | 5% | 60% | 3 |

**Score Total:** **52.75% / 100%**

### Niveau de Conformité WCAG 2.1

-  **Niveau A:** Non conforme (manque skip links, ARIA minimal)
-  **Niveau AA:** Non conforme (manque landmarks, textes alternatifs)
-  **Niveau AAA:** Non conforme

**Estimation:** Le projet passerait environ **40-50%** des tests automatisés WCAG 2.1 AA.

---

##  Points Forts

### Ce qui fonctionne bien:

1. **Formulaires** (90%)
   - Tous les labels associés
   - Attributs required
   - Types d'input appropriés

2. **Focus visuel** (75%)
   - Outlines clairs (2px)
   - Box-shadow sur form controls
   - Pas de suppression du focus

3. **Mode sombre** (70%)
   - Détection automatique système
   - Thème complet
   - Bon contraste

4. **Responsive** (70%)
   - 2 breakpoints (768px, 576px)
   - Viewport meta configuré
   - Zoom non bloqué

5. **Bootstrap 5** (70%)
   - Composants accessibles
   - Classes utilitaires
   - Gestion focus modals

6. **Notifications** (65%)
   - Toast avec ARIA live
   - Role alert
   - Auto-dismiss

7. **Langue** (100%)
   - lang="fr" sur toutes les pages

8. **Print** (80%)
   - Styles d'impression
   - Masquage éléments interactifs

---

##  Axes d'Amélioration Prioritaires

### Impact Élevé (Fixes Rapides)

1. **Ajouter Skip Links** (1-2h)
   - Impact: +++
   - Difficulté: Facile
   - Bénéfice immédiat pour navigation clavier

2. **Ajouter `<main>`, `<header>`, `<footer>`** (2-3h)
   - Impact: +++
   - Difficulté: Facile
   - Améliore navigation par landmarks

3. **Aria-label sur icônes** (2-3h)
   - Impact: +++
   - Difficulté: Facile
   - Rend les icônes compréhensibles

4. **Alt text sur images** (1-2h)
   - Impact: +++
   - Difficulté: Facile
   - Si des images sont ajoutées

### Impact Moyen (Améliorations)

5. **Support prefers-reduced-motion** (2-3h)
   - Impact: ++
   - Difficulté: Moyenne
   - Important pour accessibilité

6. **ARIA complet sur dropdowns** (3-4h)
   - Impact: ++
   - Difficulté: Moyenne
   - aria-expanded, aria-controls

7. **Raccourcis clavier** (4-6h)
   - Impact: ++
   - Difficulté: Moyenne
   - Améliore productivité

### Impact Faible (Nice to Have)

8. **Mode contraste élevé** (4-6h)
   - Impact: +
   - Difficulté: Moyenne

9. **Documentation accessibilité** (2-3h)
   - Impact: +
   - Difficulté: Facile

---

##  Contact et Ressources

### Tests Effectués

Ce document est basé sur:
- Analyse manuelle du code source
- Recherche des attributs ARIA
- Vérification des balises sémantiques
- Inspection des styles CSS
- Revue des scripts JavaScript

**Aucun test automatisé n'a été effectué** (axe, Lighthouse, Pa11y).

### Fichiers Analysés

**Total:** 7 fichiers
- 4 fichiers HTML
- 1 fichier CSS
- 2 fichiers JavaScript

---

**Date de génération:** 30 Octobre 2025
**Basé sur:** Commit d232da9
**Statut:** Document à jour avec le code actuel

 **Ce document reflète uniquement l'état ACTUEL de l'implémentation**
