# -*- coding: utf-8 -*-
import sys
import gensim
from gensim import corpora, models, similarities
import pymorphy2
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import string
tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
morph = pymorphy2.MorphAnalyzer()
import binascii


# СЧИТЫВАЕМ СПИСОК ПРЕДЛОГОВ И СОЮЗОВ
forbidden_words = 'test_docs/stoplist.txt'
forbid = open(forbidden_words,'r')
stoplist = [line.strip().decode('utf-8') for line in forbid.readlines()]
forbid.close()


# ДОКУМЕНТЫ ДЛЯ ПРОВЕРКИ
file_1 = 'test_docs/source_1.txt'
file_2 = 'test_docs/source_2.txt'
text_1 = open(file_1,'r')
text_2 = open(file_2,'r')
lines_1 = text_1.readlines()
lines_2 = text_2.readlines()
text_1.close()
text_2.close()


# НОРМАЛИЗАЦИЯ ТОКЕНА
def normalize_token(token):
	try: 
		gram_info = morph.parse(token)
		return gram_info[0].normal_form
	except:
		return token


# НОРМАЛИЗАЦИЯ ТЕКСТА
def normalize_text(text):
	sentences = []
	tokenized_lines = map(tokenizer.tokenize, [line.decode('utf-8').strip() for line in text])
	for tokenized_line in tokenized_lines: 
		for token in tokenized_line:
				if not token in string.punctuation and not token in stoplist:
 					sentences.append(normalize_token(token))
	return sentences


# ПОЛУЧЕНИЕ КОНТРОЛЬНЫХ СУММ (ПО 10 СЛОВ)
def algo_shingle(text):
	sums = []
	shingle = 2
	l = len(text)
	for i in range(l - shingle + 1):
		sums.append (binascii.crc32(' '.join( [x for x in text[i:i+shingle]] ).encode('utf-8')))
	return sums


# ИТОГ
def percent(array1, array2):
	common = 0
	for i in range(len(array1)):
		if array1[i] in array2:
			common += 1
	if len(array1) + len(array2) > 0:
		overlap = (common * 200) / (len(array1) + len(array2))
	else:
		return 100
	return overlap

lines_1 = normalize_text(lines_1)
lines_2 = normalize_text(lines_2)

<<<<<<< HEAD
# print ' '.join([w.encode('utf-8') for w in lines_1])
# print ' '.join([w.encode('utf-8') for w in lines_2])
=======
print ' '.join([w for w in lines_1])
print ' '.join([w for w in lines_2])
>>>>>>> efd3d1b41ce74ace0ff6687457ecec96e6206521
print percent(algo_shingle(lines_1), algo_shingle(lines_2))