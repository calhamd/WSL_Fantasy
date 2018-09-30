from random import shuffle, choice, uniform
import numpy

class PointsEstimator:
    def __init__(self):
        pass

    def estimate_totals(self, surfers: []):
        pass


class OddsPointEstimator(PointsEstimator):
    max_score = 15
    min_score = 10
    decimal_points = 3

    def __init__(self):
        super().__init__()

    def estimate_totals(self, surfers: []):
        updates = []
        clipped_random_scores = []
        shuffle(surfers)
        for surfer in surfers:
            adj_score = 1.2*pow(surfer.odds, -0.5)
            randomization_score = numpy.random.normal(loc=0, scale=0.3)
            trial_score = adj_score + randomization_score
            clipped_random_scores.append(max(min(trial_score, 1), 0))
        for i in range(0, len(surfers)):
            update = (clipped_random_scores[i] * (self.max_score - self.min_score)) + self.min_score
            update = round(update, self.decimal_points)
            while update in updates:
                update += choice([-pow(10, -self.decimal_points), pow(10, -self.decimal_points)])
                update = round(update, self.decimal_points)
            updates.append(update)
            surfers[i].expected_totals.append(update)
        return max(updates)

    def __get_total_odds(self, surfers):
        total_odds = 0
        for surfer in surfers:
            total_odds += surfer.odds
        return total_odds


class ComboPointsEstimator(PointsEstimator):
    max_score = 15
    min_score = 10
    decimal_points = 3

    def __init__(self):
        super().__init__()

    def estimate_totals(self, surfers: []):
        updates = []
        clipped_random_scores = []
        shuffle(surfers)
        for surfer in surfers:
            adj_score = 1.2*pow(surfer.odds, -0.5)
            randomization_score = numpy.random.normal(loc=0, scale=1)
            trial_score = adj_score + randomization_score
            clipped_random_scores.append(max(min(trial_score, 1), 0))
        for i in range(0, len(surfers)):
            update = (clipped_random_scores[i] * (self.max_score - self.min_score)) + self.min_score
            update = round(update, self.decimal_points)
            while update in updates:
                update += choice([-pow(10, -self.decimal_points), pow(10, -self.decimal_points)])
                update = round(update, self.decimal_points)
            updates.append(update)
            surfers[i].expected_totals.append(update)
        return max(updates)


class ComboPointsEstimator2(PointsEstimator):
    max_score = 17
    min_score = 8
    decimal_points = 3

    def __init__(self):
        super().__init__()

    def estimate_totals(self, surfers: []):
        updates = []
        clipped_random_scores = []
        shuffle(surfers)
        for surfer in surfers:
            adj_score = 1*pow(surfer.odds, -0.3)
            randomization_score = numpy.random.normal(loc=0, scale=0.5)
            if randomization_score > 0:
                trial_score = adj_score + (1-adj_score) * randomization_score
            else:
                trial_score = adj_score + adj_score * randomization_score
            clipped_random_scores.append(trial_score)
            #clipped_random_scores.append(max(min(trial_score, 1), 0))
        for i in range(0, len(surfers)):
            update = (clipped_random_scores[i] * (self.max_score - self.min_score)) + self.min_score
            update = min(round(update, self.decimal_points), 20-pow(10, -self.decimal_points))
            while update in updates:
                update += choice([-pow(10, -self.decimal_points), pow(10, -self.decimal_points)])
                update = round(update, self.decimal_points)
            updates.append(update)
            surfers[i].expected_totals.append(update)
        return max(updates)