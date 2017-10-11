#! /usr/bin/env python
#coding=utf-8
# 定时抓取城市气象数据、aqi 
    
import json
import time, os 
import requests
import datetime
from MSSql_SqlHelp import MSSQL 
import pymongo
# 数据备份至 mongo，需先安装 pymongo
# pip install pymongo

def download_page(url):
    return requests.get(url,cookies=cookies,proxies=proxies,headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }, timeout=120)

def parse_html_weather_aqi(json,json_aqi):
    province = json["station"]["province"]
    city = json["station"]["city"]
    publish_time = json["publish_time"]
    sql="select count(id) from Space0007A where column_0='%s' and column_1='%s' and column_2='%s' " %(province,city,publish_time)
    isRepeat = ms.ExecQuery(sql.encode('utf-8'))
    if isRepeat[0][0] == 0:
        airpressure = json["weather"]["airpressure"]
        feelst = json["weather"]["feelst"]
        humidity = json["weather"]["humidity"]
        info = json["weather"]["info"]
        rain = json["weather"]["rain"]
        temperature = json["weather"]["temperature"]
        direct = json["wind"]["direct"]
        power = json["wind"]["power"]
        speed = json["wind"]["speed"]
        sql = "insert into Space0007A values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " %(province,city,publish_time,airpressure,feelst,humidity,info,rain,temperature,direct,power,speed)
        ms.ExecNonQuery(sql.encode('utf-8'))
        # mongodb 数据备份
        db.NationalControlWeather.insert_one(json).inserted_id

        print('【气象】：' + province + " " + city + " "+ publish_time)

    if 'forecasttime' in json_aqi.keys():
        forecasttime = json_aqi["forecasttime"]
        sql="select count(id) from Space0008A where column_0='%s' and column_1='%s' and column_2='%s' " %(province,city,forecasttime)
        isRepeat = ms.ExecQuery(sql.encode('utf-8'))
        if isRepeat[0][0] == 0:
            aq = json_aqi["aq"]
            aqi = json_aqi["aqi"]
            text = json_aqi["text"]
            sql = "insert into Space0008A values ('%s','%s','%s','%s','%s','%s') " %(province,city,forecasttime,aq,aqi,text)
            ms.ExecNonQuery(sql.encode('utf-8'))
            print('【AQI】：' + province + " " + city + " "+ forecasttime)

cookies = {}

raw_cookies = 'UM_distinctid=15b8f2f73e810e-0568aad45294d8-5d4e211f-232800-15b8f2f73e91da; UM_distinctid=15baed9d9bd446-082e358903e5e6-5d4e211f-232800-15baed9d9be4f9; followcity=54511%2C58367%2C59493%2C57516%2C58321%2C57679%2C58847; CNZZDATA1254743953=1454190746-1492752603-%7C1496822745; JSESSIONID=AE68987A917F5EB0ADFF073481F60470'

for line in raw_cookies.split(':'):
    key,value = line.split('=', 1)
    cookies[key] = value

proxies = {
    "https": "http://41.118.132.69:4433"
}

#MS Sql Server 链接字符串
ms = MSSQL(host="172.16.12.35",user="sa",pwd="sa",db="SmallIsBeautiful_2017-03-15")

#MongoDB 数据库链接
client  = pymongo.MongoClient('172.16.21.232', 27017)
db = client.OriginalData

def main():
    now = datetime.datetime.now()
    #print(now.strftime('%H%M%S%f'))
    print("开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

    json_provices = download_page("http://www.nmc.cn/f/rest/province").json()
    for json_provice in json_provices:
        json_citys = download_page("http://www.nmc.cn/f/rest/province/" + json_provice["code"]).json()
        for json_city in json_citys:
            try:
                json_weather = download_page("http://www.nmc.cn/f/rest/real/" + json_city["code"] + "?_=" + now.strftime('%H%M%S%f')).json()
                json_aqi = download_page("http://www.nmc.cn/f/rest/aqi/" + json_city["code"] + "?_=" + now.strftime('%H%M%S%f')).json()
                parse_html_weather_aqi(json_weather,json_aqi)
                time.sleep(1)
            except:
                print('【异常】：请求解析异常，city 代码 ' + json_city["code"])


            #time.sleep(1) #延迟 N 秒，进行第二次抓取 
            #print(json_city["city"]+json_city["code"])
    now = datetime.datetime.now()
    print("结束时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

def re_exe(cmd, inc = 60): 
    while True: 
        os.system(cmd);
        main()
        print('ok')
        time.sleep(inc) 

# N秒 执行一次
re_exe("echo %time%", 60 * 10)

