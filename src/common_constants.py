# coding=utf-8
__author__ = 'gisly'

FLICKR_CODE = 'flickr'
ZALIZNYAK_CODE = 'zaliznyak'


FILE_RELATION = 'FILE_RELATION'
FILE_HJ_SIMPLE = 'FILE_HJ_SIMPLE'
EVALUATION_ACCURACY = 'EVALUATION_ACCURACY'

WORD_DELIMITER = ','
LINE_ENDING_CHARACTER = '\n'
FILE_EXTENSION = '.csv'


##########FEATURES##################################

FEATURE_DEGREE = 'degree'
FEATURE_PAGERANK = 'pagerank'

FEATURE_GRAPH_LIMIT = 'graphLimit'
FEATURE_GRAPH_LINK_LIST = 'linkList'
FEATURE_GRAPH_FREQ_LIST = 'freqList'
FEATURE_GRAPH_IS_CONNECTED = 'graphIsConnected'

FEATURE_GRAPH_IS_RELATED = 'link'
FEATURE_WORD0 = 'word0'
FEATURE_WORD1 = 'word1'
FEATURE_GRAPH_PATHLENGTH = 'pathLength'
FEATURE_GRAPH_JACCARD = 'jaccardSimilarity'
FEATURE_GRAPH_DICE = 'diceSimilarity'
FEATURE_VECTOR_COSINE = 'cosine'
FEATURE_GRAPH_BOTHEXIST = 'bothexist'
FEATURE_GRAPH_WEIGHTED_PATH = 'weightedPath'

FEATURE_MORPH_SAMEPOS = 'samePOS'

FEATURE_VALUE_YES = 'Y'
FEATURE_VALUE_NO = 'N'
FEATURE_VALUE_NA = 'NODATA'

ALL_FEATURES = [FEATURE_WORD0,
                FEATURE_WORD1,
                FEATURE_GRAPH_LIMIT,
                FEATURE_GRAPH_IS_CONNECTED,
                FEATURE_GRAPH_IS_RELATED,
                FEATURE_GRAPH_PATHLENGTH,
                FEATURE_GRAPH_JACCARD,
                FEATURE_GRAPH_DICE,
                FEATURE_GRAPH_BOTHEXIST,
                FEATURE_MORPH_SAMEPOS,
                FEATURE_VECTOR_COSINE,
                FEATURE_GRAPH_WEIGHTED_PATH
                ]


ALL_ENUMERABLE_FEATURES = [
                           FEATURE_GRAPH_FREQ_LIST,
                           ]

ALL_ENUMERABLE_BY_WORD_FEATURES = [FEATURE_DEGREE,
                                   FEATURE_PAGERANK,
                                   ]