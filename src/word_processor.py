# coding=utf-8
__author__ = 'gisly'

import datetime

import flickr_downloader
import file_utils
import common_constants
import word_db
import time
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def processZaliznyakDictionary(filename, fromNum, toNum):
    zaliznyakWords = file_utils.readLinesFromFile(filename)    
    processWordsFromListInFlickr(zaliznyakWords, fromNum, toNum)  

def processWordsFromListInFlickr(listOfWords, fromNum = 0, toNum = None):
    currentNum = 0
    print str(datetime.datetime.now()) + 'started processing processWordsFromListInFlickr: from '\
                                        + str(fromNum)
    for word in listOfWords:
        if toNum is not None  and currentNum > toNum:
            print str(datetime.datetime.now()) + ':ended processing: ' + str(currentNum)
            break
        if currentNum >= fromNum:
            time.sleep(10)
            curWordFreqDict, wordPhotoIds = flickr_downloader.getRussianTagsByTag(word)
            print str(datetime.datetime.now()) + ':called flickr'
            insertPairFreqs(word, curWordFreqDict)
            print str(datetime.datetime.now()) + ':inserted pair frequencies'
            #TODO: let's count in a different way
            #upsertNewWordsLinks(wordPhotoIds)
            print str(datetime.datetime.now()) + ':currentNum: ' + str(currentNum)
            print word
            
            word_db.insertCurrentNum(currentNum, common_constants.ZALIZNYAK_CODE,
                                                    common_constants.FLICKR_CODE)
        currentNum += 1
        
        
def insertPairFreqs(word, otherWordFreqDict):
    for key, value in otherWordFreqDict.iteritems():
        word_db.insertPair(word, key, value, common_constants.FLICKR_CODE)  

def upsertNewWordsLinks(wordPhotoIds):
    for word, linkList in wordPhotoIds.iteritems():
        word_db.upsertWordLink(word, linkList, common_constants.FLICKR_CODE)   
        
        
#processZaliznyakDictionary('../resources/zdf-win.txt', 821, 2000)
        
        
#processZaliznyakDictionary('../resources/zdf-win.txt', 2168, 3000)


#processZaliznyakDictionary('../resources/zdf-win.txt', 3001, 4000)
#processZaliznyakDictionary('../resources/zdf-win.txt', 4001, 10000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 10001, 16000)
#processZaliznyakDictionary('../resources/zdf-win.txt', 16000, 20000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 16450, 20000)


#processZaliznyakDictionary('../resources/zdf-win.txt', 20001, 30000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 31001, 35000)


#processZaliznyakDictionary('../resources/zdf-win.txt', 32616, 35000)

#BEFORE MY TRIP

#processZaliznyakDictionary('../resources/zdf-win.txt', 36997, 37000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 37001, 39000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 39001, 40500)


#AFTER MY TRIP


#processZaliznyakDictionary('../resources/zdf-win.txt', 40501, 42000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 43001, 45000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 45001, 47000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 47001, 48000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 46414, 47000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 48001, 49000)
#processZaliznyakDictionary('../resources/zdf-win.txt', 49001, 50000)

#TODO
#processZaliznyakDictionary('../resources/zdf-win.txt', 50716, 52000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 46152, 46153)

#processZaliznyakDictionary('../resources/zdf-win.txt', 52001, 53000)


#processZaliznyakDictionary('../resources/zdf-win.txt', 53818, 54000)

#TODO: 29.11
#processZaliznyakDictionary('../resources/zdf-win.txt', 54743, 56000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 57219, 58000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 61482, 62000)
#processZaliznyakDictionary('../resources/zdf-win.txt', 62001, 63000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 63001, 64000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 64410, 65000)
#processZaliznyakDictionary('../resources/zdf-win.txt', 65361, 66000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 66001, 67000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 67001, 68000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 68001, 70000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 70825, 72000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 72001, 74000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 74001, 75000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 78001, 80000)



#processZaliznyakDictionary('../resources/zdf-win.txt', 75001, 77000)



#processZaliznyakDictionary('../resources/zdf-win.txt', 77001, 78000)





#processZaliznyakDictionary('../resources/zdf-win.txt', 84237, 85000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 82380, 83000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 83085, 84000)


#processZaliznyakDictionary('../resources/zdf-win.txt', 80647, 82000)



#processZaliznyakDictionary('../resources/zdf-win.txt', 85095, 86000)



#processZaliznyakDictionary('../resources/zdf-win.txt', 86791, 87000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 87260, 88000)
#CURRENT

#processZaliznyakDictionary('../resources/zdf-win.txt', 88209, 89000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 89017, 90000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 91000, 92000)

#processZaliznyakDictionary('../resources/zdf-win.txt', 93000, 95000)


        