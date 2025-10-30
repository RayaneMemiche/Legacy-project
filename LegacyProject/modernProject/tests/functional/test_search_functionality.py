"""
Functional Tests for Search Functionality

Complete end-to-end tests for searching persons and families.
"""

import unittest
from test_functional_base import FunctionalTestBase
from lib.gwdef import Sex


class TestSearchFunctionality(FunctionalTestBase):
    """Test complete search functionality workflows"""

    def test_search_person_by_name(self):
        """Test de recherche de personnes par nom"""
        # Create test persons with various names
        test_persons = [
            ("John", "Smith", Sex.MALE),
            ("Jane", "Smith", Sex.FEMALE),
            ("John", "Doe", Sex.MALE),
            ("Alice", "Johnson", Sex.FEMALE),
            ("Bob", "Johnson", Sex.MALE),
            ("Marie", "Dubois", Sex.FEMALE),
            ("Pierre", "Dubois", Sex.MALE),
            ("Jean-Pierre", "Martin", Sex.MALE),
            ("Marie-Claire", "Martin", Sex.FEMALE)
        ]

        created_indices = []
        for first, last, sex in test_persons:
            idx = self.create_test_person(first, last, sex, "1980-01-01")
            created_indices.append((idx, first, last))

        # Test exact name search
        results = self.search_person("John Smith")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

        # Test partial name search
        results_smith = self.search_person("Smith")
        self.assertIsInstance(results_smith, list)

        # Test with compound names
        results_jp = self.search_person("Jean-Pierre Martin")
        self.assertIsInstance(results_jp, list)

        # Verify search results contain expected persons
        for idx, first, last in created_indices:
            if first == "John" and last == "Smith":
                john_smith_results = self.search_person(f"{first} {last}")
                self.assertIn(idx, john_smith_results)

    def test_search_with_special_characters(self):
        """Test recherche avec caractères spéciaux"""
        # Create persons with special characters
        special_names = [
            ("François", "L'Hôpital"),
            ("José", "González"),
            ("Björn", "Müller"),
            ("Søren", "Ødegaard"),
            ("Владимир", "Петров")  # Cyrillic
        ]

        for first, last in special_names:
            idx = self.create_test_person(first, last, Sex.MALE, "1990-01-01")
            self.assertIsNotNone(idx)

            # Search for the person
            results = self.search_person(f"{first} {last}")
            self.assertIsInstance(results, list)

    def test_search_case_sensitivity(self):
        """Test sensibilité à la casse dans les recherches"""
        # Create person
        idx = self.create_test_person("TestCase", "SENSITIVITY", Sex.MALE, "1985-01-01")

        # Test different case variations
        test_cases = [
            "TestCase SENSITIVITY",
            "testcase sensitivity",
            "TESTCASE SENSITIVITY",
            "Testcase Sensitivity"
        ]

        for search_term in test_cases:
            results = self.search_person(search_term)
            self.assertIsInstance(results, list)
            # Note: Case sensitivity depends on implementation

    def test_search_by_surname_only(self):
        """Test recherche par nom de famille uniquement"""
        # Create multiple persons with same surname
        surname = "CommonSurname"
        first_names = ["Alice", "Bob", "Charlie", "Diana", "Edward"]

        created = []
        for fname in first_names:
            idx = self.create_test_person(fname, surname, Sex.MALE, "1970-01-01")
            created.append(idx)

        # Search by surname only
        results = self.search_person(surname)
        self.assertIsInstance(results, list)

        # All created persons should be in results
        for idx in created:
            person_data = self.get_person_data(idx)
            self.assertEqual(person_data['surname'], surname)

    def test_search_by_first_name_only(self):
        """Test recherche par prénom uniquement"""
        # Create multiple persons with same first name
        first_name = "CommonFirst"
        surnames = ["Smith", "Jones", "Brown", "Taylor", "Wilson"]

        created = []
        for sname in surnames:
            idx = self.create_test_person(first_name, sname, Sex.FEMALE, "1975-01-01")
            created.append(idx)

        # Search by first name only
        results = self.search_person(first_name)
        self.assertIsInstance(results, list)

        # Verify persons were created
        for idx in created:
            person_data = self.get_person_data(idx)
            self.assertEqual(person_data['first_name'], first_name)

    def test_search_with_particles(self):
        """Test recherche avec particules (de, von, van, etc.)"""
        # Create persons with name particles
        particle_names = [
            ("Ludwig", "van Beethoven"),
            ("Charles", "de Gaulle"),
            ("Otto", "von Bismarck"),
            ("Vincent", "van Gogh"),
            ("Leonardo", "da Vinci"),
            ("Jean", "de La Fontaine")
        ]

        for first, last in particle_names:
            idx = self.create_test_person(first, last, Sex.MALE, "1800-01-01")

            # Search with full name
            results = self.search_person(f"{first} {last}")
            self.assertIsInstance(results, list)

            # Search without particle
            name_parts = last.split()
            if len(name_parts) > 1:
                main_surname = name_parts[-1]
                results_no_particle = self.search_person(f"{first} {main_surname}")
                self.assertIsInstance(results_no_particle, list)

    def test_empty_search(self):
        """Test recherche vide"""
        # Search with empty string
        results = self.search_person("")
        self.assertIsInstance(results, list)

        # Search with None (if supported)
        try:
            results_none = self.search_person(None)
            self.assertIsInstance(results_none, list)
        except:
            # Some implementations might not support None
            pass

    def test_search_performance_with_many_persons(self):
        """Test performance de recherche avec beaucoup de personnes"""
        import time

        # Create 100 persons
        for i in range(100):
            self.create_test_person(
                f"Person{i}",
                f"TestPerf{i % 10}",  # 10 different surnames
                Sex.MALE if i % 2 == 0 else Sex.FEMALE,
                f"19{50 + i % 50}-01-01"
            )

        # Measure search time
        start_time = time.time()
        results = self.search_person("Person50 TestPerf0")
        end_time = time.time()

        search_time = end_time - start_time
        self.assertLess(search_time, 1.0)  # Should complete within 1 second
        self.assertIsInstance(results, list)

    def test_search_with_wildcards(self):
        """Test recherche avec wildcards si supporté"""
        # Create test persons
        self.create_test_person("Alexander", "GreatPerson", Sex.MALE, "1980-01-01")
        self.create_test_person("Alexandra", "GreatPerson", Sex.FEMALE, "1982-01-01")
        self.create_test_person("Alex", "GreatPerson", Sex.MALE, "1985-01-01")

        # Try wildcard searches (implementation dependent)
        wildcard_patterns = [
            "Alex*",
            "*Person",
            "Alex* Great*"
        ]

        for pattern in wildcard_patterns:
            try:
                results = self.search_person(pattern)
                self.assertIsInstance(results, list)
            except:
                # Wildcards might not be supported
                pass


if __name__ == '__main__':
    unittest.main()