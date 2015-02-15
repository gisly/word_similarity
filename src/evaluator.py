# coding=utf-8
__author__ = 'gisly'


import codecs
from datetime import datetime

import word_db
import common_constants
import score_calculator


def simpleTest(filename, fileType, evaluationType, lastIndex):
    scores = []
    print filename
    startTime = datetime.now()
    

    
    with codecs.open(filename, 'r', 'utf-8') as fin:
        for index, line in enumerate(fin):
            if index == 0:
                continue
            elif index > lastIndex:
                break
            parts = line.strip().split(common_constants.WORD_DELIMITER)
            theirScore = findTheirScore(parts, fileType)
            ourScore = score_calculator.calculateScore(parts[0], parts[1])
            scores.append({'word0':parts[0], 'word1':parts[1], 'ours':ourScore, 'theirs':theirScore})
    evaluateScores(scores, evaluationType)
    diff = datetime.now() - startTime
    print 'processed ' + str(len(scores)) + ' pairs in ' + str(diff)

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
  
def evaluateScores(scores, evaluationType):
    if evaluationType == common_constants.EVALUATION_ACCURACY:
        evaluateAccuracy(scores)
    else:
        raise Exception('cannot evaluate:' + evaluationType)
    
    
def evaluateAccuracy(scores):
    """As each word has precisely half related and half unrelated words, one can classify pairs 
    given the scores as following:

Sort the table by “word1” and “sim”.
Set to 1 the “related” label of the first 50% relations of “word1”.
Set to 0 the “related” label of the last 50% relations of “word1”.

(we only have ones!)
    """
    truePositives = 0
    trueNegatives = 0
    falsePositives = 0
    falseNegatives = 0
    
    falsePositiveList = []
    falseNegativeList = []
    for scorePart in scores:
        ours = scorePart['ours']
        theirs = scorePart['theirs']
        if theirs >= 0.5 and ours >= 0.5:
            truePositives += 1
        elif theirs >= 0.5 and ours < 0.5:
            falseNegatives += 1
            falseNegativeList += [scorePart['word0'] + '_' + scorePart['word1']  ]
        elif theirs <0.5 and ours >= 0.5:
            falsePositives += 1
            falsePositiveList += [scorePart['word0'] + '_' + scorePart['word1']  ]
        else:
            trueNegatives += 1
    accuracy = (truePositives + trueNegatives)/float(truePositives + trueNegatives + falsePositives + falseNegatives)
    print 'accuracy:' + str(accuracy)       
    print 'falseNegativeList:' + '\r\n'.join(falseNegativeList)
    print 'falsePositiveList:' + ','.join(falsePositiveList)
               

"""simpleTest('D://CompLing//SemanticSimilarity//_data//training//rt-train.csv', 
           fileType = common_constants.FILE_RELATION,
           evaluationType = common_constants.EVALUATION_ACCURACY,
           lastIndex = 500)

"""
"""

simpleTest('D://CompLing//SemanticSimilarity//_data//training//ae-train.csv', 
           fileType = common_constants.FILE_HJ_SIMPLE,
           evaluationType = common_constants.EVALUATION_ACCURACY,
           lastIndex = 100000)
"""

"""simpleTest('D://CompLing//SemanticSimilarity//_data//training//hj-sample.csv', 
           fileType = common_constants.FILE_HJ_SIMPLE,
           evaluationType = common_constants.EVALUATION_ACCURACY,
           lastIndex = 100000)"""
           
           
simpleTest('D://CompLing//SemanticSimilarity//_data//training//negativeExamples.csv', 
           fileType = common_constants.FILE_HJ_SIMPLE,
           evaluationType = common_constants.EVALUATION_ACCURACY,
           lastIndex = 3000)
