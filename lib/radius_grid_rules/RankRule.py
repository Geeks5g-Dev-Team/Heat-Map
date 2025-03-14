from lib.radius_grid_rules.KeywordRankingRule import AnalyzeRankingReturnParams


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
