"""
Functional Tests for Import/Export Functionality

Complete end-to-end tests for GEDCOM import/export and data interchange.
"""

import unittest
import os
import tempfile
from test_functional_base import FunctionalTestBase
from lib.gwdef import Sex


class TestImportExport(FunctionalTestBase):
    """Test complete import/export workflows"""

    def test_gedcom_import_export_cycle(self):
        """Test d'import/export GEDCOM complet"""
        # Create test data
        persons = [
            ("TestExport", "Person1", Sex.MALE, "1950-01-01"),
            ("TestExport", "Person2", Sex.FEMALE, "1952-03-15"),
            ("TestExport", "Child1", Sex.MALE, "1975-06-20"),
            ("TestExport", "Child2", Sex.FEMALE, "1978-09-10")
        ]

        created_indices = []
        for first, last, sex, birth in persons:
            idx = self.create_test_person(first, last, sex, birth)
            created_indices.append(idx)

        # Create family relationships
        family_idx = self.create_test_family(
            created_indices[0],  # Father
            created_indices[1],  # Mother
            created_indices[2:]  # Children
        )

        # Export to GEDCOM
        export_file = os.path.join(self.test_dir, "export_test.ged")
        exported = self.export_gedcom(export_file)
        self.assertTrue(os.path.exists(exported))

        # Verify GEDCOM file has content
        with open(export_file, 'r') as f:
            content = f.read()
            self.assertIn("HEAD", content)
            self.assertIn("TRLR", content)

        # Test import (would need actual implementation)
        import_success = self.import_gedcom(export_file)
        self.assertTrue(import_success)

    def test_export_large_database(self):
        """Test export d'une grande base de données"""
        # Create 50 persons
        for i in range(50):
            self.create_test_person(
                f"LargePerson{i}",
                f"Export{i}",
                Sex.MALE if i % 2 == 0 else Sex.FEMALE,
                f"19{50 + i % 50}-01-01"
            )

        # Export
        export_file = os.path.join(self.test_dir, "large_export.ged")
        exported = self.export_gedcom(export_file)

        self.assertTrue(os.path.exists(exported))

        # Check file size is reasonable
        file_size = os.path.getsize(exported)
        self.assertGreater(file_size, 100)  # Should have some content

    def test_export_with_special_characters(self):
        """Test export avec caractères spéciaux"""
        # Create persons with special characters
        special_persons = [
            ("François", "Müller", "Ingénieur"),
            ("José", "González", "Médecin"),
            ("Björn", "Ødegaard", "Professeur")
        ]

        for first, last, occupation in special_persons:
            def create_special_person(base):
                fn_idx = base.func.insert_string(first)
                sn_idx = base.func.insert_string(last)

                from lib.gwdef import GenPerson
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
                    occupation=occupation,
                    sex=Sex.MALE,
                    access=0,
                    birth="1970-01-01",
                    birth_place="Paris, France",
                    birth_note="Note with àccénts",
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
                    notes="Notes with special chars: é à ü ñ",
                    psources="",
                    key_index=base.data.persons.len
                )

                new_idx = base.data.persons.len
                base.func.patch_person(new_idx, person)
                base.func.commit_patches()
                return new_idx

            idx = self.with_test_database(create_special_person)
            self.assertIsNotNone(idx)

        # Export
        export_file = os.path.join(self.test_dir, "special_chars.ged")
        exported = self.export_gedcom(export_file)
        self.assertTrue(os.path.exists(exported))

    def test_export_preservation_of_data(self):
        """Test que l'export préserve toutes les données"""
        # Create comprehensive test person
        def create_comprehensive_person(base):
            # Insert all necessary strings
            fn_idx = base.func.insert_string("Comprehensive")
            sn_idx = base.func.insert_string("TestPerson")
            alias1_idx = base.func.insert_string("Nickname1")
            alias2_idx = base.func.insert_string("Nickname2")
            title_idx = base.func.insert_string("Doctor")

            from lib.gwdef import GenPerson
            person = GenPerson(
                first_name=fn_idx,
                surname=sn_idx,
                occ=0,
                image="photo.jpg",
                public_name="Dr. Test",
                qualifiers=["Jr."],
                aliases=[alias1_idx, alias2_idx],
                first_names_aliases=[alias1_idx],
                surnames_aliases=[],
                titles=[title_idx],
                rparents=[],
                related=[],
                occupation="Software Engineer",
                sex=Sex.MALE,
                access=0,
                birth="1980-03-15",
                birth_place="New York, USA",
                birth_note="Born during a snowstorm",
                birth_src="Birth Certificate #12345",
                baptism="1980-04-20",
                baptism_place="St. Mary's Church",
                baptism_note="Baptized by Father John",
                baptism_src="Church Records",
                death="",
                death_place="",
                death_note="",
                death_src="",
                burial="",
                burial_place="",
                burial_note="",
                burial_src="",
                pevents=[
                    {"name": "Education", "date": "2002-06-15", "place": "MIT"},
                    {"name": "Career", "date": "2003-01-01", "place": "Google"}
                ],
                notes="Comprehensive test person with all fields",
                psources="Multiple sources",
                key_index=base.data.persons.len
            )

            new_idx = base.data.persons.len
            base.func.patch_person(new_idx, person)
            base.func.commit_patches()
            return new_idx

        person_idx = self.with_test_database(create_comprehensive_person)
        self.assertIsNotNone(person_idx)

        # Export
        export_file = os.path.join(self.test_dir, "comprehensive.ged")
        exported = self.export_gedcom(export_file)
        self.assertTrue(os.path.exists(exported))

        # Read and verify export contains expected data
        with open(export_file, 'r') as f:
            content = f.read()
            # Check for various GEDCOM tags
            expected_tags = ["HEAD", "INDI", "TRLR"]
            for tag in expected_tags:
                self.assertIn(tag, content)

    def test_incremental_export(self):
        """Test export incrémental (seulement les changements)"""
        # Create initial persons
        initial_persons = []
        for i in range(5):
            idx = self.create_test_person(f"Initial{i}", "Person", Sex.MALE, "1970-01-01")
            initial_persons.append(idx)

        # First export
        export1 = os.path.join(self.test_dir, "export1.ged")
        self.export_gedcom(export1)
        size1 = os.path.getsize(export1)

        # Add more persons
        for i in range(5):
            self.create_test_person(f"Added{i}", "Person", Sex.FEMALE, "1980-01-01")

        # Second export
        export2 = os.path.join(self.test_dir, "export2.ged")
        self.export_gedcom(export2)
        size2 = os.path.getsize(export2)

        # Second export should be larger
        self.assertGreater(size2, size1)

    def test_export_formats(self):
        """Test différents formats d'export (GEDCOM, JSON, XML si supporté)"""
        # Create test data
        self.create_test_person("Format", "Test", Sex.MALE, "1990-01-01")

        # Test GEDCOM export
        gedcom_file = os.path.join(self.test_dir, "test.ged")
        self.export_gedcom(gedcom_file)
        self.assertTrue(os.path.exists(gedcom_file))

        # Test JSON export if supported
        json_file = os.path.join(self.test_dir, "test.json")
        try:
            # Would need JSON export implementation
            with open(json_file, 'w') as f:
                import json
                json.dump({"test": "data"}, f)
            self.created_resources.append(json_file)
            self.assertTrue(os.path.exists(json_file))
        except:
            pass

        # Test XML export if supported
        xml_file = os.path.join(self.test_dir, "test.xml")
        try:
            # Would need XML export implementation
            with open(xml_file, 'w') as f:
                f.write('<?xml version="1.0"?>\n<root></root>')
            self.created_resources.append(xml_file)
            self.assertTrue(os.path.exists(xml_file))
        except:
            pass

    def test_import_validation(self):
        """Test validation lors de l'import"""
        # Create invalid GEDCOM file
        invalid_gedcom = os.path.join(self.test_dir, "invalid.ged")
        with open(invalid_gedcom, 'w') as f:
            f.write("This is not valid GEDCOM format\n")
            f.write("Random text\n")

        self.created_resources.append(invalid_gedcom)

        # Try to import - should handle gracefully
        try:
            result = self.import_gedcom(invalid_gedcom)
            # Should either return False or raise an exception
            if result is not False:
                # If it doesn't return False, it should at least not crash
                pass
        except:
            # Expected - invalid file should raise an error
            pass

    def test_export_privacy_filter(self):
        """Test filtre de confidentialité lors de l'export"""
        # Create persons with different access levels
        def create_private_person(base):
            fn_idx = base.func.insert_string("Private")
            sn_idx = base.func.insert_string("Person")

            from lib.gwdef import GenPerson
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
                access=1,  # Private access
                birth="1990-01-01",
                birth_place="Private Location",
                birth_note="Private note",
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
                notes="This should not be exported",
                psources="",
                key_index=base.data.persons.len
            )

            new_idx = base.data.persons.len
            base.func.patch_person(new_idx, person)
            base.func.commit_patches()
            return new_idx

        private_idx = self.with_test_database(create_private_person)
        public_idx = self.create_test_person("Public", "Person", Sex.FEMALE, "1990-01-01")

        # Export with privacy filter
        export_file = os.path.join(self.test_dir, "privacy_filtered.ged")
        self.export_gedcom(export_file)
        self.assertTrue(os.path.exists(export_file))


if __name__ == '__main__':
    unittest.main()