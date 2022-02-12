from .base import BaseTokenizer

import konlpy
from konlpy.tag import *



_TOKENIZERS = ['Kkma', 'Okt', 'Mecab', 'Komoran', 'Hannanum']
TOKENIZER_DEFAULT = _TOKENIZERS[2]

MSG = {'WrongTokenizerName':'KoNLPy does not support such tokenizer!',
          'KkmaOnly':'Only possible with Kkma!'}

def get_tokenizer(name: str):
    return getattr(konlpy.tag, name.title())


class KoNLPy(BaseTokenizer):
    def __init__(self, name: str = TOKENIZER_DEFAULT):
        if name is None:
            the_tokenizer = TOKENIZER_DEFAULT
        else:
            assert name in _TOKENIZERS, MSG['WrongTokenizerName'] 
            the_tokenizer = name

        self.tokenizer = get_tokenizer(the_tokenizer)()
        
        
    def tokenize(self, sentence:str) -> list:
        """ morpheme-level tokenization """
        return self.tokenizer.morphs(sentence)
    
    
    def split_sentence(self, text:str) -> list:
        assert self.name.title() == _TOKENIZERS[0], MSG['KkmaOnly']
        return self.tokenizer.sentences(text)
    
    
    def __call__(self):
        print('Tokenizer: ', self.tokenizer)
        print('Sample Translation:\n', self.tokenize(super().sample))