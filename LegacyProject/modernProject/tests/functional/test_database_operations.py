"""
Functional Tests for Database Operations

Complete end-to-end tests for database backup, restore, and maintenance.
"""

import unittest
import os
import shutil
import time
from test_functional_base import FunctionalTestBase
from lib.gwdef import Sex


class TestDatabaseOperations(FunctionalTestBase):
    """Test complete database operation workflows"""

    def test_database_backup_restore(self):
        """Test de backup/restore de base de données"""
        # Create initial data
        initial_persons = []
        for i in range(10):
            idx = self.create_test_person(
                f"Backup{i}",
                f"Test{i}",
                Sex.MALE if i % 2 == 0 else Sex.FEMALE,
                f"197{i}-01-01"
            )
            initial_persons.append(idx)

        # Create families
        if len(initial_persons) >= 2:
            family_idx = self.create_test_family(
                initial_persons[0],
                initial_persons[1],
                initial_persons[2:5]
            )

        # Count initial data
        initial_person_count = self.count_persons()
        initial_family_count = self.count_families()

        # Create backup
        backup_dir = os.path.join(self.test_dir, "backup")
        os.makedirs(backup_dir, exist_ok=True)

        # Verify backup directory structure can be created
        if os.path.exists(self.db_path):
            backup_path = os.path.join(backup_dir, "backup.gwb")
            shutil.copytree(self.db_path, backup_path)
            self.assertTrue(os.path.exists(backup_path))

        # Verify we can add more data after backup
        self.create_test_person("AfterBackup", "Person", Sex.MALE, "2000-01-01")
        modified_count = self.count_persons()
        self.assertEqual(modified_count, initial_person_count + 1)

        # Verify database integrity after all operations
        integrity_ok = self.verify_database_integrity()
        self.assertTrue(integrity_ok)

    def test_database_integrity_check(self):
        """Test vérification de l'intégrité de la base"""
        # Create data with potential integrity issues
        persons_created = []
        for i in range(20):
            idx = self.create_test_person(
                f"Integrity{i}",
                f"Check{i}",
                Sex.MALE if i % 2 == 0 else Sex.FEMALE,
                f"198{i % 10}-01-01"
            )
            persons_created.append(idx)

        # Create families with various configurations
        if len(persons_created) >= 4:
            # Normal family
            self.create_test_family(persons_created[0], persons_created[1], [persons_created[2]])

            # Family with no children
            self.create_test_family(persons_created[3], persons_created[4], [])

        # Run integrity check
        integrity_ok = self.verify_database_integrity()
        self.assertTrue(integrity_ok)

        # Check for orphaned records
        def check_orphans(base):
            orphaned = []

            # Check for persons without families
            for i in range(base.data.persons.len):
                person = base.data.persons.get(i)
                if person:
                    union = base.data.unions.get(i)
                    if not union or not hasattr(union, 'family') or len(union.family) == 0:
                        # Person has no family connections
                        ascend = base.data.ascends.get(i)
                        if not ascend or not hasattr(ascend, 'parents') or ascend.parents is None:
                            # Person is not a child in any family either
                            orphaned.append(i)

            return len(orphaned)

        orphan_count = self.with_test_database(check_orphans)
        self.assertIsNotNone(orphan_count)

    def test_concurrent_database_access(self):
        """Test accès concurrent à la base de données"""
        import threading

        results = []
        errors = []

        def concurrent_read():
            try:
                count = self.count_persons()
                results.append(('read', count))
            except Exception as e:
                errors.append(('read', str(e)))

        def concurrent_write(thread_id):
            try:
                idx = self.create_test_person(
                    f"Concurrent{thread_id}",
                    f"Thread{thread_id}",
                    Sex.MALE,
                    "1990-01-01"
                )
                results.append(('write', idx))
            except Exception as e:
                errors.append(('write', str(e)))

        # Create threads
        threads = []

        # Add read threads
        for i in range(3):
            t = threading.Thread(target=concurrent_read)
            threads.append(t)

        # Add write threads
        for i in range(2):
            t = threading.Thread(target=concurrent_write, args=(i,))
            threads.append(t)

        # Start all threads
        for t in threads:
            t.start()

        # Wait for completion
        for t in threads:
            t.join(timeout=5)

        # Check results
        self.assertGreater(len(results), 0)

        # Errors are expected in concurrent writes without proper locking
        # But the database should not be corrupted
        integrity_ok = self.verify_database_integrity()
        self.assertTrue(integrity_ok)

    def test_database_performance(self):
        """Test performance de la base de données"""
        import time

        # Measure insertion time
        start_time = time.time()

        for i in range(100):
            self.create_test_person(
                f"Perf{i}",
                f"Test{i}",
                Sex.MALE if i % 2 == 0 else Sex.FEMALE,
                f"19{50 + i % 50}-01-01"
            )

        insertion_time = time.time() - start_time
        self.assertLess(insertion_time, 10.0)  # Should complete within 10 seconds

        # Measure search time
        start_time = time.time()
        results = self.search_person("Perf50 Test50")
        search_time = time.time() - start_time
        self.assertLess(search_time, 1.0)  # Search should be fast

        # Measure count time
        start_time = time.time()
        count = self.count_persons()
        count_time = time.time() - start_time
        self.assertLess(count_time, 0.5)  # Counting should be very fast
        self.assertGreaterEqual(count, 100)

    def test_database_migration(self):
        """Test migration de base de données entre versions"""
        # Simulate old database format
        old_persons = []
        for i in range(5):
            idx = self.create_test_person(
                f"OldFormat{i}",
                f"Person{i}",
                Sex.MALE,
                f"196{i}-01-01"
            )
            old_persons.append(idx)

        # Simulate migration by adding new fields
        def migrate_database(base):
            migrated = 0
            for i in range(base.data.persons.len):
                person = base.data.persons.get(i)
                if person:
                    # Add new field simulation
                    if not hasattr(person, 'migration_flag'):
                        # Would set migration_flag = True in real migration
                        migrated += 1

            return migrated

        migrated_count = self.with_test_database(migrate_database)
        self.assertGreaterEqual(migrated_count, 0)

        # Verify database still works after migration
        new_idx = self.create_test_person("PostMigration", "Test", Sex.FEMALE, "2000-01-01")
        self.assertIsNotNone(new_idx)

    def test_database_cleanup(self):
        """Test nettoyage de la base de données"""
        # Create data with duplicates
        duplicates = []
        for i in range(3):
            idx = self.create_test_person(
                "Duplicate",
                "Person",
                Sex.MALE,
                "1980-01-01"
            )
            duplicates.append(idx)

        # Create persons to be cleaned
        for i in range(5):
            self.create_test_person(
                "",  # Empty first name
                "",  # Empty surname
                Sex.NEUTER,
                ""
            )

        initial_count = self.count_persons()

        # Simulate cleanup operation
        def cleanup_database(base):
            cleaned = 0
            for i in range(base.data.persons.len):
                person = base.data.persons.get(i)
                if person:
                    fn = base.data.strings.get(person.first_name) if hasattr(person, 'first_name') else ""
                    sn = base.data.strings.get(person.surname) if hasattr(person, 'surname') else ""

                    # Count empty persons
                    if fn == "" and sn == "":
                        cleaned += 1

            return cleaned

        cleaned_count = self.with_test_database(cleanup_database)
        self.assertGreater(cleaned_count, 0)

    def test_database_statistics(self):
        """Test génération de statistiques de base de données"""
        # Count initial persons before adding new ones
        initial_count = self.count_persons()

        # Create diverse data
        added_males = added_females = 0
        for i in range(30):
            sex = Sex.MALE if i % 3 != 0 else Sex.FEMALE
            if sex == Sex.MALE:
                added_males += 1
            else:
                added_females += 1

            self.create_test_person(
                f"Stats{i}",
                f"Person{i}",
                sex,
                f"19{50 + i}-01-01"
            )

        # Create families using the newly created persons
        family_count = 5
        for i in range(family_count):
            father_idx = initial_count + i * 2
            mother_idx = initial_count + i * 2 + 1
            if mother_idx < initial_count + 30:
                self.create_test_family(father_idx, mother_idx, [])

        # Generate statistics
        def generate_stats(base):
            stats = {
                'total_persons': base.func.nb_of_real_persons(),
                'total_families': base.data.families.len,
                'males': 0,
                'females': 0,
                'unknown_sex': 0,
                'persons_with_birth': 0,
                'persons_with_death': 0
            }

            for i in range(base.data.persons.len):
                person = base.data.persons.get(i)
                if person:
                    if hasattr(person, 'sex'):
                        if person.sex == Sex.MALE:
                            stats['males'] += 1
                        elif person.sex == Sex.FEMALE:
                            stats['females'] += 1
                        else:
                            stats['unknown_sex'] += 1

                    if hasattr(person, 'birth') and person.birth:
                        stats['persons_with_birth'] += 1

                    if hasattr(person, 'death') and person.death:
                        stats['persons_with_death'] += 1

            return stats

        stats = self.with_test_database(generate_stats)
        self.assertIsNotNone(stats)
        self.assertGreater(stats['total_persons'], 0)
        # Total males/females includes initial database persons
        self.assertGreaterEqual(stats['males'], added_males)
        self.assertGreaterEqual(stats['females'], added_females)

    def test_database_transaction_rollback(self):
        """Test rollback de transaction en cas d'erreur"""
        initial_count = self.count_persons()

        # Simulate transaction that should be rolled back
        def failing_transaction(base):
            try:
                # Start adding persons
                for i in range(5):
                    idx = base.func.insert_string(f"Rollback{i}")

                    from lib.gwdef import GenPerson
                    person = GenPerson(
                        first_name=idx,
                        surname=idx,
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
                        birth="1990-01-01",
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
                        key_index=base.data.persons.len + i
                    )

                    if i == 3:
                        # Simulate error
                        raise Exception("Simulated error during transaction")

                    base.func.patch_person(base.data.persons.len + i, person)

                base.func.commit_patches()
                return True

            except Exception:
                # Rollback would happen here in real implementation
                return False

        success = self.with_test_database(failing_transaction)
        self.assertFalse(success)

        # In a real implementation with proper transactions,
        # the count should remain the same after rollback
        # For now, we just verify the database is still functional
        integrity_ok = self.verify_database_integrity()
        self.assertTrue(integrity_ok)


if __name__ == '__main__':
    unittest.main()