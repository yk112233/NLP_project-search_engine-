from project import pinglun
'''
import json
from urllib import request
import time
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
from project import pinglun
header_dict = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
}
def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.enconding = "utf-8"
        return r.text
    except:
        return ""
def fillBookdata(html):
    bookdata=[]
    pattern = re.compile('<dl class="search-list J_search">\n                                    <a href=.*?data-report.*?<dt>', re.S)
    items = re.findall(pattern, html)
    for it in items:
        match=re.match('<dl class="search-list J_search">\n                                    <a href="(.*)" data-report',it)
        # print(match.group(1))
        bookdata.append(match.group(1))
    return bookdata
def getelement(p):
    new_list=[]
    for i in p:
        for j in i:
            new_list.append(j)
    return new_list
key_word=["机器学习","JAVA","人工智能","python","5G"]
page=[]
pinglun_list=[]
for word in tqdm(key_word):
    for i in range(1,21):
        url="https://so.csdn.net/so/search/s.do?q="+word+"&t=all&platform=pc&p="+str(i)+"&s=&tm=&v=&l=&u=&ft="
        html = getHTMLText(url)
        page.append(fillBookdata(html))
url_list=getelement(page)
with open('爬取网站.txt','a') as file_handle:
    for i in url_list:
        file_handle.write(i)     # 写入
        file_handle.write('\n')

url_list=[]
text = open('爬取网站.txt').readlines()
for line in text:
    url_list.append(line)
pinglun_list=pinglun.return_pinglun(url_list)
'''
from project import naive_bayes
print(naive_bayes.emotion("https://blog.csdn.net/wangjiangrong/article/details/104973117?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-4.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-4.channel_param"))