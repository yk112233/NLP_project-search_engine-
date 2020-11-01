
from csv import reader
import numpy as np
import jieba
import time
from tqdm import tqdm
import numpy as np
import pandas as pd
import re
import json
from urllib import request
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import classification_report,accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
    return returnVec
def get_word(list):
    new_list = []
    for i in list:
        for j in i:
            new_list.append(j)
    return new_list
def process(sentence):
    wordlist=[]
    for word in list(jieba.cut(sentence, cut_all=False)):
        if word not in stop:
            wordlist.append(word)
    return wordlist
stoplist = './stopword.txt'
stop = pd.read_csv(stoplist, encoding = 'utf-8', header = None, sep = 'tipdm',engine='python')
stop = [' ', ''] + list(stop[0])  # Pandas自动过滤了空格符，这里手动添加（在每条数据的开头加个空格）
'''
filename='./评论数据集.csv'
corpus=[]
grade=[]
with open(filename,'rt',encoding='gbk') as f:
    Readers=reader(f)
    Readers=list(Readers)
for readers in Readers:
    corpus.append(readers[0][0:len(readers[0])-1])
    grade.append(readers[2])
train_x, test_x, train_y, test_y = train_test_split(corpus, grade, random_state=0, test_size=0.2)
print(type(train_y[0]))
print(train_y)
list_post=[]
test_list_post=[]
for sentence in train_x:
    list_post.append(process(sentence))
for sentence in test_x:
    test_list_post.append(process(sentence))
dictionary=np.asarray(get_word(list_post))
dictionary, counts = np.unique(dictionary, return_counts=True)
freq, dictionary = (list(i) for i in zip(*(sorted(zip(counts,dictionary), reverse=True))))
dictionary=dictionary[0:6000]#6684
trainMat=[]
for i in range(len(list_post)):
    postinDoc=list_post[i]
    trainMat.append(setOfWords2Vec(dictionary, postinDoc))
with open('训练矩阵.txt','a') as file_handle:
    for i in (trainMat):
        for j in i:
            file_handle.write(str(j))
        file_handle.write('\n')
# with open('train_y.txt','a') as file_handle:
#     for i in train_y:
#         file_handle.write(str(i))
#         # file_handle.write(" ")
# with open('dictionary.txt','a') as file_handle:
#     for i in dictionary:
#         file_handle.write(str(i))
#         file_handle.write(" ")
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB()
clf.fit(trainMat, train_y)
X_test=[]
for i in tqdm(range(len(test_list_post))):
    testEntry=test_list_post[i]
    X_test.append(np.array(setOfWords2Vec(dictionary, testEntry)))

Y_predict = clf.predict(X_test)
print(classification_report(test_y, Y_predict))
'''
header_dict = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
}

def get_http(load_url, header=None):
    res = ""
    try:
        req = request.Request(url=load_url, headers=header)  # 创建请求对象
        coonect = request.urlopen(req)  # 打开该请求
        byte_res = coonect.read()  # 读取所有数据，很暴力
        try:
            res = byte_res.decode(encoding='utf-8')
        except:
            try:
                res = byte_res.decode(encoding='gbk')
            except:
                res = ""
    except Exception as e:
        print(e)
    return res


def deEnglish(sentence):
    new_sentence = ""
    for word in sentence:
        if u'\u4e00' <= word <= u'\u9fff':
            new_sentence += word
    return new_sentence
def get_comment(url):
    match = re.match(r'https://blog.csdn.net/(.*)/article/details/([0-9]*)(.*)', url)
    num_id = match.group(2)
    url_comment = "https://blog.csdn.net/phoenix/web/v1/comment/list/" + num_id + "?page=1&size=10&commentId="
    res = get_http(url_comment, header_dict)
    jobj = json.loads(res)  # 解析json
    page_count = jobj["data"]['pageCount']
    pinglun = list()
    for page in range(page_count):
        url_page = "https://blog.csdn.net/phoenix/web/v1/comment/list/" + num_id + "?page=" + str(
            page) + "&size=10&commentId="
        res = get_http(url_page, header_dict)
        time.sleep(0.1)
        if res == None or len(res) <= 30:
            print("加载错误", url)
            continue
        jobj = json.loads(res)  # 解析json
        comments = jobj["data"]['list']
        for comment in comments:
            pinglun.append(deEnglish(comment['info']['content']))
    with open('pinglun.txt', 'a') as file_handle:
        for i in pinglun:
            file_handle.write(i)  # 写入
            file_handle.write('\n')  # 有时放在循环里面需要自动转行，不然会覆盖上一条数据
    pinglun_txt = open('pinglun.txt', 'r', encoding="gbk").readlines()
    comment_sentence=[]
    for i in pinglun_txt:
        comment_sentence.append(i)
    return comment_sentence

def emotion(url):
    comments=get_comment(url)
    from sklearn.naive_bayes import MultinomialNB
    clf = MultinomialNB()
    text = open('训练矩阵.txt').readlines()
    trainMat=[]
    for line in text:
        row=[]
        for i in range(len(line)-1):
            row.append(int(line[i]))
        trainMat.append(row)
    text2 = open('train_y.txt','r', encoding="gbk").readlines()
    train_y=[]
    for i in text2:
        for j in range(len(i)):
            train_y.append(int(i[j]))
    dictionary=[]
    text3 = open('dictionary.txt', 'r', encoding="utf-8").readlines()
    text3=str(text3[0])
    for i in text3.split():
        dictionary.append(i)
    clf.fit(trainMat, train_y)
    x=[]
    for s in comments:
        s=np.array(setOfWords2Vec(dictionary, process(s)))
        x.append(s)
    y_predict=clf.predict(x)
    average_score=y_predict.sum()/len(y_predict)
    return average_score
