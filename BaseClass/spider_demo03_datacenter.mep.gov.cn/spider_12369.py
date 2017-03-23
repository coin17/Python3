#!/usr/bin/env python
# encoding=utf-8

"""

爬取环保部 “12369” 数据
http://datacenter.mep.gov.cn/index!MenuAction.action?name=e3022e3d34274fdeabccd9ca8b17fef4
"""
import json
import requests #数据抓取
from bs4 import BeautifulSoup #抓取内容解析
from MSSql_SqlHelp import MSSQL 
import datetime


#DOWNLOAD_URL = 'http://datacenter.mep.gov.cn/index!MenuAction.action?name=e3022e3d34274fdeabccd9ca8b17fef4'

DOWNLOAD_URL ='http://datacenter.mep.gov.cn:8099/ths-report/report!list.action?xmlname=1462866483032'

# 页面下载
def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }).content

def download_page_post(url,pageNum):
    #flag = {'page.pageNo':pageNum,'page.orderBy':'','page.order':'','orderby':'','ordertype':'','xmlname':'1462866483032','gisDataJson':'','queryflag':'close','isdesignpatterns':'false','YEAR':'','MONTH':'','ENTE':'','inPageNo':3}
    formdata  = {'page.pageNo':pageNum}
    #json.dumps(flag)  #
    return requests.post(url,timeout=60, data=formdata, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'        
    }).content

# 获得总页数
def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    page = str(soup.find('div', attrs = {'class': 'report_page'}).findAll('a')[-1]) # 取出 “末页” 翻页，得到总页数
    allPageNum = page[page.index('(') + 1:page.index(')')]
    print("总页数：" + allPageNum)
    return allPageNum


# 页面解析
def parse_html_post(html):
    soup = BeautifulSoup(html, "html.parser")
    table_html = soup.find('table',attrs = {'class': 'report-table'})
    #print(table.find('td'))
    for i,tr in enumerate(table_html.find_all('tr')):
         # 不解析标题行
        if i != 0: 
            td = tr.find_all('td')
            column_0 = td[0].getText().strip()
            column_1 = td[1].getText().strip()
            column_2 = td[2].getText().strip()
            column_3 = td[3].getText().strip().replace(' ','').replace('\n','').replace('？','') #数据不规范，中间空格，包含？等
            column_4 = td[4].getText().strip()
            column_5 = td[5].getText().strip()
            column_6 = td[6].getText().strip()
            column_7 = td[7].getText().strip()
            #print(column_0 + "|"+column_1 + "|"+column_2 + "|"+column_3 + "|"+column_4 + "|"+column_5 + "|"+column_6 + "|"+column_7)

            sql = "insert into Space0011A values ('%s','%s','%s','%s','%s','%s','%s','%s')"  % (column_0,column_1,column_2,column_3,column_4,column_5,column_6,column_7)
            
            #sql = "insert into Space0011A values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(column_0,column_1,column_2,column_3,column_4,column_5,column_6,column_7)
            ms.ExecNonQuery(sql.encode('utf-8'))
    pass

#MS Sql Server 链接字符串
ms = MSSQL(host=".",user="sa",pwd="sa",db="SmallIsBeautiful")

def main():
    now = datetime.datetime.now()
    print("开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

    sql = "delete from Space0011A"  #清除历史数据
    ms.ExecNonQuery(sql.encode('utf-8'))
    html = download_page(DOWNLOAD_URL)
    allPageNum = parse_html(html)
    for num in range(int(allPageNum)):
        #print(num)
        try:
            html = download_page_post(DOWNLOAD_URL,num + 1)
            parse_html_post(html)
        except: #Exception as e:
            #raise e
            print('【异常】：请求超时，请求页码' + str(num + 1))
    print("ok!")
    print("结束时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  


if __name__ == '__main__':
    main()