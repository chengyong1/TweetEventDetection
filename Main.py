#coding=utf-8
from pymongo import MongoClient
from twitterModel.Twitter import Twitter
from staticModel.Cooccurrence import p, getProb, updateProb, tweetsDeque
from onlineClusterModel.SinglePass import SinglePass
import time

tweet_db = MongoClient('mongodb://root:FzDwXxCl.121.$Root$@121.48.165.123:30011')['tweets_database']['tweets-2020-01-01']
cursor = tweet_db.find()

# 设置相似度阈值和线程数目
similarThreshold = 2.0
threadNum = 4
test = SinglePass(similarThreshold, threadNum)

begin = time.clock()
count = 0
for tweet in cursor:
    count += 1
    updateProb(tweet)
    test.addTweet(tweet)
    if count % 1000 == 0:
        print "have processed tweet num: " + str(count)
        clusters = test.getClusters()
        print "cluster num = ", len(clusters)
        # for cluster in clusters:
        #     if len(cluster.textList) >= 5:
        #         print cluster
        test.clustersList = []
        end = time.clock()
        print "time cost: ", end - begin
    if count > 10000:
        break











