# coding:UTF-8

#encoding:UTF-8
import requests
from bs4 import BeautifulSoup

url = 'https://www.douban.com/'
webPage = requests.get(url).text
soup = BeautifulSoup(webPage,"html.parser")
print(soup.title)


test = "http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/1.png"
print(test.split("/")[-1])