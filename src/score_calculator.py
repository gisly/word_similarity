# coding=utf-8
__author__ = 'gisly'


import codecs
import word_db
import random

import datetime
import sys
import os

import common_constants
import graph_property_calculator
import file_utils
import training_processor
import morphology

#sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


GRAPH_LIMIT = 4
FEATURE_FILENAME = 'D://CompLing//SemanticSimilarity/features3000_ae.csv'


def createFeatureFile(trainingFilenameList, fileTypeList, evaluationTypeList, firstIndexList, lastIndexList):
    featureList = []
    for index, trainingFilename in enumerate(trainingFilenameList):
        fileType = fileTypeList[index]
        evaluationType = evaluationTypeList[index]
        firstIndex = firstIndexList[index]
        lastIndex = lastIndexList[index]
        pairScores = training_processor.extractPairsFromTrainingFile(trainingFilename, fileType, 
                                                                    evaluationType, firstIndex, lastIndex)
        
        for pairScore in pairScores:
            pairFeatures = calculateFeatures(pairScore['word0'], pairScore['word1'])
            pairFeatures[common_constants.FEATURE_GRAPH_IS_RELATED] = pairScore['score']
            pairFeatures[common_constants.FEATURE_WORD0] = pairScore['word0']
            pairFeatures[common_constants.FEATURE_WORD1] = pairScore['word1']
            featureList.append(pairFeatures)
    random.shuffle(featureList)
    exportFeatures(featureList, FEATURE_FILENAME, GRAPH_LIMIT)  
    
def computeFeaturesForTestFile(testFilename, fromIndex, toIndex):
    outputFilename = testFilename.replace('.csv', str(fromIndex) +'_' + str(toIndex)+'.csv')
    featureNames = getFeatureNames()    
    headerLine = getHeaderLine(featureNames) + common_constants.LINE_ENDING_CHARACTER
            
    
    
    
    with codecs.open(outputFilename, 'w', 'utf-8') as fout:
        fout.write(headerLine)
        with codecs.open(testFilename, 'r', 'utf-8') as fin:
            for index, line in enumerate(fin):
                if index < fromIndex:
                    continue
                if index >= toIndex:
                    break
                parts = line.strip().split(common_constants.WORD_DELIMITER)
                pairFeatures = calculateFeatures(parts[0], parts[1])
                pairFeatures[common_constants.FEATURE_WORD0] = parts[0]
                pairFeatures[common_constants.FEATURE_WORD1] = parts[1]
                fout.write(createLineWithFeatures(featureNames, pairFeatures))
    
def getFeatureNames():
    featureNames = common_constants.ALL_FEATURES
    for feature in common_constants.ALL_ENUMERABLE_FEATURES:
        for i in range(0, GRAPH_LIMIT + 2):
            featureNames.append(feature + str(i))
            
    for feature in common_constants.ALL_ENUMERABLE_BY_WORD_FEATURES:
        for i in range(0, GRAPH_LIMIT + 1):
            featureNames.append(feature + str(i) + '_word0')
            featureNames.append(feature + str(i) + '_word1')
    return featureNames

def calculateFeatures(word1, word2):
    featureDict = dict()
    graphFeatures = countGraphFeatures(word1, word2, GRAPH_LIMIT)
    featureDict.update(graphFeatures)
    
    
    return featureDict

def createLineWithFeatures(featureNames, candidatePair):
    body = ''
    for feature in featureNames:
        if feature in candidatePair:
            featureValue = candidatePair[feature]     
        else:
            featureValue = common_constants.FEATURE_VALUE_NA
        if isinstance(featureValue, basestring):
            body += featureValue + common_constants.WORD_DELIMITER
        else:
            body += str(featureValue) + common_constants.WORD_DELIMITER
    body = body.strip() + common_constants.LINE_ENDING_CHARACTER
    return body

def countGraphFeatures(word1, word2, limit):
    print str(datetime.datetime.now()) + ':calculating features for ' + word1 + ' ' + word2
    """accumulatedDistance, accumulatedFreqList, isConnected, linkList = word_db.findWordDistance(word1, word2,
                                                                                                GRAPH_LIMIT)"""
                                                                                                
    distance, accumulatedFreqList, isConnected = word_db.dijkstraSearchFirst(word1, word2)                                                                                            
    graphFeatures = dict()
    graphFeatures[common_constants.FEATURE_GRAPH_LIMIT] = limit
    #linkList = [(word1, 0), (word2, 0)]  + linkList
    
    for index, pair in enumerate(accumulatedFreqList):
        featureFreqList = common_constants.FEATURE_GRAPH_FREQ_LIST + str(index)
        graphFeatures[featureFreqList] = pair[0]
            
        centralityFeatures = graph_property_calculator.calculateCentralityFeatures(pair[1])
            
        graphFeatures[common_constants.FEATURE_DEGREE + str(index) + '_word0'] =\
                                                    centralityFeatures[common_constants.FEATURE_DEGREE]
        graphFeatures[common_constants.FEATURE_PAGERANK + str(index) + '_word0'] =\
                                                    centralityFeatures[common_constants.FEATURE_PAGERANK]
                                                    
                                                    
        centralityFeatures = graph_property_calculator.calculateCentralityFeatures(pair[2])
            
        graphFeatures[common_constants.FEATURE_DEGREE + str(index) + '_word1'] =\
                                                    centralityFeatures[common_constants.FEATURE_DEGREE]
        graphFeatures[common_constants.FEATURE_PAGERANK + str(index) + '_word1'] =\
                                                    centralityFeatures[common_constants.FEATURE_PAGERANK]                                            
    
    if isConnected:
        graphFeatures[common_constants.FEATURE_GRAPH_IS_CONNECTED] = common_constants.FEATURE_VALUE_YES
    else:
        graphFeatures[common_constants.FEATURE_GRAPH_IS_CONNECTED] = common_constants.FEATURE_VALUE_NO
    if accumulatedFreqList:
        graphFeatures[common_constants.FEATURE_GRAPH_PATHLENGTH] = len(accumulatedFreqList) - 1
        
    if word_db.existsInDb(word1) and word_db.existsInDb(word2):
        graphFeatures[common_constants.FEATURE_GRAPH_BOTHEXIST] = common_constants.FEATURE_VALUE_YES
    else:
        graphFeatures[common_constants.FEATURE_GRAPH_BOTHEXIST] = common_constants.FEATURE_VALUE_NO
        
    graphFeatures[common_constants.FEATURE_GRAPH_JACCARD] = word_db.calculateJaccard(word1, word2)
    graphFeatures[common_constants.FEATURE_GRAPH_DICE] = word_db.calculateDice(word1, word2)
    graphFeatures[common_constants.FEATURE_VECTOR_COSINE] = word_db.calculateCosine(word1, word2)
    
    if morphology.isSamePos(word1, word2):
        graphFeatures[common_constants.FEATURE_MORPH_SAMEPOS] = common_constants.FEATURE_VALUE_YES
    else:
        graphFeatures[common_constants.FEATURE_MORPH_SAMEPOS] = common_constants.FEATURE_VALUE_NO
        
    
    
    for res in accumulatedFreqList:
        print str(res[0]) + ',' + res[1] 
    graphFeatures[common_constants.FEATURE_GRAPH_WEIGHTED_PATH] = word_db.getWeightedPathByFreqList(accumulatedFreqList)
    
    return graphFeatures


def calculateScore(word1, word2):
    features = calculateFeatures(word1, word2)
    return calculateScoreByFeatures(features)

def calculateScoreByFeatures(features):
    #TODO:
    return 0


def exportFeatures(allFeatures, outputFile, GRAPH_LIMIT):
    textToOutput = turnFeaturesIntoTable(allFeatures, GRAPH_LIMIT)
    file_utils.writeToFile(textToOutput,outputFile)


def turnFeaturesIntoTable(allFeatures, graphLimit):
    body = ''
    
    featureNames = common_constants.ALL_FEATURES
    for feature in common_constants.ALL_ENUMERABLE_FEATURES:
        for i in range(0, graphLimit + 2):
            featureNames.append(feature + str(i))
            
    for feature in common_constants.ALL_ENUMERABLE_BY_WORD_FEATURES:
        for i in range(0, graphLimit + 1):
            featureNames.append(feature + str(i) + '_word0')
            featureNames.append(feature + str(i) + '_word1')
            
    headerLine = getHeaderLine(featureNames)
            
    
    for candidatePair in allFeatures:
        for feature in featureNames:
            if feature in candidatePair:
                featureValue = candidatePair[feature]     
            else:
                featureValue = common_constants.FEATURE_VALUE_NA
            if isinstance(featureValue, basestring):
                body += featureValue +'\t'
            else:
                body += str(featureValue) +'\t'
        body = body.strip()+'\r\n'
    return headerLine.strip() + '\r\n' + body.strip()

def getHeaderLine(featureNames):
    return '\t'.join(featureNames)

"""createFeatureFile(['D://CompLing//SemanticSimilarity//_data//training//negativeExamples.csv',
                   'D://CompLing//SemanticSimilarity//_data//training//rt-train.csv'], 
           [common_constants.FILE_HJ_SIMPLE,
            common_constants.FILE_RELATION],
           [common_constants.EVALUATION_ACCURACY,
            common_constants.EVALUATION_ACCURACY],
           [8001,
            8001],
           [9000,
            9000])"""

testFilename = 'D://CompLing//SemanticSimilarity//_data//test.csv'
batchSize = 1500
#startIndex = 1
#computeFeaturesForTestFile(testFilename, startIndex, startIndex + batchSize)
#startIndex = 1501
#computeFeaturesForTestFile(testFilename, startIndex, startIndex + batchSize)

#startIndex = 4501
#startIndex = 6001
#startIndex = 7501

#startIndex = 9001
#startIndex = 10501
#startIndex = 12001
#startIndex = 13501
startIndex = 15001
#computeFeaturesForTestFile(testFilename, startIndex, startIndex + batchSize)

def countWords(foldername, prefix):
    wordCount = 0
    for filename in os.listdir(foldername):
        if filename.startswith(prefix):
            with codecs.open(os.path.join(foldername, filename), 'r', 'utf-8') as fin:
                for line in fin:
                    wordCount += 1
                wordCount -= 1
    return wordCount


def uniteFiles(foldername, prefix, outputFilename):
    fileHeader = None
    print ',\r\n'.join(os.listdir(foldername))
    with codecs.open(outputFilename, 'w', 'utf-8') as fout:
        for i in range(1, 15001, 1500):
            startIndex = i
            endIndex = i + 1500
            filename = os.path.join(foldername, prefix+str(startIndex)+'_'+str(endIndex)+'.csv')
            with codecs.open(os.path.join(foldername, filename), 'r', 'utf-8') as fin:
                for index, line in enumerate(fin):
                    if (fileHeader is None) and (index == 0):
                        fileHeader = line
                        fout.write(fileHeader)
                    elif index != 0:
                        fout.write(line)
                        
#uniteFiles('D://CompLing/SemanticSimilarity/_data/', 'test', 'D://CompLing/SemanticSimilarity/_data/commonTestOut.csv')                    
#print countWords('D://CompLing/SemanticSimilarity/_data/', 'test')
    
def mixLines(filename1, filename2, commonFilename):
    lines1 = getLinesAfterNum(filename1, 0)
    lines2 = getLinesAfterNum(filename2, 1)
    header = lines1[0]
    
    
    lastLine = lines1[-1] + '\r\n'
    
    lines1InBetween = lines1[1:-1]
    
    linesUnited = lines1InBetween + [lastLine] + lines2
    random.shuffle(linesUnited)
    mixedLines = [header] + linesUnited
    with codecs.open(commonFilename, 'w', 'utf-8') as fout:
        for line in mixedLines:
            fout.write(line.strip() + '\r\n')


    
        
        
def getLinesAfterNum(filename, numToStart):
    lines = []
    with codecs.open(filename, 'r', 'utf-8') as fin:
        for index, line in enumerate(fin):
            if index >= numToStart:
                lines.append(line)
    return lines
                
    


"""mixLines('D://CompLing//SemanticSimilarity//features1500_9000_2000_ae.csv',
         'D://CompLing//SemanticSimilarity//features3000_ae.csv',
         'D://CompLing//SemanticSimilarity//features1500_9000_3000_ae.csv',
         )

for i in range(1, 15000, batchSize):
    computeFeaturesForTestFile(testFilename, i, i + batchSize)"""
       
       
       
"""createFeatureFile([
                   'D://CompLing//SemanticSimilarity//_data//training//ae-train.csv'], 
           [common_constants.FILE_HJ_SIMPLE],
           [common_constants.EVALUATION_ACCURACY],
           [2001],
           [3000])"""     
            
"""createFeatureFile(['D://CompLing//SemanticSimilarity//_data//training//negativeExamples.csv',
                   'D://CompLing//SemanticSimilarity//_data//training//ae-train.csv'], 
           [common_constants.FILE_HJ_SIMPLE,
            common_constants.FILE_HJ_SIMPLE],
           [common_constants.EVALUATION_ACCURACY,
            common_constants.EVALUATION_ACCURACY],
           [500,
            500])"""
            
"""def corrFile(filename):
    with codecs.open(filename+'_corr.csv', 'w', 'utf-8') as fout:
        with codecs.open(filename, 'r', 'utf-8') as fin:
            for line in fin:
                lineParts = line.split('\t')
                if lineParts[4] == 'link':
                    fout.write(line)
                    continue
                if(float(lineParts[4]) > 0):
                    lineParts[4] = '1'
                fout.write('\t'.join(lineParts))"""
                 
        
#corrFile('D://CompLing//SemanticSimilarity//features1500_ae.csv')

pairFeatures = calculateFeatures(u'рис', u'крупа')
for par in pairFeatures:
    print par + ':' + str(pairFeatures[par])
