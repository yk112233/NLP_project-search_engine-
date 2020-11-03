import csv
import codecs
import jieba
import pandas as pd
from urllib import request
from gensim import corpora, models
csvfile=open(u"评论数据集.csv","r")
reader=csv.reader(csvfile)
# with open('pinglun_neg_cut.txt','a',encoding='utf-8') as file_3:
#     for i in reader:
#         if i[2]=='0':
#             wordlist = jieba.cut(i[0], cut_all=False)
#             for word in wordlist:
#                 if word is not '\n':
#                     file_3.write(word)
#                     file_3.write(" ")

# with open('pinglun_pos_cut.txt','a',encoding='utf-8') as file_4:
#     for i in reader:
#         if i[2]=='1':
#             wordlist = jieba.cut(i[0], cut_all=False)
#             for word in wordlist:
#                 if word is not '\n':
#                     file_4.write(word)
#                     file_4.write(" ")

negfile = './pinglun_neg_cut.txt'
posfile = './pinglun_pos_cut.txt'
stoplist = './stopword.txt'
neg = pd.read_csv(negfile, encoding = 'utf-8', header = None) #读入数据
pos = pd.read_csv(posfile, encoding = 'utf-8', header = None)
stop = pd.read_csv(stoplist, encoding = 'utf-8', header = None, sep = 'tipdm',engine='python')
stop = [' ', ''] + list(stop[0])  # Pandas自动过滤了空格符，这里手动添加（在每条数据的开头加个空格）

# 下面这段代码可以分为两小段，这两小段代码几乎一致，前面一个是针对负面评论，后一个是针对正面评论，所以只详解其中一个
neg[1] = neg[0].apply(lambda s: s.split(' '))  # 定义一个分割函数，然后用apply广播
neg[2] = neg[1].apply(lambda x: [i for i in x if i not in stop])  # 逐词判断是否停用词，思路同上
# 上面这句代码的语法是：列表推导式子。意思是说，如果i不在停用词列表(stop)中，就保留该词语（也就是最前面的一个i），否则就进行删除
# 上面的这句代码中，把for i in x看做整体，把if i not in stop看做判断语句，把最前面的i看做满足if语句之后的执行语句即可。
pos[1] = pos[0].apply(lambda s: s.split(' '))
pos[2] = pos[1].apply(lambda x: [i for i in x if i not in stop])
neg_dict = corpora.Dictionary(neg[2])  # 建立词典
neg_corpus = [neg_dict.doc2bow(i) for i in neg[2]]  # 建立语料库
neg_lda = models.LdaModel(neg_corpus, num_topics=3, id2word=neg_dict)  # LDA模型训练
print("负面主题分析：\n")
for i in range(2):
    print(neg_lda.print_topic(i))  # 输出每个主题（这个其实就是聚类结果的输出）

# 正面主题分析
print("正面主题分析：\n")
pos_dict = corpora.Dictionary(pos[2])
pos_corpus = [pos_dict.doc2bow(i) for i in pos[2]]
pos_lda = models.LdaModel(pos_corpus, num_topics=3, id2word=pos_dict)
for i in range(2):
    print(pos_lda.print_topic(i))  # 输出每个主题
'''
负面主题分析：

0.026*"谢谢" + 0.015*"感谢" + 0.013*"楼主" + 0.013*"博主" + 0.009*"请问" + 0.009*"链接" + 0.008*"一份" + 0.008*"发" + 0.006*"想" + 0.006*"求"
0.022*"谢谢" + 0.020*"楼主" + 0.016*"一份" + 0.015*"感谢" + 0.014*"链接" + 0.011*"博主" + 0.011*"请问" + 0.010*"发" + 0.008*"失效" + 0.008*"想"
0.033*"谢谢" + 0.017*"楼主" + 0.015*"感谢" + 0.015*"一份" + 0.014*"链接" + 0.013*"请问" + 0.012*"博主" + 0.011*"失效" + 0.010*"发" + 0.007*"厉害"
正面主题分析：

0.038*"学习" + 0.025*"感谢" + 0.025*"分享" + 0.020*"谢谢" + 0.013*"大佬" + 0.013*"楼主" + 0.012*"博主" + 0.010*"不错" + 0.008*"邮箱" + 0.007*"一份"
0.034*"学习" + 0.024*"分享" + 0.019*"谢谢" + 0.015*"感谢" + 0.011*"楼主" + 0.009*"大佬" + 0.009*"邮箱" + 0.008*"不错" + 0.008*"博主" + 0.007*"写"
0.029*"学习" + 0.022*"谢谢" + 0.018*"感谢" + 0.016*"分享" + 0.014*"楼主" + 0.010*"博主" + 0.010*"大佬" + 0.009*"一份" + 0.008*"不错" + 0.007*"邮箱"'''