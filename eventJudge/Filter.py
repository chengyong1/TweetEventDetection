#coding=utf-8
from math import log2
from staticModel.wordsTimeFreq import wordsTimeFreq
class ClusterFilter(object):
    def __init__(self, cluster):
        self.culster = cluster

    def isEvent(self):
        """
        判断簇是否满足时间突发性、空间突发性和用户多样性
        :return:
        """
        if self._checkTimeBrust() and self._checkGeoBrust() and self._checkUserDiversity():
            return True
        return False

    def _checkTimeBrust(self):
        """
        去除簇中地理位置实体词，判断这些词在当前时间段的 z分数 的平均值是否大于某个阈值，如果大于该阈值，说明具有突发性
        :return:
        """
        return True

    def _checkGeoBrust(self):
        """
        根据簇中地理位置实体的信息熵来判断是否具有地理位置突发性
        :return:
        """
        locFreq = self.culster.getLocFreq()
        tot = 0
        for freq in locFreq.values():
            tot += freq
        res = 0.0
        for freq in locFreq.values():
            p = freq * 1.0 / tot
            res += p * log2(p)
        res = -res
        return res < 2.0

    def _checkUserDiversity(self):
        users = self.culster.getUserList()
        return users >= 10

