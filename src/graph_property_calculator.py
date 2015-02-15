# coding=utf-8
__author__ = 'gisly'
import codecs

import common_constants

degrees = None
pagerank = None

DEGREE_FILE = 'D://CompLing//SemanticSimilarity//degreeIn.txt'
PAGERANK_FILE = 'D://CompLing//SemanticSimilarity//pagerank.txt'


def calculateCentralityFeatures(word):
    centralityFeatures = dict()
    centralityFeatures[common_constants.FEATURE_DEGREE] = calculate_degree_properties(word)
    centralityFeatures[common_constants.FEATURE_PAGERANK] = calculate_pagerank_properties(word)
    return centralityFeatures

def calculate_degree_properties(word):
    global degrees
    return calculate_properties_bydict(word, degrees, DEGREE_FILE)

def calculate_pagerank_properties(word):
    global pagerank
    return calculate_properties_bydict(word, pagerank, PAGERANK_FILE)


def calculate_properties_bydict(word, dictToUse, fileToUse):
    if not dictToUse:
        dictToUse = readDictFromFile(fileToUse)
    return dictToUse.get(word)




def readDictFromFile(filename):
    newDict = dict()
    with codecs.open(filename, 'r', 'utf-8') as fin:
        curWord = None
        for index, line in enumerate(fin):
            if index % 2 == 1:
                newDict[curWord] = float(line.strip())
            else:
                curWord = line.strip()
    return newDict


            
     
    