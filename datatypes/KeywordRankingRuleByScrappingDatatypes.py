from dataclasses import dataclass
from typing import Optional
from datatypes.ScrapeDatatypes import Business


@dataclass
class LocationRank ():
    """Datatype for each search term"""

    rank: int
    location: Optional[Business]
    ranking: int
    percentage: int


@dataclass
class RankingKeyword ():

    keyword: str
    location_rank: LocationRank
    all_locations_found = None
    percentage: int


@dataclass
class FinalRankAnalysis ():

    data: list[RankingKeyword]
    lat: int
    lng: int
    average_percentage: int
    final_rank: int