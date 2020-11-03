import csv
import codecs
from snownlp import SnowNLP
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False # 写中文
f=codecs.open('评论数据集.csv','w','gbk')
csv_writer=csv.writer(f)
text = open('评论.txt',"r",encoding='gbk').readlines()
# csv_writer.writerow(("评论","情感分数","情感等级"))
sentimentlist=[]
dengjilist=[]
neg=0
pos=0
for line in text:
    if line =="\n":
        continue
    if line:
        score=SnowNLP(line).sentiments
        sentimentlist.append(score)
        if score<0.75:
            neg+=1
            dengji=0
        else:
            pos+=1
            dengji=1
        dengjilist.append(dengji)
        csv_writer.writerow((line,score,dengji))
# plt.hist(sentimentlist, bins=np.arange(0, 1, 0.01), facecolor='#87CEFA')
# plt.xlabel('情感分数')
# plt.ylabel('数量')
# plt.title('情感分数分布情况')
# plt.bar(["正面评论","负面评论"],[pos,neg],width=0.45,label="num",color="#87CEFA")
# plt.ylabel('评论数量')
# plt.title('正负面情感评论数据集')
# print("一共有",pos,"条正面情感评论；",neg,"条负面情感评论") 5589 5503
# plt.show()