from datatypes.KeywordRankingRuleByScrappingDatatypes import LocationRank
from typing import Literal

ColorType = Literal["success", "warn", "info", "danger"]


class RankRule ():

    TARGET_VALUE = 20

    def set_percentage_within_a_number(self, num1, num2):

        return (num1 * 100) / num2

    def get_percentage_value(self, value, percentage):

        return (value * percentage) / 100

    def average_percentage_value(self, *percentage_values):

        if len(percentage_values) == 1:
            return percentage_values[0]
        elif len(percentage_values) == 0:
            return 0

        return sum(percentage_values) / len(percentage_values)

    def ranks_validation(self, ranks: LocationRank):

        self.set_percentage_within_a_number(ranks.rank, ranks.ranking)

    def set_number_against_percentage(self, percentage):

        return (percentage / 100) * self.TARGET_VALUE

    def avg_number_into_icon_info(self, grid_rank) -> ColorType:

        if grid_rank > 70:
            return "success"
        elif 40 <= grid_rank <= 60:
            return "info"
        elif 10 <= grid_rank <= 30:
            return "warn"
        else:
            return "danger"
