from surfer import SurferPool
from points_estimator import OddsPointEstimator, ComboPointsEstimator
import random
from random import shuffle

class RoundSettings:
    def __init__(self, name, heatcount, surferperheat, bonusround, lookupdictlist):
        self.name = name
        self.lookup_dict_list = lookupdictlist
        self.heat_count = heatcount
        self.surfer_per_heat = surferperheat
        self.bonus_round = bonusround


class Round:
    def __init__(self, settings: RoundSettings):
        self.settings = settings
        self.estimator = ComboPointsEstimator()

    def get_heat_names(self):
        heats = []
        for heat in range(0, self.settings.heat_count):
            heats.append(self.settings.name + "_" + str(heat+1))
        return heats

    def update_surfer_points(self, surfers: SurferPool):
        heat_max = 0
        for heat_name in self.get_heat_names():
            surfer_h = surfers.get_surfers_in_heat(heat_name)
            assert len(surfer_h) == self.settings.surfer_per_heat
            max = self.estimator.estimate_totals(surfer_h)
            heat_max = max if max > heat_max else heat_max
        if self.settings.bonus_round:
            previous_round_winners = surfers.get_surfers_in_heat(self.settings.name + "_w")
            for surfer in previous_round_winners:
                surfer.expected_totals += [heat_max]

    def progress_winners(self, surfer_p: SurferPool):
        for heat in self.get_heat_names():
            surfer_h = surfer_p.get_surfers_in_heat(heat)
            assert len(surfer_h) == self.settings.surfer_per_heat
            surfer_h.sort(key=lambda s: (s.expected_totals[-1], random.random()), reverse=True)
            for i in range(0, len(self.settings.lookup_dict_list)):
                surfer_h[i].heat_list += self.settings.lookup_dict_list[i][heat]

# class Round1(Round):
#     winner_heat_lookup = {1: 11, 2: 2, 3: 1, 4: 12, 5: 7, 6: 6, 7: 8, 8: 5, 9: 3, 10: 10, 11: 9, 12: 4}
#     mid_heat_lookup = {1: 7, 2: 8, 3: 9, 4: 10, 5: 11, 6: 12, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
#     loser_heat_lookup = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12}
#
#     def __init__(self, estimator: PointsEstimator):
#         super().__init__(estimator)
#
#     def get_heat_names(self):
#         heats = []
#         for heat in range(0, 12):
#             heats.append(("1_" + str(heat+1), heat+1))
#         return heats
#
#     def update_surfer_points(self, surfers: SurferPool):
#         for heat_name, _ in self.get_heat_names():
#             surfer_h = surfers.get_surfers_in_heat(heat_name)
#             assert len(surfer_h) == 3
#             _ = self.estimator.estimate_totals(surfer_h)
#
#     def progress_winners(self, surfer_p: SurferPool):
#         for heat, heat_n in self.get_heat_names():
#             surfer_h = surfer_p.get_surfers_in_heat(heat)
#             assert len(surfer_h) == 3
#             surfer_h.sort(key=lambda s: (s.expected_totals[-1], random.random()))
#             winner = surfer_h[0]
#             mid = surfer_h[1]
#             loser = surfer_h[2]
#             winner.heat_list += ["2_w", "3_"+str(self.winner_heat_lookup[heat_n])]
#             mid.heat_list += ["2_" + str(self.mid_heat_lookup[heat_n])]
#             loser.heat_list += ["2_" + str(self.loser_heat_lookup[heat_n])]
#
# class Round2(Round):
#     winner_lookup = {1: 4, 2: 9, 3: 10, 4: 3, 5: 5, 6: 8, 7: 11, 8: 2, 9: 1, 10: 12, 11: 7, 12: 6}
#
#     def __init__(self, estimator: PointsEstimator):
#         super().__init__(estimator)
#
#     def get_heat_names(self):
#         heats = []
#         for heat in range(0, 12):
#             heats.append(("2_" + str(heat+1), heat+1))
#         return heats
#
#     def update_surfer_points(self, surfers: SurferPool):
#         heat_max = 0
#         for heat_name, _ in self.get_heat_names():  #run all the heats
#             surfer_h = surfers.get_surfers_in_heat(heat_name)
#             assert len(surfer_h) == 2
#             max = self.estimator.estimate_totals(surfer_h)
#             heat_max = max if max > heat_max else heat_max
#         round1_winners = surfers.get_surfers_in_heat("2_w")
#         for surfer in round1_winners:
#             surfer.expected_totals += [heat_max]
#
#     def progress_winners(self, surfer_p: SurferPool):
#         for heat, heat_n in self.get_heat_names():
#             surfer_h = surfer_p.get_surfers_in_heat(heat)
#             assert len(surfer_h) == 2
#             surfer_h.sort(key=lambda s: (s.expected_totals[-1], random.random()))
#             winner = surfer_h[0]
#             winner.heat_list += ["3_" + str(self.winner_lookup[heat_n])]
#
# class Round3(Round):
#     winner_lookup = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3, 10: 4, 11: 4, 12: 4}
#
#     def __init__(self, estimator: PointsEstimator):
#         super().__init__(estimator)
#
#     def get_heat_names(self):
#         heats = []
#         for heat in range(0, 12):
#             heats.append(("3_" + str(heat+1), heat+1))
#         return heats
#
#     def update_surfer_points(self, surfers: SurferPool):
#
#         for heat_name, _ in self.get_heat_names():  #run all the heats
#             surfer_h = surfers.get_surfers_in_heat(heat_name)
#             assert len(surfer_h) == 2
#             self.estimator.estimate_totals(surfer_h)
#
#     def progress_winners(self, surfer_p: SurferPool):
#         for heat, heat_n in self.get_heat_names():
#             surfer_h = surfer_p.get_surfers_in_heat(heat)
#             assert len(surfer_h) == 2
#             surfer_h.sort(key=lambda s: (s.expected_totals[-1], random.random()))
#             winner = surfer_h[0]
#             winner.heat_list += ["4_" + str(self.winner_lookup[heat_n])]
#
# class Round4(Round):
#     winner_lookup = {1: 1, 2: 2, 3: 3, 4: 4}
#     mid_lookup = {1: 2, 2: 1, 3: 4, 4: 3}
#
#     def __init__(self, estimator: PointsEstimator):
#         super().__init__(estimator)
#
#     def get_heat_names(self):
#         heats = []
#         for heat in range(0, 4):
#             heats.append(("4_" + str(heat+1), heat+1))
#         return heats
#
#     def update_surfer_points(self, surfers: SurferPool):
#         for heat_name, _ in self.get_heat_names():  #run all the heats
#             surfer_h = surfers.get_surfers_in_heat(heat_name)
#             assert len(surfer_h) == 3
#             self.estimator.estimate_totals(surfer_h)
#
#     def progress_winners(self, surfer_p: SurferPool):
#         for heat, heat_n in self.get_heat_names():
#             surfer_h = surfer_p.get_surfers_in_heat(heat)
#             assert len(surfer_h) == 3
#             surfer_h.sort(key=lambda s: (s.expected_totals[-1], random.random()))
#             winner = surfer_h[0]
#             mid = surfer_h[1]
#             winner.heat_list += ["Q_" + str(self.winner_lookup[heat_n])]
#             mid.heat_list += ["Q_" + str(self.mid_lookup[heat_n])]
#
# class RoundQ(Round):
#     winner_lookup = {1: 1, 2: 1, 3: 2, 4: 2}
#
#     def __init__(self, estimator: PointsEstimator):
#         super().__init__(estimator)
#
#     def get_heat_names(self):
#         heats = []
#         for heat in range(0, 4):
#             heats.append(("Q_" + str(heat+1), heat+1))
#         return heats
#
#     def update_surfer_points(self, surfers: SurferPool):
#         for heat_name, _ in self.get_heat_names():  #run all the heats
#             surfer_h = surfers.get_surfers_in_heat(heat_name)
#             assert len(surfer_h) == 2
#             self.estimator.estimate_totals(surfer_h)
#
#     def progress_winners(self, surfer_p: SurferPool):
#         for heat, heat_n in self.get_heat_names():
#             surfer_h = surfer_p.get_surfers_in_heat(heat)
#             assert len(surfer_h) == 2
#             surfer_h.sort(key=lambda s: (s.expected_totals[-1], random.random()))
#             winner = surfer_h[0]
#             winner.heat_list += ["S_" + str(self.winner_lookup[heat_n])]
#
#
# class RoundS(Round):
#     def __init__(self, estimator: PointsEstimator):
#         super().__init__(estimator)
#
#     def get_heat_names(self):
#         heats = []
#         for heat in range(0, 2):
#             heats.append(("S_" + str(heat+1), heat+1))
#         return heats
#
#     def update_surfer_points(self, surfers: SurferPool):
#         for heat_name, _ in self.get_heat_names():  #run all the heats
#             surfer_h = surfers.get_surfers_in_heat(heat_name)
#             assert len(surfer_h) == 2
#             self.estimator.estimate_totals(surfer_h)
#
#     def progress_winners(self, surfer_p: SurferPool):
#         for heat, heat_n in self.get_heat_names():
#             surfer_h = surfer_p.get_surfers_in_heat(heat)
#             assert len(surfer_h) == 2
#             surfer_h.sort(key=lambda s: (s.expected_totals[-1], random.random()))
#             winner = surfer_h[0]
#             winner.heat_list += ["F"]
#
# class RoundF(Round):
#     def __init__(self, estimator: PointsEstimator):
#         super().__init__(estimator)
#
#     def get_heat_names(self):
#         heats = [("F", 1)]
#         return heats
#
#     def update_surfer_points(self, surfers: SurferPool):
#         for heat_name, _ in self.get_heat_names():  #run all the heats
#             surfer_h = surfers.get_surfers_in_heat(heat_name)
#             assert len(surfer_h) == 2
#             self.estimator.estimate_totals(surfer_h)
#
#     def progress_winners(self, surfer_p: SurferPool):
#         for heat, heat_n in self.get_heat_names():
#             surfer_h = surfer_p.get_surfers_in_heat(heat)
#             assert len(surfer_h) == 2
#             surfer_h.sort(key=lambda s: (s.expected_totals[-1], random.random()))
#             winner = surfer_h[0]
#             winner.heat_list += ["W"]
