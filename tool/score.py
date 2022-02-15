import numpy as np
from typing import List


class Score:
    def __init__(self, 
                 scores: List[float]):
        self.scores = scores
        
        self.iqr_weight = 1.5
        self._mean = -1.0
        self._ci = -1.0
    
    
    def get_thresholds(self):
        quantile_25 = np.percentile(self.scores, 25)
        quantile_75 = np.percentile(self.scores, 75)

        IQR = quantile_75 - quantile_25
        IQR_weight = IQR * self.iqr_weight

        lowest = quantile_25 - IQR_weight
        highest = quantile_75 + IQR_weight
        return lowest, highest
    
    
    def iqr(self):
        """ Interquartile Range 
        In descriptive statistics, the interquartile range tells you \
        the spread of the middle half of your distribution.
        """
        lowest, highest = self.get_thresholds()
        return [score for score in self.scores \
                    if score > lowest and score < highest]
        
        
    def estimate_ci(self):
        """ Confidence Interval (CI)
        A confidence interval displays the probability 
        that a parameter will fall between a pair of values around the mean.
        The 95% certainty is guaranteed in this computation: _mean +- _ci
        """
        raw_scores = sorted([x for x in self.scores])
        n = len(raw_scores)
        
        lower_idx = n // 40
        upper_idx = n - lower_idx - 1
        lower, upper = raw_scores[lower_idx], raw_scores[upper_idx]
        self._ci = 0.5 * (upper - lower)
        self._mean = np.mean(raw_scores)
        
        return self._ci, self._mean
    
    
    def normalize_over(self, limit: float = 100.0) -> List[float]:
        return [(limit if score > limit else score) \
                            for score in self.scores]