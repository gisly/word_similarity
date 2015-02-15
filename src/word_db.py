# coding=utf-8
__author__ = 'gisly'
import pymongo
import datetime
import codecs
import sys


import math

connection=pymongo.Connection('localhost', 27017)
db=connection['word_similarity']


def insertPair(word, key, value, source_code):
    colFreqs = db.pairFreqs
    colFreqs.remove({'word0':word, 'word1':key, 'source_code':source_code})
    colFreqs.insert({'word0':word, 'word1':key, 'freq':value, 'source_code':source_code})
    
    
def upsertWordLink(word, linkList, source_code):
    colWordLinks = db.wordLinks
    curWordLinks = colWordLinks.find({'word':word, 'source_code':source_code})
    newLinkList = linkList
    for res in curWordLinks:
        newLinkList += res['linkList']
    newLinkList = list(set(newLinkList))
    colWordLinks.insert({'word':word, 'linkList':newLinkList, 'source_code':source_code})
    
def insertCurrentNum(currentNum, material_code, source_code):
    colNumbers = db.numbers
    colNumbers.insert({'currentTime':datetime.datetime.now(), 
                      'currentNum':currentNum,
                      'material_code':material_code,
                      'source_code':source_code})
    

    
    
def findWordDistance(word1, word2, limit):
    dirFreq = findFreq(word1, word2)
    if dirFreq:
        return 0, [(dirFreq, word1, word2)], True, []
    if not existsInDb(word1) or not existsInDb(word2):
        return 0, [], False, []
    
    for limitCurrent in range(0, limit + 1):
        accumulatedDistance, accumulatedFreqList, isConnected, linkList  =\
                        graphSearch(word1, word2, limitCurrent, 0, [], False, [])
        if isConnected:
            return accumulatedDistance, accumulatedFreqList, isConnected, linkList
        accumulatedDistance, accumulatedFreqList, isConnected, linkList =\
                        graphSearch(word2, word1, limitCurrent, 0, [], False, [])
        if isConnected:
            return accumulatedDistance, accumulatedFreqList, isConnected, linkList
    
    return 0, [], False, []
    

    
def findFreq(word1, word2):
    freq = findFreqByPair({'word0':word1, 'word1':word2})
    if freq:
        return freq
    return findFreqByPair({'word0':word2, 'word1':word1})

def graphSearch(word1, word2, limit, accumulatedDistance, freqList, isConnected, linkList):   

    
    simpleFreq = findFreq(word1, word2)
    if simpleFreq:
        return accumulatedDistance, freqList + [(simpleFreq, word1, word2)], True, linkList


    if limit == 0:
        return accumulatedDistance, freqList, isConnected, linkList

    
    colFreqs = db.pairFreqs
    neighboursRight =  colFreqs.find({'word0':word1}).sort("freq",pymongo.DESCENDING)  
    accumulatedDistance, accumulatedFreqList, newIsConnected, linkList = \
                        graphSearchByNeighbours(neighboursRight, limit, accumulatedDistance, freqList, isConnected, word2, 'word1', linkList)
    
    if newIsConnected:
        return accumulatedDistance, accumulatedFreqList, newIsConnected, linkList 
    neighboursLeft =  colFreqs.find({'word1':word1}).sort("freq",pymongo.DESCENDING) 
    
    
    
    accumulatedDistance, accumulatedFreqList, newIsConnected, linkList = \
                        graphSearchByNeighbours(neighboursLeft, limit, accumulatedDistance, freqList, isConnected, word2, 'word0', linkList)
    
    return accumulatedDistance, accumulatedFreqList, newIsConnected, linkList
        
def graphSearchByNeighbours(neighbourCursor, limit, accumulatedDistance, freqList, isConnected, word2, pairCode, linkList):
    for neighbour in neighbourCursor:
        if neighbour[pairCode] == word2:
            return accumulatedDistance, freqList + [(neighbour['freq'], neighbour['word0'], neighbour['word1'])], True, linkList
        
        newFreqList = freqList + [(neighbour['freq'], neighbour['word0'], neighbour['word1'])]
        
        newLinkList = linkList + [(neighbour[pairCode], getWordFreq(neighbour[pairCode]))]
        newAccumulatedDistance = accumulatedDistance + 1
        accumulatedDistance, accumulatedFreqList, newIsConnected, accumulatedLinkList = graphSearch(neighbour[pairCode], word2, limit - 1, 
                                                                    newAccumulatedDistance, newFreqList, isConnected, newLinkList)
        
       
        
        if newIsConnected:
            return accumulatedDistance, accumulatedFreqList, newIsConnected, accumulatedLinkList
    return accumulatedDistance, freqList, isConnected, linkList



def dijkstraSearchFirst(word1, word2):
    dirFreq = findFreq(word1, word2)
    if dirFreq:
        return 0, [(dirFreq, word1, word2)], True
    if not existsInDb(word1) or not existsInDb(word2):
        return 0, [], False
    
    distDict = dict()
    distDict[word1] = 0
    neighboursFreq = getWordNeighboursFreq(word1)
    visited = [word1]
    freqList = []
    prevFreq = dict()
    for node in neighboursFreq.keys():
        prevFreq[node] = [word1, neighboursFreq[node]]
    neighbours = neighboursFreq.keys() + [word1]
    for node in neighbours:
        
        neighbours.remove(node)
        visited.append(node)
        nodeNeighboursFreq = getWordNeighboursFreq(node)
        if word2 in distDict:
            freqList = []
            curNode = word2
            while curNode!=word1:
                prevNodeValue = prevFreq[curNode]
                freqList.append([prevNodeValue[1], curNode, prevNodeValue[0]])
                curNode = prevNodeValue[0]
                
            
            return distDict[word2], freqList, True
        for nodeNeighbour in nodeNeighboursFreq.keys():
            
            if (not nodeNeighbour in visited) and (not nodeNeighbour in neighbours):
                neighbours.append(nodeNeighbour)
                prevFreq[nodeNeighbour] = [node, nodeNeighboursFreq[nodeNeighbour]]
                if not node in distDict:
                    #???
                    distDict[node] = 0
                alt = distDict[node] + 1
                if (not nodeNeighbour in distDict) or (alt < distDict[nodeNeighbour]):
                    distDict[nodeNeighbour] = alt
        
    return sys.maxint, [], False
                    
    
    


def findFreqByPair(wordPair):
    colFreqs = db.pairFreqs
    directPair = colFreqs.find(wordPair)
    dirRes = None
    for res in directPair:
        dirRes = res
        break
    if dirRes:
        return dirRes['freq']  
    return None 


def existsInDb(word):
    colFreqs = db.pairFreqs
    cursorFound = colFreqs.find({'word0': word})
    for res in cursorFound:
        return True
    cursorFound = colFreqs.find({'word1': word})
    for res in cursorFound:
        return True
    return False


def calculateJaccard(word0, word1):
    wordNeighbours0 = getWordNeighbours(word0)
    wordNeighbours1 = getWordNeighbours(word1)
    intersectionLen = len(list(set(wordNeighbours0).intersection(set(wordNeighbours1))))
    unionLen = len(list(set(wordNeighbours0).union(set(wordNeighbours1))))
    if unionLen == 0:
        return 0
    return intersectionLen/float(unionLen)

def calculateDice(word0, word1):
    wordNeighbours0 = getWordNeighbours(word0)
    wordNeighbours1 = getWordNeighbours(word1)
    intersectionLen = len(list(set(wordNeighbours0).intersection(set(wordNeighbours1))))
    totalLen = len(wordNeighbours0) + len(wordNeighbours1)
    if totalLen == 0:
        return 0
    
    for word in list(set(wordNeighbours0).intersection(set(wordNeighbours1))):
        print word
    
    return 2*intersectionLen/float(totalLen)

def calculateCosine(word0, word1):
    wordNeighboursFreq0 = getWordNeighboursFreq(word0)
    wordNeighboursFreq1 = getWordNeighboursFreq(word1)

   
        
    wordsTotal = list(set(wordNeighboursFreq0.keys()).union(set(wordNeighboursFreq1.keys())))
    vec0 = []
    vec1 = []
    for word in wordsTotal:
        vec0.append(wordNeighboursFreq0.get(word, 0))
        vec1.append(wordNeighboursFreq1.get(word, 0))
        
        if wordNeighboursFreq0.get(word, 0) > 0 and wordNeighboursFreq1.get(word, 0) > 0:
        
            print word + ':' + str(wordNeighboursFreq0.get(word, 0)) + ':' + str(wordNeighboursFreq1.get(word, 0))
        
   
    

        
    scalarMult = 0
    vec0Len = 0
    vec1Len = 0
    if (len(vec0) == 0) or (len(vec1) == 0):
        return 0
    for i in range(0, len(wordsTotal)):
        scalarMult += vec0[i] * vec1[i]
        vec0Len += vec0[i] * vec0[i]
        vec1Len += vec1[i] * vec1[i]
    if (vec0Len == 0) or (vec1Len == 0):
        return 0
    return scalarMult/float(math.sqrt(vec0Len) * math.sqrt(vec1Len))
        
        
        


def getWordNeighboursFreq(word):
    colFreqs = db.pairFreqs
    wordsLeftCursor = colFreqs.find({'word0': word})
    wordsFreqs = dict()
    words = []
    for word in wordsLeftCursor:
        wordsFreqs[word['word1']] =  word['freq']
        words.append(word['word1'])
        
    wordsRightCursor = colFreqs.find({'word1': word})
    for word in wordsRightCursor:
        if not word['word0'] in words:
            wordsFreqs[word['word0']] =  word['freq']
    return wordsFreqs

def getWordNeighbours(word):
    colFreqs = db.pairFreqs
    wordsLeftCursor = colFreqs.find({'word0': word})
    words = []
    for word in wordsLeftCursor:
        words.append(word['word1'])
        
    wordsRightCursor = colFreqs.find({'word1': word})
    for word in wordsRightCursor:
        if not word['word0'] in words:
            words.append(word['word0'])
    return words
        

def getWordFreq(word):
    colFreqs = db.pairFreqs
    cursorFound = colFreqs.find({'word0': word})
    wordCountLeft = 0
    wordsCounted = []
    for res in cursorFound:
        wordCountLeft += res['freq']
        wordsCounted.append(res['word1'])
    cursorFound = colFreqs.find({'word1': word})
    wordCountRight = 0
    for res in cursorFound:
        if res['word0'] not in wordsCounted:
            wordCountRight += res['freq']
    return wordCountLeft + wordCountRight


def getWeightedPathByFreqList(freqList):
    path = 0
    calculatedFreqs = dict()
    if len(freqList) == 0:
        return -sys.maxint - 1
    for element in freqList:
        freq1 = 0
        if element[1] in calculatedFreqs:
            freq1 = calculatedFreqs[element[1]]
        else:
            freq1 = getWordFreq(element[1])
            calculatedFreqs[element[1]] = freq1
            
        freq2 = 0
        if element[2] in calculatedFreqs:
            freq2 = calculatedFreqs[element[2]]
        else:
            freq2 = getWordFreq(element[2])
            calculatedFreqs[element[2]] = freq2
        if freq1!=0 and freq2!=0:
            path += (element[0]/float(freq1 * freq2))
    return math.log(path/float(len(freqList)))

"""with codecs.open('D://CompLing//SemanticSimilarity//testPositivesAnalysis.csv', 'w', 'utf-8') as fout:
    with codecs.open('D://CompLing//SemanticSimilarity//testPositives.csv', 'r', 'utf-8') as fin:
        for line in fin:
            words = line.strip().split(',')
            fout.write('=============\r\n' + words[0] + '\t' + words[1] + '\r\n=============\r\n')
    
            accumulatedDistance, accumulatedFreqList, isConnected, linkList = \
                                    findWordDistance(words[0], words[1], 1)
            for entry in accumulatedFreqList:
                fout.write(str(entry[0]) +',' + entry[1] +',' + entry[2])
                freq1 = getWordFreq(entry[1])
                freq2 = getWordFreq(entry[2])
                fout.write(str(freq1) + '\r\n')
                fout.write(str(freq2) + '\r\n')"""
                
#print str(calculateDice(u'чай', u'печенье'))
#print findWordDistance(u'авангардизм', u'формализм', 2)
#print str(calculateCosine(u'авангардизм', u'формализм'))



distance, accumulatedFreqList, isConnected = \
                                    dijkstraSearchFirst(u'диагональ', u'самолет')
for entry in accumulatedFreqList:
    print(str(entry[0]) +',' + entry[1] +',' + entry[2])
    
    
print getWeightedPathByFreqList(accumulatedFreqList)
calculateCosine(u'каланча', u'павильон')

"""pathLength, freqList, isConnected = dijkstraSearchFirst(u'автострада', u'автобус')
for entry in freqList:
    print(str(entry[0]) +',' + entry[1] +',' + entry[2])"""
    