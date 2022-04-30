import sys

import numpy
import pandas
import scipy

import nltk

import konlpy
import sentencepiece
from khaiii import KhaiiiApi
from kiwipiepy import Kiwi

import cmake
import sacrebleu

def main():
    for library in [numpy, pandas, konlpy, scipy, nltk, sacrebleu, cmake, sys, KhaiiiApi(), Kiwi()]:
        try:
            print(f'version={library.__version__}, {library}')
        except AttributeError as e:
            print(e)
            print(f'version={library.version}')
            
if __name__ == '__main__':
    main()