# # -*- coding: utf-8 -*-
#
# import logging
#
# from gensim import models
# from gensim.models import word2vec
#
#
# def main():
#     logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#     sentences = word2vec.LineSentence("output.txt")
#     model = word2vec.Word2Vec(sentences, size=250)
#
#     # 保存模型，供以后使用
#     model.save("word2vec.model")
#
#     # 模型读取
#     # model = word2vec.Word2Vec.load("your_model_name")
#
#     logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#     model = models.Word2Vec.load('word2vec.model')
#
#     print("提供 3 种测试模式\n")
#     print("输入一个词，则去寻找前一百个该词的相似词")
#     print("输入两个词，则去计算两个词的余弦相似度")
#     print("输入三个词，进行类比推理")
#
#     while True:
#         try:
#             query = input('')
#             q_list = query.split()
#
#             if len(q_list) == 1:
#                 print("相似词前 100 排序")
#                 res = model.most_similar(q_list[0], topn=100)
#                 for item in res:
#                     print(item[0] + "," + str(item[1]))
#
#             elif len(q_list) == 2:
#                 print("计算 Cosine 相似度")
#                 res = model.similarity(q_list[0], q_list[1])
#                 print(res)
#             else:
#                 print("%s之于%s，如%s之于" % (q_list[0], q_list[2], q_list[1]))
#                 res = model.most_similar([q_list[0], q_list[1]], [q_list[2]], topn=100)
#                 for item in res:
#                     print(item[0] + "," + str(item[1]))
#             print("----------------------------")
#         except Exception as e:
#             print(repr(e))
#
#
# if __name__ == "__main__":
#     main()
# -*- coding: utf-8 -*-
# import warnings
#
# warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models import word2vec
from gensim.models import KeyedVectors
import logging
from main import ans
import numpy as np
# 主程序
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentence = ans
n_dim = 300
model = word2vec.Word2Vec(sentence,size= n_dim,min_count=1,sg=1)
wv = model.wv
wv.save('word_vector1')
load_wv = KeyedVectors.load('word_vector1')
word = "数学"
res = load_wv.similar_by_word(word,topn=10)
print(res)
# raw_sentence = ["the quick brown foxs jumps over the lazy dogs yoyoyo you go home now to sleep"]
# sentence = [s.split() for s in raw_sentence]
# print(sentence)
# #sentences = word2vec.Text8Corpus(u"output.txt")  # 加载语料
# # 训练skip-gram模型;
# model = word2vec.Word2Vec(sentence, min_count=1)
# # 计算两个词的相似度/相关程度
# y1 = model.similarity('you','dogs')
# print(y1)