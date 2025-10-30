"""
Service pour la gestion des familles
"""

import sys
import os
from typing import List, Optional

# Ajouter le chemin des modules lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from database import Database
from ..models.family import FamilyCreate, FamilyUpdate, FamilyResponse


class FamilyService:
    """Service pour gérer les familles"""

    def __init__(self, db: Database = None):
        # Accepter la database pour compatibilité (sera utilisée plus tard)
        self.db = db
        # Pour l'instant, utilisation d'un stockage en mémoire
        # TODO: Intégrer avec le module database.py existant
        self.families = {}
        self.next_id = 1

    def get_all(self, skip: int = 0, limit: int = 100) -> List[FamilyResponse]:
        """Récupérer toutes les familles"""
        all_families = list(self.families.values())
        return all_families[skip:skip + limit]

    def get_by_id(self, family_id: str) -> Optional[FamilyResponse]:
        """Récupérer une famille par son ID"""
        return self.families.get(family_id)

    def create(self, family: FamilyCreate) -> FamilyResponse:
        """Créer une nouvelle famille"""
        family_id = str(self.next_id)
        self.next_id += 1

        family_data = family.model_dump()
        family_data['id'] = family_id
        family_data['created_at'] = None  # TODO: timestamp
        family_data['updated_at'] = None

        family_response = FamilyResponse(**family_data)
        self.families[family_id] = family_response

        return family_response

    def update(self, family_id: str, family: FamilyUpdate) -> Optional[FamilyResponse]:
        """Mettre à jour une famille"""
        if family_id not in self.families:
            return None

        existing = self.families[family_id]
        update_data = family.model_dump(exclude_unset=True)

        # Créer une nouvelle instance avec les données mises à jour
        family_dict = existing.model_dump()
        family_dict.update(update_data)
        family_dict['updated_at'] = None  # TODO: timestamp

        updated_family = FamilyResponse(**family_dict)
        self.families[family_id] = updated_family

        return updated_family

    def delete(self, family_id: str) -> bool:
        """Supprimer une famille"""
        if family_id in self.families:
            del self.families[family_id]
            return True
        return False
