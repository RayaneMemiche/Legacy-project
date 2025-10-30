"""
Modèles Pydantic pour l'API
"""

from .person import PersonBase, PersonCreate, PersonUpdate, PersonResponse, PersonDetail
from .family import FamilyBase, FamilyCreate, FamilyUpdate, FamilyResponse
from .auth import UserBase, UserCreate, UserLogin, UserResponse, Token
from .search import SearchQuery, SearchResponse
from .stats import Statistics, CenturyDistribution, NameDistribution

__all__ = [
    "PersonBase",
    "PersonCreate",
    "PersonUpdate",
    "PersonResponse",
    "PersonDetail",
    "FamilyBase",
    "FamilyCreate",
    "FamilyUpdate",
    "FamilyResponse",
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "Token",
    "SearchQuery",
    "SearchResponse",
    "Statistics",
    "CenturyDistribution",
    "NameDistribution",
]
