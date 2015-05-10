__author__ = 'bliq'
# -*- coding: utf-8 -*-

import pymorphy
import subprocess
from pymystem3 import Mystem
from pymorphy import get_morph
from pymorphy.contrib import tokenizers
from nltk.corpus import wordnet as wn

dictionary = {}

def initialDict():
    with open('Synonym.txt', 'r') as f:
        content = f.readlines()

    for line in content:
        splitLine = line.split('\t')

        key = unicode(splitLine[0], "UTF-8").upper()
        value = unicode(splitLine[1], "UTF-8").upper()

        dictionary[key] = value
    #lines = open('C:/path/file.txt', 'r').read().splitlines()

initialDict()

morph = get_morph('/home/bliq/PycharmProjects/Dictionary') # Подключаем словари

searchWord= ""
synonym = ""
result = ""

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

for word in dic:
    info = morph.get_graminfo(word[0])

    if info[0]['class'] != u'СОЮЗ' \
            and info[0]['class'] != u'МС' \
            and info[0]['class'] != u'ПРЕДЛ' \
            and info[0]['class'] != u'МЕЖД' \
            and info[0]['class'] != u'ЧАСТ':
        if dictionary.has_key(word[0]):
            searchWord = word
            synonym = word[0]
            break

for analyzWord in listTokens:
    info = morph.get_graminfo(analyzWord.upper())
    word = analyzWord

    if info and info[0]['norm'] == searchWord[0]:
        word = morph.inflect_ru(synonym, info[0]['info']).lower()

        if (analyzWord[0].isupper()):
            word = word[0].upper() + word[1:]

    result += word

print u"Часто встречающееся слово: " + synonym.lower()
print u"Кол-во повторов: " + str(searchWord[1])
print result

"""
"Саша машет Маше, Маша машет Саше. Маша Саши краше, Саша краше Паши."
"А что подумал по этому поводу Кролик, никто так и не узнал, потому что Кролик был очень воспитанный."
"Мало кто знает, что скульптура "Родина-мать зовёт!" на Мамаевом кургане в Сталинграде (теперь Волгоград) — это только вторая часть композиции из трёх монументов с мечом Победы в разных городах. Первая часть "Тыл — фронту" стоит в Магнитогорске, где ковали меч Победы. На нём рабочий передаёт меч солдату. "Родина-мать зовёт!" символизирует, что меч был поднят в Сталинграде. А третий монумент "Воин-освободитель" находится в Берлине, где советский воин-освободитель опустил этот меч. Специалисты называют эти монументы «Триптих: "Меч передан. Меч поднят. Меч опущен"». Примечательно, что хронология возведения этих монументов разнится с хронологией меча. В Берлине памятник воздвигли в 1949г., в Волгограде в 1967г., в Магнитогорске в 1979г."
"""
