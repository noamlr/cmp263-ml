import pandas as pd
import yaml
import numpy as np
import random
from math import log2

class Node():
    
    def __init__(self, data):
        self.is_leaf = data['is_leaf']
        self.answer = data['answer']
        self.feature_check = data['column'] 
        self.children_type = '' # if categorical C value_to_check - string, otherwise if Continuous N value_to_check numeric and validate if check_less
        self.value_to_check = data['value_to_check']
        self.check_less = data['check_less']
        self.children = [] ## just two if n_type = N (numerical) [less, greater or equal]
    
    def set_children_type(self, value):
        self.children_type = value
        
    def set_is_leaf(self, value):
        self.is_leaf = value
    
    def get_children(self):
        return self.children
    
    def insert_node(self, node):
        # self.children = self.children.append(node) 
        self.children.append(node) 
    
    def get_classification(self, row):
        if self.is_leaf: 
#             print(f'LEAF_ ans: {self.answer}', end=' ')
            return self.answer
        else:
            '''Categorical'''
            if self.children_type == 'C':
                for child in self.children:
#                     print(f'feature_check: {child.feature_check}')
                    if row[child.feature_check] == child.value_to_check:
                        return child.get_classification(row)
#                 print(f'Cans: {self.answer}', end=' ')
                return self.answer
            else:
                '''Numerical'''
#                 print(f'feature_check: {self.children[0].feature_check}')
                if row[self.children[0].feature_check] < self.children[0].value_to_check:
                    return self.children[0].get_classification(row)
                else:
                    return self.children[1].get_classification(row)
    
    def print_tree(self, level=0):
        print(f'lvl:{level}, Leaf: {self.is_leaf}, type: {self.children_type}, feature_check: {self.feature_check}, check: {self.value_to_check}, answer: {self.answer}')
        if self.is_leaf:
            print(f'lvl:{level}, answer: {self.answer}\n')
        else:
            for child in self.children:
                child.print_tree(level=level+1)
