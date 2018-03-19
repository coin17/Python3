#!/usr/bin/env python
# encoding=utf-8

"""
爬取大同市环境空气质量实时发布系统
"""

import requests #数据抓取
from bs4 import BeautifulSoup #抓取内容解析
import re
import time, os 
import datetime
from MSSql_SqlHelp import MSSQL 
import random


def download_page(url):

    try:
        response = requests.get("http://183.203.132.90:85/shishi/index.asp")
        cookies = response.cookies.get_dict()

        return requests.get(url, cookies=cookies, headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            "Referer": url,
            "Host": "183.203.132.90:85",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
            }, timeout=120).content
    except Exception as e:
        print("抓取异常：" + url)
        time.sleep(30) #延迟N秒再抓取
        main()



#站点列表
point_list = [['','0','大同市','0'],['%B9%FB%CA%F7%B3%A1','5','果树场','1'],['%D4%C6%B8%D4%B1%F6%B9%DD','83','云冈宾馆','2'],['%B4%F3%CD%AC%B4%F3%D1%A7','86','大同大学','3'],['%B0%B2%BC%D2%D0%A1%B4%E5','87','安家小村','4'],['%BD%CC%D3%FD%D1%A7%D4%BA','88','教育学院','5'],['%B9%A9%C5%C5%CB%AE%B9%AB%CB%BE','89','供排水公司','6']]
#污染物列表
pollutant_list = ['no2','so2','pm10','pm25','co','o3']

#小时URL
DOWNLOAD_Hour_URL = 'http://183.203.132.90:85/shishi/line.asp?dwname={DOWNLOAD_dwname}&newtime={DOWNLOAD_newtime}&zhibiao={DOWNLOAD_zhibiao}'
DOWNLOAD_Hour_URL_AQI = 'http://183.203.132.90:85/shishi/chengqulist.asp?dwcode={DOWNLOAD_dwcode}&dwname={DOWNLOAD_dwname}&xiabiao={DOWNLOAD_xiabiao}&newtime={DOWNLOAD_newtime}'
DOWNLOAD_Hour_URL_AQI_City = 'http://183.203.132.90:85/shishi/chengqulist.asp?newtime={DOWNLOAD_newtime}'
DOWNLOAD_Day_URL_AQI = 'http://183.203.132.90:85/ribao/line.asp?dwname={DOWNLOAD_dwname}&newtime={DOWNLOAD_newtime}'

# 24小时空气质量（分因子）数据页面解析
def parse_html_hour_value(html):
    soup = BeautifulSoup(html, "html.parser")
    pattern = "<set value='(\d+|\d+\.\d+)' />"  
    value = re.findall(pattern,str(soup))  
    return value

def parse_html_hour_aqi(html):
    soup = BeautifulSoup(html, "html.parser")
    #print(soup)
    aqi = soup.find('td', attrs={'height':'50','colspan': '2'})
    aqiinfo = soup.findAll('td', attrs={'align':'left','valign': 'top'})

    if aqi != None:
        aqi = aqi.getText().strip()
        if aqi != '/' and len(aqiinfo) == 5:
            return aqi,aqiinfo[0].getText().strip(),aqiinfo[2].getText().strip()
        elif aqi != '/' and len(aqiinfo) == 6:
            return aqi,aqiinfo[1].getText().strip(),aqiinfo[3].getText().strip()
    return "", "", ""

def parse_html_day_value(html):
    soup = BeautifulSoup(html, "html.parser")
    pattern = "<set name='(.*?)' color='(.*?)' value='(\d+|\d+\.\d+)'/>"  
    value = re.findall(pattern,str(soup))  
    return value

def start_hour(queryTime):
    
    time = queryTime.strftime('%Y/%m/%d %H:00:00')

    for point in point_list:
        time_yesterday = queryTime - datetime.timedelta(hours=24)

        for pollutant in pollutant_list:
            html_hour_value = download_page(DOWNLOAD_Hour_URL.replace('{DOWNLOAD_dwname}',point[0]).replace('{DOWNLOAD_newtime}',time).replace('{DOWNLOAD_zhibiao}',pollutant))
            hour_value_list = parse_html_hour_value(html_hour_value)

            for i, value in enumerate(hour_value_list):
                c_time = time_yesterday + datetime.timedelta(hours=(1+int(i)))
                if point[2] == '大同市':
                    sql = "select count(PK_ID) from T_EnvQuality_AirCityHourData where MonitorTime='%s' " %(c_time.strftime('%Y/%m/%d %H:00:00'))
                    isRepeat = ms.ExecQuery(sql.encode('utf-8'))
                    if isRepeat[0][0] == 0 and value != '0' and value != '':
                        sql = "insert into T_EnvQuality_AirCityHourData (MonitorTime,FK_RegionCode,%s) values ('%s','140200','%s') " %(pollutant,c_time.strftime('%Y/%m/%d %H:00:00'), value)
                        ms.ExecNonQuery(sql.encode('utf-8'))
                        #print("插入城市小时数据，时间：" + c_time.strftime('%Y/%m/%d %H:00:00') + " 站点：" + point[2] + " 因子：" + pollutant + " 值：" + value)
                    elif value != '0' and value != '':
                        sql = "update T_EnvQuality_AirCityHourData set %s = '%s' where MonitorTime='%s' " %(pollutant,value,c_time.strftime('%Y/%m/%d %H:00:00'))
                        ms.ExecNonQuery(sql.encode('utf-8'))
                        #print("更新城市小时数据，时间：" + c_time.strftime('%Y/%m/%d %H:00:00') + " 站点：" + point[2] + " 因子：" + pollutant + " 值：" + value)
                else:
                    sql = "select count(PK_ID) from T_EnvQuality_AirStationHourData where MonitorTime='%s' and FK_AirID='%s' " %(c_time.strftime('%Y/%m/%d %H:00:00'),point[3])
                    isRepeat = ms.ExecQuery(sql.encode('utf-8'))
                    if isRepeat[0][0] == 0 and value != '0' and value != '':
                        sql = "insert into T_EnvQuality_AirStationHourData (MonitorTime,FK_RegionCode,%s,FK_AirID,FK_StationCode) values ('%s','140200','%s','%s','%s') " %(pollutant,c_time.strftime('%Y/%m/%d %H:00:00'), value, point[3], point[1])
                        ms.ExecNonQuery(sql.encode('utf-8'))
                        #print("插入站点小时数据，时间：" + c_time.strftime('%Y/%m/%d %H:00:00') + " 站点：" + point[2] + " 因子：" + pollutant + " 值：" + value)
                    elif value != '0' and value != '':
                        sql = "update T_EnvQuality_AirStationHourData set %s = '%s' where MonitorTime='%s' and FK_AirID='%s' " %(pollutant,value,c_time.strftime('%Y/%m/%d %H:00:00'),point[3])
                        ms.ExecNonQuery(sql.encode('utf-8'))
                        #print("更新站点小时数据，时间：" + c_time.strftime('%Y/%m/%d %H:00:00') + " 站点：" + point[2] + " 因子：" + pollutant + " 值：" + value)

        #获取最近 1 小时 AQI
        for x in range(1):
            c_time = queryTime#time_yesterday + datetime.timedelta(hours=(21+int(x)))
            if point[1] == '0':
                html_hour_aqi = download_page(DOWNLOAD_Hour_URL_AQI_City.replace('{DOWNLOAD_newtime}',c_time.strftime('%Y/%m/%d %H:00:00')))
            else:
                html_hour_aqi = download_page(DOWNLOAD_Hour_URL_AQI.replace('{DOWNLOAD_dwname}',point[0]).replace('{DOWNLOAD_newtime}',c_time.strftime('%Y/%m/%d %H:00:00')).replace('{DOWNLOAD_dwcode}',point[1]).replace('{DOWNLOAD_xiabiao}',point[3]))
            #print(html_hour_aqi)

            hour_aqi,hour_type,hour_pollute = parse_html_hour_aqi(html_hour_aqi)

            print("时间：" + c_time.strftime('%Y/%m/%d %H:00:00') + " 站点：" + point[2] + " AQI：" + hour_aqi+" 指数类别："+hour_type+" 首要污染物："+hour_pollute)
            if point[2] == '大同市':
                sql = "select count(PK_ID) from T_EnvQuality_AirCityHourData where MonitorTime='%s' " %(c_time.strftime('%Y/%m/%d %H:00:00'))
                isRepeat = ms.ExecQuery(sql.encode('utf-8'))
                
                if isRepeat[0][0] == 0 and hour_aqi != '0' and hour_aqi != '':
                    sql = "insert into T_EnvQuality_AirCityHourData (MonitorTime,FK_RegionCode,aqi,Quality,PrimaryPollutant) values ('%s','140200','%s') " %(c_time.strftime('%Y/%m/%d %H:00:00'), hour_aqi,hour_type,hour_pollute)
                    ms.ExecNonQuery(sql.encode('utf-8'))
                    #print("插入城市小时数据，时间：" + c_time.strftime('%Y/%m/%d %H:00:00') + " 站点：" + point[2] + " AQI：" + hour_aqi)
                elif hour_aqi != '0' and hour_aqi != '':
                    sql = "update T_EnvQuality_AirCityHourData set aqi = '%s', Quality = '%s' , PrimaryPollutant = '%s' where MonitorTime='%s' " %(hour_aqi,hour_type,hour_pollute,c_time.strftime('%Y/%m/%d %H:00:00'))
                    ms.ExecNonQuery(sql.encode('utf-8'))
                    #print("更新城市小时数据，时间：" + c_time.strftime('%Y/%m/%d %H:00:00') + " 站点：" + point[2] + " AQI：" + hour_aqi)
            else:
                sql = "select count(PK_ID) from T_EnvQuality_AirStationHourData where MonitorTime='%s' and FK_AirID='%s' " %(c_time.strftime('%Y/%m/%d %H:00:00'),point[3])
                isRepeat = ms.ExecQuery(sql.encode('utf-8'))
                if isRepeat[0][0] == 0 and hour_aqi != '0' and hour_aqi != '':

                    sql = "insert into T_EnvQuality_AirStationHourData (MonitorTime,FK_RegionCode,aqi,Quality,PrimaryPollutant,FK_AirID,FK_StationCode) values ('%s','140200','%s','%s','%s','%s','%s') " %(c_time.strftime('%Y/%m/%d %H:00:00'), hour_aqi,hour_type,hour_pollute, point[3], point[1])
                    ms.ExecNonQuery(sql.encode('utf-8'))
                    #print("插入站点小时数据，时间：" + c_time.strftime('%Y/%m/%d %H:00:00') + " 站点：" + point[2] + " 因子：AQI 值：" + hour_aqi)
                elif hour_aqi != '0' and hour_aqi != '':
                    sql = "update T_EnvQuality_AirStationHourData set aqi = '%s' , Quality = '%s' , PrimaryPollutant = '%s' where MonitorTime='%s' and FK_AirID='%s' " %(hour_aqi,hour_type,hour_pollute,c_time.strftime('%Y/%m/%d %H:00:00'),point[3])
                    #print(sql)
                    ms.ExecNonQuery(sql.encode('utf-8'))
                    #print("更新站点小时数据，时间：" + c_time.strftime('%Y/%m/%d %H:00:00') + " 站点：" + point[2] + " 因子：AQI 值：" + hour_aqi)


def start_day(queryTime):
    time = queryTime.strftime('%Y/%m/%d')

    for point in point_list:
        time_yesterday = queryTime - datetime.timedelta(hours=240)

        html_day_aqi = download_page(DOWNLOAD_Day_URL_AQI.replace('{DOWNLOAD_dwname}',point[0]).replace('{DOWNLOAD_newtime}',time))
        day_aqi = parse_html_day_value(html_day_aqi)  

        for i, value in enumerate(day_aqi):
            c_time = time_yesterday + datetime.timedelta(hours=(1+int(i))*24)

            if point[2] == '大同市':
                sql = "select count(PK_ID) from T_EnvQuality_AirCityDayData where MonitorTime='%s' " %(c_time.strftime('%Y/%m/%d'))
                isRepeat = ms.ExecQuery(sql.encode('utf-8'))
                if isRepeat[0][0] == 0 and value[2] != '0':
                    sql = "insert into T_EnvQuality_AirCityDayData (MonitorTime,FK_RegionCode,AQI) values ('%s','140200','%s') " %(c_time.strftime('%Y/%m/%d'), value[2])
                    ms.ExecNonQuery(sql.encode('utf-8'))
                    #print("城市AQI日数据插入成功，时间：" + c_time.strftime('%Y/%m/%d') + " 站点：" + point[2] + " AQI：" + value[2])
            else:
                sql = "select count(PK_ID) from T_EnvQuality_AirStationDayData where MonitorTime='%s' and FK_AirID='%s' " %(c_time.strftime('%Y/%m/%d'), point[3])
                isRepeat = ms.ExecQuery(sql.encode('utf-8'))
                if isRepeat[0][0] == 0 and value[2] != '0':
                    sql = "insert into T_EnvQuality_AirStationDayData (MonitorTime,FK_RegionCode,AQI,FK_AirID,FK_StationCode) values ('%s','140200','%s','%s','%s') " %(c_time.strftime('%Y/%m/%d'), value[2], point[3], point[1])
                    ms.ExecNonQuery(sql.encode('utf-8'))
                    #print("站点AQI日数据插入成功，时间：" + c_time.strftime('%Y/%m/%d') + " 站点：" + point[2] + " AQI：" + value[2])
            


#MS Sql Server 链接字符串
ms = MSSQL(host="172.16.12.20",user="sa",pwd="sa",db="DB_DC_DaTongV1")


#主程序
def main():

    now = datetime.datetime.now()
    print("开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

    try:
        start_hour(now)
        start_day(now)
    except Exception as e:
        print("出现异常")
    

    now = datetime.datetime.now()
    print("结束时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

    time.sleep(60 * 10) #延迟N秒再抓取
    main()


main()