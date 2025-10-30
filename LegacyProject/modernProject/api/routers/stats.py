"""
Router pour les statistiques
"""

from fastapi import APIRouter, Depends
from ..models.stats import Statistics
from ..services.stats_service import StatsService
from ..dependencies import get_stats_service

router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
)


@router.get("/", response_model=Statistics)
async def get_statistics(
    service: StatsService = Depends(get_stats_service)
):
    """
    Obtenir les statistiques générales de la base de données généalogique
    """
    stats = service.get_statistics()
    return stats


@router.get("/names/surnames")
async def get_surname_distribution(
    limit: int = 20,
    service: StatsService = Depends(get_stats_service)
):
    """
    Distribution des noms de famille les plus fréquents
    """
    distribution = service.get_surname_distribution(limit)
    return distribution


@router.get("/names/firstnames")
async def get_firstname_distribution(
    limit: int = 20,
    service: StatsService = Depends(get_stats_service)
):
    """
    Distribution des prénoms les plus fréquents
    """
    distribution = service.get_firstname_distribution(limit)
    return distribution


@router.get("/timeline")
async def get_timeline_distribution(
    service: StatsService = Depends(get_stats_service)
):
    """
    Distribution temporelle (par siècle/décennie)
    """
    timeline = service.get_timeline_distribution()
    return timeline
