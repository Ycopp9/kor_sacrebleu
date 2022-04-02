from .base import Metric
from typing import Sequence, Optional

NAME = ['bleu', 'chrf', 'ter']

class SacreBLEU(Metric):
    def __init__(self,
                 name: str,
                force: bool = False,
                smooth_method: str = 'exp',
                smooth_value: Optional[float] = None,
                effective_order: bool = False,
                ):
        super().__init__()
        
        assert name.lower() in NAME, 'Metric not available!'
        self.name = name.lower()
        self.force = force
        if self.name == 'bleu': 
            self.force = True ###
        self.smooth_method = smooth_method
        self.smooth_value = smooth_value
        self.effective_order = effective_order
        
        try:
            import sacrebleu
        except:
            ImportError
        self.obj = sacrebleu
        self.method_sentence = f'sentence_{self.name}'
        self.method_corpus = f'corpus_{self.name}'
        
        
    def get_score(self, sys_level: bool = False) -> float:
        if sys_level:
            return super().get_score(method_name=self.method_corpus,
                                    corpus_level=True) 
        else:
            return super().get_score(method_name=self.method_sentence,
                                 corpus_level=False)
    