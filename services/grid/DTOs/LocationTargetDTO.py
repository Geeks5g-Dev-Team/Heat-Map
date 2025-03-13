
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
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
    types: List[str]
    nationalPhoneNumber: str
    internationalPhoneNumber: str
    formattedAddress: str
    addressComponents: List[AddressComponent]
    plusCode: PlusCode
    location: LatLng
    viewport: Viewport
    rating: float
    googleMapsUri: str
    websiteUri: str
    regularOpeningHours: OpeningHours
    utcOffsetMinutes: int
    adrFormatAddress: str
    businessStatus: str
    priceLevel: str
    userRatingCount: int
    iconMaskBaseUri: str
    iconBackgroundColor: str
    displayName: DisplayName
    primaryTypeDisplayName: DisplayName
    takeout: bool
    delivery: bool
    dineIn: bool
    curbsidePickup: bool
    reservable: bool
    servesLunch: bool
    servesDinner: bool
    servesBeer: bool
    servesWine: bool
    servesBrunch: bool
    currentOpeningHours: OpeningHours
    primaryType: str
    shortFormattedAddress: str
    reviews: List[Review]
    photos: List[Photo]
