import os
import sys
import argparse

import numpy as np
import pandas as pd

from collections import namedtuple

import processor

import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.size'] = 12
sns.color_palette('Paired')


# path
IMG_PATH = './img'
DATA_SEG = './data/segment_level/raw' # txt
DATA_CORP = './data/corpus_level' # csv

# metric, token levels
Metrics = namedtuple('Metrics', 'name group')
Token = namedtuple('Token', 'name level')

TOKENS = {'meta': 'word morpheme subword character cv'.split(),
            'morpheme': 'kiwi khaiii kkma komoran hannanum okt mecab'.split()
            }
METRICS = {'sacre': 'Bleu Ter Chrf'.split(),
            'nltk' : 'Bleu Gleu Nist Ribes'.split(),
            'others': 'EED CharacTER'.split()
            }

HUMAN = 'Human'
M_TYPE = [Metrics(name, k) for k, v in METRICS.items() for name in v]
ED_TYPE = [m.name for m in M_TYPE if m.group == 'others']




def sub_df(col_name, df):
    """To select certain columns
    
    :param col_name: metrics name in the column
    :param df: base dataframe
    """
    return df.loc[:, [col for col in df.columns if col_name in col] + [HUMAN]]


def pearson_df(df, metric_level='segment', metric=None):
    """To compute Pearson Correlation r for the given level
    
    :param df: given dataframe
    :param metric_level: segment vs. corpus
    """
    
    df = df.corr('pearson')[HUMAN]
    df = df.drop(HUMAN)
    
    if metric_level == 'segment':
        # To set the metric name
        index0 = df.index[0]
        metric_name = index0[:index0.find('.')]
        df.index = [item[item.find('.')+1:] for item in df.index.tolist()]
    else: #corpus
        metric_name = metric
    
    # To convert the scores from negative to posive in edit-distance-related metrics
    if metric_name.upper().endswith('TER') or metric_name in ED_TYPE:
        df = df.apply(lambda x: x * -1)   
    return df.to_frame(metric_name)


def divide_token_level(df, tok_level:str):
    """To divde df into meta vs. morpheme token levels
    If the token level is meta, all morpheme levels are averaged to one. 
    
    :param df: base dataframe
    :param tok_level: meta, morpheme or None
    """
    assert tok_level in TOKENS.keys(), 'Choose between \'meta\' or \'morpheme\''
    token_unit = [Token(name.title(), k) for k, v in TOKENS.items() for name in v] 
    cols = [item.name for item in token_unit if item.level == tok_level]
    df['label'] = [0 if idx.title() in cols else 1 for idx in df.index]
    
    token_df = df[df.label == 0]   
    
    if tok_level == 'meta':
        token_df.loc['Morpheme'] = [np.mean(token_df.iloc[:, 0]), 0]
    return token_df


def change_columns(df):
    df.columns = [col.replace('None', 'Word')
                     .replace('Jamo', 'CV')
                     .replace('Mecab', 'MeCab')
                     .replace('Syllable', 'Character')
                     .replace('Spm', 'Subword') for col in df.columns]
    return df


def draw(fig_id:str, df, save:bool, tok_level:str):
    df = df.sort_values(by=df.columns[0], ascending=False)

    plt.figure(figsize=(9, 5))
    xlabel = df.columns[0]
    ylabel = 'Pearson r'
    
    # y축 범위 설정
    ymin = round(min(df.iloc[:, 0]) * 0.7, 2)
    ymax = round(max(df.iloc[:, 0]) * 1.1, 2)
    
    color_dict = connect_color(df, tok_level=tok_level)
    
    # hatch
    if max(df.iloc[:, 0]) >= 0.5: # corpus-level corrs are higher
        hatch = 'x'
    else: 
        hatch = '/'
    
    ax = df.plot.bar(y = xlabel,
                     rot = 0, 
                     color = [color_dict[idx] if idx in color_dict \
                                  else 'aquamarine' for idx in df.index],
                     alpha = .9,
                     edgecolor = 'black',
                     hatch=hatch)

    plt.ylim([ymin, ymax])
    for p in ax.patches:
        left, bottom, width, height = p.get_bbox().bounds
        ax.annotate('{:.3f}'.format(height), 
                    (left + width/2, height), 
                    ha='center', va='bottom')
    ax.get_legend().remove()
    plt.ylabel(ylabel)
    plt.title(f'Pearson Correlation of {df.columns[0]}')
    
    if save:
        save_figure(fig_id)
    plt.show()
    
     
def connect_color(df, tok_level:str):
    if tok_level == 'meta':
        colors = sns.color_palette('YlOrBr', len(df))
        return {m:c for m, c in zip(df.index, colors)}
        
    else:
        return {'Khaiii':'salmon'}


def save_figure(fig_id, tight_layout=True, fig_extension='png', resolution=300):
    path = os.path.join(IMG_PATH, fig_id+'.'+fig_extension)
    print('Saving the figure: ', fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


def parse_args():
    parser = argparse.ArgumentParser(
        description='score to img'
    )
    
    parser.add_argument('level', choices=['segment', 'corpus'], help='score compute level')
    #parser.add_argument('-p', '--path', help='file path')
    parser.add_argument('-s', '--save', action='store_false', help='To save the img')
    return parser.parse_args()


def main():
    args = parse_args()
    metric_level = args.level.split()
    for tok_level in TOKENS.keys():
        print(metric_level, tok_level)
        
        metrics = [f'{m.name}' if m.group == 'others' else f'{m.group + m.name}' for m in M_TYPE]
        for metric in metrics:
            if metric_level == 'segment':
                df = processor.FileProcessor(DATA_SEG).makeFrame()
                df = sub_df(metric, df)
                df = pearson_df(df, metric_level=metric_level)
                dfs = [df]
            else:
                dfs = []
                for file in [f for f in os.listdir(DATA_CORP) if not f.endswith('checkpoints')]:
                    df = pd.read_csv(os.path.join(DATA_CORP, file), index_col=0)
                    df = change_columns(df.T)
                    df = pearson_df(df, metric_level=metric_level, metric=file[:-4])
                    dfs.append(df)
                    
            for df in dfs:
                df = divide_token_level(df, tok_level=tok_level)
                draw(fig_id=f'Pearson.{metric_level[0]}.{tok_level}.{metric}',
                     df=df, 
                     save=args.save,
                     tok_level=tok_level)   

                
if __name__ == '__main__':
    main()
    sys.exit(0)