from lib.radius_grid_rules.KeywordRankingRule import AnalyzeRankingReturnParams
from typing import Literal

ColorType = Literal["success", "warn", "info", "danger"]


class RankRule ():

    TARGET_VALUE = 20

    def set_percentage_within_a_number(self, num1, num2):

        return (num2 / num1) * 100

    def get_percentage_value(self, value, percentage):

        return (value * percentage) / 100

    def average_percentage_value(self, *percentage_values):
        avg = sum(percentage_values) / len(percentage_values)

        return self.get_percentage_value(self.TARGET_VALUE, avg)

    def ranks_validation(self, ranks: AnalyzeRankingReturnParams):

        self.set_percentage_within_a_number(ranks.rank, ranks.ranking)

    def avg_number_into_icon_info(self, grid_rank) -> ColorType:

        if grid_rank > 70:
            return "success"
        elif 60 > grid_rank < 40:
            return "info"
        elif 30 > grid_rank < 10:
            return "warn"
        elif grid_rank <= 10:
            return "danger"
