from round import Round, RoundSettings
from points_estimator import OddsPointEstimator
from surfer import Surfer, SurferPool
#from heat_mappings import round1_m, round2_m, round3_m, round4_m, roundQ_m, roundS_m, roundF_m
import heat_mappings

class Event:
    def __init__(self):
        round1_set = RoundSettings("1", 12, 3, False, heat_mappings.round1_m, heat_mappings.round1_s)
        round2_set = RoundSettings("2", 4, 3, True, heat_mappings.round2_m, heat_mappings.round2_s)
        round3_set = RoundSettings("3", 16, 2, False, heat_mappings.round3_m, heat_mappings.round3_s)
        round4_set = RoundSettings("4", 8, 2, False, heat_mappings.round4_m)
        roundQ_set = RoundSettings("Q", 4, 2, False, heat_mappings.roundQ_m)
        roundS_set = RoundSettings("S", 2, 2, False, heat_mappings.roundS_m)
        roundF_set = RoundSettings("F", 1, 2, False, heat_mappings.roundF_m)

        self.rounds = [Round(round1_set),
                       Round(round2_set),
                       Round(round3_set),
                       Round(round4_set),
                       Round(roundQ_set),
                       Round(roundS_set),
                       Round(roundF_set)]

    def update_surfers(self, surfer_pool: SurferPool):
        for r in self.rounds:
            r.update_heat_maps(surfer_pool)
            r.update_surfer_points(surfer_pool)
            r.progress_winners(surfer_pool)

    def calculate_average_points(self, surfer_pool: SurferPool, iterations):
        surfer_dict = {}
        for i in range(0, iterations):
            surfer_pool.reset()
            self.update_surfers(surfer_pool)
            #  print("{} got {}".format(surfer_pool.surfers[0].name, surfer_pool.surfers[0].expected_totals))
            for s in surfer_pool.surfers:
                if s.name not in surfer_dict:
                    surfer_dict[s.name] = 0
                surfer_dict[s.name] += (sum(s.expected_totals) - surfer_dict[s.name])/(i+1)  # This is an incremental average
        return surfer_dict