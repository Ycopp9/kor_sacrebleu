from typing import Optional
from importlib import import_module
from abc import ABCMeta, abstractmethod


_TOKENIZERS = {
        'none': 'base.BaseTokenizer',
        'konlpy': 'koNLPy.KoNLPy',
        'kiwi': 'kakao.Kiwi',
        'khaiii': 'kakao.Khaiii',
        'spm': 'subword.SPM',
        'jamo': 'subword.Jamo',
        'character': 'base.Character'
}

def get_tokenizer(name: str):
    module_name, class_name = _TOKENIZERS[name].rsplit('.', 1)
    return getattr(
        import_module(f'.tokenizer.{module_name}', 'tool'),
        class_name)



class Metric(metaclass=ABCMeta):
    TOKENIZERS = ['none', 'konlpy', 'kiwi', 'khaiii', 'subword']
    TOKENIZER_DEFAULT = TOKENIZERS[1] # Mecab
    
    def __init__(self,
                tokenize: Optional[str] = TOKENIZER_DEFAULT):
        if tokenize is None:
            best_tokenizer = self.TOKENIZER_DEFAULT
        else:
            best_tokenizer = tokenize
        self.tokenizer = get_tokenizer(best_tokenizer)()

    @abstractmethod    
    def by_sentence(self):
        pass
    
    @abstractmethod
    def by_corpus(self):
        pass
    
    @abstractmethod
    def by_document(self):
        pass
    
    @abstractmethod
    def normalize(self):
        pass