import requests
from config.GoogleConfig import GoogleConfig


class NearbyPlaces ():

    google_config = GoogleConfig()
    NEARBY_PLACE_BY_TYPE_URL = "https://places.googleapis.com/v1/places:searchNearby"
    NEARBY_PLACE_BY_KEYWORD = "https://places.googleapis.com/v1/places:searchText"

    def get_nearby_places_by_type(self, lat, lng, radius, included_types: list[str]):

        payload = {
            "includedTypes": included_types,
            "maxResultCount": 15,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": lat,
                        "longitude": lng
                    },
                    "radius": radius
                }
            }
        }

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.google_config.get_google_secret_key(),
            "X-Goog-FieldMask": "places.id,places.location,places.rating,places.googleMapsUri,places.businessStatus,places.displayName,places.name"
        }

        request = requests.post(self.NEARBY_PLACE_BY_TYPE_URL,
                                json=payload, headers=headers)
        result = request.json()

        return request, result

    def get_nearby_places_by_keyword(self, lat, lng, keyword, radius, language_code="en"):

        payload = {
            "textQuery": keyword,
            "includePureServiceAreaBusinesses": True,
            "languageCode": language_code,
            "locationBias": {
                "circle": {
                    "center": {
                        "latitude": lat,
                        "longitude": lng
                    },

                    "radius": radius
                }
            }
        }

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.google_config.get_google_secret_key(),
            "X-Goog-FieldMask": "places.id,places.location,places.rating,places.googleMapsUri,places.businessStatus,places.displayName,places.name"
            # "X-Goog-FieldMask": "places.name,places-id,places-types,places.nationalPhoneNumber,places.internationalPhoneNumber,places.viewport,places.rating,places.googleMapsUri,places.regular"
        }

        request = requests.post(self.NEARBY_PLACE_BY_KEYWORD,
                                json=payload, headers=headers)
        result = request.json()

        return request, result
