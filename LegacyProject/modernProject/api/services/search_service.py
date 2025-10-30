"""
Service pour la recherche avancée
"""

import sys
import os
from typing import List

# Ajouter le chemin des modules lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from database import Database
from ..models.search import SearchQuery, SearchResponse
from ..models.person import PersonResponse
from .person_service import PersonService


class SearchService:
    """Service pour la recherche avancée"""

    def __init__(self, db: Database = None):
        # Passer la database partagée au PersonService
        self.person_service = PersonService(db)

    def search(self, query: SearchQuery) -> SearchResponse:
        """Effectuer une recherche avancée"""
        # Récupérer toutes les personnes
        all_persons = self.person_service.get_all(skip=0, limit=10000)

        # Appliquer les filtres
        results = all_persons

        # Filtre textuel général
        if query.query:
            query_lower = query.query.lower()
            results = [
                p for p in results
                if query_lower in p.first_name.lower() or query_lower in p.last_name.lower()
            ]

        # Filtre par prénom
        if query.first_name:
            first_name_lower = query.first_name.lower()
            results = [p for p in results if first_name_lower in p.first_name.lower()]

        # Filtre par nom de famille
        if query.last_name:
            last_name_lower = query.last_name.lower()
            results = [p for p in results if last_name_lower in p.last_name.lower()]

        # Filtre par année de naissance
        if query.birth_year_min or query.birth_year_max:
            filtered = []
            for p in results:
                if p.birth_date:
                    birth_year = p.birth_date.year
                    if query.birth_year_min and birth_year < query.birth_year_min:
                        continue
                    if query.birth_year_max and birth_year > query.birth_year_max:
                        continue
                    filtered.append(p)
            results = filtered

        # Filtre par année de décès
        if query.death_year_min or query.death_year_max:
            filtered = []
            for p in results:
                if p.death_date:
                    death_year = p.death_date.year
                    if query.death_year_min and death_year < query.death_year_min:
                        continue
                    if query.death_year_max and death_year > query.death_year_max:
                        continue
                    filtered.append(p)
            results = filtered

        # Filtre par lieu de naissance
        if query.birth_place:
            place_lower = query.birth_place.lower()
            results = [
                p for p in results
                if p.birth_place and place_lower in p.birth_place.lower()
            ]

        # Filtre par lieu de décès
        if query.death_place:
            place_lower = query.death_place.lower()
            results = [
                p for p in results
                if p.death_place and place_lower in p.death_place.lower()
            ]

        # Filtre par genre
        if query.gender:
            results = [p for p in results if p.gender == query.gender]

        # Compter le total avant pagination
        total = len(results)

        # Pagination
        results = results[query.offset:query.offset + query.limit]

        return SearchResponse(
            total=total,
            results=results,
            limit=query.limit,
            offset=query.offset
        )
