__author__ = 'bliq'
# -*- coding: utf-8 -*-

import pymorphy
import subprocess
from pymystem3 import Mystem
from pymorphy import get_morph
from pymorphy.contrib import tokenizers
from nltk.corpus import wordnet as wn
morph = get_morph('/home/bliq/PycharmProjects/Dictionary') # Подключаем словари

text = raw_input("Введите текст:\n")
uni = unicode(text, "UTF-8") # Перевод строку в Unicode

# Разбиваем исходную строку на подстроки
listTokens = tokenizers.extract_tokens(uni)
listWords = tokenizers.extract_words(uni)

dic = {}

for word in listWords:
    info = morph.normalize(word.upper())
    info = list(info)[0]

    dic[info] = dic[info] + 1 if dic.has_key(info) else 1

dic = sorted(dic.items(), key = lambda elem: elem[1], reverse = True)

print dic

print wn.synsets( 'человек' )
"""
"А что подумал по этому поводу Кролик, никто так и не узнал, потому что Кролик был очень воспитанный."
"""
