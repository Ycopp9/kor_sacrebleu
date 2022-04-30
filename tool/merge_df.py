import pandas as pd
import os, sys
import argparse


COL = 'worker DocID SentID Sys Src Ref Hyp Adequacy Fluency Z_adequacy Z_fluency'.split()


def select_docID(doc_id:int, df):
    return df[df.DocID == doc_id]

def anonymize_sys(df, col='System'):
    # System info
    df['Sys'] = df[col].apply(lambda x: 'Sys_A' if x == 'Papago' 
                    else ('Sys_B' if x == 'Kakao' 
                          else ('Sys_P' if x == 'Google' else 'Sys_Q')))
    return df

def merge_tables(df1, df2):
    
    df = pd.merge(df1, df2, 
             how='outer',
             on=['worker', 'SentID', 'Sys'])
    df = df.rename(columns={col:col[:-2] for col in df.columns if '_x' in col})
    df = df.loc[:, COL].sort_values(by='SentID', ascending=True)
    return df
    

def run(file1, file2, docID:int):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2, sep='\t')
    
    # extract conditioned rows
    df1 = select_docID(docID, df1)
    df2 = select_docID(docID, df2)
    df2 = anonymize_sys(df2)
    
    # merge two tables
    df = merge_tables(df1, df2)
    df.to_csv(f'doc{docID}_merged.csv')
    
"""    
def parse_args():
    parser = argparse.ArgumentParser(
        description = 'Join tables by worker, sentID, and system'
    )
    parser.add_argument('df_to', help='base df')
    parser.add_argument('df_from', help='appended to the base df')
    parser.add_argument('doc_id', help='to select the given data', default=1)
    return parser.parse_args()


def main():
    args = parse_args()
    docID = args.doc_id.split()
    tab1 = args.df_to.split()
    tab2 = args.df_from.split()
    
    df1 = pd.read_csv(tab1)
    df2 = pd.read_csv(tab2, sep='\t')
    
    # extract conditioned rows
    df1 = select_docID(docID, df1)
    df2 = select_docID(docID, df2)
    df2 = anonymize_sys(df2)
    
    # merge two tables
    df = merge_tables(df1, df2)
    save_df(df, f'{tab1[:-4]}_{tab2[:-4]}_merged.csv')
    
if __name__ == '__main__':
    main()
    sys.exit(0)
    """