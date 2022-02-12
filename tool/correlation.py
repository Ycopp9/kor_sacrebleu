import numpy as np
import scipy.stats as sts

    
    
class Correlation:
    """
    Given a dataframe of the automatic metric scores of some candidates along with human DA scores,
    it computes the Pearson correlation coefficient (as a default choice) of each candidate,
    and make a cluster of their ranks with the help of Wilcoxon rank sum test,
    where the p-value of any two candidates bigger than 0.05 is regarded to tie with one another.    
    """
    
    def __init__(self, frame):
        self.frame = frame
    
    
    def to_array(self, col):
        return np.array((self.frame[col]), dtype=np.float64)
    
    
    def ranksums_test(self, col1: str, col2: str) -> float: 
        """ Ranksum test between col_A and col_B """
        if col1 == col2:
            return -1
        
        p_value = sts.ranksums(self.to_array(col1), self.to_array(col2)).pvalue
        return p_value
    
    
    def column_by_Pearson(self):
        """ Columns ranked by Pearson correlation to Human DA """
        assert 'Human' in self.frame.columns, 'Absent: "Human" scores'
        
        result = self.frame.corr('pearson')['Human']
        values = [v for _, v in result.items()]
        
        sortedV = np.argsort(values)[::-1]
        sortedK = np.array(result.keys())[sortedV]
        sortedCols = np.delete(sortedK, np.where(sortedK == 'Human'))
        
        return sortedCols
    
    
    def rank_cluster(self):
        """ Rank cluster of candidates """
        candidates = self.column_by_Pearson()
        num_col = len(candidates)
        
        pairwise = np.array([[self.ranksums_test(col1, col2) for col2 in candidates]\
                             for col1 in candidates])
        cluster = np.zeros(num_col).astype(int)
        
        for i in range(num_col-1):
            if all(pairwise[i, i+1:] < 0.05):
                cluster[i+1:]+=1
             
        return list(zip(candidates, cluster))

