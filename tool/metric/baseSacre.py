import sacrebleu
from base import Metric
from typing import Sequence, Optional


class BaseSacre(Metric):
    def __init__(self,
                force: bool = False,
                smooth_method: str = 'exp',
                smooth_value: Optional[float] = None,
                effective_order: bool = False):
        try:
            import sacrebleu
        except:
            ImportError
            
        self.force = force
        self.smooth_method = smooth_method
        self.smooth_value = smooth_value
        self.effective_order = effective_order
    
    
    def get_method(self, method_name):
        return getattr(sacrebleu, method_name) 
    
    
    def get_score(self, method_name, corpus_level=False):
        return super().get_score(method_name, corpus_level).score
        