# coding=utf-8

import jieba
from collections import Counter
import gensim


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
        sentence_seged = jieba.cut(sentence.strip())
        stopwords = self.stopwordslist('stopwords.txt')  # �������ͣ�ôʵ�·��
        outstr = ''
        for word in sentence_seged:
            if word not in stopwords:
                if word != '\t':
                    outstr += word
                    outstr += " "
        return outstr

    # ����ؼ���ƥ��÷�
    def score_compute(self, inputs1, inputs2):
        score = len(inputs1.intersection(inputs2)) / max(len(inputs1), len(inputs2)) 

        return score


if __name__ == '__main__':
    scoreMatcher = keywordMatchScore()
    inputs = open('test_input.txt', 'r') #����Ҫ������ļ���·��
    outputs = open('test_output.txt', 'w') #���ش������ļ�·��
    char_outputs = []
    line_outputs = []
    for line in inputs:
        line_seg = scoreMatcher.seg_sentence(line)  # ����ķ���ֵ���ַ���
        print("lines: ", line_seg)
        char_seg = [line[i] for i in range(len(line))]
        print("chars: ", char_seg)
        line_outputs.append(line_seg.split(' '))
        print("line_seg: ", line_outputs)
        char_outputs.append(char_seg)
        outputs.write(line_seg)
    outputs.close()
    inputs.close()


    inputs1, ner1 = set(char_outputs[0]), set(line_outputs[0])
    inputs2, ner2 = set(char_outputs[1]), set(line_outputs[1])
    score_char = scoreMatcher.score_compute(inputs1, inputs2)
    score_ner = scoreMatcher.score_compute(ner1, ner2)
    score = score_char * (1 / score_ner)

    print("test input: ", inputs1, " and ", inputs2)
    print("with scores:", score, " with ner:", score_ner)

    # WordCount
    with open('test_output.txt', 'r') as fr: #�����Ѿ�ȥ��ͣ�ôʵ��ļ�
        data = jieba.cut(fr.read())


    data_count = dict(Counter(data))
 
    print("sentence 1: ", data)
    # print("sentence 1: ", data[1])

    with open('wordCounts.csv', 'w') as fw: #����洢wordcount���ļ�·��
        for k,v in data_count.items():
            if k != ' ':
                fw.write('%s,%d\n' % (k, v))