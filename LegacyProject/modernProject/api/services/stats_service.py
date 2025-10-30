"""
Service pour les statistiques
"""

import sys
import os
from collections import Counter
from typing import List, Dict

# Ajouter le chemin des modules lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from database import Database
from ..models.stats import Statistics, CenturyDistribution, NameDistribution
from .person_service import PersonService
from .family_service import FamilyService


class StatsService:
    """Service pour les statistiques"""

    def __init__(self, db: Database = None):
        # Passer la database partagée aux autres services
        self.person_service = PersonService(db)
        self.family_service = FamilyService(db)

    def get_statistics(self) -> Statistics:
        """Obtenir les statistiques générales"""
        # Récupérer toutes les personnes et familles
        persons = self.person_service.get_all(skip=0, limit=100000)
        families = self.family_service.get_all(skip=0, limit=100000)

        # Compter les totaux
        total_persons = len(persons)
        total_families = len(families)

        # Compter par genre
        total_males = sum(1 for p in persons if p.gender == 'M')
        total_females = sum(1 for p in persons if p.gender == 'F')

        # Compter vivants/décédés
        total_deceased = sum(1 for p in persons if p.death_date is not None)
        total_living = total_persons - total_deceased

        # Années de naissance
        birth_years = [p.birth_date.year for p in persons if p.birth_date]
        oldest_birth_year = min(birth_years) if birth_years else None
        newest_birth_year = max(birth_years) if birth_years else None

        # Distribution par siècle
        century_dist = self._calculate_century_distribution(birth_years)

        # Top noms de famille
        surnames = [p.last_name for p in persons]
        top_surnames = self._calculate_top_names(surnames, limit=10)

        # Top prénoms
        first_names = [p.first_name for p in persons]
        top_first_names = self._calculate_top_names(first_names, limit=10)

        # Moyenne d'enfants par famille
        total_children = sum(len(f.children_ids) for f in families)
        avg_children = total_children / total_families if total_families > 0 else 0.0

        # Générations maximales (estimation simple)
        max_generations = self._estimate_max_generations(persons)

        return Statistics(
            total_persons=total_persons,
            total_families=total_families,
            total_males=total_males,
            total_females=total_females,
            total_living=total_living,
            total_deceased=total_deceased,
            oldest_birth_year=oldest_birth_year,
            newest_birth_year=newest_birth_year,
            century_distribution=century_dist,
            top_surnames=top_surnames,
            top_first_names=top_first_names,
            avg_children_per_family=round(avg_children, 2),
            max_generations=max_generations
        )

    def get_surname_distribution(self, limit: int = 20) -> List[NameDistribution]:
        """Distribution des noms de famille"""
        persons = self.person_service.get_all(skip=0, limit=100000)
        surnames = [p.last_name for p in persons]
        return self._calculate_top_names(surnames, limit)

    def get_firstname_distribution(self, limit: int = 20) -> List[NameDistribution]:
        """Distribution des prénoms"""
        persons = self.person_service.get_all(skip=0, limit=100000)
        first_names = [p.first_name for p in persons]
        return self._calculate_top_names(first_names, limit)

    def get_timeline_distribution(self) -> Dict[str, int]:
        """Distribution temporelle"""
        persons = self.person_service.get_all(skip=0, limit=100000)
        birth_years = [p.birth_date.year for p in persons if p.birth_date]

        # Grouper par décennie
        decades = {}
        for year in birth_years:
            decade = (year // 10) * 10
            decades[f"{decade}s"] = decades.get(f"{decade}s", 0) + 1

        return decades

    def _calculate_century_distribution(self, years: List[int]) -> List[CenturyDistribution]:
        """Calculer la distribution par siècle"""
        centuries = {}
        for year in years:
            century = ((year - 1) // 100) + 1
            century_label = self._get_century_label(century)
            centuries[century_label] = centuries.get(century_label, 0) + 1

        return [
            CenturyDistribution(century=c, count=count)
            for c, count in sorted(centuries.items())
        ]

    def _calculate_top_names(self, names: List[str], limit: int) -> List[NameDistribution]:
        """Calculer le top N des noms"""
        counter = Counter(names)
        top_names = counter.most_common(limit)

        return [
            NameDistribution(name=name, count=count)
            for name, count in top_names
        ]

    def _get_century_label(self, century: int) -> str:
        """Obtenir le label d'un siècle"""
        if century <= 0:
            return f"{abs(century) + 1}ème siècle av. J.-C."
        elif century == 21:
            return "21ème siècle"
        elif century == 20:
            return "20ème siècle"
        elif century == 19:
            return "19ème siècle"
        else:
            return f"{century}ème siècle"

    def _estimate_max_generations(self, persons: List) -> int:
        """Estimer le nombre maximum de générations"""
        # Estimation simple basée sur l'étendue des années de naissance
        birth_years = [p.birth_date.year for p in persons if p.birth_date]
        if not birth_years:
            return 0

        year_range = max(birth_years) - min(birth_years)
        # Assumer 25-30 ans par génération
        generations = year_range // 27
        return max(1, generations)
