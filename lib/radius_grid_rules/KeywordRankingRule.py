from services.grid.DTOs.LocationTargetDTO import LocationTargetDTO
from lib.radius_grid.NearbyPlaces import NearbyPlaces


class KeywordRankingRule ():

    def __init__(self):
        self.nearby_places = NearbyPlaces()

    def analyze_ranking(self, location_target: str, main_location_url: str):

        rank = next(
            ((i+1, target) for i, target in enumerate(location_target)
             if LocationTargetDTO(target).googleMapsUri == main_location_url),
            None
        )

        return rank if rank else len(location_target) + 1

    def analyze_ranking_by_keywords(self, lat, lng, keywords, main_location_url: str) -> list:

        analyzed_targets = []
        for keyword in keywords:
            _, place = self.nearby_places.get_nearby_places_by_keyword(
                lat, lng, keyword, "en")

            analyzed_targets.append({
                "keyword": keyword,
                "rank": self.analyze_ranking(place, main_location_url)
            })

        return analyzed_targets
