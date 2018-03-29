from round import Round, Round1, Round2, Round3, Round4, RoundQ, RoundS, RoundF
from points_estimator import OddsPointEstimator
from surfer import Surfer, SurferPool

class Event:
    def __init__(self):
        self.rounds = [Round1(OddsPointEstimator()),
                        Round2(OddsPointEstimator()),
                        Round3(OddsPointEstimator()),
                        Round4(OddsPointEstimator()),
                        RoundQ(OddsPointEstimator()),
                        RoundS(OddsPointEstimator()),
                        RoundF(OddsPointEstimator())]

    def update_surfers(self, surfer_pool: SurferPool):
        for r in self.rounds:
            r.update_surfer_points(surfer_pool)
            r.progress_winners(surfer_pool)

    def calculate_average_points(self, surfer_pool: SurferPool, iterations):
        surfer_dict = {}
        for i in range(0, iterations):
            surfer_pool.reset()
            self.update_surfers(surfer_pool)
            for s in surfer_pool.surfers:
                if s.name not in surfer_dict:
                    surfer_dict[s.name] = 0
                surfer_dict[s.name] += (sum(s.expected_totals) - surfer_dict[s.name])/(i+1)  # This is an incremental average
        return surfer_dict