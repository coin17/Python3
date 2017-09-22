#!/usr/bin/env python
# encoding=utf-8

"""
爬取全国空气质量预报信息发布系统
http://106.37.208.228:8082/
"""

import requests #数据抓取
from bs4 import BeautifulSoup #抓取内容解析
import re
import time, os 
import datetime
from MSSql_SqlHelp import MSSQL 
import json

# 城市空气质量预报
url_city = 'http://106.37.208.228:8082/Home/Default'
# 省域空气质量形势预报
url_province = 'http://106.37.208.228:8082/ProvinceForecast/GetGlobalInfo'

def download_page(url):
    try:
        return requests.get(url).content
    except Exception as e:
        print("download_page抓取异常：" + url)
        time.sleep(30) #延迟N秒再抓取
        main()

def start_spider():
    # 城市空气质量数据
    webPage = download_page(url_city)
    soup = BeautifulSoup(webPage,"html.parser")
    PublicTime = soup.find('span', attrs={'class':'pull-right update-time'}).getText()
    # 城市空气数据发布时间
    #print(PublicTime)
    pattern = "\[\[\{.+\}\]\]"  
    value = re.findall(pattern,str(soup))  
    jsonCity = json.loads(value[0])

    for x in jsonCity[0]:
        CityCode = x["CityCode"]
        sql = "select count(id) from Space0020A where column_0='%s' and column_1='%s' " %(PublicTime,CityCode)
        isRepeat = ms.ExecQuery(sql.encode('utf-8'))

        if isRepeat[0][0] == 0:
            Name = x["Name"]
            Longitude = x["Longitude"]
            Latitude = x["Latitude"]
            AirIndex_From = x["AirIndex_From"]
            AirIndex_To = x["AirIndex_To"]
            PrimaryPollutant = x["PrimaryPollutant"]

            Air48Index_From = x["Air48Index_From"]
            Air48Index_To = x["Air48Index_To"]
            Primary48Pollutant = x["Primary48Pollutant"]

            IsPublish_72Hour = x["IsPublish_72Hour"]

            Air72Index_From = x["Air72Index_From"]
            Air72Index_To = x["Air72Index_To"]
            Primary72Pollutant = x["Primary72Pollutant"]

            DetailInfo = x["DetailInfo"]
            sql = "insert into Space0020A values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " %(PublicTime,CityCode,Name,Longitude,Latitude,AirIndex_From,AirIndex_To,PrimaryPollutant,Air48Index_From,Air48Index_To,Primary48Pollutant,IsPublish_72Hour,Air72Index_From,Air72Index_To,Primary72Pollutant,DetailInfo)
            #print(sql)
            ms.ExecNonQuery(sql.encode('utf-8'))

    # 省域空气质量形势预报
    webPage = download_page(url_province)
    soup = BeautifulSoup(webPage,"html.parser")
    jsonProvince = json.loads(str(soup))

    for x in jsonProvince:
        ptime = float(x["PublishDate"][6:-5])
        PublishDate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(ptime))
        ProvinceCode = x["ProvinceCode"]

        sql = "select count(id) from Space0021A where column_0='%s' and column_1='%s' " %(PublishDate,ProvinceCode)
        isRepeat = ms.ExecQuery(sql.encode('utf-8'))

        if isRepeat[0][0] == 0:
            ProvinceName = x["ProvinceName"]
            ForecastDescription = x["ForecastDescription"]
            OtherDescription = x["OtherDescription"]
            HealthTips = x["HealthTips"]
            WarningInfo = x["WarningInfo"]
            
            sql = "insert into Space0021A values ('%s','%s','%s','%s','%s','%s','%s') " %(PublishDate,ProvinceCode,ProvinceName,ForecastDescription,OtherDescription,HealthTips,WarningInfo)
            #print(sql)
            ms.ExecNonQuery(sql.encode('utf-8'))


#MS Sql Server 链接字符串
ms = MSSQL(host="172.16.12.35",user="sa",pwd="sa",db="SmallIsBeautiful_2017-03-15")


#主程序
def main():

    now = datetime.datetime.now()
    print("spider_demo08_106.37.208.228 开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

    start_spider()

    now = datetime.datetime.now()
    print("spider_demo08_106.37.208.228 结束时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

    time.sleep(60 * 10) #延迟N秒再抓取
    main()


main()