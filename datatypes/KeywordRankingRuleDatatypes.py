from dataclasses import dataclass
from typing import Optional
from services.grid.DTOs.LocationTargetDTO import LocationTargetDTO
from datatypes.DataTypeError import CustomError


@dataclass
class AnalyzeRankingReturnParams ():
    """Datatype for each search term"""

    rank: int
    location: Optional[LocationTargetDTO]
    ranking: int
    percentage: int


@dataclass
class AnalyzeRankingWithKeywords ():

    keyword: str
    location_rank: AnalyzeRankingReturnParams
    all_locations_found: list[LocationTargetDTO]
    percentage: int


@dataclass
class AnalyzeRankingWithKeywordsReturnParams ():

    data: list[AnalyzeRankingWithKeywords | CustomError]
    lat: int
    lng: int
    average_percentage: int
