"""
Module d'analyse de connectivité
Identifie les composantes connexes (lignées distinctes) dans une base généalogique

Une composante connexe est un groupe de personnes reliées par des liens familiaux.
Identifier les composantes permet de:
- Détecter les lignées distinctes
- Trouver les personnes isolées
- Analyser la structure de la base de données
"""

from typing import Dict, List, Set, Tuple
from collections import deque, defaultdict


class ConnectivityAnalyzer:
    """
    Analyseur de connectivité pour bases généalogiques

    Méthodes:
    - find_connected_components(): Trouver toutes les composantes connexes
    - get_component(person_id): Obtenir la composante d'une personne
    - find_isolated_persons(): Trouver les personnes isolées
    - get_component_statistics(): Statistiques sur les composantes
    """

    def __init__(self, persons: Dict[str, Dict], families: Dict[str, Dict] = None):
        """
        Initialiser l'analyseur

        Args:
            persons: Dict {person_id: {'father_id': ..., 'mother_id': ..., ...}}
            families: Dict optionnel {family_id: {'father_id': ..., 'mother_id': ..., 'children_ids': ...}}
        """
        self.persons = persons
        self.families = families or {}
        self._build_graph()

    def _build_graph(self):
        """Construire le graphe de relations familiales"""
        # Graphe bidirectionnel: adjacency list
        self.graph: Dict[str, Set[str]] = defaultdict(set)

        # Ajouter les relations parent-enfant
        for person_id, person in self.persons.items():
            father_id = person.get('father_id') or person.get('fatherId')
            mother_id = person.get('mother_id') or person.get('motherId')

            if father_id and father_id in self.persons:
                self.graph[person_id].add(father_id)
                self.graph[father_id].add(person_id)

            if mother_id and mother_id in self.persons:
                self.graph[person_id].add(mother_id)
                self.graph[mother_id].add(person_id)

        # Ajouter les relations conjugales depuis les familles
        for family in self.families.values():
            father_id = family.get('father_id') or family.get('husband_id')
            mother_id = family.get('mother_id') or family.get('wife_id')

            if father_id and mother_id:
                if father_id in self.persons and mother_id in self.persons:
                    self.graph[father_id].add(mother_id)
                    self.graph[mother_id].add(father_id)

    def find_connected_components(self) -> List[Set[str]]:
        """
        Trouver toutes les composantes connexes

        Utilise BFS (Breadth-First Search) pour parcourir le graphe

        Returns:
            List[Set[str]]: Liste des composantes (ensembles d'IDs de personnes)
        """
        visited = set()
        components = []

        for person_id in self.persons:
            if person_id not in visited:
                component = self._bfs(person_id, visited)
                components.append(component)

        # Trier par taille décroissante
        components.sort(key=len, reverse=True)
        return components

    def _bfs(self, start_id: str, visited: Set[str]) -> Set[str]:
        """
        BFS pour trouver une composante connexe

        Args:
            start_id: ID de départ
            visited: Ensemble des IDs déjà visités

        Returns:
            Set[str]: Composante connexe contenant start_id
        """
        component = set()
        queue = deque([start_id])

        while queue:
            current_id = queue.popleft()

            if current_id in visited:
                continue

            visited.add(current_id)
            component.add(current_id)

            # Ajouter tous les voisins non visités
            for neighbor_id in self.graph.get(current_id, set()):
                if neighbor_id not in visited:
                    queue.append(neighbor_id)

        return component

    def get_component(self, person_id: str) -> Optional[Set[str]]:
        """
        Obtenir la composante connexe d'une personne

        Args:
            person_id: ID de la personne

        Returns:
            Set[str]: Composante connexe ou None si personne inexistante
        """
        if person_id not in self.persons:
            return None

        visited = set()
        return self._bfs(person_id, visited)

    def find_isolated_persons(self) -> List[str]:
        """
        Trouver les personnes isolées (sans connexion)

        Returns:
            List[str]: Liste des IDs des personnes isolées
        """
        isolated = []

        for person_id in self.persons:
            if not self.graph.get(person_id):
                isolated.append(person_id)

        return isolated

    def get_component_statistics(self) -> Dict:
        """
        Obtenir des statistiques sur les composantes connexes

        Returns:
            Dict avec statistiques détaillées
        """
        components = self.find_connected_components()
        isolated = self.find_isolated_persons()

        if not components:
            return {
                'total_persons': len(self.persons),
                'num_components': 0,
                'num_isolated': len(isolated),
                'largest_component_size': 0,
                'smallest_component_size': 0,
                'average_component_size': 0.0
            }

        component_sizes = [len(c) for c in components]

        stats = {
            'total_persons': len(self.persons),
            'num_components': len(components),
            'num_isolated': len(isolated),
            'largest_component_size': max(component_sizes),
            'smallest_component_size': min(component_sizes),
            'average_component_size': sum(component_sizes) / len(components),
            'component_size_distribution': self._get_size_distribution(component_sizes)
        }

        return stats

    def _get_size_distribution(self, sizes: List[int]) -> Dict[str, int]:
        """Obtenir la distribution des tailles de composantes"""
        distribution = {
            'very_small (1-5)': 0,
            'small (6-20)': 0,
            'medium (21-100)': 0,
            'large (101-500)': 0,
            'very_large (500+)': 0
        }

        for size in sizes:
            if size <= 5:
                distribution['very_small (1-5)'] += 1
            elif size <= 20:
                distribution['small (6-20)'] += 1
            elif size <= 100:
                distribution['medium (21-100)'] += 1
            elif size <= 500:
                distribution['large (101-500)'] += 1
            else:
                distribution['very_large (500+)'] += 1

        return distribution

    def get_component_info(self, component: Set[str]) -> Dict:
        """
        Obtenir des informations détaillées sur une composante

        Args:
            component: Ensemble d'IDs de personnes

        Returns:
            Dict avec informations sur la composante
        """
        if not component:
            return {}

        # Compter les générations
        num_generations = self._estimate_generations(component)

        # Compter les personnes avec/sans parents
        roots = []
        leaves = []

        for person_id in component:
            person = self.persons[person_id]
            father_id = person.get('father_id') or person.get('fatherId')
            mother_id = person.get('mother_id') or person.get('motherId')

            # Root = pas de parents connus dans la composante
            if not father_id and not mother_id:
                roots.append(person_id)

            # Leaf = pas d'enfants connus
            has_children = any(person_id in self.graph.get(child_id, set())
                              for child_id in component if child_id != person_id)
            if not has_children:
                leaves.append(person_id)

        # Compter les mariages
        num_marriages = self._count_marriages(component)

        return {
            'size': len(component),
            'num_roots': len(roots),
            'num_leaves': len(leaves),
            'estimated_generations': num_generations,
            'num_marriages': num_marriages,
            'roots': roots[:10],  # Limiter à 10 pour l'affichage
            'oldest_persons': self._get_oldest_persons(component)[:10]
        }

    def _estimate_generations(self, component: Set[str]) -> int:
        """Estimer le nombre de générations dans une composante"""
        max_depth = 0

        # Trouver les racines (personnes sans parents)
        roots = []
        for person_id in component:
            person = self.persons[person_id]
            father_id = person.get('father_id') or person.get('fatherId')
            mother_id = person.get('mother_id') or person.get('motherId')

            if not father_id and not mother_id:
                roots.append(person_id)

        # Si pas de racines, prendre une personne au hasard
        if not roots:
            roots = [next(iter(component))]

        # BFS pour trouver la profondeur maximale
        for root in roots:
            depth = self._get_max_depth(root, component)
            max_depth = max(max_depth, depth)

        return max_depth

    def _get_max_depth(self, start_id: str, component: Set[str]) -> int:
        """Obtenir la profondeur maximale depuis un nœud"""
        queue = deque([(start_id, 0)])
        visited = set()
        max_depth = 0

        while queue:
            current_id, depth = queue.popleft()

            if current_id in visited:
                continue

            visited.add(current_id)
            max_depth = max(max_depth, depth)

            # Parcourir les enfants seulement (pas remonter aux parents)
            for neighbor_id in self.graph.get(current_id, set()):
                if neighbor_id in component and neighbor_id not in visited:
                    neighbor = self.persons[neighbor_id]
                    father_id = neighbor.get('father_id') or neighbor.get('fatherId')
                    mother_id = neighbor.get('mother_id') or neighbor.get('motherId')

                    # Vérifier que c'est bien un enfant de current_id
                    if father_id == current_id or mother_id == current_id:
                        queue.append((neighbor_id, depth + 1))

        return max_depth

    def _count_marriages(self, component: Set[str]) -> int:
        """Compter le nombre de mariages dans une composante"""
        marriages = set()

        for family in self.families.values():
            father_id = family.get('father_id') or family.get('husband_id')
            mother_id = family.get('mother_id') or family.get('wife_id')

            if father_id in component and mother_id in component:
                # Utiliser un tuple trié pour éviter les doublons
                marriage_key = tuple(sorted([father_id, mother_id]))
                marriages.add(marriage_key)

        return len(marriages)

    def _get_oldest_persons(self, component: Set[str]) -> List[Tuple[str, str]]:
        """Obtenir les personnes les plus anciennes (par date de naissance)"""
        persons_with_birth = []

        for person_id in component:
            person = self.persons[person_id]
            birth_date = person.get('birth_date') or person.get('birthDate')

            if birth_date:
                first_name = person.get('first_name') or person.get('firstName', '')
                last_name = person.get('last_name') or person.get('lastName', '')
                full_name = f"{first_name} {last_name}".strip()

                persons_with_birth.append((person_id, full_name, birth_date))

        # Trier par date de naissance
        persons_with_birth.sort(key=lambda x: x[2])

        return [(pid, name) for pid, name, _ in persons_with_birth]


# Exemple d'utilisation
if __name__ == "__main__":
    # Données de test: 3 familles distinctes
    test_persons = {
        # Famille 1
        'F1_P1': {'id': 'F1_P1', 'first_name': 'Jean', 'last_name': 'Martin'},
        'F1_P2': {'id': 'F1_P2', 'first_name': 'Marie', 'last_name': 'Dupont'},
        'F1_P3': {'id': 'F1_P3', 'first_name': 'Pierre', 'last_name': 'Martin', 'father_id': 'F1_P1', 'mother_id': 'F1_P2'},
        'F1_P4': {'id': 'F1_P4', 'first_name': 'Sophie', 'last_name': 'Martin', 'father_id': 'F1_P1', 'mother_id': 'F1_P2'},

        # Famille 2
        'F2_P1': {'id': 'F2_P1', 'first_name': 'Robert', 'last_name': 'Durand'},
        'F2_P2': {'id': 'F2_P2', 'first_name': 'Alice', 'last_name': 'Bernard'},
        'F2_P3': {'id': 'F2_P3', 'first_name': 'Thomas', 'last_name': 'Durand', 'father_id': 'F2_P1', 'mother_id': 'F2_P2'},

        # Famille 3 (personne isolée)
        'F3_P1': {'id': 'F3_P1', 'first_name': 'Isolé', 'last_name': 'Sans-Famille'},
    }

    test_families = {
        'FAM1': {'id': 'FAM1', 'father_id': 'F1_P1', 'mother_id': 'F1_P2', 'children_ids': ['F1_P3', 'F1_P4']},
        'FAM2': {'id': 'FAM2', 'father_id': 'F2_P1', 'mother_id': 'F2_P2', 'children_ids': ['F2_P3']},
    }

    analyzer = ConnectivityAnalyzer(test_persons, test_families)

    print("=== Analyseur de Connectivité - Test ===\n")

    # Test 1: Trouver les composantes
    print("Test 1: Composantes connexes")
    components = analyzer.find_connected_components()
    print(f"  Nombre de composantes: {len(components)}")
    for i, component in enumerate(components, 1):
        print(f"  Composante {i}: {len(component)} personnes - {component}")

    # Test 2: Personnes isolées
    print("\nTest 2: Personnes isolées")
    isolated = analyzer.find_isolated_persons()
    print(f"  Nombre de personnes isolées: {len(isolated)}")
    print(f"  IDs: {isolated}")

    # Test 3: Statistiques
    print("\nTest 3: Statistiques globales")
    stats = analyzer.get_component_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Test 4: Info détaillée sur la plus grande composante
    if components:
        print("\nTest 4: Détails de la plus grande composante")
        largest = components[0]
        info = analyzer.get_component_info(largest)
        for key, value in info.items():
            print(f"  {key}: {value}")

    # Test 5: Obtenir la composante d'une personne
    print("\nTest 5: Composante d'une personne spécifique (F1_P3)")
    component = analyzer.get_component('F1_P3')
    if component:
        print(f"  Taille de la composante: {len(component)}")
        print(f"  Membres: {component}")
