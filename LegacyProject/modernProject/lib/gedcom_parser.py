"""
Parser GEDCOM pour import de fichiers généalogiques
GEDCOM = Genealogical Data Communication (format standard)

Support des versions GEDCOM 5.5 et 5.5.1
"""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class GedcomPerson:
    """Représente une personne dans un fichier GEDCOM"""
    id: str
    first_name: str = ""
    last_name: str = ""
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    birth_place: Optional[str] = None
    death_date: Optional[str] = None
    death_place: Optional[str] = None
    occupation: Optional[str] = None
    notes: List[str] = field(default_factory=list)
    father_id: Optional[str] = None
    mother_id: Optional[str] = None
    families_spouse: List[str] = field(default_factory=list)
    families_child: List[str] = field(default_factory=list)


@dataclass
class GedcomFamily:
    """Représente une famille dans un fichier GEDCOM"""
    id: str
    husband_id: Optional[str] = None
    wife_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    marriage_date: Optional[str] = None
    marriage_place: Optional[str] = None
    divorce_date: Optional[str] = None
    notes: List[str] = field(default_factory=list)


class GedcomParser:
    """
    Parser pour fichiers GEDCOM

    Format GEDCOM basique:
    0 @I1@ INDI
    1 NAME John /Doe/
    1 SEX M
    1 BIRT
    2 DATE 1 JAN 1950
    2 PLAC New York, USA
    1 DEAT
    2 DATE 31 DEC 2020
    """

    def __init__(self):
        self.persons: Dict[str, GedcomPerson] = {}
        self.families: Dict[str, GedcomFamily] = {}
        self.current_person: Optional[GedcomPerson] = None
        self.current_family: Optional[GedcomFamily] = None
        self.current_context: List[str] = []

    def parse_file(self, filepath: str) -> Tuple[Dict[str, GedcomPerson], Dict[str, GedcomFamily]]:
        """Parse un fichier GEDCOM et retourne les personnes et familles"""
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()

        self._parse_lines(lines)
        self._link_families()

        return self.persons, self.families

    def parse_string(self, content: str) -> Tuple[Dict[str, GedcomPerson], Dict[str, GedcomFamily]]:
        """Parse une chaîne GEDCOM"""
        lines = content.split('\n')
        self._parse_lines(lines)
        self._link_families()

        return self.persons, self.families

    def _parse_lines(self, lines: List[str]):
        """Parse les lignes du fichier GEDCOM"""
        for line in lines:
            line = line.strip()
            if not line:
                continue

            level, tag, value = self._parse_line(line)

            if level == 0:
                self._handle_level_0(tag, value)
            elif level == 1:
                self._handle_level_1(tag, value)
            elif level == 2:
                self._handle_level_2(tag, value)

    def _parse_line(self, line: str) -> Tuple[int, str, str]:
        """
        Parse une ligne GEDCOM
        Format: LEVEL [ID] TAG [VALUE]
        Exemple: 0 @I1@ INDI
                 1 NAME John /Doe/
                 2 DATE 1 JAN 1950
        """
        parts = line.split(None, 2)
        level = int(parts[0])

        if len(parts) < 2:
            return level, "", ""

        # Vérifier si c'est un ID (format @XXX@)
        if parts[1].startswith('@') and parts[1].endswith('@'):
            tag = parts[2] if len(parts) > 2 else ""
            value = parts[1]  # L'ID est la valeur
        else:
            tag = parts[1]
            value = parts[2] if len(parts) > 2 else ""

        return level, tag, value

    def _handle_level_0(self, tag: str, value: str):
        """Traite les tags de niveau 0 (INDI, FAM, etc.)"""
        if tag == "INDI":
            # Nouvelle personne
            person_id = value.strip('@')
            self.current_person = GedcomPerson(id=person_id)
            self.persons[person_id] = self.current_person
            self.current_family = None
            self.current_context = ['INDI']

        elif tag == "FAM":
            # Nouvelle famille
            family_id = value.strip('@')
            self.current_family = GedcomFamily(id=family_id)
            self.families[family_id] = self.current_family
            self.current_person = None
            self.current_context = ['FAM']

        else:
            self.current_person = None
            self.current_family = None
            self.current_context = []

    def _handle_level_1(self, tag: str, value: str):
        """Traite les tags de niveau 1"""
        if self.current_person:
            self._handle_person_tag(tag, value)
        elif self.current_family:
            self._handle_family_tag(tag, value)

        # Mettre à jour le contexte
        if len(self.current_context) > 1:
            self.current_context = self.current_context[:1]
        self.current_context.append(tag)

    def _handle_level_2(self, tag: str, value: str):
        """Traite les tags de niveau 2 (sous-tags)"""
        if not self.current_context:
            return

        parent_tag = self.current_context[-1] if len(self.current_context) > 0 else ""

        if self.current_person:
            if parent_tag == "BIRT":
                if tag == "DATE":
                    self.current_person.birth_date = self._parse_date(value)
                elif tag == "PLAC":
                    self.current_person.birth_place = value

            elif parent_tag == "DEAT":
                if tag == "DATE":
                    self.current_person.death_date = self._parse_date(value)
                elif tag == "PLAC":
                    self.current_person.death_place = value

        elif self.current_family:
            if parent_tag == "MARR":
                if tag == "DATE":
                    self.current_family.marriage_date = self._parse_date(value)
                elif tag == "PLAC":
                    self.current_family.marriage_place = value

            elif parent_tag == "DIV":
                if tag == "DATE":
                    self.current_family.divorce_date = self._parse_date(value)

    def _handle_person_tag(self, tag: str, value: str):
        """Traite les tags spécifiques aux personnes"""
        if tag == "NAME":
            self._parse_name(value)

        elif tag == "SEX":
            gender = value.strip().upper()
            if gender in ['M', 'F']:
                self.current_person.gender = gender
            else:
                self.current_person.gender = 'U'  # Unknown

        elif tag == "OCCU":
            self.current_person.occupation = value

        elif tag == "NOTE":
            self.current_person.notes.append(value)

        elif tag == "FAMC":
            # Famille dont cette personne est un enfant
            family_id = value.strip('@')
            self.current_person.families_child.append(family_id)

        elif tag == "FAMS":
            # Famille où cette personne est un conjoint
            family_id = value.strip('@')
            self.current_person.families_spouse.append(family_id)

    def _handle_family_tag(self, tag: str, value: str):
        """Traite les tags spécifiques aux familles"""
        if tag == "HUSB":
            self.current_family.husband_id = value.strip('@')

        elif tag == "WIFE":
            self.current_family.wife_id = value.strip('@')

        elif tag == "CHIL":
            child_id = value.strip('@')
            self.current_family.children_ids.append(child_id)

        elif tag == "NOTE":
            self.current_family.notes.append(value)

    def _parse_name(self, name_value: str):
        """
        Parse un nom GEDCOM
        Format: Prénom /Nom de famille/
        Exemple: John William /Doe/
        """
        match = re.match(r'^(.*?)\s*/([^/]*)/(.*)$', name_value)
        if match:
            first_name = match.group(1).strip()
            last_name = match.group(2).strip()
            # group(3) serait un suffixe (Jr., III, etc.)

            self.current_person.first_name = first_name
            self.current_person.last_name = last_name
        else:
            # Pas de format standard, tout mettre dans first_name
            self.current_person.first_name = name_value.strip()

    def _parse_date(self, date_value: str) -> Optional[str]:
        """
        Parse une date GEDCOM et la convertit en ISO 8601
        Formats GEDCOM:
        - 1 JAN 1950
        - JAN 1950
        - 1950
        - ABT 1950 (about)
        - BEF 1950 (before)
        - AFT 1950 (after)
        """
        date_value = date_value.strip()

        # Supprimer les préfixes (ABT, BEF, AFT, etc.)
        for prefix in ['ABT', 'BEF', 'AFT', 'CAL', 'EST']:
            if date_value.startswith(prefix):
                date_value = date_value[len(prefix):].strip()

        # Essayer de parser la date
        months = {
            'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04',
            'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
            'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
        }

        parts = date_value.split()

        if len(parts) == 3:
            # Format: 1 JAN 1950
            day, month, year = parts
            month_num = months.get(month.upper(), '01')
            try:
                return f"{year}-{month_num}-{int(day):02d}"
            except ValueError:
                return None

        elif len(parts) == 2:
            # Format: JAN 1950
            month, year = parts
            month_num = months.get(month.upper(), '01')
            return f"{year}-{month_num}-01"

        elif len(parts) == 1:
            # Format: 1950
            return f"{parts[0]}-01-01"

        return None

    def _link_families(self):
        """Lie les personnes aux familles pour établir les relations parent-enfant"""
        for family in self.families.values():
            # Lier les enfants à leurs parents
            for child_id in family.children_ids:
                if child_id in self.persons:
                    child = self.persons[child_id]
                    if family.husband_id:
                        child.father_id = family.husband_id
                    if family.wife_id:
                        child.mother_id = family.wife_id

    def get_statistics(self) -> Dict[str, int]:
        """Obtenir des statistiques sur les données parsées"""
        males = sum(1 for p in self.persons.values() if p.gender == 'M')
        females = sum(1 for p in self.persons.values() if p.gender == 'F')
        with_birth = sum(1 for p in self.persons.values() if p.birth_date)
        with_death = sum(1 for p in self.persons.values() if p.death_date)

        return {
            'total_persons': len(self.persons),
            'total_families': len(self.families),
            'males': males,
            'females': females,
            'with_birth_date': with_birth,
            'with_death_date': with_death,
            'living': len(self.persons) - with_death
        }


# Exemple d'utilisation
if __name__ == "__main__":
    # Test avec un exemple GEDCOM
    sample_gedcom = """
0 HEAD
1 SOUR GeneWeb
1 GEDC
2 VERS 5.5.1
0 @I1@ INDI
1 NAME John /Doe/
1 SEX M
1 BIRT
2 DATE 1 JAN 1950
2 PLAC New York, USA
1 FAMC @F1@
0 @I2@ INDI
1 NAME Jane /Smith/
1 SEX F
1 BIRT
2 DATE 15 MAR 1952
2 PLAC Boston, USA
1 FAMC @F1@
0 @I3@ INDI
1 NAME Robert /Doe/
1 SEX M
1 BIRT
2 DATE 10 JUN 1920
2 PLAC London, UK
1 DEAT
2 DATE 5 DEC 2005
2 PLAC New York, USA
1 FAMS @F1@
0 @I4@ INDI
1 NAME Mary /Johnson/
1 SEX F
1 BIRT
2 DATE 25 AUG 1925
2 PLAC Paris, France
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I3@
1 WIFE @I4@
1 CHIL @I1@
1 CHIL @I2@
1 MARR
2 DATE 20 JUN 1945
2 PLAC New York, USA
0 TRLR
"""

    parser = GedcomParser()
    persons, families = parser.parse_string(sample_gedcom)

    print("=== GEDCOM Parser Test ===")
    print(f"\nPersons found: {len(persons)}")
    for person_id, person in persons.items():
        print(f"\n{person_id}: {person.first_name} {person.last_name}")
        print(f"  Gender: {person.gender}")
        print(f"  Birth: {person.birth_date} at {person.birth_place}")
        if person.death_date:
            print(f"  Death: {person.death_date} at {person.death_place}")
        if person.father_id:
            print(f"  Father: {person.father_id}")
        if person.mother_id:
            print(f"  Mother: {person.mother_id}")

    print(f"\n\nFamilies found: {len(families)}")
    for family_id, family in families.items():
        print(f"\n{family_id}:")
        print(f"  Husband: {family.husband_id}")
        print(f"  Wife: {family.wife_id}")
        print(f"  Children: {', '.join(family.children_ids)}")
        if family.marriage_date:
            print(f"  Marriage: {family.marriage_date} at {family.marriage_place}")

    stats = parser.get_statistics()
    print(f"\n\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
