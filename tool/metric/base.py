from typing import Sequence, Optional


class Metric:
    def __init__(self, 
                 hypothesis: str = None,
                references: Optional[Sequence[Sequence[str]]] = None):
        self.hypothesis = hypothesis
        self.references = references
        
    
    def get_score(self, method_name, corpus_level=False):
        if corpus_level:
            self.hypothesis = [self.hypothesis]
            self.references = [self.references]
            
        return self.get_method(method_name)(self.hypothesis, self.references)