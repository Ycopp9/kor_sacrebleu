import random
from collections import OrderedDict

import numpy as np
import pandas as pd

np.random.seed(42)

from .correlation import Correlation



class Resampling:
    """
    Given a dataframe, it realizes Bootstrapping by performing three random selections:
        i) #m samples from the total sample size
        ii) #n samples from the #m
        iii) #n samples from the #n while simultaneously iterating #iteration times.
    
    The final result is an average of the accumulated rankings on every 100 iterations. 
    """
    
    def __init__(self, frame, m, n, iteration):
        self.frame = frame
        self.m = m
        self.n = n
        self.iteration = iteration
        self.sample = len(self.frame) # 7727
        
        
    def pop(self, bag, size):
        return np.random.choice(bag, size)
    
    
    def pop_index(self) -> list:
        """ 1. Select #m from the total samples
            2. Select #n from #m """
        round_1 = self.pop(self.sample-1, self.m)
        round_2 = self.pop(round_1, self.n)
        return round_2
        
        
    def selectFrame(self, sample_idx:list):
        """ A partial dataframe of selected indexes """
        sample_df = pd.DataFrame(columns=self.frame.columns)
        
        for i, idx in enumerate(sample_idx):
            assert idx < len(self.frame), "Error: index out of range"
            sample_df.loc[i] = self.frame.iloc[idx, :]
        return sample_df
    
    
    def bootstrapping(self):
        """ Select #n on every iteration, and measure Pearson """
        pops = self.pop_index()
        zeros = OrderedDict((col, 0) for col in self.frame.columns)
        
        for i in range(1, self.iteration+1):
            round_3 = self.pop(pops, self.n)
            correlation = Correlation(self.selectFrame(round_3))
            ranking = correlation.rank_cluster()
            
            for k, v in ranking:
                zeros[k] += v
                    
            yield i, sorted(zeros.items(), key=lambda x: x[1])
        

    def bootstrap_resampling(self, every=100):
        """ Output a result on every # iterations """
        result_frame = pd.DataFrame(columns=self.frame.columns)
        
        for i, result in self.bootstrapping():
            if i%every == 0:
                for k, v in result:
                    result_frame.loc[i, k] = round((v/i), 3)
                
        return result_frame