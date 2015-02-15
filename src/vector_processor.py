# coding=utf-8
__author__ = 'gisly'

import codecs


def extractFirstLines(filename, numOfLines):
    newFilename = filename + str(numOfLines)
    with codecs.open(filename, 'r', 'utf-8') as fin:
        with codecs.open(newFilename, 'w', 'utf-8') as fout:
            for index, line in enumerate(fin):
                if index > numOfLines:
                    break
                fout.write(line)
                
extractFirstLines('D://CompLing//SemanticSimilarity//word2vec//word2vec-win32-master//word2vec-win32-master//ru',
                  100)
        