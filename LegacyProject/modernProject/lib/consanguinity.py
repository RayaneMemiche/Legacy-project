"""
Module de calcul de consanguinité
Calcule les coefficients de parenté et de consanguinité entre individus

La consanguinité mesure la probabilité qu'un individu hérite du même allèle
de ses deux parents. C'est crucial pour l'analyse généalogique et la détection
d'héritiers légitimes.
"""

from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict, deque


class ConsanguinityCalculator:
    """
    Calculateur de consanguinité et de degrés de parenté

    Méthodes:
    - calculate_kinship(person1_id, person2_id): Coefficient de parenté
    - calculate_consanguinity(person_id): Coefficient de consanguinité
    - get_relationship_degree(person1_id, person2_id): Degré de parenté
    - find_common_ancestors(person1_id, person2_id): Ancêtres communs
    """

    def __init__(self, persons: Dict[str, Dict]):
        """
        Initialiser avec un dictionnaire de personnes

        Args:
            persons: Dict {person_id: {'father_id': ..., 'mother_id': ..., ...}}
        """
        self.persons = persons
        self._kinship_cache: Dict[Tuple[str, str], float] = {}
        self._build_indices()

    def _build_indices(self):
        """Construire des index pour accélérer les calculs"""
        # Index des enfants par parent
        self.children_by_parent: Dict[str, Set[str]] = defaultdict(set)

        for person_id, person in self.persons.items():
            father_id = person.get('father_id') or person.get('fatherId')
            mother_id = person.get('mother_id') or person.get('motherId')

            if father_id:
                self.children_by_parent[father_id].add(person_id)
            if mother_id:
                self.children_by_parent[mother_id].add(person_id)

    def calculate_kinship(self, person1_id: str, person2_id: str) -> float:
        """
        Calculer le coefficient de parenté entre deux personnes

        Le coefficient de parenté φ(i,j) est la probabilité que deux allèles
        tirés au hasard chez i et j soient identiques par descendance.

        Formule récursive:
        - φ(i,i) = 1/2 * (1 + F_i) où F_i est le coefficient de consanguinité de i
        - φ(i,j) = 1/2 * [φ(père_i, j) + φ(mère_i, j)]

        Returns:
            float: Coefficient de parenté (0 à 0.5)
        """
        # Vérifier le cache
        cache_key = tuple(sorted([person1_id, person2_id]))
        if cache_key in self._kinship_cache:
            return self._kinship_cache[cache_key]

        # Calculer
        result = self._calculate_kinship_recursive(person1_id, person2_id)
        self._kinship_cache[cache_key] = result
        return result

    def _calculate_kinship_recursive(self, person1_id: str, person2_id: str) -> float:
        """Calcul récursif du coefficient de parenté"""
        # Cas de base: personnes inexistantes
        if person1_id not in self.persons or person2_id not in self.persons:
            return 0.0

        # Cas spécial: même personne
        if person1_id == person2_id:
            consang = self.calculate_consanguinity(person1_id)
            return 0.5 * (1 + consang)

        # S'assurer que person1 est le "plus jeune" (a des parents)
        person1 = self.persons[person1_id]
        person2 = self.persons[person2_id]

        father1_id = person1.get('father_id') or person1.get('fatherId')
        mother1_id = person1.get('mother_id') or person1.get('motherId')

        # Si person1 n'a pas de parents, il n'y a pas de parenté
        if not father1_id and not mother1_id:
            return 0.0

        # Formule récursive: φ(i,j) = 1/2 * [φ(père_i, j) + φ(mère_i, j)]
        kinship_father = 0.0
        kinship_mother = 0.0

        if father1_id:
            kinship_father = self.calculate_kinship(father1_id, person2_id)
        if mother1_id:
            kinship_mother = self.calculate_kinship(mother1_id, person2_id)

        return 0.5 * (kinship_father + kinship_mother)

    def calculate_consanguinity(self, person_id: str) -> float:
        """
        Calculer le coefficient de consanguinité d'une personne

        Le coefficient de consanguinité F est la probabilité qu'un individu
        hérite du même allèle de ses deux parents.

        F = φ(père, mère)

        Returns:
            float: Coefficient de consanguinité (0 à 1)
                   0 = pas de consanguinité
                   0.0625 = cousins germains
                   0.125 = demi-frères/sœurs, oncle-nièce
                   0.25 = frères/sœurs
        """
        if person_id not in self.persons:
            return 0.0

        person = self.persons[person_id]
        father_id = person.get('father_id') or person.get('fatherId')
        mother_id = person.get('mother_id') or person.get('motherId')

        if not father_id or not mother_id:
            return 0.0

        # F = φ(père, mère)
        return self.calculate_kinship(father_id, mother_id)

    def get_relationship_degree(self, person1_id: str, person2_id: str) -> Optional[Tuple[int, int]]:
        """
        Déterminer le degré de parenté entre deux personnes

        Returns:
            Tuple[int, int]: (degré_ascendant, degré_descendant)
            ou None si pas de relation

        Exemples:
        - (1, 1) = frères/sœurs
        - (2, 2) = cousins germains
        - (1, 0) = parent-enfant
        - (2, 0) = grand-parent/petit-enfant
        - (2, 1) = oncle/neveu
        """
        if person1_id == person2_id:
            return (0, 0)

        # Trouver les ancêtres communs
        common_ancestors = self.find_common_ancestors(person1_id, person2_id)
        if not common_ancestors:
            return None

        # Trouver le chemin le plus court
        min_degree = None
        for ancestor_id in common_ancestors:
            degree1 = self._get_generation_distance(ancestor_id, person1_id)
            degree2 = self._get_generation_distance(ancestor_id, person2_id)

            if degree1 is not None and degree2 is not None:
                if min_degree is None or (degree1 + degree2) < sum(min_degree):
                    min_degree = (degree1, degree2)

        return min_degree

    def find_common_ancestors(self, person1_id: str, person2_id: str) -> Set[str]:
        """
        Trouver tous les ancêtres communs à deux personnes

        Returns:
            Set[str]: Ensemble des IDs des ancêtres communs
        """
        ancestors1 = self._get_all_ancestors(person1_id)
        ancestors2 = self._get_all_ancestors(person2_id)

        return ancestors1.intersection(ancestors2)

    def _get_all_ancestors(self, person_id: str) -> Set[str]:
        """Obtenir tous les ancêtres d'une personne"""
        ancestors = set()
        queue = deque([person_id])

        while queue:
            current_id = queue.popleft()
            if current_id not in self.persons:
                continue

            person = self.persons[current_id]
            father_id = person.get('father_id') or person.get('fatherId')
            mother_id = person.get('mother_id') or person.get('motherId')

            if father_id and father_id not in ancestors:
                ancestors.add(father_id)
                queue.append(father_id)

            if mother_id and mother_id not in ancestors:
                ancestors.add(mother_id)
                queue.append(mother_id)

        return ancestors

    def _get_generation_distance(self, ancestor_id: str, descendant_id: str) -> Optional[int]:
        """
        Calculer la distance générationnelle entre un ancêtre et un descendant

        Returns:
            int: Nombre de générations (0 = même personne, 1 = parent-enfant, etc.)
            None: Si pas de relation directe
        """
        if ancestor_id == descendant_id:
            return 0

        queue = deque([(descendant_id, 0)])
        visited = set()

        while queue:
            current_id, distance = queue.popleft()

            if current_id == ancestor_id:
                return distance

            if current_id in visited:
                continue
            visited.add(current_id)

            if current_id not in self.persons:
                continue

            person = self.persons[current_id]
            father_id = person.get('father_id') or person.get('fatherId')
            mother_id = person.get('mother_id') or person.get('motherId')

            if father_id:
                queue.append((father_id, distance + 1))
            if mother_id:
                queue.append((mother_id, distance + 1))

        return None

    def get_relationship_name(self, person1_id: str, person2_id: str) -> str:
        """
        Obtenir le nom de la relation en français

        Returns:
            str: Nom de la relation (ex: "cousins germains", "oncle/neveu")
        """
        if person1_id == person2_id:
            return "même personne"

        degree = self.get_relationship_degree(person1_id, person2_id)
        if degree is None:
            return "aucune relation"

        deg1, deg2 = degree

        # Relations directes
        if deg1 == 0 and deg2 == 1:
            return "parent-enfant"
        elif deg1 == 1 and deg2 == 0:
            return "enfant-parent"
        elif deg1 == 0 and deg2 == 2:
            return "grand-parent/petit-enfant"
        elif deg1 == 2 and deg2 == 0:
            return "petit-enfant/grand-parent"

        # Frères et sœurs
        elif deg1 == 1 and deg2 == 1:
            return "frères/sœurs"

        # Oncles/tantes et neveux/nièces
        elif (deg1 == 2 and deg2 == 1) or (deg1 == 1 and deg2 == 2):
            return "oncle-tante/neveu-nièce"

        # Cousins
        elif deg1 == deg2:
            if deg1 == 2:
                return "cousins germains"
            elif deg1 == 3:
                return "cousins issus de germains"
            elif deg1 == 4:
                return "cousins au 3ème degré"
            else:
                return f"cousins au {deg1 - 1}ème degré"

        # Relation complexe
        else:
            return f"relation au {deg1}ème et {deg2}ème degré"

    def analyze_population_consanguinity(self) -> Dict:
        """
        Analyser la consanguinité de toute la population

        Returns:
            Dict avec statistiques de consanguinité
        """
        consanguinity_values = []
        consanguinous_count = 0

        for person_id in self.persons:
            f = self.calculate_consanguinity(person_id)
            if f > 0:
                consanguinity_values.append(f)
                consanguinous_count += 1

        if not consanguinity_values:
            return {
                'total_persons': len(self.persons),
                'consanguinous_persons': 0,
                'consanguinity_rate': 0.0,
                'average_consanguinity': 0.0,
                'max_consanguinity': 0.0
            }

        return {
            'total_persons': len(self.persons),
            'consanguinous_persons': consanguinous_count,
            'consanguinity_rate': consanguinous_count / len(self.persons),
            'average_consanguinity': sum(consanguinity_values) / len(consanguinity_values),
            'max_consanguinity': max(consanguinity_values),
            'min_consanguinity': min(v for v in consanguinity_values if v > 0)
        }


# Exemple d'utilisation
if __name__ == "__main__":
    # Données de test: famille avec consanguinité
    test_persons = {
        'I1': {'id': 'I1', 'first_name': 'Grand-Père'},  # Fondateur
        'I2': {'id': 'I2', 'first_name': 'Grand-Mère'},  # Fondatrice
        'I3': {'id': 'I3', 'first_name': 'Fils1', 'father_id': 'I1', 'mother_id': 'I2'},
        'I4': {'id': 'I4', 'first_name': 'Fille1', 'father_id': 'I1', 'mother_id': 'I2'},
        'I5': {'id': 'I5', 'first_name': 'Conjoint-Fils1'},  # Non apparenté
        'I6': {'id': 'I6', 'first_name': 'Conjoint-Fille1'},  # Non apparenté
        'I7': {'id': 'I7', 'first_name': 'Petit-Fils1', 'father_id': 'I3', 'mother_id': 'I5'},
        'I8': {'id': 'I8', 'first_name': 'Petite-Fille1', 'father_id': 'I6', 'mother_id': 'I4'},
        # Mariage de cousins germains
        'I9': {'id': 'I9', 'first_name': 'Enfant-Cousins', 'father_id': 'I7', 'mother_id': 'I8'},
    }

    calc = ConsanguinityCalculator(test_persons)

    print("=== Calculateur de Consanguinité - Test ===\n")

    # Test 1: Cousins germains
    print("Test 1: Degré de parenté entre cousins germains (I7 et I8)")
    degree = calc.get_relationship_degree('I7', 'I8')
    print(f"  Degré: {degree}")
    print(f"  Relation: {calc.get_relationship_name('I7', 'I8')}")
    kinship = calc.calculate_kinship('I7', 'I8')
    print(f"  Coefficient de parenté: {kinship:.4f} (attendu: 0.0625 pour cousins germains)")

    # Test 2: Consanguinité de l'enfant de cousins germains
    print("\nTest 2: Consanguinité de l'enfant de cousins germains (I9)")
    consang = calc.calculate_consanguinity('I9')
    print(f"  Coefficient de consanguinité: {consang:.4f} (attendu: 0.0625)")

    # Test 3: Frères et sœurs
    print("\nTest 3: Relation frères/sœurs (I3 et I4)")
    degree = calc.get_relationship_degree('I3', 'I4')
    print(f"  Degré: {degree}")
    print(f"  Relation: {calc.get_relationship_name('I3', 'I4')}")
    kinship = calc.calculate_kinship('I3', 'I4')
    print(f"  Coefficient de parenté: {kinship:.4f} (attendu: 0.25 pour frères/sœurs)")

    # Test 4: Ancêtres communs
    print("\nTest 4: Ancêtres communs de I7 et I8")
    ancestors = calc.find_common_ancestors('I7', 'I8')
    print(f"  Ancêtres communs: {ancestors}")

    # Test 5: Analyse de population
    print("\nTest 5: Analyse de la population")
    stats = calc.analyze_population_consanguinity()
    print(f"  Total personnes: {stats['total_persons']}")
    print(f"  Personnes consanguines: {stats['consanguinous_persons']}")
    print(f"  Taux de consanguinité: {stats['consanguinity_rate']:.2%}")
    if stats['consanguinous_persons'] > 0:
        print(f"  Consanguinité moyenne: {stats['average_consanguinity']:.4f}")
        print(f"  Consanguinité max: {stats['max_consanguinity']:.4f}")
