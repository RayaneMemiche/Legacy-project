#  Guide d'Accessibilité - AWKWARD LEGACY

**Date:** 30 Octobre 2025
**Version:** 1.0
**Projet:** AWKWARD LEGACY - Modernisation de bases généalogiques

---

##  Table des Matières

1. [Vue d'Ensemble](#-vue-densemble)
2. [Principes Fondamentaux](#-principes-fondamentaux)
3. [Accessibilité Visuelle](#-accessibilité-visuelle)
4. [Accessibilité Auditive](#-accessibilité-auditive)
5. [Accessibilité Motor](#-accessibilité-motrice)
6. [Accessibilité Cognitive](#-accessibilité-cognitive)
7. [Standards et Conformité](#-standards-et-conformité)
8. [Implémentation Technique](#-implémentation-technique)
9. [Tests et Validation](#-tests-et-validation)
10. [Checklist de Conformité](#-checklist-de-conformité)

---

##  Vue d'Ensemble

Le projet AWKWARD LEGACY s'engage à fournir une application accessible à **tous les utilisateurs**, indépendamment de leurs capacités physiques, sensorielles ou cognitives.

### Objectifs d'Accessibilité

-  **Conformité WCAG 2.1 Niveau AA** (minimum)
-  **Support des technologies d'assistance** (lecteurs d'écran, navigation clavier)
-  **Design inclusif** pour tous les types de handicaps
-  **Performance optimale** sur connexions lentes
-  **Compatibilité multi-appareils** (desktop, mobile, tablette)

### Public Cible

- Personnes aveugles ou malvoyantes
- Personnes sourdes ou malentendantes
- Personnes avec handicaps moteurs
- Personnes avec troubles cognitifs ou d'apprentissage
- Personnes âgées
- Utilisateurs avec connexions limitées

---

##  Principes Fondamentaux

### Les 4 Piliers POUR (WCAG)

#### 1. **Perceptible**
Les informations et composants de l'interface doivent être présentés de manière perceptible par tous.

#### 2. **Opérable**
Les composants de l'interface et la navigation doivent être utilisables par tous.

#### 3. **Compréhensible**
Les informations et le fonctionnement de l'interface doivent être compréhensibles.

#### 4. **Robuste**
Le contenu doit être suffisamment robuste pour être interprété par tous les agents utilisateurs.

---

##  Accessibilité Visuelle

### Pour les Personnes Aveugles

#### 1. **Lecteurs d'Écran (Screen Readers)**

**Technologies supportées:**
- NVDA (Windows)
- JAWS (Windows)
- VoiceOver (macOS, iOS)
- TalkBack (Android)
- Orca (Linux)

**Implémentation:**

```html
<!-- Balises sémantiques HTML5 -->
<header role="banner">
  <nav role="navigation" aria-label="Navigation principale">
    <ul>
      <li><a href="/" aria-current="page">Accueil</a></li>
      <li><a href="/search">Rechercher</a></li>
    </ul>
  </nav>
</header>

<main role="main">
  <h1>Titre principal de la page</h1>
  <article aria-labelledby="person-heading">
    <h2 id="person-heading">Jean Martin (1850-1920)</h2>
    <!-- Contenu -->
  </article>
</main>

<footer role="contentinfo">
  <!-- Pied de page -->
</footer>
```

**Attributs ARIA requis:**

```html
<!-- Labels descriptifs -->
<button aria-label="Rechercher une personne">
  <span class="icon-search" aria-hidden="true"></span>
</button>

<!-- États dynamiques -->
<div role="alert" aria-live="polite" aria-atomic="true">
  La personne a été ajoutée avec succès
</div>

<!-- Navigation -->
<nav aria-label="Fil d'Ariane">
  <ol>
    <li><a href="/">Accueil</a></li>
    <li><a href="/persons">Personnes</a></li>
    <li aria-current="page">Jean Martin</li>
  </ol>
</nav>

<!-- Formulaires -->
<label for="first-name">Prénom *</label>
<input
  id="first-name"
  type="text"
  required
  aria-required="true"
  aria-describedby="first-name-help"
>
<span id="first-name-help" class="help-text">
  Le prénom doit contenir au moins 2 caractères
</span>
```

#### 2. **Texte Alternatif**

```html
<!-- Images significatives -->
<img
  src="/photos/jean-martin-1900.jpg"
  alt="Portrait de Jean Martin en 1900, assis devant sa maison"
>

<!-- Images décoratives -->
<img src="/decorations/border.png" alt="" role="presentation">

<!-- Graphiques et visualisations -->
<figure>
  <img
    src="/charts/family-tree.svg"
    alt="Arbre généalogique de la famille Martin sur 5 générations"
  >
  <figcaption>
    Arbre généalogique complet avec 127 personnes
  </figcaption>
</figure>

<!-- Données tabulaires alternatives -->
<table>
  <caption>Liste des descendants de Jean Martin</caption>
  <thead>
    <tr>
      <th scope="col">Nom</th>
      <th scope="col">Date de naissance</th>
      <th scope="col">Relation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Pierre Martin</th>
      <td>1875</td>
      <td>Fils</td>
    </tr>
  </tbody>
</table>
```

### Pour les Personnes Malvoyantes

#### 1. **Contrastes de Couleurs**

**Ratios minimum WCAG 2.1 AA:**
- Texte normal (< 18pt): **4.5:1**
- Texte large (≥ 18pt ou ≥ 14pt gras): **3:1**
- Composants UI et graphiques: **3:1**

**Palette de couleurs accessible:**

```css
/* Variables CSS pour contrastes élevés */
:root {
  /* Texte sur fond clair */
  --text-primary: #1a1a1a;        /* Ratio: 16.9:1 sur blanc */
  --text-secondary: #4a4a4a;      /* Ratio: 9.7:1 sur blanc */

  /* Texte sur fond sombre */
  --text-light: #ffffff;          /* Ratio: 21:1 sur noir */
  --text-light-secondary: #e0e0e0; /* Ratio: 14.6:1 sur noir */

  /* Liens et actions */
  --link-color: #0056b3;          /* Ratio: 7.5:1 sur blanc */
  --link-hover: #003d82;          /* Ratio: 10.2:1 sur blanc */

  /* Erreurs et alertes */
  --error-color: #c62828;         /* Ratio: 5.9:1 sur blanc */
  --success-color: #2e7d32;       /* Ratio: 4.6:1 sur blanc */
  --warning-color: #c77700;       /* Ratio: 4.5:1 sur blanc */

  /* Bordures et séparateurs */
  --border-color: #757575;        /* Ratio: 4.6:1 sur blanc */
}

/* Exemple d'utilisation */
body {
  color: var(--text-primary);
  background-color: #ffffff;
}

a {
  color: var(--link-color);
  text-decoration: underline; /* Important: ne pas se fier uniquement à la couleur */
}

a:hover, a:focus {
  color: var(--link-hover);
  text-decoration: underline;
  outline: 2px solid var(--link-hover);
}
```

**Vérification des contrastes:**

```bash
# Outils recommandés
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Chrome DevTools: Lighthouse Accessibility Audit
- axe DevTools (extension navigateur)
```

#### 2. **Agrandissement de Texte**

**Support du zoom jusqu'à 200%:**

```css
/* Unités relatives (rem, em) au lieu de px */
body {
  font-size: 16px; /* Base */
}

h1 {
  font-size: 2rem;    /* 32px à 100%, 64px à 200% */
}

p {
  font-size: 1rem;    /* 16px à 100%, 32px à 200% */
  line-height: 1.5;   /* 24px à 100%, 48px à 200% */
}

/* Éviter les hauteurs fixes */
.card {
  min-height: 10rem; /* Au lieu de height: 160px */
  padding: 1rem;
}

/* Responsive breakpoints pour zoom */
@media (min-width: 320px) and (max-width: 768px) {
  /* Styles mobile qui s'appliquent aussi au zoom 200% sur desktop */
}
```

#### 3. **Mode Sombre (Dark Mode)**

```css
/* Mode automatique selon préférences système */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #121212;
    --bg-secondary: #1e1e1e;
    --text-primary: #e0e0e0;
    --text-secondary: #b0b0b0;
    --link-color: #64b5f6;
  }

  body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
  }
}

/* Toggle manuel */
body.dark-mode {
  background-color: #121212;
  color: #e0e0e0;
}
```

#### 4. **Modes de Contraste Élevé**

```css
/* Support du mode contraste élevé Windows */
@media (prefers-contrast: high) {
  * {
    border-width: 2px !important;
  }

  a {
    text-decoration: underline !important;
    font-weight: bold;
  }

  button {
    border: 3px solid currentColor !important;
  }
}

/* Mode contraste personnalisé */
body.high-contrast {
  background: #000000;
  color: #ffff00;
}

body.high-contrast a {
  color: #00ffff;
  text-decoration: underline;
  font-weight: bold;
}
```

---

##  Accessibilité Auditive

### Pour les Personnes Sourdes ou Malentendantes

#### 1. **Sous-titres et Transcriptions**

**Pour le contenu vidéo:**

```html
<!-- Vidéo avec sous-titres -->
<video controls>
  <source src="/videos/tutorial.mp4" type="video/mp4">
  <track
    kind="captions"
    src="/videos/tutorial.fr.vtt"
    srclang="fr"
    label="Français"
    default
  >
  <track
    kind="captions"
    src="/videos/tutorial.en.vtt"
    srclang="en"
    label="English"
  >
  <!-- Transcription textuelle comme fallback -->
  <p>
    <a href="/videos/tutorial-transcript.html">
      Lire la transcription complète
    </a>
  </p>
</video>
```

**Format WebVTT:**

```vtt
WEBVTT

00:00:00.000 --> 00:00:04.000
Bienvenue sur AWKWARD LEGACY, votre outil de généalogie moderne.

00:00:04.000 --> 00:00:08.000
Dans ce tutoriel, nous allons apprendre à importer un fichier GEDCOM.

00:00:08.000 --> 00:00:12.000
[Clic de souris]
Commençons par cliquer sur le bouton "Importer".
```

#### 2. **Alternatives Visuelles aux Sons**

```javascript
// Notifications visuelles au lieu de sonores
function showNotification(message, type = 'info') {
  // Créer une notification visuelle
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.setAttribute('role', 'alert');
  notification.setAttribute('aria-live', 'assertive');
  notification.textContent = message;

  // Ajouter une icône visuelle
  const icon = document.createElement('span');
  icon.className = `icon icon-${type}`;
  icon.setAttribute('aria-hidden', 'true');
  notification.prepend(icon);

  // Animation et retrait
  document.body.appendChild(notification);
  setTimeout(() => notification.remove(), 5000);
}

// Utilisation
showNotification('La personne a été enregistrée avec succès', 'success');
showNotification('Erreur lors de la sauvegarde', 'error');
```

#### 3. **Indicateurs Visuels Clairs**

```html
<!-- États de chargement -->
<button
  class="btn-save"
  aria-busy="true"
  disabled
>
  <span class="spinner" aria-hidden="true"></span>
  <span>Enregistrement en cours...</span>
</button>

<!-- Erreurs de formulaire -->
<div class="form-group" aria-invalid="true">
  <label for="email">Email *</label>
  <input
    id="email"
    type="email"
    aria-invalid="true"
    aria-describedby="email-error"
  >
  <span id="email-error" class="error-message" role="alert">
     Veuillez entrer une adresse email valide
  </span>
</div>
```

---

##  Accessibilité Motrice

### Pour les Personnes avec Handicaps Moteurs

#### 1. **Navigation au Clavier**

**Ordre de tabulation logique:**

```html
<!-- tabindex=0 pour éléments personnalisés -->
<div
  class="custom-button"
  role="button"
  tabindex="0"
  onclick="handleClick()"
  onkeypress="handleKeyPress(event)"
>
  Action
</div>

<script>
function handleKeyPress(event) {
  // Activer sur Entrée ou Espace
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    handleClick();
  }
}
</script>
```

**Raccourcis clavier:**

```javascript
// Raccourcis clavier globaux
document.addEventListener('keydown', (event) => {
  // Ctrl/Cmd + K pour recherche
  if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
    event.preventDefault();
    openSearchDialog();
  }

  // Échap pour fermer les modales
  if (event.key === 'Escape') {
    closeAllModals();
  }

  // Flèches pour navigation dans les listes
  if (event.key === 'ArrowDown') {
    navigateToNextItem();
  }
});
```

**Skip links (liens d'évitement):**

```html
<body>
  <!-- Lien invisible jusqu'au focus -->
  <a href="#main-content" class="skip-link">
    Aller au contenu principal
  </a>

  <header>
    <!-- Navigation -->
  </header>

  <main id="main-content" tabindex="-1">
    <!-- Contenu principal -->
  </main>
</body>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
  text-decoration: none;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
</style>
```

#### 2. **Zones de Clic Suffisantes**

**Taille minimum: 44×44 pixels (WCAG 2.1 AA)**

```css
/* Boutons et liens */
button, a.button {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 20px;
  margin: 4px;
}

/* Checkboxes et radios */
input[type="checkbox"],
input[type="radio"] {
  width: 24px;
  height: 24px;
  cursor: pointer;
}

/* Labels cliquables */
label {
  cursor: pointer;
  padding: 8px;
  display: inline-block;
}

/* Touch targets espacés */
.button-group button {
  margin: 8px;
}
```

#### 3. **Support des Technologies d'Assistance**

```javascript
// Détection de la navigation au clavier
let isUsingKeyboard = false;

document.addEventListener('keydown', (event) => {
  if (event.key === 'Tab') {
    isUsingKeyboard = true;
    document.body.classList.add('using-keyboard');
  }
});

document.addEventListener('mousedown', () => {
  isUsingKeyboard = false;
  document.body.classList.remove('using-keyboard');
});

// Afficher les focus uniquement pour le clavier
.using-keyboard *:focus {
  outline: 3px solid #0056b3;
  outline-offset: 2px;
}
```

---

##  Accessibilité Cognitive

### Pour les Personnes avec Troubles Cognitifs

#### 1. **Clarté et Simplicité**

**Principes:**
-  Langage simple et direct
-  Phrases courtes (maximum 20 mots)
-  Une idée par paragraphe
-  Structure claire avec titres
-  Listes à puces pour énumérations

**Exemple:**

```html
<!--  Mauvais -->
<p>
  L'application AWKWARD LEGACY, qui est un système de gestion de bases
  généalogiques moderne développé en Python 3.12 avec Flask comme framework
  web, permet aux utilisateurs de gérer leurs arbres généalogiques de manière
  efficace et intuitive tout en supportant l'import et l'export de fichiers
  au format GEDCOM qui est le standard international.
</p>

<!--  Bon -->
<h2>Qu'est-ce qu'AWKWARD LEGACY ?</h2>
<p>
  AWKWARD LEGACY est un outil de généalogie moderne.
</p>

<h3>Que pouvez-vous faire ?</h3>
<ul>
  <li>Créer votre arbre généalogique</li>
  <li>Ajouter des photos et documents</li>
  <li>Importer des fichiers GEDCOM</li>
  <li>Partager avec votre famille</li>
</ul>
```

#### 2. **Messages d'Erreur Compréhensibles**

```javascript
//  Mauvais
"Error 422: Unprocessable Entity. Invalid GEDCOM syntax at line 1247."

//  Bon
function showUserFriendlyError(error) {
  const messages = {
    'gedcom_invalid': {
      title: 'Fichier non valide',
      message: 'Le fichier GEDCOM contient des erreurs.',
      action: 'Vérifiez que le fichier provient d\'un logiciel de généalogie.',
      icon: ''
    },
    'file_too_large': {
      title: 'Fichier trop volumineux',
      message: 'Le fichier dépasse la taille maximum de 10 MB.',
      action: 'Essayez de diviser votre arbre en plusieurs fichiers.',
      icon: ''
    }
  };

  const msg = messages[error.code] || {
    title: 'Une erreur est survenue',
    message: 'Veuillez réessayer dans quelques instants.',
    action: 'Si le problème persiste, contactez le support.',
    icon: ''
  };

  return `
    <div class="error-message" role="alert">
      <span class="icon">${msg.icon}</span>
      <h3>${msg.title}</h3>
      <p>${msg.message}</p>
      <p class="help-text">${msg.action}</p>
    </div>
  `;
}
```

#### 3. **Prévention des Erreurs**

```html
<!-- Confirmation avant suppression -->
<button
  onclick="confirmDelete()"
  aria-label="Supprimer la personne Jean Martin"
>
  Supprimer
</button>

<script>
function confirmDelete() {
  const confirmed = confirm(
    'Êtes-vous sûr de vouloir supprimer cette personne ?\n\n' +
    'Cette action est irréversible.\n\n' +
    'Cliquez sur OK pour confirmer ou Annuler pour revenir.'
  );

  if (confirmed) {
    deletePerson();
  }
}
</script>

<!-- Annulation d'actions -->
<div class="toast" role="alert">
  <p>La personne a été supprimée</p>
  <button onclick="undoDelete()">Annuler</button>
</div>
```

#### 4. **Aide Contextuelle**

```html
<!-- Info-bulles (tooltips) -->
<button
  aria-describedby="tooltip-export"
  onmouseenter="showTooltip('tooltip-export')"
>
  Exporter
  <span class="icon-help" aria-hidden="true">?</span>
</button>

<div
  id="tooltip-export"
  role="tooltip"
  class="tooltip"
  hidden
>
  Téléchargez votre arbre au format GEDCOM pour l'utiliser dans d'autres logiciels
</div>

<!-- Instructions étape par étape -->
<div class="wizard">
  <h2>Importer un fichier (Étape 1/3)</h2>
  <p class="step-description">
    Sélectionnez un fichier GEDCOM depuis votre ordinateur
  </p>

  <ol class="steps">
    <li aria-current="step">Choisir le fichier</li>
    <li>Vérifier les données</li>
    <li>Confirmer l'import</li>
  </ol>

  <!-- Formulaire -->
</div>
```

---

##  Standards et Conformité

### WCAG 2.1 Niveau AA

**Critères de conformité obligatoires:**

| Critère | Niveau | Description | Status |
|---------|--------|-------------|--------|
| **1.1.1** | A | Contenu non textuel |  |
| **1.3.1** | A | Information et relations |  |
| **1.4.3** | AA | Contraste minimum (4.5:1) |  |
| **1.4.4** | AA | Redimensionnement du texte |  |
| **1.4.5** | AA | Texte sous forme d'image |  |
| **2.1.1** | A | Clavier |  |
| **2.1.2** | A | Pas de piège au clavier |  |
| **2.4.3** | A | Parcours du focus |  |
| **2.4.7** | AA | Focus visible |  |
| **3.1.1** | A | Langue de la page |  |
| **3.2.3** | AA | Navigation cohérente |  |
| **3.3.1** | A | Identification des erreurs |  |
| **3.3.2** | A | Étiquettes ou instructions |  |
| **4.1.1** | A | Analyse syntaxique |  |
| **4.1.2** | A | Nom, rôle et valeur |  |

### RGAA 4.1 (France)

**Référentiel Général d'Amélioration de l'Accessibilité**

Le projet vise la conformité RGAA 4.1 niveau AA pour les services publics français.

**Déclaration d'accessibilité requise:**

```html
<!-- Footer de toutes les pages -->
<footer>
  <nav aria-label="Liens légaux">
    <ul>
      <li><a href="/mentions-legales">Mentions légales</a></li>
      <li>
        <a href="/accessibilite">
          Accessibilité : partiellement conforme
        </a>
      </li>
      <li><a href="/contact">Contact</a></li>
    </ul>
  </nav>
</footer>
```

### Section 508 (États-Unis)

Conformité avec Section 508 pour les projets gouvernementaux US.

---

##  Implémentation Technique

### Configuration Flask

```python
# lib/wserver.py - Configuration accessibilité

from flask import Flask, render_template, request
from flask_talisman import Talisman

app = Flask(__name__)

# Sécurité et accessibilité
Talisman(app,
    content_security_policy={
        'default-src': "'self'",
        'img-src': ['*', 'data:'],
        'script-src': ["'self'", "'unsafe-inline'"],
        'style-src': ["'self'", "'unsafe-inline'"]
    }
)

# Headers accessibilité
@app.after_request
def add_accessibility_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

# Template de base accessible
@app.route('/')
def index():
    return render_template('base_accessible.html',
        page_title="Accueil - AWKWARD LEGACY",
        lang="fr"
    )
```

### Template HTML de Base

```html
<!-- templates/base_accessible.html -->
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ page_title }}</title>

  <!-- Préférences utilisateur -->
  <meta name="color-scheme" content="light dark">

  <!-- CSS accessible -->
  <link rel="stylesheet" href="/static/css/accessible.css">

  <!-- Pas de zoom désactivé -->
  <!--  INTERDIT: <meta name="viewport" content="user-scalable=no"> -->
</head>

<body>
  <!-- Skip link -->
  <a href="#main-content" class="skip-link">
    Aller au contenu principal
  </a>

  <!-- Annonce des mises à jour -->
  <div
    role="region"
    aria-live="polite"
    aria-atomic="true"
    class="sr-only"
    id="announcements"
  ></div>

  <!-- Header -->
  <header role="banner">
    <h1>{{ site_name }}</h1>
    <nav role="navigation" aria-label="Navigation principale">
      {% block navigation %}{% endblock %}
    </nav>
  </header>

  <!-- Contenu principal -->
  <main id="main-content" role="main" tabindex="-1">
    <!-- Fil d'Ariane -->
    <nav aria-label="Fil d'Ariane">
      {% block breadcrumb %}{% endblock %}
    </nav>

    <!-- Contenu -->
    {% block content %}{% endblock %}
  </main>

  <!-- Footer -->
  <footer role="contentinfo">
    {% block footer %}{% endblock %}
  </footer>

  <!-- Scripts -->
  <script src="/static/js/accessibility.js"></script>
  {% block scripts %}{% endblock %}
</body>
</html>
```

### JavaScript Accessible

```javascript
// static/js/accessibility.js

/**
 * Gestionnaire d'accessibilité global
 */
class AccessibilityManager {
  constructor() {
    this.init();
  }

  init() {
    this.setupFocusManagement();
    this.setupKeyboardShortcuts();
    this.setupAriaLive();
    this.setupPreferences();
  }

  /**
   * Gestion du focus
   */
  setupFocusManagement() {
    // Piéger le focus dans les modales
    document.querySelectorAll('[role="dialog"]').forEach(modal => {
      this.trapFocus(modal);
    });

    // Retour du focus après fermeture
    document.addEventListener('modalClosed', (event) => {
      const trigger = event.detail.trigger;
      if (trigger) {
        trigger.focus();
      }
    });
  }

  trapFocus(element) {
    const focusableElements = element.querySelectorAll(
      'a[href], button:not([disabled]), textarea, input, select'
    );
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    element.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    });
  }

  /**
   * Raccourcis clavier
   */
  setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      // Ctrl/Cmd + K = Recherche
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        this.openSearch();
      }

      // Alt + H = Aide
      if (e.altKey && e.key === 'h') {
        e.preventDefault();
        this.openHelp();
      }
    });
  }

  /**
   * Annonces pour lecteurs d'écran
   */
  setupAriaLive() {
    this.announcer = document.getElementById('announcements');
  }

  announce(message, priority = 'polite') {
    if (!this.announcer) return;

    this.announcer.setAttribute('aria-live', priority);
    this.announcer.textContent = message;

    // Nettoyer après annonce
    setTimeout(() => {
      this.announcer.textContent = '';
    }, 1000);
  }

  /**
   * Préférences utilisateur
   */
  setupPreferences() {
    // Détecter les préférences système
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const prefersHighContrast = window.matchMedia('(prefers-contrast: high)');

    // Appliquer
    if (prefersDark.matches) {
      document.body.classList.add('dark-mode');
    }

    if (prefersReducedMotion.matches) {
      document.body.classList.add('reduced-motion');
    }

    if (prefersHighContrast.matches) {
      document.body.classList.add('high-contrast');
    }

    // Écouter les changements
    prefersDark.addEventListener('change', (e) => {
      document.body.classList.toggle('dark-mode', e.matches);
    });
  }
}

// Initialiser
const a11y = new AccessibilityManager();

// Export pour utilisation globale
window.a11y = a11y;
```

---

##  Tests et Validation

### Outils de Test Automatisés

#### 1. **axe DevTools**

```bash
# Installation
npm install --save-dev @axe-core/cli

# Test d'une page
axe https://localhost:5000 --tags wcag2a,wcag2aa

# Test complet du site
axe-crawler https://localhost:5000 --output results.json
```

#### 2. **Lighthouse CI**

```yaml
# .github/workflows/accessibility.yml
name: Accessibility Tests

on: [push, pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v9
        with:
          urls: |
            http://localhost:5000
            http://localhost:5000/search
            http://localhost:5000/persons/123
          uploadArtifacts: true
          temporaryPublicStorage: true
```

#### 3. **Pa11y**

```javascript
// test/accessibility.test.js
const pa11y = require('pa11y');

describe('Accessibility Tests', () => {
  test('Homepage meets WCAG 2.1 AA', async () => {
    const results = await pa11y('http://localhost:5000', {
      standard: 'WCAG2AA',
      includeWarnings: true
    });

    expect(results.issues.length).toBe(0);
  });
});
```

### Tests Manuels Essentiels

#### 1. **Navigation au Clavier**

**Checklist:**
- [ ] Tous les éléments interactifs sont atteignables avec Tab
- [ ] L'ordre de tabulation est logique
- [ ] Le focus est toujours visible
- [ ] Échap ferme les modales et menus
- [ ] Entrée active les boutons
- [ ] Espace active les checkboxes

#### 2. **Tests avec Lecteur d'Écran**

**Procédure NVDA (Windows):**

```
1. Installer NVDA (gratuit): https://www.nvaccess.org/
2. Lancer NVDA
3. Naviguer sur le site avec:
   - Tab: Élément suivant
   - Shift+Tab: Élément précédent
   - H: Titre suivant
   - Shift+H: Titre précédent
   - K: Lien suivant
   - B: Bouton suivant

4. Vérifier que:
   - Tous les éléments sont annoncés
   - Les labels sont compréhensibles
   - Les changements dynamiques sont annoncés
   - Les erreurs sont identifiables
```

**Procédure VoiceOver (macOS):**

```
1. Activer VoiceOver: Cmd+F5
2. Naviguer avec:
   - VO+→: Élément suivant
   - VO+←: Élément précédent
   - VO+H: Menu des titres
   - VO+U: Rotor (navigation rapide)

3. Vérifier l'accessibilité comme ci-dessus
```

#### 3. **Tests de Contraste**

```bash
# Outils en ligne
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Contrast Ratio: https://contrast-ratio.com/

# Extensions navigateur
- WAVE (Chrome, Firefox)
- axe DevTools (Chrome, Firefox, Edge)
```

#### 4. **Tests de Zoom**

**Procédure:**

```
1. Zoomer à 200%: Ctrl/Cmd + (+)
2. Vérifier que:
   - Tout le contenu reste visible
   - Pas de défilement horizontal
   - Les textes ne se chevauchent pas
   - Les boutons restent cliquables

3. Tester aussi:
   - Zoom 150%
   - Zoom 300%
   - Zoom texte seul (Firefox)
```

---

##  Checklist de Conformité

### Avant Chaque Release

#### Contenu

- [ ] Tous les textes sont en français correct
- [ ] Pas de jargon technique non expliqué
- [ ] Toutes les images ont un alt text
- [ ] Les vidéos ont des sous-titres
- [ ] Les documents PDF sont accessibles

#### Structure

- [ ] Hiérarchie de titres correcte (H1→H2→H3)
- [ ] Balises sémantiques HTML5 utilisées
- [ ] Landmarks ARIA présents (banner, main, navigation, contentinfo)
- [ ] Langue déclarée: `<html lang="fr">`

#### Navigation

- [ ] Skip link fonctionnel
- [ ] Navigation possible au clavier complet
- [ ] Ordre de tabulation logique
- [ ] Focus toujours visible
- [ ] Pas de piège au clavier

#### Visuels

- [ ] Contrastes ≥ 4.5:1 (texte normal)
- [ ] Contrastes ≥ 3:1 (texte large, UI)
- [ ] Information non véhiculée uniquement par la couleur
- [ ] Texte redimensionnable jusqu'à 200%
- [ ] Mode sombre disponible

#### Formulaires

- [ ] Tous les champs ont un label
- [ ] Erreurs clairement identifiées
- [ ] Messages d'aide disponibles
- [ ] Validation côté client ET serveur

#### Multimédia

- [ ] Sous-titres pour toutes les vidéos
- [ ] Transcriptions disponibles
- [ ] Contrôles accessibles au clavier
- [ ] Pas de lecture automatique

#### Tests

- [ ] Tests automatisés axe/Pa11y passent
- [ ] Test manuel au clavier OK
- [ ] Test avec NVDA/VoiceOver OK
- [ ] Test de zoom à 200% OK
- [ ] Score Lighthouse ≥ 90

---

##  Ressources et Formation

### Documentation Officielle

- **WCAG 2.1:** https://www.w3.org/WAI/WCAG21/quickref/
- **RGAA 4.1:** https://accessibilite.numerique.gouv.fr/
- **ARIA Authoring Practices:** https://www.w3.org/WAI/ARIA/apg/

### Outils

- **axe DevTools:** https://www.deque.com/axe/devtools/
- **WAVE:** https://wave.webaim.org/
- **Color Contrast Analyzer:** https://www.tpgi.com/color-contrast-checker/
- **NVDA:** https://www.nvaccess.org/

### Formation

- **WebAIM:** https://webaim.org/training/
- **Deque University:** https://dequeuniversity.com/
- **A11ycasts (Google):** https://www.youtube.com/playlist?list=PLNYkxOF6rcICWx0C9LVWWVqvHlYJyqw7g

### Communauté

- **A11Y Project:** https://www.a11yproject.com/
- **24 Jours de Web:** https://www.24joursdeweb.fr/
- **AccessiWeb:** https://accessiweb.org/

---

##  Contact et Support

### Signaler un Problème d'Accessibilité

Si vous rencontrez un problème d'accessibilité sur AWKWARD LEGACY:

**Email:** accessibility@awkward-legacy.com
**Formulaire:** https://awkward-legacy.com/contact-accessibilite
**Temps de réponse:** 5 jours ouvrés maximum

### Demander une Assistance

Nous proposons:
- Démonstrations personnalisées
- Formation à l'utilisation avec technologies d'assistance
- Formats alternatifs (DAISY, Braille, audio)

---

**Date de dernière mise à jour:** 30 Octobre 2025
**Version du document:** 1.0
**Prochaine révision:** Janvier 2026

 **AWKWARD LEGACY - Accessible pour tous**
