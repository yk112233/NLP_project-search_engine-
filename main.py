# coding:utf-8
#  建索引
# from docx import Document
import jieba
import math
import operator


class Document:
    def __init__(self, key, title, neirong, link):
        self.dict = {'key': key, 'title': title, 'neirong':neirong, 'link': link}

    def get(self, index):
        for first in self.dict:
            if index == first:
                return self.dict[first]

        return None


class Indexer:
    inverted = {}  # 记录词所在文档及词频
    idf = {}  # 词的逆文档频率
    id_doc = {}  # 文档与词的对应关系

    def __init__(self, file_path):
        self.doc_list = []
        self.index_writer(file_path)

    def index_writer(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                key, title, neirong, link = line.strip().split('\t\t\t')
                doc = Document(key, title, neirong, link)
                self.doc_list.append(doc)
        self.index()

    def index(self):
        doc_num = len(self.doc_list)  # 文档总数
        for doc in self.doc_list:
            key = doc.get('key')
            # 正排
            self.id_doc[key] = doc

            # 倒排
            term_list = list(jieba.cut_for_search(doc.get('neirong')))  # 分词
            for t in term_list:
                if t in self.inverted:

                    if key not in self.inverted[t]:
                        self.inverted[t][key] = 1
                    else:
                        self.inverted[t][key] += 1
                else:
                    self.inverted[t] = {key: 1}

        for t in self.inverted:
            self.idf[t] = math.log10(doc_num / len(self.inverted[t]))

        print("inverted terms:%d" % len(self.inverted))
        print("index done")
        print(self.inverted)


"""
搜索
返回结果：(相关问题,相似度)列表
搜索步骤：
    1.分词
    2.计算tf-idf,找出候选doc
    3.对文档排序
"""


class Searcher:

    def __init__(self, index):
        self.index = index

    def search(self, query):
        term_list = []
        query = query.split()
        for entry in query:
            # 分词
            term_list.extend(jieba.cut_for_search(entry))

        # 计算tf-idf,找出候选doc
        tf_idf = {}
        for term in term_list:
            if term in self.index.inverted:
                for doc_id, fre in self.index.inverted[term].items():
                    if doc_id in tf_idf:
                        tf_idf[doc_id] += (1 + math.log10(fre)) * self.index.idf[term]
                    else:
                        tf_idf[doc_id] = (1 + math.log10(fre)) * self.index.idf[term]
        # 排序
        sorted_doc = sorted(tf_idf.items(), key=operator.itemgetter(1), reverse=True)
        print("sorted_tf_idf:")
        print(sorted_doc)
        res = [self.index.id_doc[doc_id] for doc_id, score in sorted_doc]
        return res


from flask import Flask, request, render_template, redirect, url_for
import jieba

app = Flask(__name__, static_url_path='')
@app.route("/", methods=['POST', 'GET'])
def main():
    if request.method == 'POST' and request.form.get('query'):
        query = request.form['query']
        return redirect(url_for('search', query=query))

    return render_template('index.html')


@app.route("/q/<query>", methods=['POST', 'GET'])
def search(query):
    docs = searcher.search(query)
    terms = list(jieba.cut_for_search(query))
    result = highlight(docs, terms)
    return render_template('search.html', docs=result, value=query, length=len(docs))


def highlight(docs, terms):
    result = []
    for doc in docs:
        content = doc.get('title')
        for term in terms:
            content = content.replace(term, '<em><font color="red">{}</font></em>'.format(term))
        result.append((doc.get('link'), content))
    return result


index = Indexer("docs.txt")
searcher = Searcher(index)

if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)