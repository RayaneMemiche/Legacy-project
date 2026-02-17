"""
Tests d'accessibilité WCAG 2.1 AA - AWKWARD LEGACY

Vérifie la conformité du frontend aux normes d'accessibilité WCAG 2.1
niveau AA, conformément à la stratégie d'assurance qualité (C28.2).

Catégories testées :
- Structure sémantique HTML5
- Navigation clavier (skip links, tabindex, focus)
- Attributs ARIA
- Formulaires accessibles
- Contrastes de couleurs
- Préférences utilisateur (reduced-motion, high-contrast)
- Langue de la page
- Lecteurs d'écran
"""

import os
import re
import unittest


def _read_file(filename):
    """Lit un fichier frontend par son nom."""
    base_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "frontend"
    )
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        # Essayer un chemin alternatif
        alt_dir = os.path.join(
            os.path.dirname(__file__), "..", "frontend"
        )
        filepath = os.path.join(alt_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def _find_frontend_dir():
    """Trouve le répertoire frontend."""
    base = os.path.dirname(__file__)
    candidates = [
        os.path.join(base, "..", "..", "frontend"),
        os.path.join(base, "..", "frontend"),
    ]
    for c in candidates:
        if os.path.isdir(c):
            return os.path.abspath(c)
    return None


class TestHTMLSemanticStructure(unittest.TestCase):
    """Tests de structure sémantique HTML5 (WCAG 1.3.1)."""

    @classmethod
    def setUpClass(cls):
        cls.html = _read_file("index_new.html")

    def test_has_lang_attribute(self):
        """WCAG 3.1.1 : La page déclare une langue."""
        self.assertRegex(
            self.html,
            r'<html\s[^>]*lang="[a-z]{2}"',
            "L'attribut lang doit être présent sur <html>",
        )

    def test_lang_is_french(self):
        """La langue déclarée est le français."""
        self.assertIn('lang="fr"', self.html)

    def test_has_main_element(self):
        """WCAG 1.3.1 : Un élément <main> est présent."""
        self.assertRegex(
            self.html,
            r"<main[\s>]",
            "L'élément <main> doit être présent pour le contenu principal",
        )

    def test_has_header_element(self):
        """WCAG 1.3.1 : Un élément <header> est présent."""
        self.assertRegex(
            self.html,
            r"<header[\s>]",
            "L'élément <header> doit être présent",
        )

    def test_has_footer_element(self):
        """WCAG 1.3.1 : Un élément <footer> est présent."""
        self.assertRegex(
            self.html,
            r"<footer[\s>]",
            "L'élément <footer> doit être présent",
        )

    def test_has_nav_element(self):
        """WCAG 1.3.1 : Un élément <nav> est présent."""
        self.assertRegex(
            self.html,
            r"<nav[\s>]",
            "L'élément <nav> doit être présent pour la navigation",
        )

    def test_nav_has_aria_label(self):
        """WCAG 1.3.1 : La navigation a un label ARIA."""
        self.assertRegex(
            self.html,
            r'<nav[^>]*aria-label="[^"]+"',
            "L'élément <nav> doit avoir un aria-label",
        )

    def test_has_section_or_article_elements(self):
        """WCAG 1.3.1 : Des éléments <section> ou <article> sont utilisés."""
        has_section = re.search(r"<section[\s>]", self.html)
        has_article = re.search(r"<article[\s>]", self.html)
        self.assertTrue(
            has_section or has_article,
            "Des éléments <section> ou <article> doivent être utilisés",
        )

    def test_heading_hierarchy(self):
        """WCAG 1.3.1 : La hiérarchie des titres est correcte (h1 avant h2, etc.)."""
        headings = re.findall(r"<h([1-6])", self.html)
        if headings:
            # Le premier heading doit être h1
            self.assertEqual(
                headings[0], "1",
                "Le premier titre de la page doit être un <h1>",
            )

    def test_has_viewport_meta(self):
        """WCAG 1.4.4 : Le viewport est configuré sans bloquer le zoom."""
        self.assertIn("viewport", self.html)
        # Vérifier qu'il n'y a pas de maximum-scale=1 ou user-scalable=no
        viewport_match = re.search(
            r'<meta[^>]*name="viewport"[^>]*content="([^"]*)"', self.html
        )
        if viewport_match:
            content = viewport_match.group(1)
            self.assertNotIn(
                "user-scalable=no", content,
                "Le zoom ne doit pas être désactivé (user-scalable=no)",
            )


class TestSkipLinks(unittest.TestCase):
    """Tests de navigation par skip links (WCAG 2.4.1)."""

    @classmethod
    def setUpClass(cls):
        cls.html = _read_file("index_new.html")

    def test_skip_link_exists(self):
        """WCAG 2.4.1 : Un lien 'Aller au contenu principal' existe."""
        self.assertRegex(
            self.html,
            r'<a[^>]*href="#main-content"[^>]*class="skip-link"',
            "Un skip link vers le contenu principal doit exister",
        )

    def test_skip_link_target_exists(self):
        """Le target du skip link existe dans la page."""
        self.assertRegex(
            self.html,
            r'id="main-content"',
            "L'élément cible du skip link (id='main-content') doit exister",
        )


class TestARIAAttributes(unittest.TestCase):
    """Tests des attributs ARIA (WCAG 4.1.2)."""

    @classmethod
    def setUpClass(cls):
        cls.html = _read_file("index_new.html")

    def test_icons_have_aria_hidden(self):
        """WCAG 1.1.1 : Les icônes décoratives sont masquées aux lecteurs d'écran."""
        # Trouver les icônes Bootstrap Icons
        icons = re.findall(r'<i\s+class="bi\s[^"]*"[^>]*>', self.html)
        icons_without_aria = [
            icon for icon in icons if 'aria-hidden="true"' not in icon
        ]
        self.assertEqual(
            len(icons_without_aria), 0,
            f"{len(icons_without_aria)} icône(s) sans aria-hidden='true': "
            f"{icons_without_aria[:3]}",
        )

    def test_dropdown_has_aria_expanded(self):
        """WCAG 4.1.2 : Les dropdowns ont aria-expanded."""
        dropdowns = re.findall(r'<a[^>]*dropdown-toggle[^>]*>', self.html)
        for dropdown in dropdowns:
            self.assertIn(
                "aria-expanded",
                dropdown,
                f"Le dropdown doit avoir aria-expanded: {dropdown[:80]}",
            )

    def test_dropdown_has_aria_haspopup(self):
        """WCAG 4.1.2 : Les dropdowns ont aria-haspopup."""
        dropdowns = re.findall(r'<a[^>]*dropdown-toggle[^>]*>', self.html)
        for dropdown in dropdowns:
            self.assertIn(
                "aria-haspopup",
                dropdown,
                f"Le dropdown doit avoir aria-haspopup: {dropdown[:80]}",
            )

    def test_toast_container_has_aria_live(self):
        """WCAG 4.1.3 : Le container de notifications a aria-live."""
        self.assertRegex(
            self.html,
            r'id="toast-container"[^>]*aria-live="polite"',
            "Le toast container doit avoir aria-live='polite'",
        )

    def test_loading_spinner_has_role_status(self):
        """WCAG 4.1.3 : Le spinner de chargement a role='status'."""
        self.assertRegex(
            self.html,
            r'spinner-border[^>]*role="status"',
            "Le spinner doit avoir role='status'",
        )

    def test_dynamic_pages_have_aria_label(self):
        """WCAG 1.3.1 : Les pages dynamiques ont des labels ARIA."""
        pages = re.findall(r'<div\s+id="\w+Page"[^>]*>', self.html)
        for page in pages:
            self.assertIn(
                "aria-label",
                page,
                f"La page dynamique doit avoir un aria-label: {page[:80]}",
            )

    def test_main_has_role(self):
        """WCAG 1.3.1 : L'élément main a le rôle approprié."""
        self.assertRegex(
            self.html,
            r'<main[^>]*role="main"',
            "L'élément <main> doit avoir role='main'",
        )


class TestFormAccessibility(unittest.TestCase):
    """Tests d'accessibilité des formulaires (WCAG 1.3.1, 3.3.2)."""

    @classmethod
    def setUpClass(cls):
        cls.html = _read_file("index_new.html")

    def test_search_form_has_role_search(self):
        """WCAG 1.3.1 : Le formulaire de recherche a role='search'."""
        self.assertRegex(
            self.html,
            r'<form[^>]*role="search"',
            "Le formulaire de recherche doit avoir role='search'",
        )

    def test_search_input_has_label(self):
        """WCAG 1.3.1 : Le champ de recherche a un label (visible ou masqué)."""
        # Chercher un label for="quickSearchInput" ou un aria-label
        has_label = re.search(
            r'for="quickSearchInput"', self.html
        )
        has_aria_label = re.search(
            r'id="quickSearchInput"[^>]*aria-label', self.html
        )
        self.assertTrue(
            has_label or has_aria_label,
            "Le champ de recherche doit avoir un label associé",
        )

    def test_buttons_have_accessible_names(self):
        """WCAG 4.1.2 : Les boutons de feature cards ont des noms accessibles."""
        # Chercher les boutons avec data-page qui ont un aria-label
        buttons = re.findall(
            r'<button[^>]*data-page="[^"]*"[^>]*>', self.html
        )
        for button in buttons:
            self.assertIn(
                "aria-label",
                button,
                f"Le bouton doit avoir un aria-label: {button[:80]}",
            )


class TestCSSAccessibility(unittest.TestCase):
    """Tests d'accessibilité CSS (WCAG 1.4, 2.3)."""

    @classmethod
    def setUpClass(cls):
        cls.css = _read_file("styles.css")

    def test_focus_styles_exist(self):
        """WCAG 2.4.7 : Des styles de focus sont définis."""
        self.assertIn(
            ":focus",
            self.css,
            "Des styles :focus doivent être définis",
        )

    def test_focus_not_removed(self):
        """WCAG 2.4.7 : Le focus n'est pas supprimé globalement."""
        # Vérifier qu'il n'y a pas de *:focus { outline: none }
        global_outline_none = re.search(
            r"\*\s*:\s*focus\s*\{[^}]*outline\s*:\s*none", self.css
        )
        self.assertIsNone(
            global_outline_none,
            "Le focus outline ne doit pas être supprimé globalement",
        )

    def test_sr_only_class_exists(self):
        """Une classe .sr-only est définie pour le contenu réservé aux lecteurs d'écran."""
        self.assertIn(
            ".sr-only",
            self.css,
            "La classe .sr-only doit être définie",
        )

    def test_skip_link_styles_exist(self):
        """WCAG 2.4.1 : Les styles de skip links sont définis."""
        self.assertIn(
            ".skip-link",
            self.css,
            "Les styles .skip-link doivent être définis",
        )

    def test_prefers_reduced_motion(self):
        """WCAG 2.3.3 : Le support prefers-reduced-motion est implémenté."""
        self.assertIn(
            "prefers-reduced-motion",
            self.css,
            "Le support @media (prefers-reduced-motion: reduce) doit être implémenté",
        )

    def test_prefers_contrast_high(self):
        """WCAG 1.4.11 : Le support prefers-contrast: high est implémenté."""
        self.assertIn(
            "prefers-contrast",
            self.css,
            "Le support @media (prefers-contrast: high) doit être implémenté",
        )

    def test_print_styles_exist(self):
        """Des styles d'impression sont définis."""
        self.assertIn(
            "@media print",
            self.css,
            "Des styles @media print doivent être définis",
        )

    def test_dark_mode_support(self):
        """WCAG 1.4.3 : Le mode sombre est supporté."""
        self.assertIn(
            "prefers-color-scheme: dark",
            self.css,
            "Le support @media (prefers-color-scheme: dark) doit être implémenté",
        )

    def test_color_contrast_variables(self):
        """WCAG 1.4.3 : Les variables de couleurs sont définies."""
        self.assertIn("--primary-color", self.css)
        self.assertIn("--danger-color", self.css)
        self.assertIn("--success-color", self.css)


class TestKeyboardNavigation(unittest.TestCase):
    """Tests de navigation clavier (WCAG 2.1.1)."""

    @classmethod
    def setUpClass(cls):
        cls.html = _read_file("index_new.html")

    def test_navbar_toggler_has_aria_controls(self):
        """WCAG 4.1.2 : Le toggler navbar a aria-controls."""
        self.assertRegex(
            self.html,
            r'navbar-toggler[^>]*aria-controls="[^"]+"',
            "Le toggler navbar doit avoir aria-controls",
        )

    def test_navbar_toggler_has_aria_expanded(self):
        """WCAG 4.1.2 : Le toggler navbar a aria-expanded."""
        self.assertRegex(
            self.html,
            r'navbar-toggler[^>]*aria-expanded="[^"]+"',
            "Le toggler navbar doit avoir aria-expanded",
        )

    def test_navbar_toggler_has_aria_label(self):
        """WCAG 4.1.2 : Le toggler navbar a un aria-label."""
        self.assertRegex(
            self.html,
            r'navbar-toggler[^>]*aria-label="[^"]+"',
            "Le toggler navbar doit avoir un aria-label",
        )

    def test_no_positive_tabindex(self):
        """WCAG 2.4.3 : Pas de tabindex positif (perturbe l'ordre naturel)."""
        positive_tabindex = re.findall(
            r'tabindex="([1-9]\d*)"', self.html
        )
        self.assertEqual(
            len(positive_tabindex), 0,
            f"Pas de tabindex positif autorisé, trouvés: {positive_tabindex}",
        )


class TestScreenReaderSupport(unittest.TestCase):
    """Tests de support des lecteurs d'écran (WCAG 4.1)."""

    @classmethod
    def setUpClass(cls):
        cls.html = _read_file("index_new.html")

    def test_visually_hidden_on_spinner(self):
        """WCAG 1.1.1 : Le spinner a du texte masqué pour les lecteurs d'écran."""
        self.assertIn(
            "visually-hidden",
            self.html,
            "La classe visually-hidden doit être utilisée pour le spinner",
        )

    def test_footer_has_role_contentinfo(self):
        """WCAG 1.3.1 : Le footer a le rôle approprié."""
        self.assertRegex(
            self.html,
            r'<footer[^>]*role="contentinfo"',
            "Le footer doit avoir role='contentinfo'",
        )

    def test_stat_cards_have_aria_labels(self):
        """WCAG 1.1.1 : Les cartes statistiques ont des labels ARIA."""
        stat_cards = re.findall(
            r'<div[^>]*class="stat-card[^"]*"[^>]*>', self.html
        )
        for card in stat_cards:
            self.assertIn(
                "aria-label",
                card,
                f"Stat card doit avoir un aria-label: {card[:80]}",
            )


class TestAccessibilityComplianceSummary(unittest.TestCase):
    """Test de synthèse : vérifie le score global d'accessibilité."""

    @classmethod
    def setUpClass(cls):
        cls.html = _read_file("index_new.html")
        cls.css = _read_file("styles.css")

    def test_wcag_checklist(self):
        """Vérifie que les critères WCAG 2.1 AA essentiels sont respectés."""
        checks = {
            "lang attribute": bool(re.search(r'lang="fr"', self.html)),
            "main element": bool(re.search(r"<main[\s>]", self.html)),
            "header element": bool(re.search(r"<header[\s>]", self.html)),
            "footer element": bool(re.search(r"<footer[\s>]", self.html)),
            "nav element": bool(re.search(r"<nav[\s>]", self.html)),
            "skip link": bool(re.search(r"skip-link", self.html)),
            "aria-live region": bool(re.search(r"aria-live", self.html)),
            "focus styles": bool(re.search(r":focus", self.css)),
            "sr-only class": bool(re.search(r"\.sr-only", self.css)),
            "reduced motion": bool(
                re.search(r"prefers-reduced-motion", self.css)
            ),
            "high contrast": bool(
                re.search(r"prefers-contrast", self.css)
            ),
            "dark mode": bool(
                re.search(r"prefers-color-scheme", self.css)
            ),
            "print styles": bool(re.search(r"@media print", self.css)),
            "viewport meta": bool(re.search(r"viewport", self.html)),
        }

        passed = sum(1 for v in checks.values() if v)
        total = len(checks)
        score = (passed / total) * 100

        # Afficher le rapport
        print(f"\n{'='*60}")
        print(f"  RAPPORT D'ACCESSIBILITÉ WCAG 2.1 AA")
        print(f"{'='*60}")
        for name, passed_check in checks.items():
            status = "PASS" if passed_check else "FAIL"
            print(f"  [{status}] {name}")
        print(f"{'='*60}")
        print(f"  Score: {passed}/{total} ({score:.1f}%)")
        print(f"{'='*60}\n")

        # Le score doit être d'au moins 75%
        self.assertGreaterEqual(
            score, 75,
            f"Score d'accessibilité insuffisant: {score:.1f}% (minimum 75%)",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
