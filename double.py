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
stoplist = forbid.readlines()
forbid.close()


# ДОКУМЕНТЫ ДЛЯ ПРОВЕРКИ
file_1 = 'test_docs/source.vert'
text = open(file_1, 'r')
lines = text.readlines()
text.close()


# ПОЛУЧЕНИЕ КОНТРОЛЬНЫХ СУММ (ПО 10 СЛОВ)
def algo_shingle(text):
	sums = []
	shingle = 10
	l = len(text)
	for i in range(l - shingle + 1):
		sums.append (binascii.crc32(' '.join( [x for x in text[i:i+shingle]] )))
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


# СОБСТВЕННО, ОБРАБОТКА КОРПУСА
textid = []
qwerty = []

i = 0
while i < len(lines):
	if "<doc" in lines[i]:
		buf = []
		c = lines[i].split()[1].split('=')[1].strip('"')
		textid.append(c)
		i += 1
		while not "</doc" in lines[i]:
			if not "<" in lines[i] and not ">" in lines[i]:
				s = (lines[i].split()[3]).split("-")[0]
				if not s in string.punctuation:
					if not s in stoplist:
						buf.append(s)
			i += 1
		qwerty.append(algo_shingle(buf))
	i += 1

# ВЫВОД РЕЗУЛЬТАТОВ ПОПАРНОГО СРАВНЕНИЯ ТЕКСТОВ
for j in range(0, len(textid) - 1):
	for k in range(j + 1, len(textid)):
		print textid[j] + " and " + textid[k] + " - " + str(percent(qwerty[j], qwerty[k])) + "%"