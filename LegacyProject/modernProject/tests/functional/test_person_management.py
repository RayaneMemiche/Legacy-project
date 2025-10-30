"""
Functional Tests for Person Management

Complete end-to-end tests for person creation, modification, and deletion.
"""

import unittest
from test_functional_base import FunctionalTestBase
from lib.gwdef import Sex


class TestPersonManagement(FunctionalTestBase):
    """Test complete person management workflows"""

    def test_create_person_complete_workflow(self):
        """Test complet de création d'une personne avec toutes les étapes"""
        # 1. Créer une personne
        person_idx = self.create_test_person(
            first_name="Alice",
            surname="Johnson",
            sex=Sex.FEMALE,
            birth="1985-03-15"
        )

        # 2. Vérifier qu'elle existe dans la base
        self.assertIsNotNone(person_idx)
        self.assertGreaterEqual(person_idx, 0)

        # 3. Récupérer les données de la personne
        person_data = self.get_person_data(person_idx)
        self.assertIsNotNone(person_data)
        self.assertEqual(person_data['first_name'], "Alice")
        self.assertEqual(person_data['surname'], "Johnson")
        self.assertEqual(person_data['sex'], Sex.FEMALE)
        self.assertEqual(person_data['birth'], "1985-03-15")

        # 4. Vérifier qu'elle apparaît dans les recherches
        search_results = self.search_person("Alice Johnson")
        self.assertIsInstance(search_results, list)
        self.assertIn(person_idx, search_results)

        # 5. Vérifier le comptage des personnes
        initial_count = self.count_persons()

        # Créer une autre personne
        person2_idx = self.create_test_person(
            first_name="Bob",
            surname="Williams",
            sex=Sex.MALE,
            birth="1983-07-20"
        )

        new_count = self.count_persons()
        self.assertEqual(new_count, initial_count + 1)

    def test_person_with_multiple_names(self):
        """Test création de personne avec aliases et surnoms"""
        def create_complex_person(base):
            # Insert strings
            fn_idx = base.func.insert_string("Robert")
            sn_idx = base.func.insert_string("Anderson")
            alias1_idx = base.func.insert_string("Bob")
            alias2_idx = base.func.insert_string("Bobby")
            surname_alias_idx = base.func.insert_string("Andy")

            from lib.gwdef import GenPerson
            person = GenPerson(
                first_name=fn_idx,
                surname=sn_idx,
                occ=0,
                image="",
                public_name="",
                qualifiers=[],
                aliases=[alias1_idx, alias2_idx],
                first_names_aliases=[alias1_idx, alias2_idx],
                surnames_aliases=[surname_alias_idx],
                titles=[],
                rparents=[],
                related=[],
                occupation="Engineer",
                sex=Sex.MALE,
                access=0,
                birth="1990-01-01",
                birth_place="New York",
                birth_note="Born at St. Mary's Hospital",
                birth_src="Birth Certificate #12345",
                baptism="",
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death="",
                death_place="",
                death_note="",
                death_src="",
                burial="",
                burial_place="",
                burial_note="",
                burial_src="",
                pevents=[],
                notes="Test person with multiple names",
                psources="Test source",
                key_index=base.data.persons.len
            )

            new_idx = base.data.persons.len
            base.func.patch_person(new_idx, person)
            base.func.commit_patches()

            return new_idx

        person_idx = self.with_test_database(create_complex_person)
        self.assertIsNotNone(person_idx)

        # Verify the person was created
        person_data = self.get_person_data(person_idx)
        self.assertEqual(person_data['first_name'], "Robert")
        self.assertEqual(person_data['surname'], "Anderson")

    def test_person_modification(self):
        """Test modification of existing person data"""
        # Create initial person
        person_idx = self.create_test_person(
            first_name="Initial",
            surname="Name",
            sex=Sex.MALE,
            birth="2000-01-01"
        )

        # Modify the person
        def modify_person(base):
            person = base.data.persons.get(person_idx)

            # Change birth date
            if hasattr(person, 'birth'):
                person.birth = "2000-12-31"

            # Update occupation
            if hasattr(person, 'occupation'):
                person.occupation = "Software Developer"

            base.func.patch_person(person_idx, person)
            base.func.commit_patches()

            return True

        success = self.with_test_database(modify_person)
        self.assertTrue(success)

        # Verify modifications
        updated_data = self.get_person_data(person_idx)
        self.assertEqual(updated_data['birth'], "2000-12-31")

    def test_person_with_events(self):
        """Test person creation with life events"""
        def create_person_with_events(base):
            fn_idx = base.func.insert_string("EventTest")
            sn_idx = base.func.insert_string("Person")

            from lib.gwdef import GenPerson

            # Create events list
            events = [
                {
                    "name": "Graduation",
                    "date": "2010-06-15",
                    "place": "University",
                    "note": "Bachelor's degree"
                },
                {
                    "name": "Marriage",
                    "date": "2015-09-20",
                    "place": "Church",
                    "note": "Married to Jane Doe"
                }
            ]

            person = GenPerson(
                first_name=fn_idx,
                surname=sn_idx,
                occ=0,
                image="",
                public_name="",
                qualifiers=[],
                aliases=[],
                first_names_aliases=[],
                surnames_aliases=[],
                titles=[],
                rparents=[],
                related=[],
                occupation="",
                sex=Sex.MALE,
                access=0,
                birth="1988-05-10",
                birth_place="Boston",
                birth_note="",
                birth_src="",
                baptism="1988-06-01",
                baptism_place="St. John's Church",
                baptism_note="",
                baptism_src="",
                death="",
                death_place="",
                death_note="",
                death_src="",
                burial="",
                burial_place="",
                burial_note="",
                burial_src="",
                pevents=events,
                notes="Person with multiple life events",
                psources="",
                key_index=base.data.persons.len
            )

            new_idx = base.data.persons.len
            base.func.patch_person(new_idx, person)
            base.func.commit_patches()

            return new_idx

        person_idx = self.with_test_database(create_person_with_events)
        self.assertIsNotNone(person_idx)

        # Verify person was created
        person_data = self.get_person_data(person_idx)
        self.assertEqual(person_data['first_name'], "EventTest")

    def test_batch_person_creation(self):
        """Test création de plusieurs personnes en lot"""
        initial_count = self.count_persons()

        # Create 10 persons in batch
        created_indices = []
        for i in range(10):
            idx = self.create_test_person(
                first_name=f"Person{i}",
                surname=f"Batch{i}",
                sex=Sex.MALE if i % 2 == 0 else Sex.FEMALE,
                birth=f"199{i}-01-01"
            )
            created_indices.append(idx)

        # Verify all were created
        final_count = self.count_persons()
        self.assertEqual(final_count, initial_count + 10)

        # Verify each person
        for i, idx in enumerate(created_indices):
            person_data = self.get_person_data(idx)
            self.assertEqual(person_data['first_name'], f"Person{i}")
            self.assertEqual(person_data['surname'], f"Batch{i}")


if __name__ == '__main__':
    unittest.main()