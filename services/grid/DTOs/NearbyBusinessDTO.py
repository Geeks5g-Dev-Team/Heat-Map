
from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class Geometry:
    lat: float
    lng: float


@dataclass
class Viewport:
    northeast: Geometry
    southwest: Geometry


@dataclass
class LocationInfo:
    location: Geometry
    viewport: Viewport


@dataclass
class OpeningHours:
    open_now: Optional[bool] = None


@dataclass
class Photo:
    height: int
    html_attributions: List[str]
    photo_reference: str
    width: int


@dataclass
class PlusCode:
    compound_code: Optional[str] = None
    global_code: Optional[str] = None


@dataclass
class NearbyBusinessData:
    business_status: Optional[str] = None
    geometry: Optional[LocationInfo] = None
    icon: Optional[str] = None
    icon_background_color: Optional[str] = None
    icon_mask_base_uri: Optional[str] = None
    name: Optional[str] = None
    opening_hours: Optional[OpeningHours] = None
    photos: List[Photo] = field(default_factory=list)
    place_id: Optional[str] = None
    plus_code: Optional[PlusCode] = None
    rating: Optional[float] = None
    reference: Optional[str] = None
    scope: Optional[str] = None
    types: List[str] = field(default_factory=list)
    user_ratings_total: Optional[int] = None
    vicinity: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'NearbyBusinessData':
        # Handle nested structures
        geometry = data.get("geometry")
        location_info = None
        if geometry:
            location = geometry.get("location")
            viewport = geometry.get("viewport")
            location_info = LocationInfo(
                location=Geometry(**location),
                viewport=Viewport(
                    northeast=Geometry(**viewport['northeast']),
                    southwest=Geometry(**viewport['southwest'])
                )
            )

        photos = [Photo(**photo) for photo in data.get("photos", [])]

        plus_code = data.get("plus_code")
        if plus_code:
            plus_code = PlusCode(**plus_code)

        opening_hours = data.get("opening_hours")
        if opening_hours:
            opening_hours = OpeningHours(**opening_hours)

        return cls(
            business_status=data.get("business_status"),
            geometry=location_info,
            icon=data.get("icon"),
            icon_background_color=data.get("icon_background_color"),
            icon_mask_base_uri=data.get("icon_mask_base_uri"),
            name=data.get("name"),
            opening_hours=opening_hours,
            photos=photos,
            place_id=data.get("place_id"),
            plus_code=plus_code,
            rating=data.get("rating"),
            reference=data.get("reference"),
            scope=data.get("scope"),
            types=data.get("types", []),
            user_ratings_total=data.get("user_ratings_total"),
            vicinity=data.get("vicinity")
        )
