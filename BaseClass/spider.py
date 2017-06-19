# coding:UTF-8

#encoding:UTF-8
import requests
import json
from bs4 import BeautifulSoup

url = 'https://www.douban.com/'
webPage = requests.get(url).text
soup = BeautifulSoup(webPage,"html.parser")
print(soup.title)


test = "http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/1.png"
print(test.split("/")[-1])

test2 = "https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=0&limit=20"

jsonC = requests.get(test2, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }, timeout=120).json()

print(jsonC)