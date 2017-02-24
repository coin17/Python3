# coding:UTF-8

#encoding:UTF-8
import urllib.request
from bs4 import BeautifulSoup

url = 'http://www.douban.com/'
webPage=urllib.request.urlopen(url)
data = webPage.read()
data = data.decode('UTF-8')

soup = BeautifulSoup(data,"html.parser")
print(soup.title)