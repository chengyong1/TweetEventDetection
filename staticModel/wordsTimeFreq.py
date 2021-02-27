#coding=utf-8
from collections import defaultdict
from twitterModel.Twitter import Twitter
T = 2  # 时间窗大小为2h

# 时间戳列表
timeList = set()
# 单词在不同时间段的出现次数
wordsTimeFreq = defaultdict(lambda: defaultdict(lambda: 0))

def updateWordsFreq(tweet):
    tweet = Twitter(tweet)
    time = tweet.getTime() // T // 3600 * 3600 * T
    timeList.add(time)
    for word in tweet.getLocs():
        wordsTimeFreq[word][time] += 1
    for word in tweet.getWordsWeight().keys():
        wordsTimeFreq[word][time] += 1

