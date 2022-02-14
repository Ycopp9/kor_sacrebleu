from typing import List
from .base import BaseTokenizer
from khaiii import KhaiiiApi
from kiwipiepy import Kiwi, Option


class Kiwi(BaseTokenizer):
    def __init__(self,
                punctuations: List[str] = None,
                top_n: int = None):
        try:
            from kiwipiepy import Kiwi, Option
        except:
            ImportError
            print("Installation guideline => https://github.com/bab2min/Kiwi")
        self.tokenizer = Kiwi()
        
        # Error occurs when with these punctuations in a sentence
        self.punctuations = ['@']
        if punctuations:
            self.punctuations += punctuations
    
        self.top_n = 5
        

    def tokenize(self, text):
        for item in self.punctuations:
            text = text.replace(item, '')
        
        for line in self.tokenizer.analyze(text, self.top_n):
            return [item[0] for item in line[0]]


class Khaiii(BaseTokenizer):
    def __init__(self):
        try:
            from khaiii import KhaiiiApi
        except:
            ImportError
            print("Installation guideline => https://github.com/kakao/khaiii")
        self.tokenizer = KhaiiiApi()
        

    def tokenize(self, text):
        return [word.lex for line in self.tokenizer.analyze(text)\
                    for word in line.morphs]
    
    