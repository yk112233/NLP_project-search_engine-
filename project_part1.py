# encoding=utf-8
# 导入爬虫包
from selenium import webdriver
# 睡眠时间
import time
import re
import os
import requests
import lxml.html


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4)\
        AppleWebKit/537.36(KHTML, like Gecko) Chrome/52 .0.2743. 116 Safari/537.36'

    }
    response = requests.get(url, headers=headers)
    html = response.text
    return html

if __name__ == '__main__':

    # 要爬取的网页
    neirongs = []  # 网页内容
    travel_urls = []
    urls = []
    titles = []
    writefile = open("docs.txt", 'w', encoding='UTF-8')
    url = 'https://ai.csdn.net'
    # 第一页

    reg = r'(//blog.csdn.net/.+/article/details/[0-9]+)"' # 正则表达式
    reg_ques = re.compile(reg)  # 编译一下正则表达式，运行的更快
    travel_urls = reg_ques.findall(get_html('https://ai.csdn.net/'))  # 匹配正则表达式

    travel_urls = list(set(travel_urls))

    print(travel_urls)

    # 打印出来放在一个列表里
    for i in range(len(travel_urls)):
        url1 = 'https:' + travel_urls[i]
        urls.append(url1)
        b = get_html(url1)
        # 重点
        html = lxml.html.fromstring(b)
        # 获取标签下所有文本
        travel_neirong = html.xpath('//*[@id="article_content"]//text()')

        # 正则 匹配以下内容 \s+ 首空格 \s+$ 尾空格 \n 换行
        pattern = re.compile("^\s+|\s+$|\n")

        clause_text = ""
        for item in travel_neirong:
            # 将匹配到的内容用空替换，即去除匹配的内容，只留下文本
            line = re.sub(pattern, "", item)
            if len(line) > 0:
                clause_text += line
                #clause_text += line + "\n"
        #

        neirongs.append(clause_text)
        travel_name = html.xpath('//title/text()')
        titles.append(travel_name)
    print(titles)
    print(urls)
    for j in range(len(titles)):
        writefile.write(str(j) + '\t\t\t' + str(titles[j]) + '\t\t\t' + str(neirongs[j]) + '\t\t\t' + str(urls[j]) + '\n')