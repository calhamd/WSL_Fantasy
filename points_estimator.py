
class PointsEstimator:
    def __init__(self):
        pass

    def estimate_totals(self, surfers: []):
        pass


class OddsPointEstimator(PointsEstimator):
    max_score = 15
    min_score = 10
    def __init__(self):
        super().__init__()

    def estimate_totals(self, surfers: []):
        total_odds = self.__get_total_odds(surfers)
        update_max = 0
        for surfer in surfers:
            update = ((1 - surfer.odds / total_odds) * (self.max_score - self.min_score)) + self.min_score
            surfer.expected_totals += [update]
            update_max = update if update > update_max else update_max
        return update_max

    def __get_total_odds(self, surfers):
        total_odds = 0
        for surfer in surfers:
            total_odds += surfer.odds
        return total_odds