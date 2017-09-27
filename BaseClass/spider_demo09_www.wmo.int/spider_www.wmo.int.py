#!/usr/bin/env python
# encoding=utf-8

"""
爬取全球空气监测站点列表
https://www.wmo.int/cpdb/volume_a_observing_stations/list_stations
"""

import requests #数据抓取
import time, os 
import datetime
from MSSql_SqlHelp import MSSQL 
import json

# 城市空气质量预报
url_temp = 'https://www.wmo.int/cpdb/volume_a_observing_stations/list_stations?sEcho=7&iColumns=6&sColumns=station_name%2Cstation_id%2Cindex_nbr%2Clatitude%2Clongitude%2Cobs_rems&iDisplayStart={iDisplayStart}&iDisplayLength=100&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&_={temp}'

cookies = {}

raw_cookies = '_ga=GA1.2.533883790.1505975474; _gid=GA1.2.1105338317.1505975474'

for line in raw_cookies.split(':'):
    key,value = line.split('=', 1)
    cookies[key] = value



def download_page(url):
    try:
        return requests.get(url, cookies=cookies,headers={
                'X-Requested-With':'XMLHttpRequest',
                'Accept':'application/json, text/javascript, */*; q=0.01',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
                }, timeout=120).json()
    except Exception as e:
        print("download_page抓取异常：" + url)
        time.sleep(30) #延迟N秒再抓取
        main()

def start_spider(pageNum):
    json = download_page(url_temp.replace('{temp}',str(time.time())).replace('{iDisplayStart}',str(pageNum * 100)))

    for x in json["aaData"]:
        station_name = x[0].replace("'", "''")
        station_id = x[1]
        index_nbr = x[2]
        latitude = x[3]
        longitude = x[4]
        obs_rems = x[5]

        sql = "select count(id) from Space0022A where column_1='%s' and column_2='%s' " %(station_id,index_nbr)
        isRepeat = ms.ExecQuery(sql.encode('utf-8'))

        if isRepeat[0][0] == 0:

            sql = "insert into Space0022A values ('%s','%s','%s','%s','%s','%s') " %(station_name,station_id,index_nbr,latitude,longitude,obs_rems)
            
            ms.ExecNonQuery(sql.encode('utf-8'))


#MS Sql Server 链接字符串
ms = MSSQL(host="172.16.12.35",user="sa",pwd="sa",db="SmallIsBeautiful_2017-03-15")


#主程序
def main():

    now = datetime.datetime.now()
    print("spider_demo08_www.wmo.int 开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

    for x in range(131):
        start_spider(x)

    now = datetime.datetime.now()
    print("spider_demo08_www.wmo.int 结束时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  



main()