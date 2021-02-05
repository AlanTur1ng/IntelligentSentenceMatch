# coding=GBK

import sys
import csv
import traceback
import warnings
import numpy as np
from gensim.models import KeyedVectors
from flask import Flask
from pandas.core.frame import DataFrame
import pandas as pd

from Word2VecEmbedding import *

def load_model():
    #����ģ�͵��ڴ���
    global model
    model = KeyedVectors.load_word2vec_format('pretrainModel\\pretrain_word2vec_modelV1.vector', binary=False) 

def preprocessDataframe(df, mode=True):
    #����dataframe��ȡ����
    questionList = df['knowledge'].values.tolist()
    answerList = df['Answer'].values.tolist()
    qaDict = dict(zip(questionList, answerList))
    if mode:
        print("�����б����:",qaDict)

    return qaDict

if __name__ == "__main__":

    tmp_lst = []
    with open('��������v2.csv', 'r') as fh:
        reader = csv.reader(fh)
        for row in reader:
            tmp_lst.append(row)
    df = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0]) 
    #df_simsplit = df['similarQuestion'].str.split('\n', expand=True)
    print("����������ȡ���ݣ� \n")
    print(df)

    emb_dict = preprocessDataframe(df)

    print(("* Loading Keras model and Flask starting server..."
    "please wait until server has fully started"))
    load_model()
    #app.run()
    scoreMatcher = keywordMatchScore()
    inputs = open('knowledge\\test_input.txt', 'r') #����Ҫ������ļ���·��
    outputs = open('test_output.txt', 'w') #���ش������ļ�·��
    line_keys = []
    line_values = []
    embeddings_index = {}

    for line in emb_dict.keys():
        print("�ؼ��ʣ�", HanLP.extractKeyword(line, 4))
        # �Զ�ժҪ
        print("ժҪ�䣺", HanLP.extractSummary(line, 2))
        line_seg = scoreMatcher.seg_sentence(line).strip()  # ����ķ���ֵ���ַ���
        line_keys.append(line_seg.split(' '))
        line_values.append(emb_dict[line])
        print("line_outputs: ", (line_keys, line_values))
    

    emb_output = []
    cos_output = []
    for sentence in line_keys:
        avg_vec = []
        for token in sentence:
            #print("word ", token, "with embedding vector: ", model[token])#, embeddings_index[word])
            avg_vec.append(model[token])
        avg_embedding_test = np.mean(avg_vec,axis=0)
        print("average embedding: ", avg_embedding_test)
        cos_output.append(''.join(sentence))
        emb_output.append(avg_embedding_test)

    #index2word_set = set(model.wv.index2word)
    embeddings = 'knowledge\\test_embedding.txt' #����֪ʶ�������洢���ļ�·��
    with open(embeddings, 'w') as file_object:
        for question, answer,embedding in line_keys, line_values, emb_output:
            file_object.write(question + '\t'+ answer + '\t' +  ','.join([str(x) for x in embedding]))

    print("���Ԥѵ�������ļ���")