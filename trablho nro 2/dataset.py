import pandas as pd
import yaml
import numpy as np
import random
from math import log2

class Dataset():
    data = pd.DataFrame()
    categorical_features = []
    continuous_features = []
    yaml_structure = {}
    target_feature = ''
    target_type = ''

    '''
    Load the CSV/TSV file, saves it in data
    '''
    def load_dataset(self, input_path, separator):
        self.data = pd.read_csv(input_path, sep=separator)
        self.data.columns = self.data.columns.astype(str)
    
    
    '''
    Read the structure and get the types of the columns in two list [categorical, coninuous]
    Set target_column and target_type
    '''
    def read_structure(self, input_file, target_column):
        with open(input_file) as f:
            self.yaml_structure = yaml.load(f, Loader=yaml.FullLoader)
        self.target_feature = target_column
        self.target_type = self.yaml_structure['target']['type']
        
        self.categorical_features = []
        self.continuous_features = []
        
        for feature in self.yaml_structure['features']:
            if feature['type'] == 'continuous':
                self.continuous_features.append({'name': str(feature['name'])})
                
            else:
                self.categorical_features.append({'name': str(feature['name'])})

    
    '''##############################'''
    '''##############################'''
    '''BOOTSTRAP'''
    def build_bootstrap(self, data):
        data.reset_index(drop=True, inplace=True)
        [m,n] = data.shape
        index_train = [] # index set of training set
        index_test  = [] # index set of test set
        tol = 0
        data_split = {'train':index_train} # set that contain train and test set split of Dataset
#         data_split = {'train':index_train, 'test': index_test} # set that contain train and test set split of Dataset
        while tol<100:
            for i in range(0,m):
                index_train.append(np.random.randint(0, m))
            for i in range(0,m):
                try:
                    index_train.index(i)
                except:
                    index_test.append(i)

            if len(index_test)<=round(0.35*m):
                    tol =100
            else:
                index_train = []
                index_test  = []
                if tol == 99:
                    print(tol)
                    tol = 0
            tol = tol+1

        data_split['train'] = data.iloc[index_train]
        return data_split

    def get_n_bootstrap(self, data, n_tree):
        data.reset_index(drop=True, inplace=True)
        [m,n] = data.shape
        S_data_boostrap = {}
        for i in range(0,n_tree):
            S_data_boostrap[i] = self.build_bootstrap(data)
        return S_data_boostrap

    
    def K_folds(self, data, k): # Split a group in k- subgroups
        data.reset_index(drop=True, inplace=True)
        N = data.shape[0]
        index = np.random.randint(0, N,size=N)
        n_folds = N//k
        idfold = np.arange(0,N,n_folds)
        k_folds = {}
        for i in range(0,k):
            if i == k-1:
                k_folds[i] = data.iloc[index[idfold[i]:N]]
            else:
                k_folds[i] = data.iloc[index[idfold[i]:idfold[i+1]]]
        return k_folds
    
    
    def K_folds_final(self, k_folds,k): # Takes k-1 folds for training, and the remaining fold for testing
        date_fold = {}
        temp = {}
        aux = 0
        for i in range(0, k):
            test = None
            train = pd.DataFrame(columns=list(k_folds[0].columns))
            for j in range(0,k):
                if i == j:
                    test = k_folds[j]
                else:
                    train = train.append(k_folds[j])
            date_fold[i] = {'train': train, 'test': test}   
        return date_fold
    
    def get_n_class_k_final_folds(self, k):
        '''
        k-fold cross-validation stratified
        ----------------------------------
        k: # number of split of the k-folds
        '''
        
        k_folds_c = []
        for tar in self.data.target.unique():
            ci = self.data[self.data.target==tar]   
            k_folds_c.append(self.K_folds(ci,k))
#         c1 = self.data[self.data.target==1]   # c1: represent the one class(ceros)
#         c2 = self.data[self.data.target==2]   # c2: represent the two class(ones)
#         c3 = self.data[self.data.target==3]   # c3: represent the two class(ones)
#         k_folds_c1 = self.K_folds(c1,k) # Split of c1 in k=folds
#         k_folds_c2 = self.K_folds(c2,k) # Split of c2 in k=folds
#         k_folds_c3 = self.K_folds(c3,k) # Split of c3 in k=folds
        k_folds = {} # represent of k-fold cross-validation stratified total
        for i in range(0,k):
            k_folds[i] = k_folds_c[0][i]
            for j in range(1, len(self.data.target.unique())):
                k_folds[i] = k_folds[i].append(k_folds_c[j][i])
#             k_folds[i] = k_folds_c1[i].append(k_folds_c2[i])
#             k_folds[i] = k_folds[i].append(k_folds_c3[i])
        k_folds_final = self.K_folds_final(k_folds,k) # contains all test and training combinations of the k groups

        return k_folds_final
    
    '''##############################'''
    '''##############################'''
    
    '''
    Initialization
    '''
    def __init__(self, file_dataset_path, file_structure_path, char_separator='\t', target_column='target'):
        self.load_dataset(file_dataset_path, char_separator)
        self.read_structure(file_structure_path, target_column)
