
# coding=utf-8

import jieba
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups

if __name__ == '__main__':
	"""
	����������learn_kernel���൱��cos similarity��
	��Ϊsklearn.feature_extraction.text.TfidfVectorizer����õ��ľ��ǹ�һ�����������
	����cosine_similarity���൱��linear_kernel
	"""
	twenty = fetch_20newsgroups()
	tfidf = TfidfVectorizer().fit_transform(twenty.data)

	print(" tfidf[0:1] is : ",  tfidf[0:1])

	#ʹ��scikit-learn�����Ѿ�����õļ������
	from sklearn.metrics.pairwise import linear_kernel
	cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
	print(" cosine_similarities is : ",  cosine_similarities)

	related_docs_indices = cosine_similarities.argsort()[:-5:-1]
	print(related_docs_indices)
	#array([    0,   958, 10576,  3277])
	print(cosine_similarities[related_docs_indices])
	#array([ 1.        ,  0.54967926,  0.32902194,  0.2825788 ])
	#��һ��������ڼ�飬����query�������ƶ�Ϊ1