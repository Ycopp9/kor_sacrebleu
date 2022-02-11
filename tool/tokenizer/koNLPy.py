from konlpy.tag import *
from .base import BaseTokenizer


class KoNLPy(BaseTokenizer):
    global msg
    msg = {'WrongTokenizerName':'KoNLPy does not support such tokenizer!',
          'KkmaOnly':'Only possible with Kkma!'}

    def __init__(self, tokenizer):
        self.tokenizers = {'kkma': Kkma, 'okt': Okt, 'mecab': Mecab,
                          'komoran': Komoran, 'hannanum': Hannanum}
        
        if tokenizer not in self.tokenizers.keys():
            raise ValueError(msg['WrongTokenizerName'])
        self.tokenizer = self.tokenizers[tokenizer]
        
        
    def tokenize(self, sentence:str) -> list:
        """ morpheme-level tokenization """
        
        return self.tokenizer().morphs(sentence)
    
    def split_sentence(self, text:str) -> list:
        assert self.tokenizers['kkma'] == self.tokenizer, msg['KkmaOnly']
        return self.tokenizer().sentences(text)
    
    def __call__(self):
        print('Tokenizer: ', self.tokenizer)
        print('Sample Translation:\n', self.tokenize(super().sample))