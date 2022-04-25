import sys
import argparse
import pandas as pd
import time
import random

import MeCab
TOKENIZER = MeCab.Tagger(f"--dicdir /usr/local/lib/mecab/dic/mecab-ko-dic")
import sentencepiece as spm
SPM = spm.SentencePieceProcessor()
from konlpy.tag import Kkma
KMA = Kkma()
from konlpy.tag import Hannanum
HNN = Hannanum()
from konlpy.tag import Okt
OKT = Okt()
from konlpy.tag import Komoran
KMR = Komoran()
from khaiii import KhaiiiApi
KHA = KhaiiiApi()
from kiwipiepy import Kiwi
KWI = Kiwi()
from jamo import h2j

class Konlpytokenizer:
    def __init__(self, tokenizer):
        self.tokenizer=tokenizer
    def __call__(self, text):
        return " ".join(self.tokenizer.morphs(text))
    
def mecabtokenize(text):
    tokenized = []
    for mor in TOKENIZER.parse(text).split("\n"):
        if "\t" in mor:
            tokenized.append(mor.split("\t")[0])
    return " ".join(tokenized)

def spmtokenize(text):
    tokenized = []
    for token in SPM.EncodeAsPieces(text):
        if "▁" in token:
            tokenized.append(token[1:])
        else:
            tokenized.append(token)
    return " ".join(tokenized)

def khaiiitokenize(text):
    return " ".join([l.lex for morph in KHA.analyze(text) for l in morph.morphs])

def kiwitokenize(text):
    #return " ".join([tok.form for tok in KWI.tokenize(text)]) 
    return " ".join([tok[0][0].form for tok in KWI.analyze(text)]) 

def syllable(text):
    return " ".join(list(text.replace(" ", "")))

def CV(text):
    return " ".join(list(h2j(text).replace(" ", "")))

def preprocessing(pp):
    if 'Mecab' in pp:
        return mecabtokenize
    if 'Spm' in pp:
        return spmtokenize
    if 'Kkma' in pp:
        return Konlpytokenizer(KMA)
    if 'Hannanum' in pp:
        return Konlpytokenizer(HNN)
    if 'Okt' in pp:
        return Konlpytokenizer(OKT)
    if 'Komoran' in pp:
        return Konlpytokenizer(KMR)
    if 'Khaiii' in pp:
        return khaiiitokenize
    if 'Kiwi' in pp:
        return kiwitokenize
    if 'Syllable' in pp:
        return syllable
    if 'CV' in pp:
        return CV
    return (lambda x: x)


def check_args(args, index):
    for column in args.columns:
            if column not in index:
                print("Error! no attribute {0}".format(column))
                sys.exit(1)
    return

def parse_args():
    parser = argparse.ArgumentParser(
        description='Tsv to Txt',
        )
    parser.add_argument('-i', '--input', help='Input csv/tsv file',
                        required=True)
    parser.add_argument('-s', '--spm', help='path of spm model', default='ko.model')
    parser.add_argument('-p', '--preprocessing', type=str, help='preprocessing tokenizer')
    parser.add_argument('-c', '--columns', type=str, help='ref/hyp etc', required=True)
    return parser.parse_args()

def main():
    args = parse_args()
    args.columns=args.columns.split()
    if args.input.split('.')[-1]=='tsv':
        args.tsv=True
    else:
        args.tsv=False
    if not args.tsv:
        df = pd.read_csv(args.input)
    else:
        df = pd.read_csv(args.input, sep='\t')
    SPM.load(args.spm)
    check_args(args, df.columns)
    preprocesses = args.preprocessing.split()
    random.shuffle(preprocesses)
    print('preprocessing', preprocesses)
    for column in args.columns:
        df[column]=df[column].apply((lambda x: x.strip()))
#     times= []
    for process in preprocesses:
        for column in args.columns:
            preprocess_func = preprocessing(process)
            start = time.time()
            df["{0}_{1}".format(column, process)] = df[column].apply(preprocess_func)
            print('{} {} completed'.format(column, process))
#             times.add(process, time.time()-start)
            print("time :", time.time() - start)

    if not args.tsv:
        df.to_csv("{0}.ppc.csv".format(args.input[:-4]))
    else:
        df.to_csv("{0}.ppc.tsv".format(args.input[:-4]), sep='\t')
    
    
        
if __name__ == '__main__':
    main()
    sys.exit(0)
    