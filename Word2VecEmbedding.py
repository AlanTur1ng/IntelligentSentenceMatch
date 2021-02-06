# coding=GBK

from pyhanlp import *
import traceback
import warnings
import numpy as np
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import logging
from gensim.models import KeyedVectors
from scipy import spatial
from flask import Flask
import sys

app = Flask(__name__)

model=None

def load_model():
    #����ģ�͵��ڴ���
    global model
    model = KeyedVectors.load_word2vec_format('pretrainModel\\pretrain_word2vec_modelV1.vector', binary=False) 

class Word2VecTester():

    def __init__(self):
        model = Word2Vec(sentences, sg=1, size=100, window=5, min_count=5, negative=3, sample=0.001, hs=1, workers=4)

    def filtered_punctuations(self, token_list):
        try:
            punctuations = ['']
            token_list_without_punctuations = [word for word in token_list
                                                             if word not in punctuations]
            #print "[INFO]: filtered_punctuations is finished!"
            return token_list_without_punctuations

        except Exception as e:
            print (traceback.print_exc())


    def list_crea(self, everyone):
        list_word = []
        for k in everyone:
            fenci= filtered_punctuations(k)
            list_word.append(fenci)

        return list_word

class keywordMatchScore():

    def __init__(self):
        self.listpath = None
        self.sentence = None

    # ����ͣ�ô��б�
    def stopwordslist(self,listpath):
	    stopwords = [line.strip() for line in open(listpath, encoding='GBK').readlines()]
	    return stopwords


    # �Ծ��ӽ��зִ�
    def seg_sentence(self,sentence):
        sentence_seged = HanLP.segment(sentence.strip())
        stopwords = self.stopwordslist('stopwords.txt')  # �������ͣ�ôʵ�·��
        outstr = ''
        print("hanlp outputs: ", sentence_seged)
        for word in sentence_seged:
            if word.word not in stopwords:
                if word != '\t':
                    outstr += word.word
                    outstr += " "
        return outstr

    # ����ؼ���ƥ��÷�
    def score_compute(self, inputs1, inputs2):
        score = len(inputs1.intersection(inputs2)) / max(len(inputs1), len(inputs2)) 

        return score



def simlarityCalu(vector1,vector2):
    #�����������ƶ�
    vector1Mod = np.sqrt(vector1.dot(vector1))
    vector2Mod = np.sqrt(vector2.dot(vector2))

    if vector2Mod!=0 and vector1Mod!=0:
        simlarity=(vector1.dot(vector2))/(vector1Mod*vector2Mod)
    else:
        simlarity=0
    return simlarity

if __name__ == '__main__':

    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    load_model()
    #app.run()
    scoreMatcher = keywordMatchScore()
    inputs = open('knowledge\\test_input.txt', 'r') #����Ҫ������ļ���·��
    outputs = open('test_output.txt', 'w') #���ش������ļ�·��
    line_outputs = []
    embeddings_index = {}

    print('model sim: ', model.similarity('����', '�����'))
    print('model sim: ', model.similarity('����', '����ʡ'))
    print('model sim: ', model.similarity('������', '�����'))

    for line in inputs:
        print("�ؼ��ʣ�", HanLP.extractKeyword(line, 4))
        # �Զ�ժҪ
        print("ժҪ�䣺", HanLP.extractSummary(line, 2))
        line_seg = scoreMatcher.seg_sentence(line).strip()  # ����ķ���ֵ���ַ���
        line_outputs.append(line_seg.split(' '))
        print("line_outputs: ", line_outputs)
    
    cos_input = {}
    cos_output = []
    for sentence in line_outputs:
        avg_vec = []
        for token in sentence:
            #print("word ", token, "with embedding vector: ", model[token])#, embeddings_index[word])
            avg_vec.append(model[token])
        avg_embedding_test = np.mean(avg_vec,axis=0)
        print("average embedding: ", avg_embedding_test)
        cos_input[''.join(sentence)] = avg_embedding_test
        cos_output.append(avg_embedding_test)

    #index2word_set = set(model.wv.index2word)
    embeddings = 'knowledge\\test_embedding.txt' #����֪ʶ�������洢���ļ�·��
    with open(embeddings, 'w') as file_object:
        for k,v in cos_input.items():
            file_object.write(k + '\t'+ ','.join([str(x) for x in v])+'\t'
            + k��Ӧ�Ĵ�)

    print("���Ԥѵ�������ļ���")