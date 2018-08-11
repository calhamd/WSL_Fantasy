from surfer import SurferPool
from points_estimator import OddsPointEstimator, ComboPointsEstimator
import random
from random import shuffle

class RoundSettings:
    def __init__(self, name, heatcount, surferperheat, bonusround, lookupdictlist, seed_dict=None):
        self.name = name
        self.lookup_dict_list = lookupdictlist
        self.seed_dict = seed_dict
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

    def get_default_heat_name(self):
        return self.settings.name + "_?"

    def update_heat_maps(self, surfers: SurferPool):
        if self.settings.seed_dict:
            surfers.sort_surfers('rank')
            surfers = surfers.get_surfers_in_heat(self.get_default_heat_name())
            for i in range(0, len(surfers)):
                element_index = surfers[i].heat_list.index(self.get_default_heat_name())
                surfers[i].heat_list[element_index] = self.settings.seed_dict[i+1]

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
