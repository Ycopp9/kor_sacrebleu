from tool import processor, correlation, resampling, score
from tool.tokenizer import koNLPy, kakao, base, subword, cv
from tool.metric.sacreBLEU import SacreBLEU
from tool.metric import nltkMetric
from tool import ver

import numpy
import pandas as pd
import os, sys
import argparse

DATA_PATH = './data'
SEG_PATH = os.path.join(DATA_PATH, 'segment_level/raw')
SACRE = ['bleu', 'chrf', 'ter']

TOOL = processor.FileProcessor(SEG_PATH)
FRAME = TOOL.makeFrame()

    
#2. quality control: IQR
def iqr():
    data = FRAME.iloc[:, 0].tolist()
    scores = score.Score(data)
    print('[Sample #] Before QC= {}, After QC= {}'.format(scores, scores.iqr()))
    return scores
    
def ci():
    ci, mean_score = iqr().estimate_ci()
    print('Confidence 95% = {:.2f} ~ {:.2f}'.format(mean_score - ci, mean_score + ci))
    
def ranking_cluster():
    for metric in SACRE:
        df = TOOL.selectFrame(metric)
        pearson = correlation.Correlation(df)
        print('Metric = {0}, Result = {1}'.format(metric, pearson.rank_cluster()), end='\n\n')
    
def bootstrap(step: int):
    m, n, iteration = 3000, 1000, 10
    print('# of sample_m: {0}, # of sample_n: {1}, iteration: {2} times'.format(m, n, iteration))
    samples = resampling.Resampling(frame=TOOL.selectFrame('bleu'), m=m, n=n, iteration=iteration)
    return samples.bootstrap_resampling(step)


def tokenizers():
    hyp = os.path.join(DATA_PATH, 'hyp_example.txt')
    ref = os.path.join(DATA_PATH, 'ref_example.txt')

    def read_file(file):
        with open(file, encoding='utf-8') as f:
            return f.readlines()[0]
    
    # prepare sample sentences
    hypothesis = read_file(hyp)
    reference = read_file(ref)
    sample = hypothesis.split('.')[0]
    
    # load tokenizers
    mecab = koNLPy.KoNLPy('mecab')
    kiwi = kakao.Kiwi()
    khaiii = kakao.Khaiii()
    char = base.Character()
    jamo = cv.Jamo(jamo_split=True)
    spm = subword.SPM()
    
    for tokenizer in [mecab, kiwi, khaiii, char, jamo, spm]:
        print(f'{tokenizer.__class__.__name__}: {tokenizer.tokenize(sample)}', end='\n\n')
    
    return hypothesis, reference
    

def parse_args():
    parser = argparse.ArgumentParser(
        description="An examplary script for the evaluation tools"
    )
    parser.add_argument('-s', '--step', default=2, type=int, help='resampling step')
    parser.add_argument('metric', type=str, help='bleu chrf ter gleu')
    return parser.parse_args()

def main():
    args = parse_args()
    
    #0. version info
    print('==Version Info==')
    ver.main()
    
    #1. rank clustering
    print('\n==Rank Cluster by Pearson by Metrics==')
    ranking_cluster()
    
    #2. bootstrap sampling
    bootstrap(args.step)
    
    #3. tokenize samples
    hyp, ref = tokenizers()
    
    #4. compute scores
    metric = args.metric
    if metric in SACRE:
        metric = SacreBLEU(metric)
    else:
        metric = nltkMetric.NLTK(metric)
    
    metric.hypothesis = hyp
    metric.references = ref
    score = metric.get_score(sys_level=False)
    print(f'{args.metric.upper()} score: {score:.4f}')
    
    
if __name__ == '__main__':
    main()
    sys.exit(0)