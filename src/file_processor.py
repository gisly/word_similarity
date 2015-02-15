# coding=utf-8
__author__ = 'gisly'

import codecs

import score_calculator
import common_constants

def processFile(filename):
    ouputFilename = filename.replace(common_constants.FILE_EXTENSION, '_out' + common_constants.FILE_EXTENSION)
    with codecs.open(filename, 'r', 'utf-8') as fin:
        with codecs.open(ouputFilename, 'w', 'utf-8') as fout:
            for line in fin:
                words = line.strip().split(common_constants.WORD_DELIMITER)
                score = score_calculator.calculateScore(words[0], words[1])
                fout.write(words[0] + common_constants.WORD_DELIMITER 
                           + words[1] + common_constants.WORD_DELIMITER
                           + str(score) + common_constants.LINE_ENDING_CHARACTER)
                
                
                
                