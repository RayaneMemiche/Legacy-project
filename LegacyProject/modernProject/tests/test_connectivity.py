"""
Tests pour l'analyseur de connectivité
"""

import pytest
import sys
import os

# Ajouter le chemin des modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

from connectivity import ConnectivityAnalyzer


class TestConnectivityAnalyzer:
    """Tests de l'analyseur de connectivité"""

    def setup_method(self):
        """Setup avant chaque test"""
        # Créer 3 familles distinctes
        self.persons = {
            # Famille 1
            'F1_P1': {'id': 'F1_P1'},
            'F1_P2': {'id': 'F1_P2'},
            'F1_P3': {'id': 'F1_P3', 'father_id': 'F1_P1', 'mother_id': 'F1_P2'},
            'F1_P4': {'id': 'F1_P4', 'father_id': 'F1_P1', 'mother_id': 'F1_P2'},

            # Famille 2
            'F2_P1': {'id': 'F2_P1'},
            'F2_P2': {'id': 'F2_P2'},
            'F2_P3': {'id': 'F2_P3', 'father_id': 'F2_P1', 'mother_id': 'F2_P2'},

            # Personne isolée
            'ISO1': {'id': 'ISO1'},
        }

        self.families = {
            'FAM1': {'id': 'FAM1', 'father_id': 'F1_P1', 'mother_id': 'F1_P2'},
            'FAM2': {'id': 'FAM2', 'father_id': 'F2_P1', 'mother_id': 'F2_P2'},
        }

        self.analyzer = ConnectivityAnalyzer(self.persons, self.families)

    def test_find_connected_components(self):
        """Test recherche de composantes connexes"""
        components = self.analyzer.find_connected_components()

        # Devrait trouver 3 composantes (2 familles + 1 isolé)
        assert len(components) == 3

        # La plus grande composante devrait avoir 4 personnes
        assert len(components[0]) == 4

    def test_get_component(self):
        """Test obtention de la composante d'une personne"""
        component = self.analyzer.get_component('F1_P3')

        assert component is not None
        assert len(component) == 4
        assert all(pid in component for pid in ['F1_P1', 'F1_P2', 'F1_P3', 'F1_P4'])

    def test_find_isolated_persons(self):
        """Test recherche de personnes isolées"""
        isolated = self.analyzer.find_isolated_persons()

        assert len(isolated) == 1
        assert 'ISO1' in isolated

    def test_get_component_statistics(self):
        """Test statistiques des composantes"""
        stats = self.analyzer.get_component_statistics()

        assert stats['total_persons'] == 8
        assert stats['num_components'] == 3
        assert stats['num_isolated'] == 1
        assert stats['largest_component_size'] == 4
        assert stats['smallest_component_size'] == 1

    def test_component_with_marriage(self):
        """Test que les mariages connectent les personnes"""
        # F1_P1 et F1_P2 doivent être dans la même composante via le mariage
        comp1 = self.analyzer.get_component('F1_P1')
        comp2 = self.analyzer.get_component('F1_P2')

        assert comp1 == comp2

    def test_get_component_info(self):
        """Test informations détaillées sur une composante"""
        component = self.analyzer.get_component('F1_P1')
        info = self.analyzer.get_component_info(component)

        assert info['size'] == 4
        assert info['num_roots'] > 0  # Au moins un fondateur
        assert 'estimated_generations' in info

    def test_single_person_component(self):
        """Test composante avec une seule personne"""
        component = self.analyzer.get_component('ISO1')

        assert component is not None
        assert len(component) == 1
        assert 'ISO1' in component

    def test_component_size_distribution(self):
        """Test distribution des tailles de composantes"""
        stats = self.analyzer.get_component_statistics()
        dist = stats['component_size_distribution']

        # Vérifier que la distribution contient bien toutes les catégories
        assert 'very_small (1-5)' in dist
        assert 'small (6-20)' in dist
        assert 'medium (21-100)' in dist

    def test_empty_persons(self):
        """Test avec une base vide"""
        analyzer = ConnectivityAnalyzer({}, {})
        components = analyzer.find_connected_components()

        assert len(components) == 0

    def test_graph_building(self):
        """Test construction du graphe"""
        # Vérifier que le graphe est bien bidirectionnel
        assert 'F1_P1' in self.analyzer.graph['F1_P3']
        assert 'F1_P3' in self.analyzer.graph['F1_P1']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
