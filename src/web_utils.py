# coding=utf-8
__author__ = 'gisly'
import urllib
import urllib2
import re
import urlparse


def getDataFromURL(url, encoding, paramDict):
    if paramDict:
        dictInUtf = dict()
        for k, v in paramDict.iteritems():
            dictInUtf[k] = unicode(v).encode('utf-8')
        encodedParams = urllib.urlencode(dictInUtf)
        url = url + '?%s'%encodedParams
    urlEncoded = iriToUri(url)
    usock = urllib2.urlopen(urlEncoded)
    data = usock.read()
    usock.close()
    return data.decode(encoding)


#http://stackoverflow.com/questions/4389572/how-to-fetch-a-non-ascii-url-with-python-urlopen
def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )