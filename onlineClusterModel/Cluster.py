#coding=utf-8
from collections import defaultdict

class Cluster(object):
    def __init__(self):
        # 簇内推文组成的列表
        self.textList = []
        # 推文时间组成的列表
        self.timeList = []
        # 推文发送者组成的列表
        self.userList = []
        # 推文发送的经纬度坐标组成的列表
        self.coordinatesList = []
        # 地理实体单词及其出现次数组成的字典
        self.locFreq = defaultdict(lambda: 0)
        # 每个单词及其权重
        self.wordsWight = defaultdict(lambda: 0)
        # 由每个单词的word2vec向量得到簇的语义向量
        self.semanticVector = None

    def getTextList(self):
        return self.textList

    def getTimeList(self):
        return self.timeList

    def getUserList(self):
        return self.userList

    def getCoordinatesList(self):
        return self.coordinatesList

    def getLocFreq(self):
        return self.locFreq

    def getWordsWeight(self):
        return self.wordsWight

    def getSemanticVector(self):
        return self.semanticVector

    def __str__(self):
        """
        重载toString()方法，打印出簇中需要的信息，方便调试
        :return:
        """
        textInfo = '\n'.join(self.textList[:30])
        return "num: " + str(len(self.textList)) + \
               ", locsFreq: " + str(self.getLocFreq().keys()) + '\n' + \
               textInfo + '\n'