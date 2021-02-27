#coding:utf-8
import time

stopWords = ["RT", "'d", "'ll", "'s", "'t", "'ve", 'a', "a's", 'able', 'about', 'above', 'according', 'accordingly',
             'across',
             'actually', 'after', 'afterwards', 'again', 'against', "ain't", 'all', 'allow', 'allows', 'almost',
             'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'amp', 'an', 'and',
             'another', 'any', 'anybody', 'anyhow', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart',
             'appear', 'appreciate', 'appropriate', 'are', "aren't", 'around', 'as', 'aside', 'ask', 'asking',
             'associated', 'at', 'available', 'away', 'awfully', 'b', 'bbc', 'be', 'became', 'because', 'become',
             'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'believe', 'below', 'beside',
             'besides', 'best', 'better', 'between', 'beyond', 'big', 'bitch', 'both', 'brief', 'but', 'by', 'c',
             "c'mon", "c's", 'ca', 'came', 'can', "can't", 'cannot', 'cant', 'cause', 'causes', 'certain', 'certainly',
             'changes', 'clearly', 'cnn', 'co', 'com', 'come', 'comes', 'concerning', 'consequently', 'consider',
             'considering', 'contain', 'containing', 'contains', 'corresponding', 'could', "couldn't", 'course',
             'currently', 'd', 'definitely', 'described', 'despite', 'did', "didn't", 'different', 'do', 'does',
             "doesn't", 'doing', "don't", 'done', 'down', 'downwards', 'during', 'e', 'each', 'edu', 'eg', 'eight',
             'either', 'else', 'elsewhere', 'enough', 'entirely', 'especially', 'et', 'etc', 'even', 'ever', 'every',
             'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'exactly', 'example', 'except', 'f', 'far',
             'feel', 'feeling', 'feels', 'felt', 'few', 'fifth', 'first', 'five', 'followed', 'following', 'follows',
             'for', 'former', 'formerly', 'forth', 'four', 'from', 'fun', 'fuck', 'fucked', 'fucker', 'fucking',
             'fucks', 'further', 'furthermore', 'g', 'get', 'gets', 'getting', 'given', 'gives', 'go', 'goes', 'going',
             'gone', 'good', 'got', 'gotten', 'greetings', 'gt', 'h', 'had', "hadn't", 'happens', 'happy', 'hardly',
             'has', "hasn't", 'have', "haven't", 'having', 'he', "he's", 'hello', 'help', 'hence', 'her', 'here',
             "here's", 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'hey', 'hi', 'him', 'himself',
             'his', 'hither', 'hopefully', 'how', 'howbeit', 'however', 'http', 'i', "i'd", "i'll", "i'm", "i've", 'ie',
             'if', 'ignored', 'immediate', 'in', 'inasmuch', 'inc', 'indeed', 'indicate', 'indicated', 'indicates',
             'inner', 'insofar', 'instead', 'into', 'inward', 'is', "isn't", 'it', "it'd", "it'll", "it's", 'its',
             'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kept', 'know', 'knows', 'known', 'l', 'last', 'lately',
             'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', "let's", 'like', 'liked', 'likely', 'lol',
             'little', 'look', 'looking', 'looks', 'lt', 'ltd', 'luck', 'm', 'mainly', 'made', 'make', 'making', 'many',
             'may', 'maybe', 'me', 'mean', 'meanwhile', 'merely', 'might', 'more', 'moreover', 'most', 'mostly', 'much',
             'must', 'my', 'myself', 'n', "n't", 'name', 'namely', 'nd', 'near', 'nearly', 'necessary', 'need', 'needs',
             'neither', 'never', 'nevertheless', 'new', 'next', 'nice', 'nine', 'no', 'nobody', 'non', 'none', 'noone',
             'nor', 'normally', 'not', 'nothing', 'novel', 'now', 'nowhere', 'o', 'obviously', 'of', 'off', 'often',
             'oh', 'ok', 'okay', 'old', 'omg', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'org', 'other',
             'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'own',
             'p', 'particular', 'particularly', 'per', 'perhaps', 'photo', 'picture', 'pix', 'placed', 'please', 'plus',
             'pm', 'possible', 'presumably', 'probably', 'provides', 'q', 'que', 'quite', 'qv', 'r', 'rather', 'rd',
             're', 'really', 'reasonably', 'regarding', 'regardless', 'regards', 'relatively', 'respectively',
             'retweet', 'retweeting', 'retweets', 'right', 'rt', 'rts', 's', 'sad', 'said', 'same', 'saw', 'say',
             'saying', 'says', 'second', 'secondly', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen',
             'self', 'selves', 'sensible', 'sent', 'serious', 'seriously', 'seven', 'several', 'shall', 'she', 'shit',
             'should', "shouldn't", 'since', 'six', 'so', 'some', 'somebody', 'somehow', 'someone', 'something',
             'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specified', 'specify', 'specifying',
             'still', 'sub', 'such', 'sup', 'sure', 't', "t's", 'take', 'taken', 'tell', 'tends', 'th', 'than', 'thank',
             'thanks', 'thanx', 'that', "that's", 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then',
             'thence', 'there', "there's", 'thereafter', 'thereby', 'therefore', 'therein', 'theres', 'thereupon',
             'these', 'they', "they'd", "they'll", "they're", "they've", 'think', 'third', 'this', 'thorough',
             'thoroughly', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'today',
             'together', 'tonight', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying',
             'twice', 'two', 'u', 'ugh', 'un', 'under', 'unfortunately', 'unless', 'unlikely', 'until', 'unto', 'up',
             'upon', 'us', 'use', 'used', 'useful', 'uses', 'using', 'usually', 'uucp', 'v', 'value', 'various', 'very',
             'via', 'video', 'viz', 'vs', 'w', 'wanna', 'want', 'wants', 'was', "wasn't", 'watch', 'way', 'we', "we'd",
             "we'll", "we're", "we've", 'welcome', 'well', 'went', 'were', "weren't", 'what', "what's", 'whatever',
             'when', 'whence', 'whenever', 'where', "where's", 'whereafter', 'whereas', 'whereby', 'wherein',
             'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', "who's", 'whoever', 'whole',
             'whom', 'whose', 'why', 'will', 'willing', 'wish', 'with', 'within', 'without', "won't", 'wonder', 'would',
             "wouldn't", 'wow', 'wtf', 'x', 'y', 'yes', 'yet', 'you', "you'd", "you'll", "you're", "you've", 'your',
             'yours', 'yourself', 'yourselves', 'z', 'zero']

def isStopWord(word):
    """
    判断一个单词是否是停词
    :param word: 输入一个单词
    :return: 是停词则返回True
    """
    if word in stopWords:
        return True
    return False

def timeTrans(timestamp):
    """
    时间戳转化器
    :param timestamp: 输入时间戳，s或ms为单位均可
    :return: 按照标准事件格式输出，例如输入 1577859568，返回 2020-01-01 14:19:28
    """
    timeStamp = int(str(timestamp)[:10])
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

if __name__ == '__main__':
   print timeTrans(1577859568)