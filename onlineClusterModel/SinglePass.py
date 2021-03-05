#coding=utf-8
from Cluster import Cluster
from twitterModel.Twitter import Twitter
from collections import defaultdict
from staticModel.Cooccurrence import getProb
import threading
from util.common import timer

class SinglePass(object):
    def __init__(self, threshold, threads_num):
        # 当前簇列表，只保留最近的100个簇
        self.clustersList = []
        # 相似度阈值，只有当推文与某个簇相似度大于等于此阈值时才会将该推文加入到该簇中
        self.threshold = threshold
        # 线程数目
        self.threads_num = threads_num

        self.mostSimilar = 0.0
        self.idx = -1
        self.lock = threading.Lock()

    def getClusters(self):
        return self.clustersList

    def addTweet(self, tweet):
        """
        在线聚类主函数，传入一条推文，计算该推文与目前已有簇的相似度，找出与当前推文相似度最高的簇，
        如果其相似度大于等于给定阈值，在该推文加入该簇，并更新该簇信息；否则将该推文单独作为一个簇。
        :param tweet: 传入的推文
        :return:
        """
        # 将该推文进行封装
        tweet = Twitter(tweet)
        n = len(self.clustersList)

        # 记录簇列表中与当前推文最相似的簇索引和对应的相似度取值
        self.mostSimilar = 0.0
        self.idx = -1

        # # 遍历当前簇列表中所有簇，一一计算该推文与这些簇的相似度
        # for i in range(num):
        #     cluster = self.clustersList[i]
        #     similar = self._fusionSimilar(tweet, cluster)
        #     if similar > mostSimilar:
        #         mostSimilar = similar
        #         idx = i
        if n > 0:
            threads = []  # 线程对象列表
            avg = n // self.threads_num  # 每一个线程需要计算的数据量
            # print "thread works: ", avg
            for i in range(self.threads_num):
                begin = i * avg
                end = begin + avg
                # 遇到不能均分的情况，让最后一个线程处理剩下来所有的
                if i == self.threads_num - 1:
                    end = n - 1
                t = threading.Thread(target=self.func(tweet, begin, end))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

        if self.mostSimilar >= self.threshold:
            # 当相似度大于阈值时，将推文放入索引为idx的簇中，并跟新簇信息
            self._update(tweet, self.idx)
            # 只保留簇中重要信息，减少内存占用和时间消耗，同时减少噪声带来的影响
            self._gc(self.clustersList[self.idx])
        else:
            # 否则新建一个簇，该簇目前仅包含当前推文，并放入簇列表
            self.clustersList.append(self._createCluster(tweet))

    def func(self, tweet, begin, end):
        """
        多线程的运行函数，找出当前推特与self.clustersList[begin: end]中最相似的簇的相似度值和索引，并更新
        :param tweet: 当前推文
        :param begin: 当前线程只计算簇列表部分簇，开始下标为 begin
        :param end: 前线程只计算簇列表部分簇，结束下标为 end
        :return:
        """
        # 记录簇列表中与当前推文最相似的簇索引和对应的相似度取值
        mostSimilar = 0.0
        idx = -1
        # 遍历当前簇列表中所有簇，一一计算该推文与这些簇的相似度
        for i in range(begin, end + 1):
            cluster = self.clustersList[i]
            similar = self._fusionSimilar(tweet, cluster)
            if similar > mostSimilar:
                mostSimilar = similar
                idx = i
        # 这里涉及到全局变量的修改，需要加锁
        self.lock.acquire()
        if mostSimilar > self.mostSimilar:
            self.mostSimilar = mostSimilar
            self.idx = idx
        self.lock.release()

    def _fusionSimilar(self, tweet, cluster):
        """
        计算推文与簇的融合相似度，分为四个方面
            - 地理位置实体相似度
            - 文本相似度
            - 语义相似度
            - 共现相似度
        :param tweet: 推文
        :param cluster: 簇
        :return:
        """
        geoSimilar = self._getGeoSimilar(tweet, cluster)
        textSimilar = self._getTextSimilar(tweet, cluster)
        senmanticSimilar = self._getSenmanticSimilar(tweet, cluster)
        coOccurrenceSimilar = self._getCoOccurrenceSimilar(tweet, cluster)
        similar = geoSimilar + textSimilar + senmanticSimilar + coOccurrenceSimilar
        return similar

    def _update(self, tweet, idx):
        """
        将推文放入索引为idx的簇中，更新簇中各信息
        :param tweet: 推文
        :param idx: 簇索引
        :return:
        """
        cluster = self.clustersList[idx]
        cluster.textList.append(tweet.getText())
        cluster.timeList.append(tweet.getTime())
        cluster.userList.append(tweet.getUsername())
        if tweet.getCoordinates() != None:
            cluster.coordinatesList.append(tweet.getCoordinates())
        for word in tweet.getLocs():
            cluster.locFreq[word] += 1
        for word, weight in tweet.getWordsWeight().items():
            cluster.wordsWight[word] += weight
        # 更新簇的语义向量
        vec1 = tweet.getSemanticVector()
        vec2 = cluster.getSemanticVector()
        # 当前簇中推文数目
        num = len(cluster.getTextList()) - 1
        temp = [(vec1[i] + num * vec2[i]) / (num + 1) for i in range(len(vec1))]
        cluster.semanticVector = temp


    def _createCluster(self, tweet):
        """
        根据该条推文新建一个簇，簇中信息全部来自该推文
        :param tweet: 推文
        :return:
        """
        cluster = Cluster()
        cluster.textList.append(tweet.getText())
        cluster.timeList.append(tweet.getTime())
        cluster.userList.append(tweet.getUsername())
        if tweet.getCoordinates() != None:
            cluster.coordinatesList.append(tweet.getCoordinates())
        for word in tweet.getLocs():
            cluster.locFreq[word] += 1
        for word, weight in tweet.getWordsWeight().items():
            cluster.wordsWight[word] += weight
        cluster.semanticVector = tweet.getSemanticVector()
        return cluster

    def _getGeoSimilar(self, tweet, cluster):
        """
        计算地理位置相似度，如果推文或者簇中无地理实体，则相似度为0.5；如果推文和簇中地理位置实体相同，则为1；如果不同则为0
        :param tweet: 推文
        :param cluster: 簇
        :return:
        """
        tweetLocs = tweet.getLocs()
        clusterLocs = cluster.getLocFreq()
        if len(tweetLocs) == 0 or len(clusterLocs) == 0:
            return 0.5
        for tweetLoc in tweetLocs:
            if clusterLocs[tweetLoc] != 0:
                return 1.0
        return 0.0

    def _getTextSimilar(self, tweet, cluster):
        """
        文本相似度，传入推文和簇的单词权重字典，利用余弦相似度计算其相似度
        :param tweet: 推文
        :param cluster: 簇
        :return:
        """
        tweetWords = tweet.getWordsWeight()
        clusterWords = cluster.getWordsWeight()
        common = 0.0
        for word, weight in tweetWords.items():
            common += clusterWords[word] * weight
        if common <= 0.0:
            return 0.0
        # 推文词权重字典的模值
        norm1 = 0.0
        for weight in tweetWords.values():
            norm1 += weight * weight
        norm1 = norm1 ** 0.5
        # 簇词权重字典的模值
        norm2 = 0.0
        for weight in clusterWords.values():
            norm2 += weight * weight
        norm2 = norm2 ** 0.5
        ret = common / (norm1 * norm2)
        return ret

    def _getSenmanticSimilar(self, tweet, cluster):
        """
        计算推文和簇的语义相似度
        :param tweet: 推文
        :param cluster: 簇
        :return:
        """
        vec1 = tweet.getSemanticVector()
        vec2 = cluster.getSemanticVector()
        common = 0.0
        for i in range(len(vec1)):
            common += vec1[i] * vec2[i]
        norm1, norm2 = 0.0, 0.0
        for i in range(len(vec1)):
            norm1 += vec1[i] * vec1[i]
            norm2 += vec2[i] * vec2[i]
        norm1, norm2 = norm1 ** 0.5, norm2 ** 0.5
        if norm1 * norm2 == 0.0:
            return 0.0
        similar = common / (norm1 * norm2)
        return similar

    def _getCoOccurrenceSimilar(self, tweet, cluster):
        """
        共现相似度，传入传入推文和簇的单词权重字典，从统计模块中计算中当前时间窗口内
        :param tweet: 推文
        :param cluster: 簇
        :return:
        """
        tweetWords = tweet.getWordsWeight().keys()
        clusterWords = cluster.getWordsWeight().keys()
        m, n = len(tweetWords), len(clusterWords)
        if m * n == 0:
            return 0.0
        similar = 0.0
        for a in tweetWords:
            for b in clusterWords:
                similar += max(getProb(a, b), getProb(b, a))
        similar /= (m * n)
        return similar

    def _gc(self, cluster):
        """
        删除簇中不太重要的信息，对于单词而言，只保留累积权值最高的50个单词即可，这样可以加快文本相似度计算的速度，也能减小内存占用
        :param cluster: 簇
        :return:
        """
        temp = cluster.getWordsWeight().items()
        if len(temp) >= 100:
            # 按照单词累积权值从大到小排序，并只保留前50个
            temp = sorted(temp, key=lambda item: -item[1], reverse=True)[:50]
            dic = defaultdict(lambda: 0.0)
            for word, weight in temp:
                dic[word] += weight
            cluster.wordsWight = dic


