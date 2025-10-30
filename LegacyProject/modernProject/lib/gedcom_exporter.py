"""
Exporteur GEDCOM pour export de données généalogiques
Génère des fichiers GEDCOM 5.5.1 compatibles avec les logiciels de généalogie standard
"""

from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass


class GedcomExporter:
    """
    Exporteur pour générer des fichiers GEDCOM

    Format GEDCOM:
    - Niveau 0: Enregistrements principaux (HEAD, INDI, FAM, TRLR)
    - Niveau 1: Tags principaux
    - Niveau 2: Sous-tags (détails)
    """

    def __init__(self, source: str = "AWKWARD LEGACY"):
        self.source = source
        self.lines: List[str] = []

    def export_to_file(self, persons: List[Dict], families: List[Dict], filepath: str):
        """Exporter vers un fichier GEDCOM"""
        content = self.export_to_string(persons, families)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def export_to_string(self, persons: List[Dict], families: List[Dict]) -> str:
        """Exporter vers une chaîne GEDCOM"""
        self.lines = []

        # En-tête
        self._write_header()

        # Personnes
        for person in persons:
            self._write_person(person)

        # Familles
        for family in families:
            self._write_family(family)

        # Pied de page
        self._write_trailer()

        return '\n'.join(self.lines)

    def _write_header(self):
        """Écrire l'en-tête GEDCOM"""
        self._add_line(0, "HEAD")
        self._add_line(1, "SOUR", self.source)
        self._add_line(2, "VERS", "1.0.0")
        self._add_line(2, "NAME", "AWKWARD LEGACY")
        self._add_line(1, "DATE", datetime.now().strftime("%d %b %Y").upper())
        self._add_line(1, "FILE", "export.ged")
        self._add_line(1, "GEDC")
        self._add_line(2, "VERS", "5.5.1")
        self._add_line(2, "FORM", "LINEAGE-LINKED")
        self._add_line(1, "CHAR", "UTF-8")
        self._add_line(1, "LANG", "French")

    def _write_person(self, person: Dict):
        """
        Écrire une personne au format GEDCOM

        Champs attendus:
        - id: Identifiant unique
        - first_name: Prénom
        - last_name: Nom de famille
        - gender: M/F/U
        - birth_date: Date de naissance (ISO ou GEDCOM)
        - birth_place: Lieu de naissance
        - death_date: Date de décès
        - death_place: Lieu de décès
        - occupation: Profession
        - notes: Notes
        - father_id: ID du père
        - mother_id: ID de la mère
        """
        person_id = person.get('id', person.get('ID'))
        if not person_id:
            return

        # Ligne INDI
        self._add_line(0, f"@{person_id}@", "INDI")

        # Nom
        first_name = person.get('first_name', person.get('firstName', ''))
        last_name = person.get('last_name', person.get('lastName', ''))
        if first_name or last_name:
            name = f"{first_name} /{last_name}/"
            self._add_line(1, "NAME", name)

        # Genre
        gender = person.get('gender', person.get('sex'))
        if gender:
            gender_code = gender.upper()
            if gender_code in ['M', 'F', 'U']:
                self._add_line(1, "SEX", gender_code)

        # Naissance
        birth_date = person.get('birth_date', person.get('birthDate'))
        birth_place = person.get('birth_place', person.get('birthPlace'))
        if birth_date or birth_place:
            self._add_line(1, "BIRT")
            if birth_date:
                self._add_line(2, "DATE", self._format_date(birth_date))
            if birth_place:
                self._add_line(2, "PLAC", birth_place)

        # Décès
        death_date = person.get('death_date', person.get('deathDate'))
        death_place = person.get('death_place', person.get('deathPlace'))
        if death_date or death_place:
            self._add_line(1, "DEAT")
            if death_date:
                self._add_line(2, "DATE", self._format_date(death_date))
            if death_place:
                self._add_line(2, "PLAC", death_place)

        # Profession
        occupation = person.get('occupation', person.get('occu'))
        if occupation:
            self._add_line(1, "OCCU", occupation)

        # Notes
        notes = person.get('notes', '')
        if notes:
            if isinstance(notes, list):
                for note in notes:
                    self._add_line(1, "NOTE", note)
            else:
                self._add_line(1, "NOTE", notes)

        # Famille en tant qu'enfant
        father_id = person.get('father_id', person.get('fatherId'))
        mother_id = person.get('mother_id', person.get('motherId'))
        if father_id or mother_id:
            # Trouver la famille correspondante
            # Pour l'instant, on génère un ID de famille basé sur les parents
            family_id = self._get_family_id(father_id, mother_id)
            self._add_line(1, "FAMC", f"@{family_id}@")

    def _write_family(self, family: Dict):
        """
        Écrire une famille au format GEDCOM

        Champs attendus:
        - id: Identifiant unique
        - father_id / husband_id: ID du père/mari
        - mother_id / wife_id: ID de la mère/femme
        - children_ids: Liste des IDs d'enfants
        - marriage_date: Date de mariage
        - marriage_place: Lieu de mariage
        - divorce_date: Date de divorce
        - notes: Notes
        """
        family_id = family.get('id', family.get('ID'))
        if not family_id:
            return

        # Ligne FAM
        self._add_line(0, f"@{family_id}@", "FAM")

        # Mari
        husband_id = family.get('father_id', family.get('husband_id', family.get('fatherId')))
        if husband_id:
            self._add_line(1, "HUSB", f"@{husband_id}@")

        # Femme
        wife_id = family.get('mother_id', family.get('wife_id', family.get('motherId')))
        if wife_id:
            self._add_line(1, "WIFE", f"@{wife_id}@")

        # Enfants
        children_ids = family.get('children_ids', family.get('childrenIds', []))
        if children_ids:
            for child_id in children_ids:
                self._add_line(1, "CHIL", f"@{child_id}@")

        # Mariage
        marriage_date = family.get('marriage_date', family.get('marriageDate'))
        marriage_place = family.get('marriage_place', family.get('marriagePlace'))
        if marriage_date or marriage_place:
            self._add_line(1, "MARR")
            if marriage_date:
                self._add_line(2, "DATE", self._format_date(marriage_date))
            if marriage_place:
                self._add_line(2, "PLAC", marriage_place)

        # Divorce
        divorce_date = family.get('divorce_date', family.get('divorceDate'))
        if divorce_date:
            self._add_line(1, "DIV")
            self._add_line(2, "DATE", self._format_date(divorce_date))

        # Notes
        notes = family.get('notes', '')
        if notes:
            if isinstance(notes, list):
                for note in notes:
                    self._add_line(1, "NOTE", note)
            else:
                self._add_line(1, "NOTE", notes)

    def _write_trailer(self):
        """Écrire le pied de page GEDCOM"""
        self._add_line(0, "TRLR")

    def _add_line(self, level: int, tag: str, value: str = ""):
        """Ajouter une ligne GEDCOM"""
        if value:
            line = f"{level} {tag} {value}"
        else:
            line = f"{level} {tag}"
        self.lines.append(line)

    def _format_date(self, date_value: str) -> str:
        """
        Formatter une date au format GEDCOM
        Entrée: ISO 8601 (YYYY-MM-DD) ou format GEDCOM
        Sortie: Format GEDCOM (DD MMM YYYY)
        """
        if not date_value:
            return ""

        # Si déjà au format GEDCOM, retourner tel quel
        if any(month in date_value.upper() for month in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                                                          'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']):
            return date_value

        # Essayer de parser ISO 8601
        try:
            if 'T' in date_value:
                # Format datetime ISO
                dt = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
            else:
                # Format date ISO
                parts = date_value.split('-')
                if len(parts) == 3:
                    year, month, day = parts
                    dt = datetime(int(year), int(month), int(day))
                elif len(parts) == 2:
                    year, month = parts
                    dt = datetime(int(year), int(month), 1)
                else:
                    # Juste l'année
                    return date_value

            # Formatter en GEDCOM
            months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                     'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
            return f"{dt.day} {months[dt.month - 1]} {dt.year}"

        except (ValueError, IndexError):
            # Si parsing échoue, retourner la valeur originale
            return date_value

    def _get_family_id(self, father_id: Optional[str], mother_id: Optional[str]) -> str:
        """Générer un ID de famille basé sur les parents"""
        if father_id and mother_id:
            return f"F_{father_id}_{mother_id}"
        elif father_id:
            return f"F_{father_id}"
        elif mother_id:
            return f"F_{mother_id}"
        else:
            return "F_UNKNOWN"


# Exemple d'utilisation
if __name__ == "__main__":
    # Données de test
    persons = [
        {
            'id': 'I1',
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': 'M',
            'birth_date': '1950-01-01',
            'birth_place': 'New York, USA',
            'father_id': 'I3',
            'mother_id': 'I4'
        },
        {
            'id': 'I2',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'gender': 'F',
            'birth_date': '1952-03-15',
            'birth_place': 'Boston, USA',
            'father_id': 'I3',
            'mother_id': 'I4'
        },
        {
            'id': 'I3',
            'first_name': 'Robert',
            'last_name': 'Doe',
            'gender': 'M',
            'birth_date': '1920-06-10',
            'birth_place': 'London, UK',
            'death_date': '2005-12-05',
            'death_place': 'New York, USA'
        },
        {
            'id': 'I4',
            'first_name': 'Mary',
            'last_name': 'Johnson',
            'gender': 'F',
            'birth_date': '1925-08-25',
            'birth_place': 'Paris, France'
        }
    ]

    families = [
        {
            'id': 'F1',
            'father_id': 'I3',
            'mother_id': 'I4',
            'children_ids': ['I1', 'I2'],
            'marriage_date': '1945-06-20',
            'marriage_place': 'New York, USA'
        }
    ]

    # Exporter
    exporter = GedcomExporter()
    gedcom_content = exporter.export_to_string(persons, families)

    print("=== GEDCOM Exporter Test ===\n")
    print(gedcom_content)

    # Sauvegarder dans un fichier
    # exporter.export_to_file(persons, families, "test_export.ged")
    # print("\n✅ Export sauvegardé dans test_export.ged")
