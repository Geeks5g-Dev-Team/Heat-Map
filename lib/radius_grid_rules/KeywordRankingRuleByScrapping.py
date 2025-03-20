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

        rank = LocationRank(
            self.rank_rule.TARGET_VALUE + 1, None, self.rank_rule.TARGET_VALUE,
            0
        )
        try:

            i = 0
            while i < len(location_target) - 1:
                target = location_target[i]
                if target.name == business_name:
                    rank = LocationRank(
                        rank=i+1,
                        location=target,
                        ranking=self.rank_rule.TARGET_VALUE,
                        percentage=self.rank_rule.set_percentage_within_a_number(
                            i+1, self.rank_rule.TARGET_VALUE)
                    )
                    break
                i += 1
            return rank

        except Exception as e:
            print(f"Error: {e}")
            return rank

    async def analyze_ranking_by_keywords(self, lat, lng, keywords, business_name: str, **kwargs) -> FinalRankAnalysis:

        analyzed_targets = []
        percentage_values = []

        scrapper = ScrapeGoogleMapsSearch(self.rank_rule.TARGET_VALUE)
        businesses = await scrapper.activate(
            keywords=keywords,
            lat=lat,
            lng=lng,
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
                percentage=business_ranked.percentage
            )

            analyzed_targets.append(ranked_business_data)
            percentage_values.append(business_ranked.percentage)

        avg_percentage = self.rank_rule.average_percentage_value(
            *percentage_values)

        return FinalRankAnalysis(
            data=analyzed_targets,
            lat=lat,
            lng=lng,
            average_percentage=int(avg_percentage),
            final_rank=int(
                self.rank_rule.set_number_against_percentage(avg_percentage))
        )
