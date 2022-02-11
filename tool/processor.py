import os

import pandas as pd
import numpy as np


class FileProcessor:
    
    def __init__(self, folder):
        self.folder = folder
    
    def openFile(self, file_path):
        """ Open one .txt file """
        
        with open(file_path) as f:
            data = [line.strip() for line in f.readlines()]    
        #print('Toal: {} sentences'.format(len(data)))
        
        return data
        
    def openFiles(self, ending='.txt'):
        """ Open multiple .txt files """
        
        score_dict = dict()
        for file in os.listdir(self.folder):
            if file.endswith(ending):
                data = self.openFile(os.path.join(self.folder, file))
                score_dict[file.replace(ending, '')] = data
        
        print('Total number of files: {}'.format(len(score_dict)))
        return score_dict
    
    def makeFrame(self, human_score='adequacy_zscore.txt'):
        """ Make a dataframe of metric scores with human DA """
        
        df = pd.DataFrame(self.openFiles())
        df['Human'] = self.openFile(os.path.join('./data/humanDA', human_score))
        
        return df.astype(np.float64).round(4)
        
    def write(self, text, file_path):
        """ Write a file out """
        
        with open(file_path, 'w') as f:
            for line in text:
                f.write(str(line)+'\n')
        print('File written in... ', file_name)