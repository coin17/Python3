#! /usr/bin/env python
#coding=utf-8
# 抓取特定知乎用户关注对象，每次仅能抓取每页 HTML 前三条
    
import time, os #定时抓取
import requests 
from bs4 import BeautifulSoup
import datetime #精确时间

def beginSpider(pageNum):
    print(str(pageNum))
    try:
        html = download_page(DOWNLOAD_URL + str(pageNum))
    except:
        print("抓取异常：" + DOWNLOAD_URL + str(pageNum))
        time.sleep(2) #延迟N秒再抓取
        html = download_page(DOWNLOAD_URL + str(pageNum))

    soup = BeautifulSoup(html, "html.parser")
    list_soup = soup.find(id = 'Profile-following')
    #print(list_soup)

    if os.path.exists(DOWNLOAD_User) == False:
        os.makedirs(DOWNLOAD_User)

    for item in list_soup.find_all('div', class_='List-item'):
        #print(item.find('a', class_='UserLink-link'))
        if(item.find('a', class_='UserLink-link') == None):
            continue

        image_name = item.find('a', class_='UserLink-link')["href"].replace('/','_')
        image_url = item.find('img', class_='Avatar Avatar--large UserLink-avatar')["srcset"][0:-3]
        #只能取到前三条数据
        #print(image_name.replace('/','_') + "："+image_url)

        img_localhost = DOWNLOAD_User + '\\' + image_name + '.jpg'

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
    if list_soup.find_all('button')[-1].text == "下一页":
        beginSpider(pageNum + 1)


def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }, timeout=120).content


#下载URL   DOWNLOAD_URL + number
#轮子哥
#DOWNLOAD_URL = "https://www.zhihu.com/people/excited-vczh/following?page="
#DOWNLOAD_User = "excited-vczh"
#跳舞
DOWNLOAD_URL = "https://www.zhihu.com/people/chen-bin-99-5-4/following?page="
DOWNLOAD_User = "chen-bin-99-5-4"

def main():
    print("开始时间：" +  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  

    beginSpider(1)

    print("结束时间：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  


main()
