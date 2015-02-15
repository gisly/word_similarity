# coding=utf-8
__author__ = 'gisly'
from pymorphy import get_morph
morph = get_morph('D:\\LingM\\pymorphy\\ru.sqlite-json\\')
DELIM = ','



def isSamePos(word1, word2):
    morphInfo1 = getMorphoInfo(word1)
    morphInfo2 = getMorphoInfo(word2)
    if (morphInfo1 is None) or (morphInfo2 is None):
        return False
    for morphVariant in morphInfo1:
        curPos = morphVariant[0]
        for morphVariant2 in morphInfo2:
            if curPos == morphVariant2[0]:
                return True
    return False

def getMorphoInfo(word):   
    info = morph.get_graminfo(word.upper())
    if not info:
        return None
    return [[info_variant['class'],info_variant['info'].split(DELIM), info_variant['method']] for info_variant in info]

    