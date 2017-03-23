import json
import requests #数据抓取
from bs4 import BeautifulSoup #抓取内容解析
from MSSql_SqlHelp import MSSQL 
import datetime


DOWNLOAD_URL = 'http://datacenter.mep.gov.cn:8099/ths-report/report!list.action?xmlname=1462866483032'

# 页面下载
def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }).content

# 获得总页数
def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    print(soup.find('div', attrs = {'class': 'report_page'}))   
    #None

html = download_page(DOWNLOAD_URL)
allPageNum = parse_html(html)