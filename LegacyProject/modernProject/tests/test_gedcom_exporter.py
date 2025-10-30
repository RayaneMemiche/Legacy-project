"""
Tests pour l'exporteur GEDCOM
"""

import pytest
import sys
import os

# Ajouter le chemin des modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

from gedcom_exporter import GedcomExporter


class TestGedcomExporter:
    """Tests de l'exporteur GEDCOM"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.exporter = GedcomExporter(source="Test Suite")

    def test_export_simple_person(self):
        """Test export d'une personne simple"""
        persons = [
            {
                'id': 'I1',
                'first_name': 'John',
                'last_name': 'Doe',
                'gender': 'M',
                'birth_date': '1950-01-01',
                'birth_place': 'New York, USA'
            }
        ]

        gedcom = self.exporter.export_to_string(persons, [])

        assert "@I1@ INDI" in gedcom
        assert "NAME John /Doe/" in gedcom
        assert "SEX M" in gedcom
        assert "BIRT" in gedcom
        assert "DATE 1 JAN 1950" in gedcom
        assert "PLAC New York, USA" in gedcom

    def test_export_family(self):
        """Test export d'une famille"""
        persons = [
            {'id': 'I1', 'first_name': 'Father', 'last_name': 'Doe', 'gender': 'M'},
            {'id': 'I2', 'first_name': 'Mother', 'last_name': 'Smith', 'gender': 'F'},
            {'id': 'I3', 'first_name': 'Child', 'last_name': 'Doe', 'gender': 'M'}
        ]

        families = [
            {
                'id': 'F1',
                'father_id': 'I1',
                'mother_id': 'I2',
                'children_ids': ['I3'],
                'marriage_date': '1945-06-15',
                'marriage_place': 'London, UK'
            }
        ]

        gedcom = self.exporter.export_to_string(persons, families)

        assert "@F1@ FAM" in gedcom
        assert "HUSB @I1@" in gedcom
        assert "WIFE @I2@" in gedcom
        assert "CHIL @I3@" in gedcom
        assert "MARR" in gedcom
        assert "DATE 15 JUN 1945" in gedcom
        assert "PLAC London, UK" in gedcom

    def test_export_header(self):
        """Test de l'en-tête GEDCOM"""
        gedcom = self.exporter.export_to_string([], [])

        assert "0 HEAD" in gedcom
        assert "SOUR Test Suite" in gedcom
        assert "GEDC" in gedcom
        assert "VERS 5.5.1" in gedcom
        assert "CHAR UTF-8" in gedcom

    def test_export_trailer(self):
        """Test du pied de page GEDCOM"""
        gedcom = self.exporter.export_to_string([], [])

        assert "0 TRLR" in gedcom
        assert gedcom.strip().endswith("TRLR")

    def test_format_date_iso(self):
        """Test formatage de dates ISO"""
        test_cases = [
            ("1950-01-01", "1 JAN 1950"),
            ("2020-12-31", "31 DEC 2020"),
            ("1975-07-15", "15 JUL 1975"),
        ]

        for iso_date, expected_gedcom in test_cases:
            result = self.exporter._format_date(iso_date)
            assert result == expected_gedcom

    def test_format_date_gedcom_passthrough(self):
        """Test que les dates déjà en format GEDCOM passent inchangées"""
        test_cases = [
            "1 JAN 1950",
            "JAN 1950",
            "ABT 1950",
        ]

        for gedcom_date in test_cases:
            result = self.exporter._format_date(gedcom_date)
            assert result == gedcom_date

    def test_export_person_with_death(self):
        """Test export d'une personne avec décès"""
        persons = [
            {
                'id': 'I1',
                'first_name': 'John',
                'last_name': 'Doe',
                'death_date': '2020-12-31',
                'death_place': 'Paris, France'
            }
        ]

        gedcom = self.exporter.export_to_string(persons, [])

        assert "DEAT" in gedcom
        assert "DATE 31 DEC 2020" in gedcom
        assert "PLAC Paris, France" in gedcom

    def test_export_multiple_persons(self):
        """Test export de plusieurs personnes"""
        persons = [
            {'id': 'I1', 'first_name': 'John', 'last_name': 'Doe'},
            {'id': 'I2', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'id': 'I3', 'first_name': 'Bob', 'last_name': 'Johnson'}
        ]

        gedcom = self.exporter.export_to_string(persons, [])

        assert "@I1@ INDI" in gedcom
        assert "@I2@ INDI" in gedcom
        assert "@I3@ INDI" in gedcom

    def test_export_occupation(self):
        """Test export de la profession"""
        persons = [
            {
                'id': 'I1',
                'first_name': 'John',
                'last_name': 'Doe',
                'occupation': 'Engineer'
            }
        ]

        gedcom = self.exporter.export_to_string(persons, [])

        assert "OCCU Engineer" in gedcom

    def test_export_notes(self):
        """Test export des notes"""
        persons = [
            {
                'id': 'I1',
                'first_name': 'John',
                'last_name': 'Doe',
                'notes': ['First note', 'Second note']
            }
        ]

        gedcom = self.exporter.export_to_string(persons, [])

        assert "NOTE First note" in gedcom
        assert "NOTE Second note" in gedcom


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
