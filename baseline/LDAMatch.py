import codecs
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from gensim import corpora, models
import numpy as np
import jieba
import tutorials.data_util as du

def get_dict():
    train = []
    fp = codecs.open('../xx.txt', 'r', encoding='utf8')#�ı��ļ���������Ҫ��ȡ������ĵ�
    stopwords = ['��', '��', '��', '��', 'ʹ��', '��', '��', '��', 'ʲô', '���', '��', '����', '��', 'Ҫ', '��ô', '��', '��', '��']#ȡ��ͣ�ô�
    for line in fp:
        line = list(jieba.cut(line))
        train.append([w for w in line if w not in stopwords])

    dictionary = Dictionary(train)
    return dictionary,train
def train_model():
    dictionary=get_dict()[0]
    train=get_dict()[1]
    corpus = [ dictionary.doc2bow(text) for text in train ]
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=7)
    #ģ�͵ı���/ ����
    lda.save('test_lda.model')
#���������ĵ������ƶ�
def lda_sim(s1,s2):
    lda = models.ldamodel.LdaModel.load('test_lda.model')
    test_doc = list(jieba.cut(s1))  # ���ĵ����зִ�
    dictionary=get_dict()[0]
    doc_bow = dictionary.doc2bow(test_doc)  # �ĵ�ת����bow
    doc_lda = lda[doc_bow]  # �õ����ĵ�������ֲ�
    # ������ĵ�������ֲ�
    # print(doc_lda)
    list_doc1 = [i[1] for i in doc_lda]
    # print('list_doc1',list_doc1)

    test_doc2 = list(jieba.cut(s2))  # ���ĵ����зִ�
    doc_bow2 = dictionary.doc2bow(test_doc2)  # �ĵ�ת����bow
    doc_lda2 = lda[doc_bow2]  # �õ����ĵ�������ֲ�
    # ������ĵ�������ֲ�
    # print(doc_lda)
    list_doc2 = [i[1] for i in doc_lda2]
    # print('list_doc2',list_doc2)
    try:
        sim = np.dot(list_doc1, list_doc2) / (np.linalg.norm(list_doc1) * np.linalg.norm(list_doc2))
    except ValueError:
        sim=0
    #�õ��ĵ�֮������ƶȣ�Խ���ʾԽ���
    return sim