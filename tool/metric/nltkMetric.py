import nltk
from nltk.translate import *

from .base import Metric
from typing import Sequence, Optional

NAME = ['bleu', 'gleu', 'nist', 'ribes']
# nltk.translate -> ribes_score -> sentence_ribes

class NLTK(Metric):
    def __init__(self, name: str,
                smooth_method: bool = False
                ):
        super().__init__()
        
        assert name.lower() in NAME, 'Wrong tokenizer name!'
        self.name = name.lower() #ribes
        self.obj = nltk.translate
        self.tokenizer = super().get_method(f'{self.name}_score') #ribes_score
        self.obj = self.tokenizer
        self.method_sentence = f'sentence_{self.name}' #sentence_ribes
        self.method_corpus = f'corpus_{self.name}'
        self.reverse = True
        
        # smoothing_function
        self.smooth_method = smooth_method
        self.smoothing_function = None
        if self.smooth_method:
            self.smoothing_function = self.tokenizer.SmoothingFunction().method1
           
        
    def get_score(self, sys_level: bool = False) -> float:
        if sys_level:
            return super().get_score(method_name=self.method_corpus,
                                    corpus_level=True,
                                    smoothing_function=self.smoothing_function
                                    )
        else:
            return super().get_score(method_name=self.method_sentence,
                                 corpus_level=False,
                                    smoothing_function=self.smoothing_function
                                    )
        
 