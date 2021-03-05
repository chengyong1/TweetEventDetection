#coding=utf-8
from collections import defaultdict, deque
from twitterModel.Twitter import Twitter

# 统计的事件窗口大小，只统计[当前推文的时间-时间窗口, 当前推文时间]内的推文，默认为24小时
T = 24
# 单词两两间共现次数
p = defaultdict(lambda: defaultdict(lambda: 0))
# 新建一个双端队列
tweetsDeque = deque([])

def updateProb(tweet):
    tweet = Twitter(tweet)
    time = tweet.getTime()
    words = tweet.getWordsWeight().keys()
    # 将该数据加入双端队列并更新条件概率
    tweetsDeque.append([time, words])
    for i in range(len(words)):
        a = words[i]
        p[a][a] += 1
        for j in range(i + 1, len(words)):
            b = words[j]
            p[a][b] += 1
            p[b][a] += 1
    begin = time - T * 3600  # 开始的时间戳
    # 删除时间窗口之前的数据
    while tweetsDeque != None and tweetsDeque[0][0] < begin:
        # 存放要删除的数据
        temp = tweetsDeque.popleft()
        words = temp[1]
        # 更新删除数据后的共现次数
        for i in range(len(words)):
            a = words[i]
            p[a][a] -= 1
            for j in range(i + 1, len(words)):
                b = words[j]
                p[a][b] -= 1
                p[b][a] -= 1
                if p[a][b] <= 0:
                    del p[a][b]
                if p[b][a] <= 0:
                    del p[b][a]
            if len(p[a]) == 0:
                del p[a]


def getProb(a, b):
    """
    计算P(b|a)，即a出现的时候b出现的概率, p(b|a) = p(a, b) / p(b) = freq(a, b) / freq(b)，
    即为a，b在推文中共同出现的次数比上b出现的次数
    :param a: 单词a
    :param b: 单词b
    :return: P(b|a)
    """
    common = p[a][b]  # a, b共同出现次数
    if common == 0:
        return 0.0
    b_cnt = p[b][b]  # b出现次数
    if b_cnt == 0:
        return 0.0
    return common * 1.0 / b_cnt
