# coding=utf-8
__author__ = 'gisly'
from langdetect import detect
import re
from pymorphy import get_morph


import file_utils


RUSSIAN_CODE = 'ru'

BADSYMBOLS = "[\"'#\!\?\.]"

RUSSIAN_DICT_FILENAME = '../resources/zdf-win.txt'
morph = get_morph('D:\\LingM\\pymorphy\\ru.sqlite-json\\')

zaliznyakWords = None


def isRussian(text):
    try:
        return isWordInDictionary(text) or detect(text) == RUSSIAN_CODE
    #TODO: it's ugly but the detection module raises an exception in case of numbers etc
    except Exception, e:
        return False
    
def isWordInDictionary(word):
    global zaliznyakWords
    cacheDictionary()
    lemmata =  getLemmaSet(word)
    for lemma in lemmata:
        if lemma.lower() in zaliznyakWords:
            return True
    return False
    
def cacheDictionary():
    global zaliznyakWords
    if zaliznyakWords is None:
        zaliznyakWords = file_utils.readLinesFromFile(RUSSIAN_DICT_FILENAME)    
    
def normalize(text):
    return replaceBadSymbols(text.strip().lower())


def replaceBadSymbols(text):
    return re.sub(BADSYMBOLS, "", text)


def getLemmaSet(word):
    lemmaSet =  morph.normalize(word.upper())
    if type(lemmaSet) == set:
        return lemmaSet
    return set(lemmaSet)





