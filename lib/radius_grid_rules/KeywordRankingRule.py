from services.grid.DTOs.LocationTargetDTO import LocationTargetDTO
from lib.radius_grid.NearbyPlaces import NearbyPlaces
from datatypes.KeywordRankingRuleDatatypes import AnalyzeRankingReturnParams, AnalyzeRankingWithKeywords, AnalyzeRankingWithKeywordsReturnParams
from datatypes.DataTypeError import CustomError
from lib.radius_grid_rules.RankRule import RankRule


class KeywordRankingRule ():

    def __init__(self):
        self.nearby_places = NearbyPlaces()
        self.rank_rule = RankRule()
        self.iterations_allowed = 3

    def analyze_ranking(self, location_target: list[dict], main_location_url: str) -> AnalyzeRankingReturnParams:

        location_count = len(location_target)
        rank = AnalyzeRankingReturnParams(
            len(location_target) + 1, None, len(location_target), 0)
        try:

            i = 0
            while i < location_count - 1:
                target = LocationTargetDTO.from_dict(location_target[i])
                if target.googleMapsUri == main_location_url:
                    rank = AnalyzeRankingReturnParams(
                        location=target,
                        rank=i+1,
                        ranking=location_count,
                        percentage=self.rank_rule.set_percentage_within_a_number(
                            i+1, location_count)
                    )
                    break
                i += 1
            print(f"Rank: {rank.location}")
            return rank

        except Exception as e:
            print(f"Error: {e}")
            return rank

    def analyze_ranking_by_keywords(self, lat, lng, keywords, main_location_url: str) -> AnalyzeRankingWithKeywordsReturnParams:

        analyzed_targets = []
        percentage_values = []
        for keyword in keywords:

            current_iterations_per_search = 0
            percentage, search_statement = self.return_search_keyword_statement(
                lat=lat,
                lng=lng,
                keyword=keyword,
                main_location_url=main_location_url
            )

            print(
                f"Instance {search_statement}, Is instance {isinstance(search_statement, CustomError)}")

            def is_location_none(search_statement=search_statement): return isinstance(
                search_statement, CustomError) or search_statement.location_rank.location is None

            if is_location_none() and current_iterations_per_search < self.iterations_allowed:

                while current_iterations_per_search < self.iterations_allowed or is_location_none():

                    percentage, search_statement = self.return_search_keyword_statement(
                        lat=lat,
                        lng=lng,
                        keyword=keyword,
                        main_location_url=main_location_url
                    )

                    current_iterations_per_search += 1

            analyzed_targets.append(search_statement)
            percentage_values.append(percentage)

        avg_percentage = 0

        if len(percentage_values) != 0:
            avg_percentage = self.rank_rule.average_percentage_value(
                *percentage_values)
        return AnalyzeRankingWithKeywordsReturnParams(
            data=analyzed_targets,
            lat=lat,
            lng=lng,
            average_percentage=avg_percentage
        )

    def return_search_keyword_statement(self, lat, lng, keyword, main_location_url):

        try:
            _, place = self.nearby_places.get_nearby_places_by_keyword(
                lat, lng, keyword, "en")

            location_rank = self.analyze_ranking(
                place["places"], main_location_url)

            targets = AnalyzeRankingWithKeywords(
                keyword=keyword,
                location_rank=location_rank,
                all_locations_found=[LocationTargetDTO.from_dict(
                    p) for p in place["places"]]
            )

            return location_rank.percentage, targets

        except Exception as e:
            return 0, CustomError(
                message=f"Fail to analyze keyword {keyword}",
                details=e,
                has_error=True
            )
