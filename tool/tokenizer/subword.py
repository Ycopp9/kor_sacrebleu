from .base import BaseTokenizer
import os


class SPM(BaseTokenizer):
    def __init__(self):
        try:
            import sentencepiece as spm
        except:
            ImportError
            print("!pip install sentencepiece")
        self.SPM = spm.SentencePieceProcessor()
        self.SPM.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),'spm.ko.model'))
    
    def tokenize(self, text):
        tokenized = []
        for token in self.SPM.EncodeAsPieces(text):
            if "▁" in token:
                tokenized.append(token[1:])
            else:
                tokenized.append(token)
        return tokenized
    