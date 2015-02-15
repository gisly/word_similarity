# coding=utf-8
__author__ = 'gisly'
import operator
import json
import datetime

import web_utils
import language_utils


import codecs



FLICKR_ENCODING = 'utf-8'





api_key = 'adfc6f63ff62939834486ed4bac2f480'
api_secret = 'e71f76e2a42db9eb'

ENDPOINT = 'https://www.flickr.com/services/rest'

FLICKR_HEADER = 'jsonFlickrApi('
FLICKR_ENDING = ')'

PER_PAGE = 100







def getRussianTagsByTag(seedTag):
    curWordFreqDict = dict()
    wordPhotoIds = dict()
    #print str(datetime.datetime.now()) + ':before getPhotosByTag'
    photos = getPhotosByTag(seedTag)
    #print str(datetime.datetime.now()) + ':after getPhotosByTag'
    curWordPhotoIds = []
    if seedTag in wordPhotoIds:
        curWordPhotoIds = wordPhotoIds[seedTag]
    for photo in photos:
        photoId = photo['id']
        if photoId in curWordPhotoIds:
            continue
        curWordPhotoIds.append(photoId)
        #print str(datetime.datetime.now()) + ':before getRussianTagsByPhotoId'
        newTags = getRussianTagsByPhotoId(photoId)
        #print str(datetime.datetime.now()) + ':after getRussianTagsByPhotoId'
        for newTag in newTags:
            if newTag != seedTag:
                addFreqsToDict(newTag, seedTag, curWordFreqDict)
                addLinksToDict(newTag, photoId, wordPhotoIds)
    return curWordFreqDict, wordPhotoIds
            
        

def getRussianTagsByPhotoId(photoId):
    paramDict = {'photo_id':photoId}
    
    result =  callFlickrMethodWithParams('flickr.tags.getListPhoto', paramDict)
    if not 'photo' in result:
        print str(result)
        return []
    
    return [language_utils.normalize(tag['raw']) for tag in result['photo']['tags']['tag'] if tag['machine_tag'] == 0 
                                                                    and language_utils.isRussian(tag['raw'])]

def getPhotosByTag(tag):
    paramDict = {'tags' : tag, 'per_page' : PER_PAGE}
    totalFound = -1
    curPage = 0
    results = []
    while True:
        remainingPhotos = totalFound - curPage * PER_PAGE
        if totalFound >=0 and remainingPhotos <= 0:
            break
        curPage += 1
        curResults, totalFound = getPhotoPageByParams(paramDict, curPage)
        results += curResults
        
    return results
    
def getPhotoPageByParams(paramDict, pageNum):
    paramDict['page'] = pageNum
    result =  callFlickrMethodWithParams('flickr.photos.search', paramDict)
    return [photo for photo in result['photos']['photo']], int(result['photos']['total']) 

    
def callFlickrMethodWithParams(methodName, paramDict):
    paramDict['api_key'] = api_key
    paramDict['method'] = methodName
    paramDict['format'] = 'json'
    jsonData =  web_utils.getDataFromURL(ENDPOINT, FLICKR_ENCODING, paramDict)
    jsonContent = json.loads(jsonData.replace(FLICKR_HEADER, '').strip(FLICKR_ENDING));
    if jsonContent['stat'] == 'failed':
        raise Exception(jsonContent['code']+':' +jsonContent['message'])
    return jsonContent


def addFreqsToDict(newTag, seedTag, curWordFreqDict):
    if newTag == seedTag:
        return
    if newTag in curWordFreqDict:
        curWordFreqDict[newTag] += 1
    else:
        curWordFreqDict[newTag] = 1

def addLinksToDict(newTag, photoId, wordPhotoIds):
    if newTag in wordPhotoIds:
        wordPhotoIds[newTag].append(photoId)
    else:
        wordPhotoIds[newTag] = [photoId]
    

"""curWordFreqDict, wordPhotoIds = getRussianTagsByTag(u'запекать мальбек')



sorted_freqs = sorted(curWordFreqDict.items(), key=operator.itemgetter(1), reverse = True)
with codecs.open('D://testProg4.txt', 'w', 'utf-8') as fout:
    for (key, value) in sorted_freqs:
        fout.write(key + ':' + str(value) + '\r\n')"""
    
    
    
