from pymongo import MongoClient
from twitterModel.Twitter import Twitter
from onlineClusterModel.SinglePass import SinglePass

tweet_db = MongoClient('mongodb://root:FzDwXxCl.121.$Root$@121.48.165.123:30011')['tweets_database']['tweets-2020-01-01']
cursor = tweet_db.find()

test = SinglePass(1.7)
count = 0
for tweet in cursor:
    count += 1
    if(count == 2000):
        break
    if count % 100 == 0:
        print "have processed tweet num: " + str(count)
    clusters = test.getClusters()
    if len(clusters) >= 500:
        for cluster in clusters:
            if len(cluster.textList) >= 5:
                print cluster
        test.clustersList = []
    test.addTweet(tweet)







