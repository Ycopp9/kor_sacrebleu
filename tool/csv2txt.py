import sys
import argparse
import pandas as pd
import csv

def parse_args():
    parser = argparse.ArgumentParser(
        description='Tsv to Txt',
        )
    parser.add_argument('-i', '--input', help='Input csv/tsv file',
                        required=True)
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
    preprocesses = args.preprocessing.split()
    for column in args.columns:
        for ppc in preprocesses:
            f=open("./result/{0}_{1}.txt".format(column, ppc), 'w')
            f.writelines([data+'\n' for data in df["{0}_{1}".format(column, ppc)].values.tolist()])
            f.close
        f=open("./result/{0}_None.txt".format(column), 'w')
        f.writelines([data+'\n' for data in df[column].values.tolist()])
        f.close
        

        
if __name__ == '__main__':
    main()
    sys.exit(0)
    