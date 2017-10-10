#! /usr/bin/env python
#coding=utf-8
# 定时抓取城市 aqi 数据
# http://www.pm25.in
    
import json
import time, os 
import requests
import datetime
from MSSql_SqlHelp import MSSQL 
import pymongo
# 数据备份至 mongo，需先安装 pymongo
# pip install pymongo

def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }, timeout=120)

def parse_html_aqi(dis_aqi):
    print(len(dis_aqi))
    for index,x in enumerate(dis_aqi):
        
        area = x["area"]
        position_name = x["position_name"]
        station_code = x["station_code"]
        time_point = x["time_point"]
        sql = "select count(id) from Space0012A where column_1='%s' and column_14='%s' and column_19='%s' and column_20='%s' " %(area,position_name,station_code,time_point)
        isRepeat = ms.ExecQuery(sql.encode('utf-8'))

        if isRepeat[0][0] == 0:
            aqi = x["aqi"]
            co = x["co"]
            co_24h = x["co_24h"]
            no2 = x["no2"]
            no2_24h = x["no2_24h"]
            o3 = x["o3"]
            o3_24h = x["o3_24h"]
            o3_8h = x["o3_8h"]
            o3_8h_24h = x["o3_8h_24h"]
            pm10 = x["pm10"]
            pm10_24h = x["pm10_24h"]
            pm2_5 = x["pm2_5"]
            pm2_5_24h = x["pm2_5_24h"]
            primary_pollutant = x["primary_pollutant"]
            quality = x["quality"]
            so2 = x["so2"]
            so2_24h = x["so2_24h"]
            sql = "insert into Space0012A values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " %(aqi,area,co,co_24h,no2,no2_24h,o3,o3_24h,o3_8h,o3_8h_24h,pm10,pm10_24h,pm2_5,pm2_5_24h,position_name,primary_pollutant,quality,so2,so2_24h,station_code,time_point)
            ms.ExecNonQuery(sql.encode('utf-8'))
            # mongodb 数据备份
            db.NationalControlAQI.insert_one(x).inserted_id

        print("完成解析数据index为："+str(index))


#MS Sql Server 链接字符串
ms = MSSQL(host="172.16.12.35",user="sa",pwd="sa",db="SmallIsBeautiful_2017-03-15")

#MongoDB 数据库链接
client  = pymongo.MongoClient('172.16.21.232', 27017)
db = client.OriginalData

#每个 token 每小时最多调用 5 次
token = ['7rMwJqMxrmuDRFsAxBqP','5j1znBVAsnSf5xQyNQyq','K6LgqdJKZP2R9Svedskd']

def main():
    now = datetime.datetime.now()
    print("开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  
    dist_aqi = download_page("http://pm25.in/api/querys/all_cities.json?token=K6LgqdJKZP2R9Svedskd").json()
    if type(dist_aqi) == dict:
        print(dist_aqi["error"])
    else:
        parse_html_aqi(dist_aqi)


    now = datetime.datetime.now()
    print("结束时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  


def re_exe(cmd, inc = 60): 
    while True: 
        os.system(cmd);
        print("PM25.in 抓取_Start")
        main()
        print('PM25.in 抓取_End')
        time.sleep(inc) 

# N秒 执行一次
re_exe("echo %time%", 60 * 10)

