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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def download_page(url):
    return requests.get(url, headers={
        'content-type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }, timeout=120)

def parse_html_aqi(dis_aqi):
    print(len(dis_aqi))
    for x in dis_aqi:

        area = x["area"] if 'area' in x else ''
        position_name = x["position_name"] if 'position_name' in x else ''
        station_code = x["station_code"] if 'station_code' in x else ''
        time_point = x["time_point"] if 'time_point' in x else ''
        sql = "select count(id) from Space0012A where column_1='%s' and column_14='%s' and column_19='%s' and column_20='%s' " %(area,position_name,station_code,time_point)
        isRepeat = ms.ExecQuery(sql.encode('utf-8'))

        if isRepeat[0][0] == 0:
            aqi = x["aqi"] if 'aqi' in x else ''
            co = x["co"] if 'co' in x else ''
            co_24h = x["co_24h"] if 'co_24h' in x else ''
            no2 = x["no2"] if 'no2' in x else ''
            no2_24h = x["no2_24h"] if 'no2_24h' in x else ''
            o3 = x["o3"] if 'o3' in x else ''
            o3_24h = x["o3_24h"] if 'o3_24h' in x else ''
            o3_8h = x["o3_8h"] if 'o3_8h' in x else ''
            o3_8h_24h = x["o3_8h_24h"] if 'o3_8h_24h' in x else ''
            pm10 = x["pm10"] if 'pm10' in x else ''
            pm10_24h = x["pm10_24h"] if 'pm10_24h' in x else ''
            pm2_5 = x["pm2_5"] if 'pm2_5' in x else ''
            pm2_5_24h = x["pm2_5_24h"] if 'pm2_5_24h' in x else ''
            primary_pollutant = x["primary_pollutant"] if 'primary_pollutant' in x else ''
            quality = x["quality"] if 'quality' in x else ''
            so2 = x["so2"] if 'so2' in x else ''
            so2_24h = x["so2_24h"] if 'so2_24h' in x else ''
            sql = "insert into Space0012A values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " %(aqi,area,co,co_24h,no2,no2_24h,o3,o3_24h,o3_8h,o3_8h_24h,pm10,pm10_24h,pm2_5,pm2_5_24h,position_name,primary_pollutant,quality,so2,so2_24h,station_code,time_point)
            ms.ExecNonQuery(sql.encode('utf-8'))
            # mongodb 数据备份
            x["time_point"] = datetime.datetime.strptime(time_point,'%Y-%m-%dT%H:%M:%SZ')
            db.NationalControlAQI.insert_one(x).inserted_id

        print("完成解析数据："+area+"_"+position_name+"_"+time_point)


#MS Sql Server 链接字符串
ms = MSSQL(host="172.16.12.35",user="sa",pwd="sa",db="SmallIsBeautiful_2017-03-15")

#MongoDB 数据库链接
#client  = pymongo.MongoClient('172.16.21.232', 27017)
client  = pymongo.MongoClient('mongodb://172.16.12.155:30000,172.16.12.156:30000,172.16.12.157:30000')
db = client.OriginalData

#每个 token 每小时最多调用 5 次
token = ['7rMwJqMxrmuDRFsAxBqP','5j1znBVAsnSf5xQyNQyq','K6LgqdJKZP2R9Svedskd']

def main():
    now = datetime.datetime.now()
    print("开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  
    
    try:
        dist_aqi = download_page("http://www.pm25.in/api/querys/all_cities.json?token=5j1znBVAsnSf5xQyNQyq").json()
        if type(dist_aqi) == dict:
            print(dist_aqi["error"])
        else:
            parse_html_aqi(dist_aqi)
    except Exception as e:
        print(e)

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
re_exe("echo %time%", 60 * 30)

