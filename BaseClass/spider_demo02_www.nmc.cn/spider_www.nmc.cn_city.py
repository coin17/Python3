#! /usr/bin/env python
#coding=utf-8
# 定时抓取城市气象预报数据 
    
import json
import time, os 
import requests
import datetime
from MSSql_SqlHelp import MSSQL 

def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    })

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


#MS Sql Server 链接字符串
ms = MSSQL(host=".",user="sa",pwd="sa",db="SmallIsBeautiful")

def main():
    now = datetime.datetime.now()
    print(now.strftime('%H%M%S%f'))
    print("开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

    json_provices = download_page("http://www.nmc.cn/f/rest/province").json()
    for json_provice in json_provices:
        json_citys = download_page("http://www.nmc.cn/f/rest/province/" + json_provice["code"]).json()
        for json_city in json_citys:
            json_weather = download_page("http://www.nmc.cn/f/rest/real/" + json_city["code"] + "?_=" + now.strftime('%H%M%S%f')).json()
            json_aqi = download_page("http://www.nmc.cn/f/rest/aqi/" + json_city["code"] + "?_=" + now.strftime('%H%M%S%f')).json()
            parse_html_weather_aqi(json_weather,json_aqi)
            time.sleep(2) #延迟 N 秒，进行第二次抓取 
            #print(json_city["city"]+json_city["code"])
    now = datetime.datetime.now()
    print("结束时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

main()

