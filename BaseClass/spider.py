# coding:UTF-8

#encoding:UTF-8
import urllib.request
from bs4 import BeautifulSoup

url = 'http://www.douban.com/'
webPage = urllib.request.urlopen(url)

soup = BeautifulSoup(webPage,"html.parser")
print(soup.title)