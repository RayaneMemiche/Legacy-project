"""
Functional Tests for Family Relationships

Complete end-to-end tests for family creation and relationship management.
"""

import unittest
from test_functional_base import FunctionalTestBase
from lib.gwdef import Sex


class TestFamilyRelationships(FunctionalTestBase):
    """Test complete family relationship workflows"""

    def test_family_tree_navigation(self):
        """Test de navigation dans l'arbre généalogique"""
        # Create grandparents
        grandfather_idx = self.create_test_person("Grand", "Father", Sex.MALE, "1940-01-01")
        grandmother_idx = self.create_test_person("Grand", "Mother", Sex.FEMALE, "1942-03-15")

        # Create parents
        father_idx = self.create_test_person("Father", "Family", Sex.MALE, "1965-05-20")
        mother_idx = self.create_test_person("Mother", "Family", Sex.FEMALE, "1967-08-10")

        # Create children
        child1_idx = self.create_test_person("Child", "One", Sex.MALE, "1990-02-14")
        child2_idx = self.create_test_person("Child", "Two", Sex.FEMALE, "1992-11-30")

        # Create family relationships
        grandparents_family = self.create_test_family(
            grandfather_idx,
            grandmother_idx,
            [father_idx]
        )

        parents_family = self.create_test_family(
            father_idx,
            mother_idx,
            [child1_idx, child2_idx]
        )

        # Verify families were created
        self.assertIsNotNone(grandparents_family)
        self.assertIsNotNone(parents_family)

        # Test family navigation
        def navigate_family(base):
            # Get father's data
            father = base.data.persons.get(father_idx)
            self.assertIsNotNone(father)

            # Get father's union (families where he's a parent)
            father_union = base.data.unions.get(father_idx)
            self.assertIsNotNone(father_union)

            # Get father's ascendants (his parents)
            father_ascend = base.data.ascends.get(father_idx)

            # Get family where father is a child
            if father_ascend and hasattr(father_ascend, 'parents'):
                parents_fam_idx = father_ascend.parents
                if parents_fam_idx is not None:
                    parents_couple = base.data.couples.get(parents_fam_idx)
                    self.assertIsNotNone(parents_couple)

            # Get children of parents_family
            parents_descend = base.data.descends.get(parents_family)
            self.assertIsNotNone(parents_descend)

            return True

        success = self.with_test_database(navigate_family)
        self.assertTrue(success)

    def test_create_complex_family_structure(self):
        """Test création d'une structure familiale complexe avec plusieurs générations"""
        # Generation 1 - Great-grandparents
        ggf1_idx = self.create_test_person("GreatGrand", "Father1", Sex.MALE, "1920-01-01")
        ggm1_idx = self.create_test_person("GreatGrand", "Mother1", Sex.FEMALE, "1922-01-01")
        ggf2_idx = self.create_test_person("GreatGrand", "Father2", Sex.MALE, "1921-01-01")
        ggm2_idx = self.create_test_person("GreatGrand", "Mother2", Sex.FEMALE, "1923-01-01")

        # Generation 2 - Grandparents
        gf1_idx = self.create_test_person("Grand", "Father1", Sex.MALE, "1945-01-01")
        gm1_idx = self.create_test_person("Grand", "Mother1", Sex.FEMALE, "1947-01-01")

        # Generation 3 - Parents
        father_idx = self.create_test_person("Parent", "Father", Sex.MALE, "1970-01-01")
        mother_idx = self.create_test_person("Parent", "Mother", Sex.FEMALE, "1972-01-01")

        # Generation 4 - Children
        children_idx = []
        for i in range(3):
            child_idx = self.create_test_person(
                f"Child{i+1}",
                "Generation4",
                Sex.MALE if i % 2 == 0 else Sex.FEMALE,
                f"199{5+i}-01-01"
            )
            children_idx.append(child_idx)

        # Create family links
        ggfam1 = self.create_test_family(ggf1_idx, ggm1_idx, [gf1_idx])
        ggfam2 = self.create_test_family(ggf2_idx, ggm2_idx, [gm1_idx])
        gfam = self.create_test_family(gf1_idx, gm1_idx, [father_idx])
        pfam = self.create_test_family(father_idx, mother_idx, children_idx)

        # Verify all families exist
        self.assertIsNotNone(ggfam1)
        self.assertIsNotNone(ggfam2)
        self.assertIsNotNone(gfam)
        self.assertIsNotNone(pfam)

        # Count total families
        family_count = self.count_families()
        self.assertGreaterEqual(family_count, 4)

    def test_marriage_and_divorce(self):
        """Test gestion des mariages et divorces"""
        # Create persons
        husband_idx = self.create_test_person("Husband", "Name", Sex.MALE, "1980-01-01")
        wife_idx = self.create_test_person("Wife", "Name", Sex.FEMALE, "1982-01-01")

        def create_marriage(base):
            from lib.gwdef import GenFamily

            family = GenFamily(
                marriage="2005-06-15",
                marriage_place="City Hall",
                marriage_note="Beautiful ceremony",
                marriage_src="Marriage Certificate",
                witnesses=[],
                relation=0,  # Married
                divorce=0,  # Not divorced initially
                fevents=[],
                comment="First marriage",
                origin_file="",
                fsources="",
                fam_index=base.data.families.len
            )

            couple = {"father": husband_idx, "mother": wife_idx}
            descend = {"children": []}

            new_fam_idx = base.data.families.len
            base.func.patch_family(new_fam_idx, family)
            base.func.patch_couple(new_fam_idx, couple)
            base.func.patch_descend(new_fam_idx, descend)
            base.func.commit_patches()

            return new_fam_idx

        family_idx = self.with_test_database(create_marriage)
        self.assertIsNotNone(family_idx)

        # Update to divorced status
        def update_to_divorced(base):
            family = base.data.families.get(family_idx)
            if hasattr(family, 'divorce'):
                family.divorce = 1  # Set as divorced
            if hasattr(family, 'comment'):
                family.comment = "Divorced in 2010"

            base.func.patch_family(family_idx, family)
            base.func.commit_patches()
            return True

        success = self.with_test_database(update_to_divorced)
        self.assertTrue(success)

    def test_multiple_marriages(self):
        """Test personne avec plusieurs mariages"""
        # Create persons
        person_idx = self.create_test_person("MultiMarriage", "Person", Sex.MALE, "1975-01-01")
        spouse1_idx = self.create_test_person("First", "Spouse", Sex.FEMALE, "1977-01-01")
        spouse2_idx = self.create_test_person("Second", "Spouse", Sex.FEMALE, "1980-01-01")

        # First marriage
        family1_idx = self.create_test_family(person_idx, spouse1_idx, [])

        # Second marriage
        family2_idx = self.create_test_family(person_idx, spouse2_idx, [])

        # Verify both families exist
        self.assertIsNotNone(family1_idx)
        self.assertIsNotNone(family2_idx)
        self.assertNotEqual(family1_idx, family2_idx)

        # Verify person is linked to both families
        def verify_multiple_unions(base):
            person_union = base.data.unions.get(person_idx)
            if hasattr(person_union, 'family'):
                # Person should be in both families
                self.assertIn(family1_idx, person_union.family)
                self.assertIn(family2_idx, person_union.family)
                self.assertEqual(len(person_union.family), 2)
            return True

        success = self.with_test_database(verify_multiple_unions)
        self.assertTrue(success)

    def test_siblings_relationship(self):
        """Test relations entre frères et sœurs"""
        # Create parents
        father_idx = self.create_test_person("Father", "Siblings", Sex.MALE, "1960-01-01")
        mother_idx = self.create_test_person("Mother", "Siblings", Sex.FEMALE, "1962-01-01")

        # Create siblings
        siblings = []
        for i in range(4):
            sibling_idx = self.create_test_person(
                f"Sibling{i+1}",
                "Family",
                Sex.MALE if i % 2 == 0 else Sex.FEMALE,
                f"198{5+i}-01-01"
            )
            siblings.append(sibling_idx)

        # Create family with all siblings
        family_idx = self.create_test_family(father_idx, mother_idx, siblings)
        self.assertIsNotNone(family_idx)

        # Verify siblings are all in the same family
        def verify_siblings(base):
            family_descend = base.data.descends.get(family_idx)
            if hasattr(family_descend, 'children'):
                self.assertEqual(len(family_descend.children), 4)
                for sibling_idx in siblings:
                    self.assertIn(sibling_idx, family_descend.children)

            # Each sibling should have the same parents
            for sibling_idx in siblings:
                sibling_ascend = base.data.ascends.get(sibling_idx)
                if hasattr(sibling_ascend, 'parents'):
                    self.assertEqual(sibling_ascend.parents, family_idx)

            return True

        success = self.with_test_database(verify_siblings)
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()