from .base import BaseTokenizer
from jamo import h2j, j2hcj


class SPM(BaseTokenizer):
    def __init__(self):
        pass
    
    def tokenize():
        pass
    

class Jamo(BaseTokenizer):
    def __init__(self,
                 jamo_split: bool = False):
        try:
            from jamo import h2j, j2hcj
        except:
            ImportError
            print("!pip install jamo (https://pypi.org/project/jamo/)")
            
        # if True, all jamos are given as a seperate token
        # if False, a string boundary remains at word
        self.jamo_split = jamo_split    
        
    
    def tokenize(self, text):
        text = j2hcj(h2j(text))
        if self.jamo_split:
            return [token for token in text]
        return text.split()