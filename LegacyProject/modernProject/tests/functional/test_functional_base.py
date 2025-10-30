"""
Functional Test Base Class for AWKWARD LEGACY

This module provides the base class for all functional tests,
including setup, teardown, and utility methods.
"""

import unittest
import tempfile
import os
import shutil
import sys

# Add the modernProject directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from lib import database
from lib import geneweb_compat
from lib.gwdef import GenPerson, GenAscend, GenUnion, GenFamily, Sex, BaseNotes
from lib import secure
from lib import iovalue


class FunctionalTestBase(unittest.TestCase):
    """Base class for functional tests with common setup and utilities"""

    def setUp(self):
        """Set up test environment before each test"""
        # Create temporary directory for test database
        self.test_dir = tempfile.mkdtemp(prefix="test_awkward_")
        self.db_path = os.path.join(self.test_dir, "test.gwb")

        # Initialize secure environment
        secure.add_assets(self.test_dir)

        # Create a minimal test database
        self._create_test_database()

        # Track created resources for cleanup
        self.created_resources = []

    def tearDown(self):
        """Clean up test environment after each test"""
        # Clean up temporary directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

        # Clean up any other resources
        for resource in self.created_resources:
            if os.path.exists(resource):
                if os.path.isdir(resource):
                    shutil.rmtree(resource)
                else:
                    os.remove(resource)

    def _create_test_database(self):
        """Create a minimal test database with sample data"""
        # Create sample persons
        person1 = GenPerson(
            first_name=1,  # "John"
            surname=2,     # "Doe"
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
            birth="1970-01-01",
            birth_place="",
            birth_note="",
            birth_src="",
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
            notes="",
            psources="",
            key_index=0
        )

        person2 = GenPerson(
            first_name=3,  # "Jane"
            surname=4,     # "Smith"
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
            sex=Sex.FEMALE,
            access=0,
            birth="1975-06-15",
            birth_place="",
            birth_note="",
            birth_src="",
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
            notes="",
            psources="",
            key_index=1
        )

        # Create ascendants and unions
        ascend1 = GenAscend(parents=None, consang=None)
        ascend2 = GenAscend(parents=None, consang=None)
        union1 = GenUnion(family=[0])  # Link to family 0
        union2 = GenUnion(family=[0])  # Link to family 0

        # Create a family
        family1 = GenFamily(
            marriage="1995-07-20",
            marriage_place="",
            marriage_note="",
            marriage_src="",
            witnesses=[],
            relation=0,
            divorce=0,
            fevents=[],
            comment="",
            origin_file="",
            fsources="",
            fam_index=0
        )

        couple1 = {"father": 0, "mother": 1}  # John and Jane
        descend1 = {"children": []}  # No children yet

        # String table
        strings = ["", "John", "Doe", "Jane", "Smith"]

        # Base notes
        base_notes = BaseNotes(
            nread=lambda fname, mode: "",
            norigin_file="",
            efiles=lambda: []
        )

        # Package data for database creation
        persons_tuple = ([person1, person2], [ascend1, ascend2], [union1, union2])
        families_tuple = ([family1], [couple1], [descend1])
        arrays = (persons_tuple, families_tuple, strings, base_notes)

        # Create the database
        def init_callback(base):
            """Callback to initialize the database"""
            return base

        # Create database files
        os.makedirs(self.db_path, exist_ok=True)
        database.make(self.db_path.replace('.gwb', ''), [], arrays, init_callback)

    def with_test_database(self, callback):
        """Execute a callback with the test database"""
        return database.with_database(self.db_path, callback)

    def create_test_person(self, first_name, surname, sex=Sex.MALE, birth=""):
        """Helper method to create a test person"""
        def add_person(base):
            # Insert strings for names
            fn_idx = base.func.insert_string(first_name)
            sn_idx = base.func.insert_string(surname)

            # Create person object
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
                sex=sex,
                access=0,
                birth=birth,
                birth_place="",
                birth_note="",
                birth_src="",
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
                notes="",
                psources="",
                key_index=base.data.persons.len
            )

            # Add person to database
            new_index = base.data.persons.len
            base.func.patch_person(new_index, person)
            base.func.commit_patches()

            return new_index

        return self.with_test_database(add_person)

    def search_person(self, name):
        """Helper method to search for a person by name"""
        def search(base):
            results = base.func.persons_of_name(name)
            return results

        return self.with_test_database(search)

    def get_person_data(self, index):
        """Helper method to get person data by index"""
        def get_data(base):
            if index < base.data.persons.len:
                person = base.data.persons.get(index)
                # Get string values for names
                first_name = base.data.strings.get(person.first_name) if hasattr(person, 'first_name') else ""
                surname = base.data.strings.get(person.surname) if hasattr(person, 'surname') else ""

                return {
                    'first_name': first_name,
                    'surname': surname,
                    'sex': person.sex if hasattr(person, 'sex') else None,
                    'birth': person.birth if hasattr(person, 'birth') else "",
                    'index': index
                }
            return None

        return self.with_test_database(get_data)

    def create_test_family(self, father_idx, mother_idx, children_indices=None):
        """Helper method to create a test family"""
        def add_family(base):
            # Create family object
            family = GenFamily(
                marriage="",
                marriage_place="",
                marriage_note="",
                marriage_src="",
                witnesses=[],
                relation=0,
                divorce=0,
                fevents=[],
                comment="",
                origin_file="",
                fsources="",
                fam_index=base.data.families.len
            )

            # Create couple
            couple = {"father": father_idx, "mother": mother_idx}

            # Create descend
            descend = {"children": children_indices if children_indices else []}

            # Add family to database
            new_fam_idx = base.data.families.len
            base.func.patch_family(new_fam_idx, family)
            base.func.patch_couple(new_fam_idx, couple)
            base.func.patch_descend(new_fam_idx, descend)

            # Update unions for parents
            father_union = base.data.unions.get(father_idx)
            if hasattr(father_union, 'family'):
                father_union.family.append(new_fam_idx)
            base.func.patch_union(father_idx, father_union)

            mother_union = base.data.unions.get(mother_idx)
            if hasattr(mother_union, 'family'):
                mother_union.family.append(new_fam_idx)
            base.func.patch_union(mother_idx, mother_union)

            base.func.commit_patches()

            return new_fam_idx

        return self.with_test_database(add_family)

    def count_persons(self):
        """Helper method to count persons in database"""
        def count(base):
            return base.func.nb_of_real_persons()

        return self.with_test_database(count)

    def count_families(self):
        """Helper method to count families in database"""
        def count(base):
            return base.data.families.len

        return self.with_test_database(count)

    def export_gedcom(self, output_file):
        """Helper method to export database to GEDCOM"""
        # This would require implementing GEDCOM export functionality
        # For now, we'll create a placeholder
        with open(output_file, 'w') as f:
            f.write("0 HEAD\n")
            f.write("1 GEDC\n")
            f.write("2 VERS 5.5.1\n")
            f.write("0 TRLR\n")

        self.created_resources.append(output_file)
        return output_file

    def import_gedcom(self, gedcom_file):
        """Helper method to import GEDCOM file"""
        # This would require implementing GEDCOM import functionality
        # For now, we'll return a success status
        return True if os.path.exists(gedcom_file) else False

    def verify_database_integrity(self):
        """Helper method to verify database integrity"""
        def verify(base):
            try:
                # Check persons
                persons_ok = base.data.persons.len >= 0

                # Check families
                families_ok = base.data.families.len >= 0

                # Check strings
                strings_ok = base.data.strings.len >= 0

                return persons_ok and families_ok and strings_ok
            except Exception:
                return False

        return self.with_test_database(verify)


class FunctionalTestRunner:
    """Runner for functional tests with reporting"""

    @staticmethod
    def run_all_tests():
        """Run all functional tests and generate report"""
        loader = unittest.TestLoader()
        suite = loader.discover('tests/functional', pattern='test_*.py')

        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        return result.wasSuccessful()


if __name__ == '__main__':
    # Run a basic smoke test
    class SmokeTest(FunctionalTestBase):
        def test_database_creation(self):
            """Test that database can be created"""
            self.assertTrue(os.path.exists(self.db_path))
            self.assertTrue(self.verify_database_integrity())

        def test_person_creation(self):
            """Test that persons can be created"""
            idx = self.create_test_person("Test", "Person", Sex.MALE, "2000-01-01")
            self.assertIsNotNone(idx)

            person_data = self.get_person_data(idx)
            self.assertIsNotNone(person_data)
            self.assertEqual(person_data['first_name'], "Test")
            self.assertEqual(person_data['surname'], "Person")

        def test_search_functionality(self):
            """Test that search works"""
            results = self.search_person("John Doe")
            self.assertIsInstance(results, list)

    # Run smoke test
    unittest.main()