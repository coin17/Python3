#! /usr/bin/env python
#coding=utf-8
# 递归抓取知乎用户关注对象

import json
import time, os 
import requests
import datetime
from MSSql_SqlHelp import MSSQL 

#MS Sql Server 链接字符串
ms = MSSQL(host=".",user="sa",pwd="sa",db="SmallIsBeautiful")

#获取抓取种子
def getSeed():
    sql = "select top(1) column_0 from Space0017A where column_4='0' " 
    json = ms.ExecQuery(sql.encode('utf-8'))
    if(len(json) == 0):
        return -1
    else:
        return json[0][0]


#完成抓取，更新用户状态
def updateUser(DOWNLOAD_User):
    sql = "update Space0017A set column_4='1' where column_0='" + DOWNLOAD_User + "'"
    ms.ExecNonQuery(sql.encode('utf-8'))


cookies = {}

raw_cookies = '_zap=8da04c21-f694-43b4-b806-d57ecb2a5591; d_c0="ADAC_MJc-AqPTrEN8y4oBdLW58zPE-qCwn8=|1481246007"; _zap=111062a0-2178-469e-96fb-8010b5c5b0f7; _ga=GA1.2.1593604370.1492574559; r_cap_id="NTUxOTNkM2JkZDg4NDQ4ODlhZmNkMmQxNGI5MjVhMzY=|1500448867|73a8c0d29a7d466f339e9dc3f5107be2e593b921"; cap_id="ZWI3NDUzZTkzNjQ1NDc0NWFkY2Q5ZjliNmExZmMyZWQ=|1500448867|f4eba8cc225482cf6e03359a35eaecfe68bec032"; z_c0=Mi4wQUFBQVZKOGpBQUFBTUFMOHdsejRDaGNBQUFCaEFsVk5vWldXV1FCc3lqb2huMmhLM01ZUTQxRnRPMWJkODQ0YzJ3|1500448929|4db031e62bac6db8b7f76df5bc8cd79db3d99c41; q_c1=eb629a1deb0d469ea653ebad3d22c244|1500530546000|1489651714000; aliyungf_tc=AQAAAJFHtFpB8Q0AcocyPeEtPtqHNZXB; __utma=155987696.1593604370.1492574559.1502683792.1502683792.1; __utmc=155987696; __utmz=155987696.1502683792.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _xsrf=9df349c6-d15d-43e7-9bb3-266e68f37af3'

for line in raw_cookies.split(':'):
    key,value = line.split('=', 1)
    cookies[key] = value

def download_page(url):
    return requests.get(url,cookies=cookies, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }, timeout=120).json()

def beginSpider(DOWNLOAD_User, pageNum):
    print("抓取用户 "+ DOWNLOAD_User + " ，页码 "+ str(pageNum))

    try:
        json = download_page(DOWNLOAD_URL.replace('{DOWNLOAD_User}',DOWNLOAD_User).replace('{offset}',str(pageNum * 20)))
    except:
        print("抓取异常：" + DOWNLOAD_URL.replace('{DOWNLOAD_User}',DOWNLOAD_User).replace('{offset}',str(pageNum * 20)))
        time.sleep(2) #延迟N秒再抓取
        json = download_page(DOWNLOAD_URL.replace('{DOWNLOAD_User}',DOWNLOAD_User).replace('{offset}',str(pageNum * 20)))

    #print(json)

    #print(json["paging"]["is_end"])

    if os.path.exists(DOWNLOAD_User) == False:
        os.makedirs(DOWNLOAD_User)

    for item in json["data"]:
        if(item["avatar_url_template"] == None):
            continue

        image_name = item["url_token"]
        sql = "select count(id) column_0 from Space0017A where column_0='" + image_name + "' " 
        isRepeat = ms.ExecQuery(sql.encode('utf-8'))
        if isRepeat[0][0] != 0:
            continue

        #"name" 名称
        #"headline" 一句话简介
        # url https://www.zhihu.com/people/+ item["url_token"] + /activities
        image_url = item["avatar_url_template"].replace('{size}','xl')

        img_localhost = DOWNLOAD_User + '\\' + image_name + '.jpg'
        
        sql = "select count(id) column_0 from Space0017A where column_0='" + image_name + "' " 
        isRepeat = ms.ExecQuery(sql.encode('utf-8'))
        if isRepeat[0][0] != 0:
            sql = "insert into Space0017A values ('%s','%s','%s','%s','%s') " %(image_name,'https://www.zhihu.com/people/'+image_name+'/following',img_localhost,DOWNLOAD_User,'1')
        else:
            sql = "insert into Space0017A values ('%s','%s','%s','%s','%s') " %(image_name,'https://www.zhihu.com/people/'+image_name+'/following',img_localhost,DOWNLOAD_User,'0')

        ms.ExecNonQuery(sql.encode('utf-8'))


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
        return pageNum + 1
    return None

DOWNLOAD_URL = "https://www.zhihu.com/api/v4/members/{DOWNLOAD_User}/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset={offset}&limit=20"

#主程序
def main():

    now = datetime.datetime.now()
    print("开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

    DOWNLOAD_User = getSeed()

    if DOWNLOAD_User == -1:
        print("无待抓取序列，程序终止")
        return None

    pageNum = 0

    while pageNum != None:
        pageNum = beginSpider(DOWNLOAD_User, pageNum)

    updateUser(DOWNLOAD_User)

    now = datetime.datetime.now()
    print("结束时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

    time.sleep(30) #延迟N秒再抓取
    main()


main()