
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AddressComponent:
    longText: str
    shortText: str
    types: List[str]
    languageCode: str


@dataclass
class PlusCode:
    globalCode: str
    compoundCode: str


@dataclass
class LatLng:
    latitude: float
    longitude: float


@dataclass
class Viewport:
    low: LatLng
    high: LatLng


@dataclass
class TimeOfDay:
    day: int
    hour: int
    minute: int
    date: Optional[Dict[str, int]] = None
    truncated: Optional[bool] = None


@dataclass
class Period:
    open: TimeOfDay
    close: TimeOfDay


@dataclass
class OpeningHours:
    openNow: bool
    periods: List[Period]
    weekdayDescriptions: List[str]
    nextCloseTime: str


@dataclass
class AuthorAttribution:
    displayName: str
    uri: str
    photoUri: str


@dataclass
class Text:
    text: str
    languageCode: str


@dataclass
class Review:
    name: str
    relativePublishTimeDescription: str
    rating: int
    text: Text
    originalText: Text
    authorAttribution: AuthorAttribution
    publishTime: str
    flagContentUri: str
    googleMapsUri: str


@dataclass
class Photo:
    name: str
    widthPx: int
    heightPx: int
    authorAttributions: List[AuthorAttribution]
    flagContentUri: str
    googleMapsUri: str


@dataclass
class DisplayName:
    text: str
    languageCode: str


@dataclass
class LocationTargetDTO:
    name: str
    id: str
    types: List[str] = field(default_factory=list)
    nationalPhoneNumber: Optional[str] = None
    internationalPhoneNumber: Optional[str] = None
    formattedAddress: Optional[str] = None
    addressComponents: List[Any] = field(default_factory=list)
    plusCode: Optional[Any] = None
    location: Optional[Any] = None
    viewport: Optional[Any] = None
    rating: Optional[float] = None
    googleMapsUri: Optional[str] = None
    websiteUri: Optional[str] = None
    regularOpeningHours: Optional[Any] = None
    utcOffsetMinutes: Optional[int] = None
    adrFormatAddress: Optional[str] = None
    businessStatus: Optional[str] = None
    priceLevel: Optional[str] = None
    userRatingCount: Optional[int] = None
    iconMaskBaseUri: Optional[str] = None
    iconBackgroundColor: Optional[str] = None
    displayName: Optional[Any] = None
    primaryTypeDisplayName: Optional[Any] = None
    takeout: Optional[bool] = None
    delivery: Optional[bool] = None
    dineIn: Optional[bool] = None
    curbsidePickup: Optional[bool] = None
    reservable: Optional[bool] = None
    servesLunch: Optional[bool] = None
    servesDinner: Optional[bool] = None
    servesBeer: Optional[bool] = None
    servesWine: Optional[bool] = None
    servesBrunch: Optional[bool] = None
    currentOpeningHours: Optional[Any] = None
    primaryType: Optional[str] = None
    shortFormattedAddress: Optional[str] = None
    reviews: List[Any] = field(default_factory=list)
    photos: List[Any] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        """Creates an instance from a dictionary while ignoring extra fields."""
        filtered_data = {key: data[key]
                         for key in cls.__annotations__.keys() if key in data}
        return cls(**filtered_data)
