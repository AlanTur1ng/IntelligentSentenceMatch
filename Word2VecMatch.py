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
            if word not in stopwords:
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
    scoreMatcher = keywordMatchScore()
    #app.run()
    knowledgeBase = {}
    embeddings = 'knowledge\\test_embedding.txt' #����֪ʶ�������洢���ļ�·��
    with open(embeddings, 'r') as file_object:
        for line in file_object:
            knowledgeBase[line.split(':')[0]] = line.split(':')[1].split(',')
            print('model input embedding: ', line)
    

    #index2word_set = set(model.wv.index2word)

    #s1_afv = avg_feature_vector(line_outputs[0], model=model, num_features=300, index2word_set=index2word_set)
    #s2_afv = avg_feature_vector(line_outputs[1], model=model, num_features=300, index2word_set=index2word_set)
    #sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)

    inputs = sys.argv[1]

    line_seg = scoreMatcher.seg_sentence(inputs).strip()  # ����ķ���ֵ���ַ���
    line_inputs = line_seg.split(' ')
    print("line_inputs: ", line_inputs)
    inputs = [inputs]
    for line in inputs:
        print("�ؼ��ʣ�", HanLP.extractKeyword(line, 4))
        # �Զ�ժҪ
        print("ժҪ�䣺", HanLP.extractSummary(line, 2))
        line_seg = scoreMatcher.seg_sentence(line).strip()  # ����ķ���ֵ���ַ���


    load_model()

    sin_output = []
    avg_vec = []
    rankList = []
    rankDict = {}
    for token in line_inputs:
        #print("word ", token, "with embedding vector: ", model[token])#, embeddings_index[word])
        avg_vec.append(model[token])
    sin_output = np.mean(avg_vec,axis=0)

    
    for sentence, embedding in knowledgeBase.items():
        trans_emb = np.array(embedding, dtype=np.float)
        sim_score = simlarityCalu(sin_output, trans_emb)
        rankList.append(sim_score)
        print("cos outputs: ",sentence,' with ', sim_score)
        rankDict[sentence] = sim_score
    # print("ranked list: ", sorted(rankDict.items()))

    def sorted_dict(container, keys, reverse):
         """���� keys ���б�,����container�ж�Ӧ��ֵ����"""
         aux = [ (container[k], k) for k in keys]
         aux.sort()
         if reverse: aux.reverse()
         return [(k, v) for v, k in aux]
    print("\n")
    order = 0

    for seg in sorted_dict(rankDict,rankDict.keys(),True):
        print("ƥ�䵽����ܵ�Top%d ����Ϊ"% order,seg[0], " ���ʣ�", order,seg[1])
        order += 1

   # model = gensim.models.Word2Vec.load('D:\BaiduNetdiskDownload\sgns.weibo.word\sgns.weibo.word')
    # ������
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    #sentences = word2vec.Text8Corpus("D:\wiki\11.txt")  
    n_dim=300
     # ѵ��skip-gramģ��; 
    #model = word2vec.Word2Vec(sentences, size=n_dim, min_count=5,sg=1) 
    # ���������ʵ����ƶ�/��س̶�
    print("y1")
    print("--------")
    # Ѱ�Ҷ�Ӧ��ϵ

