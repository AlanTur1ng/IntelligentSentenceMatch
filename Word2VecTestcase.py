# coding=GBK

import traceback
import warnings
import numpy as np
from gensim.models import KeyedVectors
from flask import Flask
import sys

import csv
from pandas.core.frame import DataFrame
import pandas as pd




if __name__ == "__main__":

    tmp_lst = []
    with open('��������v1.csv', 'r') as fh:
        reader = csv.reader(fh)
        for row in reader:
            tmp_lst.append(row)
    df = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0]) 

    print("����������ȡ���ݣ� \n")
    print(df['similarQuestion'].str.split('\n', expand=True))