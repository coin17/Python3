#! /usr/bin/env python
#coding=utf-8
# 抓取特定知乎用户关注对象，使用 cookies，直接请求 json

import codecs
import json
import time, os #定时抓取
import requests 
import datetime #精确时间

def beginSpider(pageNum):
    print(str(pageNum))

    peoples = []

    try:
        json = download_page(DOWNLOAD_URL.replace('{offset}',str(pageNum * 20)))
    except:
        print("抓取异常：" + DOWNLOAD_URL.replace('{offset}',str(pageNum * 20)))
        time.sleep(2) #延迟N秒再抓取
        json = download_page(DOWNLOAD_URL.replace('{offset}',str(pageNum * 20)))

    #print(json)

    #print(json["paging"]["is_end"])

    if os.path.exists(DOWNLOAD_User) == False:
        os.makedirs(DOWNLOAD_User)

    for item in json["data"]:
        if(item["avatar_url_template"] == None):
            continue

        image_name = item["url_token"]

        #"name" 名称
        #"headline" 一句话简介
        # url https://www.zhihu.com/people/+ item["url_token"] + /activities
        image_url = item["avatar_url_template"].replace('{size}','xl')

        img_localhost = DOWNLOAD_User + '\\' + image_name + '.jpg'
        img_localhost_git = DOWNLOAD_User + '/' + image_name + '.jpg'

        peoples.append("## [" + item["name"]+"](https://www.zhihu.com/people/"+item["url_token"]+"/activities)")
        peoples.append(item["headline"])
        peoples.append("")
        peoples.append('!['+item["name"]+']('+img_localhost_git+' "'+item["name"]+'")')
        peoples.append("")
        peoples.append("***")
        peoples.append("")

        if os.path.isfile(img_localhost) == False or os.path.getsize(img_localhost) == 0:
            try:
                img_req = requests.get(image_url, timeout=20)
                with open(img_localhost, 'wb') as f:
                    f.write(img_req.content)
            except:
                now = datetime.datetime.now()
                with open("error.log", 'w') as f:
                    f.write(now.strftime('%Y-%m-%d %H:%M:%S') + ' 【错误】当前图片无法下载，失效地址为：' + image_url)

    #如果有下页，递归
    if json["paging"]["is_end"] == False:
        return peoples, pageNum + 1
    return peoples, None

cookies = {}

raw_cookies = '_zap=8da04c21-f694-43b4-b806-d57ecb2a5591; d_c0="ADAC_MJc-AqPTrEN8y4oBdLW58zPE-qCwn8=|1481246007"; _zap=111062a0-2178-469e-96fb-8010b5c5b0f7; _ga=GA1.2.1593604370.1492574559; r_cap_id="NTUxOTNkM2JkZDg4NDQ4ODlhZmNkMmQxNGI5MjVhMzY=|1500448867|73a8c0d29a7d466f339e9dc3f5107be2e593b921"; cap_id="ZWI3NDUzZTkzNjQ1NDc0NWFkY2Q5ZjliNmExZmMyZWQ=|1500448867|f4eba8cc225482cf6e03359a35eaecfe68bec032"; z_c0=Mi4wQUFBQVZKOGpBQUFBTUFMOHdsejRDaGNBQUFCaEFsVk5vWldXV1FCc3lqb2huMmhLM01ZUTQxRnRPMWJkODQ0YzJ3|1500448929|4db031e62bac6db8b7f76df5bc8cd79db3d99c41; q_c1=eb629a1deb0d469ea653ebad3d22c244|1500530546000|1489651714000; aliyungf_tc=AQAAAJFHtFpB8Q0AcocyPeEtPtqHNZXB; __utma=155987696.1593604370.1492574559.1502683792.1502683792.1; __utmc=155987696; __utmz=155987696.1502683792.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _xsrf=9df349c6-d15d-43e7-9bb3-266e68f37af3'

for line in raw_cookies.split(':'):
    key,value = line.split('=', 1)
    cookies[key] = value


def download_page(url):
    return requests.get(url,cookies=cookies, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }, timeout=120).json()


#下载URL   DOWNLOAD_URL + number
#轮子哥
DOWNLOAD_URL = "https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset={offset}&limit=20"
DOWNLOAD_User = "excited-vczh"


def main():
    print("开始时间：" +  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  
    pageNum = 0

    with codecs.open('excited-vczh_followees.md', 'wb', encoding='utf-8') as fp:
        while pageNum != None:
            peoples, pageNum = beginSpider(pageNum)
            fp.write(u'{peoples}\n'.format(peoples='\n'.join(peoples)))

    print("结束时间：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  


main()
