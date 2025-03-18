from services.grid.DTOs.LocationTargetDTO import LocationTargetDTO
from lib.radius_grid.NearbyPlaces import NearbyPlaces
from datatypes.KeywordRankingRuleByScrappingDatatypes import RankingKeyword, FinalRankAnalysis, LocationRank
from datatypes.DataTypeError import CustomError
from lib.radius_grid_rules.RankRule import RankRule
from services.scraping.main import ScrapeGoogleMapsSearch
from datatypes.ScrapeDatatypes import Business


class KeywordRankingRuleByScrapping ():

    def __init__(self):
        self.nearby_places = NearbyPlaces()
        self.rank_rule = RankRule()
        self.iterations_allowed = 3

    def analyze_ranking(self, location_target: list[Business], business_name: str) -> LocationRank:
        """Analyze each search term given a keyword. It returns the element found and its rank"""

        location_count = len(location_target)

        rank = LocationRank(
            len(location_target) + 1, None, len(location_target), 0)
        try:

            i = 0
            while i < location_count - 1:
                target = location_target[i]
                if target.name == business_name:
                    rank = LocationRank(
                        rank=i+1,
                        location=target,
                        ranking=location_count,
                        percentage=self.rank_rule.set_percentage_within_a_number(
                            i+1, location_count)
                    )
                    break
                i += 1
            return rank

        except Exception as e:
            print(f"Error: {e}")
            return rank

    async def analyze_ranking_by_keywords(self, lat, lng, keywords, business_name: str) -> FinalRankAnalysis:

        analyzed_targets = []
        percentage_values = []

        scrapper = ScrapeGoogleMapsSearch(15)
        businesses = await scrapper.activate(
            keywords=keywords,
            lat=lat,
            lng=lng
        )

        scrapper.display_scraped_data(businesses)

        for i, (k, businesses) in enumerate(businesses.items()):

            business_ranked = self.analyze_ranking(
                business_name=business_name,
                location_target=businesses
            )
            ranked_business_data = RankingKeyword(
                keyword=k,
                location_rank=business_ranked,
                all_locations_found=businesses,
                percentage=business_ranked.percentage
            )

            analyzed_targets.append(ranked_business_data)
            percentage_values.append(business_ranked.percentage)

        avg_percentage = 0

        if len(percentage_values) != 0:
            avg_percentage = self.rank_rule.average_percentage_value(
                *percentage_values)

        return FinalRankAnalysis(
            data=analyzed_targets,
            lat=lat,
            lng=lng,
            average_percentage=avg_percentage
        )
