"""
Tests pour le calculateur de consanguinité
"""

import pytest
import sys
import os

# Ajouter le chemin des modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

from consanguinity import ConsanguinityCalculator


class TestConsanguinityCalculator:
    """Tests du calculateur de consanguinité"""

    def setup_method(self):
        """Setup avant chaque test"""
        # Créer une famille de test
        self.persons = {
            'I1': {'id': 'I1', 'first_name': 'Grand-Père'},
            'I2': {'id': 'I2', 'first_name': 'Grand-Mère'},
            'I3': {'id': 'I3', 'first_name': 'Père', 'father_id': 'I1', 'mother_id': 'I2'},
            'I4': {'id': 'I4', 'first_name': 'Mère', 'father_id': 'I1', 'mother_id': 'I2'},
            'I5': {'id': 'I5', 'first_name': 'Enfant', 'father_id': 'I3', 'mother_id': 'I4'},
        }
        self.calc = ConsanguinityCalculator(self.persons)

    def test_kinship_same_person(self):
        """Test coefficient de parenté pour la même personne"""
        kinship = self.calc.calculate_kinship('I1', 'I1')
        assert kinship == 0.5  # φ(i,i) = 0.5 pour une personne non consanguine

    def test_kinship_parent_child(self):
        """Test coefficient de parenté parent-enfant"""
        kinship = self.calc.calculate_kinship('I1', 'I3')
        assert kinship == 0.25  # Parent-enfant = 0.25

    def test_kinship_siblings(self):
        """Test coefficient de parenté entre frères/sœurs"""
        kinship = self.calc.calculate_kinship('I3', 'I4')
        assert kinship == 0.25  # Frères/sœurs = 0.25

    def test_kinship_unrelated(self):
        """Test coefficient de parenté entre personnes non apparentées"""
        kinship = self.calc.calculate_kinship('I1', 'I2')
        assert kinship == 0.0  # Non apparentés = 0

    def test_consanguinity_child_of_siblings(self):
        """Test consanguinité d'un enfant de frères/sœurs"""
        consang = self.calc.calculate_consanguinity('I5')
        # F = φ(père, mère) = φ(I3, I4) = 0.25
        assert abs(consang - 0.25) < 0.001

    def test_consanguinity_normal_person(self):
        """Test consanguinité d'une personne normale"""
        consang = self.calc.calculate_consanguinity('I3')
        assert consang == 0.0  # Parents non apparentés

    def test_get_relationship_degree_parent_child(self):
        """Test degré de parenté parent-enfant"""
        degree = self.calc.get_relationship_degree('I1', 'I3')
        assert degree == (1, 0)  # 1 génération en descendant

    def test_get_relationship_degree_siblings(self):
        """Test degré de parenté frères/sœurs"""
        degree = self.calc.get_relationship_degree('I3', 'I4')
        assert degree == (1, 1)  # Même génération depuis l'ancêtre commun

    def test_find_common_ancestors(self):
        """Test recherche d'ancêtres communs"""
        ancestors = self.calc.find_common_ancestors('I3', 'I4')
        assert 'I1' in ancestors
        assert 'I2' in ancestors

    def test_find_common_ancestors_none(self):
        """Test recherche d'ancêtres communs (aucun)"""
        ancestors = self.calc.find_common_ancestors('I1', 'I2')
        assert len(ancestors) == 0

    def test_get_relationship_name_same_person(self):
        """Test nom de relation pour la même personne"""
        name = self.calc.get_relationship_name('I1', 'I1')
        assert name == "même personne"

    def test_get_relationship_name_siblings(self):
        """Test nom de relation frères/sœurs"""
        name = self.calc.get_relationship_name('I3', 'I4')
        assert "frères/sœurs" in name

    def test_get_relationship_name_unrelated(self):
        """Test nom de relation non apparentés"""
        name = self.calc.get_relationship_name('I1', 'I2')
        assert "aucune relation" in name

    def test_analyze_population_consanguinity(self):
        """Test analyse de la population"""
        stats = self.calc.analyze_population_consanguinity()

        assert stats['total_persons'] == 5
        assert stats['consanguinous_persons'] == 1  # I5
        assert stats['consanguinity_rate'] > 0
        assert stats['max_consanguinity'] > 0

    def test_cousins_kinship(self):
        """Test coefficient de parenté entre cousins"""
        # Ajouter des cousins
        persons = {
            'GP1': {},
            'GP2': {},
            'P1': {'father_id': 'GP1', 'mother_id': 'GP2'},
            'P2': {'father_id': 'GP1', 'mother_id': 'GP2'},
            'C1': {'father_id': 'P1'},
            'C2': {'father_id': 'P2'},
        }
        calc = ConsanguinityCalculator(persons)

        kinship = calc.calculate_kinship('C1', 'C2')
        # Cousins germains = 0.0625
        assert abs(kinship - 0.0625) < 0.001


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
