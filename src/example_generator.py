# coding=utf-8
__author__ = 'gisly'
import codecs
import common_constants
import random

PAIR_NUM = 10000
LINE_LIMIT = 1000000

def createNegativeExamples(inputFilename, outputFilename):
    words = readWordsFromFile(inputFilename, LINE_LIMIT)
    print 'read ' + str(len(words)) + ' words'
    pairsCreated = []
    with codecs.open(outputFilename, 'w', 'utf-8') as fout:
        fout.write('word1,word2,sim\n')
        for i in range(0, PAIR_NUM):
            word1 = getRandomWord(words)
            word2 = getRandomWord(words)
            if (word1, word2) in pairsCreated:
                i -= 1
                continue
            pairsCreated.append((word1, word2))
            #print word1, word2
            fout.write(word1 + common_constants.WORD_DELIMITER + word2 + common_constants.WORD_DELIMITER + '0\n')
            
            
def readWordsFromFile(filename, lineLimit):
    words = []
    with codecs.open(filename, 'r', 'utf-8') as fin:
        for index, line in enumerate(fin):
            if index > lineLimit:
                break
            words+= line.split('\t')[0:2]
    return list(set(words))
        
        
def getRandomWord(words):
    return random.choice(words)


createNegativeExamples('D://CompLing//SemanticSimilarity//word2vec//word2vec-win32-master//word2vec-win32-master//fwiki-cooccur-ge2.csv',
                       'D://CompLing//SemanticSimilarity//_data/training/negativeExamples.csv')
    