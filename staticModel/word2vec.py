#coding=utf-8
from collections import defaultdict

# 存放每个单词的词向量
wordVector = defaultdict(lambda: None)

with open(r'C:\Users\chengyong\PycharmProjects\TwitterEventDetectionDev\data\glove.twitter.27B.25d.txt', 'r') as f:
    for line in f.readlines():
        temp = line.split()
        isValue = True
        word = temp[0].lower()
        for c in word:
            if c >= 'a' and c <= 'z':
                continue
            else:
                isValue = False
        if len(word) >= 18 or len(word) <= 2:
            isValue = False
        if isValue:
            vec = [float(temp[i]) for i in range(1, 26)]
            wordVector[word] = vec

def query(word):
    """
    查询某个单词的词向量
    :param word: 传入的单词
    :return:
    """
    vec = wordVector[word]
    if vec == None:
        del wordVector[word]
        return vec
    return wordVector[word]

if __name__ == '__main__':
    print query("aaaahh")
