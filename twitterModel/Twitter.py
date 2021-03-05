#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from staticModel.word2vec import query
from util.common import isStopWord
"""
将从数据库中取出的推文包装成一个实体类，会对推文合法性进行判断，只保留需要的字段，并对某些字段进行处理
"""
class Twitter(object):
    def __init__(self, tweet):
        """
        传入数据库的一条推文，更新信息
        :param tweet: 数据库中的原始推文
        """
        # 推文文本
        self.text = None
        # 推文单词列表，每个单词是一个字典，里面包含该单词的词性和实体信息
        self.words = []
        # 推文经纬度坐标，大部分推文该字段为None
        self.coordinates = None
        # 推文事件戳
        self.time = None
        # 推文发送者名称
        self.username = None
        # 推文语义向量
        self.semanticVector = None

        self.text = tweet.get("text")
        self.words = tweet.get("words")
        self.words = self._removeStopWords()
        self.coordinates = tweet.get("coordinates")
        self.time = tweet.get("created_at_ts")
        self.username = tweet.get("user")

    def getText(self):
        """
        处理推文文本
        :return: 返回去除空行和网址后的文本
        """
        self.text = self.text.replace('\n', '')
        idx = self.text.rfind("https://t.co/")
        self.text = self.text[:idx]
        return self.text

    def getCoordinates(self):
        """
        处理经纬度坐标
        :return: [经度, 维度]组成的列表，例如：[-118.3965, 34.1649]
        """
        if self.coordinates != None:
            self.coordinates = self.coordinates.get("coordinates")
        return self.coordinates

    def getLocs(self):
        """
        获取该推文的地理位置实体
        :return: 地理位置单词组成的列表，例如[us, new york]
        """
        locsList = []
        if(self.words == None):
            return locsList
        for item in self.words:
            word, ner = item['word'].lower(), item['ner']
            if ner == 'LOC':
                locsList.append(word)
        return locsList

    def getWordsWeight(self):
        """
        按照词性不同给单词赋权，赋权策略是：
            - 地理实体词不予考虑(已单独考虑)
            - 人名和机构名赋权 1.2
            - 名词和动词赋权 1.0
            - 其他词赋权 0.5
        :return: 赋权后单词及其权重组成的字典，例如：{"us": 1.2, "trump": 1.2, "eat": 1.0, "actually": 0.5}
        """
        wordsWeight = {}
        if(self.words == None):
            return wordsWeight
        for item in self.words:
            word, ner, pos = item['word'].lower(), item['ner'], item['pos']
            if ner == 'LOC':
                continue
            if ner in ['ORG', 'PER']:
                wordsWeight[word] = 1.2
            elif pos in ['NOUN', 'VERB']:
                wordsWeight[word] = 1.0
            else:
                wordsWeight[word] = 0.5
        return wordsWeight

    def getUsername(self):
        if self.username != None:
            self.username = self.username.get("screen_name", "null")
        return self.username

    def getSemanticVector(self):
        """
        计算推文的语义向量，只考虑名词，动词和数量词，每个单词会得到一个词向量，累加后求平均即可得到推文的语义向量
        :return:
        """
        self.semanticVector = [0.0 for i in range(25)]
        if self.words == None:
            return self.semanticVector
        temp = []
        for item in self.words:
            word, pos = item['word'].lower(), item['pos']
            if pos in ['NOUN', "VERB", "NUM"]:
                temp.append(word)

        n = len(temp)
        if n == 0:
            return self.semanticVector
        for word in temp:
            vec = query(word)
            if vec != None:
                for i in range(25):
                    self.semanticVector[i] += vec[i]
        self.semanticVector = [item / n for item in self.semanticVector]
        return self.semanticVector

    def getTime(self):
        return self.time

    def _removeStopWords(self):
        """去除停词后的单词"""
        temp = []
        if self.words == None:
            return
        for item in self.words:
            word = item['word'].lower()
            # 去除单词中的'#'和'@'
            word = word.replace('#', '').replace('@', '')
            # 如果单词由数字和字母组成且不是停词才加入
            if word.isalnum() and isStopWord(word) == False:
                temp.append(item)
        return temp

    def __str__(self):
        """
        重写toString方法，方便打印出推文
        :return:
        """
        return "Tweet:{" + \
               "text:" + self.getText() + \
               ', location:' + str(self.getCoordinates()) + \
               ", time:" + str(self.time) + \
               ", locs:" + str(self.getLocs()) + \
               '}'