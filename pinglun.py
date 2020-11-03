'''
import re
import json
import time
from urllib import request
from tqdm import tqdm
header_dict = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
}
def deEnglish(sentence):
    new_sentence = ""
    for word in sentence:
        if u'\u4e00' <= word <= u'\u9fff':
            new_sentence += word
    return new_sentence

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

def return_pinglun(url_list):
    pinglun_list = list()
    for url in tqdm(url_list):
        match = re.match(r'https://blog.csdn.net/(.*)/article/details/([0-9]*)(.*)', url)
        if match:
            num_id = match.group(2)
            url_comment = "https://blog.csdn.net/phoenix/web/v1/comment/list/" + num_id + "?page=1&size=10&commentId="
            res = get_http(url_comment, header_dict)
            if res == None or len(res) <= 30:
                print("加载错误", url)
                continue
            jobj = json.loads(res)  # 解析json
            page_count = jobj["data"]['pageCount']
            for page in range(page_count):
                url_page = "https://blog.csdn.net/phoenix/web/v1/comment/list/" + num_id + "?page=" + str(page) + "&size=10&commentId="
                res = get_http(url_page, header_dict)
                time.sleep(0.1)
                if res == None or len(res) <= 30:
                    print("加载错误", url)
                    continue
                jobj = json.loads(res)  # 解析json
                comments = jobj["data"]['list']
                for comment in comments:
                    pinglun_list.append(deEnglish(comment['info']['content']))
    print(len(pinglun_list))
    with open('评论.txt', 'a') as file_handle:
        for i in pinglun_list:
            file_handle.write(i)  # 写入
            file_handle.write('\n')
    return pinglun_list
'''
# return_pinglun(url_list=["https://blog.csdn.net/sinat_40624829/article/details/103310502?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522160280906619725271727201%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=160280906619725271727201&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-9-103310502.pc_first_rank_v2_rank_v28&utm_term=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0"])