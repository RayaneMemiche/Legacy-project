"""
Service pour la gestion des personnes
"""

import sys
import os
from typing import List, Optional
from datetime import datetime

# Ajouter le chemin des modules lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from database import Database
from ..models.person import PersonCreate, PersonUpdate, PersonResponse, PersonDetail


class PersonService:
    """Service pour gérer les personnes"""

    def __init__(self, db: Database = None):
        # Utiliser la database fournie (singleton partagé) ou créer une nouvelle instance
        self.db = db if db is not None else Database()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[PersonResponse]:
        """Récupérer toutes les personnes"""
        persons = self.db.get_all_persons()
        # Pagination
        persons = persons[skip:skip + limit]
        return [self._to_response(p) for p in persons]

    def get_by_id(self, person_id: str) -> Optional[PersonDetail]:
        """Récupérer une personne par son ID avec détails"""
        person = self.db.get_person(person_id)
        if not person:
            return None

        # Récupérer les relations
        detail = PersonDetail(**self._to_dict(person))

        # Ajouter le père
        if person.get('father_id'):
            father = self.db.get_person(person['father_id'])
            if father:
                detail.father = PersonResponse(**self._to_dict(father))

        # Ajouter la mère
        if person.get('mother_id'):
            mother = self.db.get_person(person['mother_id'])
            if mother:
                detail.mother = PersonResponse(**self._to_dict(mother))

        # Ajouter les enfants
        children = self.db.get_children(person_id)
        detail.children = [PersonResponse(**self._to_dict(c)) for c in children]

        # Ajouter les conjoints
        spouses = self.db.get_spouses(person_id)
        detail.spouses = [PersonResponse(**self._to_dict(s)) for s in spouses]

        # Ajouter les frères et sœurs
        siblings = self.db.get_siblings(person_id)
        detail.siblings = [PersonResponse(**self._to_dict(s)) for s in siblings]

        return detail

    def create(self, person: PersonCreate) -> PersonResponse:
        """Créer une nouvelle personne"""
        person_data = person.model_dump()

        # Valider les parents si fournis
        if person.father_id:
            father = self.db.get_person(person.father_id)
            if not father:
                raise ValueError(f"Father with id {person.father_id} not found")

        if person.mother_id:
            mother = self.db.get_person(person.mother_id)
            if not mother:
                raise ValueError(f"Mother with id {person.mother_id} not found")

        # Créer la personne
        new_person = self.db.create_person(person_data)
        return PersonResponse(**self._to_dict(new_person))

    def update(self, person_id: str, person: PersonUpdate) -> Optional[PersonResponse]:
        """Mettre à jour une personne"""
        existing = self.db.get_person(person_id)
        if not existing:
            return None

        # Ne mettre à jour que les champs fournis
        update_data = person.model_dump(exclude_unset=True)

        # Valider les parents si mis à jour
        if 'father_id' in update_data and update_data['father_id']:
            father = self.db.get_person(update_data['father_id'])
            if not father:
                raise ValueError(f"Father with id {update_data['father_id']} not found")

        if 'mother_id' in update_data and update_data['mother_id']:
            mother = self.db.get_person(update_data['mother_id'])
            if not mother:
                raise ValueError(f"Mother with id {update_data['mother_id']} not found")

        updated_person = self.db.update_person(person_id, update_data)
        return PersonResponse(**self._to_dict(updated_person))

    def delete(self, person_id: str) -> bool:
        """Supprimer une personne"""
        return self.db.delete_person(person_id)

    def get_ancestors(self, person_id: str, generations: int = 4) -> Optional[List[PersonResponse]]:
        """Récupérer les ancêtres d'une personne"""
        person = self.db.get_person(person_id)
        if not person:
            return None

        ancestors = []
        self._collect_ancestors(person_id, generations, ancestors, 1)
        return [PersonResponse(**self._to_dict(a)) for a in ancestors]

    def get_descendants(self, person_id: str, generations: int = 4) -> Optional[List[PersonResponse]]:
        """Récupérer les descendants d'une personne"""
        person = self.db.get_person(person_id)
        if not person:
            return None

        descendants = []
        self._collect_descendants(person_id, generations, descendants, 1)
        return [PersonResponse(**self._to_dict(d)) for d in descendants]

    def _collect_ancestors(self, person_id: str, max_gen: int, result: list, current_gen: int):
        """Collecter récursivement les ancêtres"""
        if current_gen > max_gen:
            return

        person = self.db.get_person(person_id)
        if not person:
            return

        # Ajouter le père
        if person.get('father_id'):
            father = self.db.get_person(person['father_id'])
            if father and father not in result:
                result.append(father)
                self._collect_ancestors(person['father_id'], max_gen, result, current_gen + 1)

        # Ajouter la mère
        if person.get('mother_id'):
            mother = self.db.get_person(person['mother_id'])
            if mother and mother not in result:
                result.append(mother)
                self._collect_ancestors(person['mother_id'], max_gen, result, current_gen + 1)

    def _collect_descendants(self, person_id: str, max_gen: int, result: list, current_gen: int):
        """Collecter récursivement les descendants"""
        if current_gen > max_gen:
            return

        children = self.db.get_children(person_id)
        for child in children:
            if child not in result:
                result.append(child)
                self._collect_descendants(child['id'], max_gen, result, current_gen + 1)

    def _to_response(self, person: dict) -> PersonResponse:
        """Convertir un dict en PersonResponse"""
        return PersonResponse(**self._to_dict(person))

    def _to_dict(self, person: dict) -> dict:
        """Convertir les données de personne pour Pydantic"""
        return {
            'id': person.get('id'),
            'first_name': person.get('first_name', person.get('firstName', '')),
            'last_name': person.get('last_name', person.get('lastName', '')),
            'birth_date': person.get('birth_date', person.get('birthDate')),
            'birth_place': person.get('birth_place', person.get('birthPlace')),
            'death_date': person.get('death_date', person.get('deathDate')),
            'death_place': person.get('death_place', person.get('deathPlace')),
            'gender': person.get('gender'),
            'occupation': person.get('occupation'),
            'notes': person.get('notes'),
            'father_id': person.get('father_id', person.get('fatherId')),
            'mother_id': person.get('mother_id', person.get('motherId')),
            'created_at': person.get('created_at', person.get('createdAt')),
            'updated_at': person.get('updated_at', person.get('updatedAt')),
        }
