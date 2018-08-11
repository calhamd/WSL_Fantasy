
class Surfer:
    def __init__(self, name, odds, tier, initial_heat, rank):
        self.name = name
        self.odds = odds
        self.tier = tier
        self.heat_list = ["1_"+str(initial_heat)]
        self.expected_totals = []
        self.rank = rank

    def reset(self):
        self.heat_list = [self.heat_list[0]]
        self.expected_totals = []

class SurferPool:
    def __init__(self, surfers: [Surfer]):
        self.surfers = surfers

    def reset(self):
        for s in self.surfers:
            s.reset()

    def get_surfers_in_heat(self, heat_name):
        return [s for s in self.surfers if heat_name in s.heat_list]

    def get_surfers_in_tier(self, tier_name):
        return [s for s in self.surfers if tier_name in s.tier]

    def sort_surfers(self, key='rank'):
        try:
            self.surfers.sort(key=lambda x: getattr(x, key))
        except Exception as e:
            raise ValueError("Key not part of surfer class")
