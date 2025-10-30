"""
Tests pour le parser GEDCOM
"""

import pytest
import sys
import os

# Ajouter le chemin des modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

from gedcom_parser import GedcomParser, GedcomPerson, GedcomFamily


class TestGedcomParser:
    """Tests du parser GEDCOM"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.parser = GedcomParser()

    def test_parse_simple_person(self):
        """Test parsing d'une personne simple"""
        gedcom = """
0 @I1@ INDI
1 NAME John /Doe/
1 SEX M
1 BIRT
2 DATE 1 JAN 1950
2 PLAC New York, USA
"""
        persons, families = self.parser.parse_string(gedcom)

        assert len(persons) == 1
        assert 'I1' in persons

        person = persons['I1']
        assert person.first_name == "John"
        assert person.last_name == "Doe"
        assert person.gender == "M"
        assert person.birth_date == "1950-01-01"
        assert person.birth_place == "New York, USA"

    def test_parse_person_with_death(self):
        """Test parsing d'une personne avec décès"""
        gedcom = """
0 @I1@ INDI
1 NAME Jane /Smith/
1 SEX F
1 DEAT
2 DATE 31 DEC 2020
2 PLAC Paris, France
"""
        persons, _ = self.parser.parse_string(gedcom)

        person = persons['I1']
        assert person.first_name == "Jane"
        assert person.last_name == "Smith"
        assert person.gender == "F"
        assert person.death_date == "2020-12-31"
        assert person.death_place == "Paris, France"

    def test_parse_family(self):
        """Test parsing d'une famille"""
        gedcom = """
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
1 CHIL @I4@
1 MARR
2 DATE 15 JUN 1945
2 PLAC London, UK
"""
        _, families = self.parser.parse_string(gedcom)

        assert len(families) == 1
        assert 'F1' in families

        family = families['F1']
        assert family.husband_id == "I1"
        assert family.wife_id == "I2"
        assert len(family.children_ids) == 2
        assert "I3" in family.children_ids
        assert "I4" in family.children_ids
        assert family.marriage_date == "1945-06-15"
        assert family.marriage_place == "London, UK"

    def test_parse_multiple_persons(self):
        """Test parsing de plusieurs personnes"""
        gedcom = """
0 @I1@ INDI
1 NAME John /Doe/
0 @I2@ INDI
1 NAME Jane /Smith/
0 @I3@ INDI
1 NAME Bob /Johnson/
"""
        persons, _ = self.parser.parse_string(gedcom)

        assert len(persons) == 3
        assert all(id in persons for id in ['I1', 'I2', 'I3'])

    def test_parse_date_formats(self):
        """Test parsing de différents formats de dates"""
        test_cases = [
            ("1 JAN 1950", "1950-01-01"),
            ("JAN 1950", "1950-01-01"),
            ("1950", "1950-01-01"),
            ("ABT 1950", "1950-01-01"),
            ("BEF 1950", "1950-01-01"),
        ]

        for gedcom_date, expected in test_cases:
            parsed = self.parser._parse_date(gedcom_date)
            assert parsed == expected, f"Failed for {gedcom_date}"

    def test_parse_name_formats(self):
        """Test parsing de différents formats de noms"""
        test_cases = [
            ("John /Doe/", ("John", "Doe")),
            ("John William /Doe/", ("John William", "Doe")),
            ("/Doe/", ("", "Doe")),
            ("John /Doe/ Jr.", ("John", "Doe")),
        ]

        for name_value, (expected_first, expected_last) in test_cases:
            self.parser.current_person = GedcomPerson(id="TEST")
            self.parser._parse_name(name_value)
            assert self.parser.current_person.first_name == expected_first
            assert self.parser.current_person.last_name == expected_last

    def test_link_families(self):
        """Test liaison des familles et des enfants"""
        gedcom = """
0 @I1@ INDI
1 NAME Father /Doe/
0 @I2@ INDI
1 NAME Mother /Smith/
0 @I3@ INDI
1 NAME Child /Doe/
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
"""
        persons, families = self.parser.parse_string(gedcom)

        # Vérifier que l'enfant a les bons parents
        child = persons['I3']
        assert child.father_id == "I1"
        assert child.mother_id == "I2"

    def test_statistics(self):
        """Test des statistiques"""
        gedcom = """
0 @I1@ INDI
1 NAME John /Doe/
1 SEX M
1 BIRT
2 DATE 1 JAN 1950
0 @I2@ INDI
1 NAME Jane /Smith/
1 SEX F
1 DEAT
2 DATE 31 DEC 2020
"""
        persons, families = self.parser.parse_string(gedcom)
        stats = self.parser.get_statistics()

        assert stats['total_persons'] == 2
        assert stats['males'] == 1
        assert stats['females'] == 1
        assert stats['with_birth_date'] == 1
        assert stats['with_death_date'] == 1
        assert stats['living'] == 1

    def test_parse_empty_gedcom(self):
        """Test parsing d'un GEDCOM vide"""
        gedcom = ""
        persons, families = self.parser.parse_string(gedcom)

        assert len(persons) == 0
        assert len(families) == 0

    def test_parse_occupation(self):
        """Test parsing de la profession"""
        gedcom = """
0 @I1@ INDI
1 NAME John /Doe/
1 OCCU Engineer
"""
        persons, _ = self.parser.parse_string(gedcom)
        person = persons['I1']
        assert person.occupation == "Engineer"

    def test_parse_notes(self):
        """Test parsing des notes"""
        gedcom = """
0 @I1@ INDI
1 NAME John /Doe/
1 NOTE This is a note
1 NOTE Another note
"""
        persons, _ = self.parser.parse_string(gedcom)
        person = persons['I1']
        assert len(person.notes) == 2
        assert "This is a note" in person.notes
        assert "Another note" in person.notes


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
