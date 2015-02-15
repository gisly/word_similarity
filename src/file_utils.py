# coding=utf-8
__author__ = 'gisly'
import codecs

def readLinesFromFile(filename):
    lines = []
    with codecs.open(filename, 'r', 'utf-8') as fin:
        for line in fin:
            lines.append(line.strip())
            
    return lines

def writeToFile(text, filename):
    with codecs.open(filename, 'w', 'utf-8') as fout:
        fout.write(text)