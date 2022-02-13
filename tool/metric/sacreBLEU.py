from baseSacre import BaseSacre


class SacreBLEU(BaseSacre):
    def __init__(self, name: str):        
        assert name.lower() in ['bleu', 'chrf', 'ter'], 'Metric not available!'
        self.name = name.lower()
        if self.name == 'bleu': 
            self.force = True ###
            
        self.method_sentence = f'sentence_{self.name}'
        self.method_corpus = f'corpus_{self.name}'
        
        
    def compute_score(self, sys_level=False) -> float:
        if sys_level:
            method = self.method_corpus
            corpus_level = True
        else:
            method = self.method_sentence
            corpus_level = False
        return super().get_score(method, corpus_level)