# coding=utf-8
__author__ = 'gisly'

import codecs
from datetime import datetime

import common_constants


def extractPairsFromTrainingFile(filename, fileType, evaluationType, firstIndex, lastIndex):
    scores = []
    with codecs.open(filename, 'r', 'utf-8') as fin:
        for index, line in enumerate(fin):
            if index < firstIndex:
                continue
            elif index > lastIndex:
                break
            parts = line.strip().split(common_constants.WORD_DELIMITER)
            theirScore = findTheirScore(parts, fileType)
            scores.append({'word0':parts[0], 'word1':parts[1], 'score':theirScore})
    return scores
    
    
def findTheirScore(parts, fileType):
    if fileType == common_constants.FILE_RELATION:
        if parts[2] in ['syn', 'hyper', 'hypo']:
            return 1
        elif parts[2] in ['random']:
            return 0
        raise Exception('unknown relation type:' + parts[2])
    elif fileType == common_constants.FILE_HJ_SIMPLE:
        return float(parts[2])
    raise Exception('unknown file type:' + fileType)