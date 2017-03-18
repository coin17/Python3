#! /usr/bin/env python
#coding=utf-8
# 定时抓取城市气象预报数据———7天 
    

import time, os 
import requests
import datetime
from MSSql_SqlHelp import MSSQL 
from bs4 import BeautifulSoup

def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    })

icon_list = {}

def parse_html_forecast_code(html):
    soup = BeautifulSoup(html, "html.parser")
    #获取建立图标对应气象字典，因字典变化较少，抓取一次即可
    icon_list_soup = soup.find('div', attrs={'class': 'forecast'}).find_all('div',attrs={'class': 'day'})

    for icon in icon_list_soup:
        icon_key = icon.find('img')["src"].split("/")[-1]

        if (icon_key in icon_list) == False:
            icon_list[icon_key] = icon.find('div', attrs={'class': 'wdesc'}).getText().strip()

    print("气象代码字典：" + icon_list)

def parse_html_forecast(html):
    soup = BeautifulSoup(html, "html.parser")
    #发布城市
    publish_city = soup.find('div', attrs={'class': 'cname'}).getText().strip()
    #发布时间
    publish_time = soup.find('div', attrs={'class': 'btitle'}).find('span').getText().replace('发布于：','')

    print("抓取：" + publish_time + " " + publish_city)
    days_html = soup.find_all('div', attrs={'class':'hour3'})
    values_list = []
    
    for day_html in days_html:

        text = "" # imgurl 或 数值
        value1_list = []
        value2_list = []
        value3_list = []
        value4_list = []
        value5_list = []
        value6_list = []
        value7_list = []
        value8_list = []

        flag_date = int(day_html["id"].replace('day',''))
        forecast_date = datetime.datetime.strptime(publish_time,"%Y-%m-%d %H:%M").date() + datetime.timedelta(flag_date)
        #print(forecast_date)
        for i,row_table in enumerate(day_html.find_all('div', attrs={'class': 'row'})):
            is_new_day = False
            for j,column_table in enumerate(row_table.find_all('div')):
                if j != 0:
                    if i == 1:
                        text = column_table.find("img")["src"].split("/")[-1]
                    else:
                        text = column_table.getText().strip()

                    if i == 0:
                        if "日" in text:
                            text = str(forecast_date + datetime.timedelta(1)) +" "+ text.split('日')[1]
                            is_new_day = True
                        elif is_new_day:
                            text = str(forecast_date + datetime.timedelta(1)) + " " + text
                        else:
                            text = str(forecast_date) + " " + text

                    if j == 1:
                        value1_list.append(text)
                    elif j == 2:
                        value2_list.append(text)
                    elif j == 3:
                        value3_list.append(text)
                    elif j == 4:
                        value4_list.append(text)
                    elif j == 5:
                        value5_list.append(text)
                    elif j == 6:
                        value6_list.append(text)
                    elif j == 7:
                        value7_list.append(text)
                    elif j == 8:
                        value8_list.append(text)

        values_list.append(value1_list)
        values_list.append(value2_list)
        values_list.append(value3_list)
        values_list.append(value4_list)
        values_list.append(value5_list)
        values_list.append(value6_list)
        values_list.append(value7_list)
        values_list.append(value8_list)

    #print(values_list)

    for value in values_list:
        f_sj = value[0]
        f_tqxx = value[1]
        f_qw = value[2]
        f_js = value[3]
        f_fs = value[4]
        f_fx = value[5]
        f_qy = value[6]
        f_sd = value[7]
        f_yl = value[8]
        f_njd = value[9]

        sql="select count(id) from Space0009A where column_0='%s' and column_1='%s' and column_2='%s' " %(publish_city,publish_time,f_sj)
        isRepeat = ms.ExecQuery(sql.encode('utf-8'))
        if isRepeat[0][0] == 0:
            sql = "insert into Space0009A values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " %(publish_city,publish_time,f_sj,f_tqxx,f_qw,f_js,f_fs,f_fx,f_qy,f_sd,f_yl,f_njd)
            ms.ExecNonQuery(sql.encode('utf-8'))


#MS Sql Server 链接字符串
ms = MSSQL(host=".",user="sa",pwd="sa",db="SmallIsBeautiful")

def Test():
    html_forecast = download_page("http://www.nmc.cn/publish/forecast/AGD/shenzhen.html")
    html_forecast.encoding = "utf-8"
    parse_html_forecast(html_forecast.text)

def main():
    now = datetime.datetime.now()
    print(now.strftime('%H%M%S%f'))
    print("开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

    json_provices = download_page("http://www.nmc.cn/f/rest/province").json()
    for json_provice in json_provices:
        json_citys = download_page("http://www.nmc.cn/f/rest/province/" + json_provice["code"]).json()
        for json_city in json_citys:
            try:
                html_forecast = download_page("http://www.nmc.cn" + json_city["url"])
                html_forecast.encoding = "utf-8"
                parse_html_forecast_code(html_forecast.text) #初始化时运行一次 获取气象代码
                #parse_html_forecast(html_forecast.text)

            except Exception as e:
                #raise e
                print('【异常】：请求解析异常，city 代码 ' + json_city["code"])

    now = datetime.datetime.now()
    print("结束时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

def re_exe(cmd, inc = 60): 
    while True: 
        os.system(cmd);
        try:
            main()
        except:
            print("【崩溃】：因未知原因导致程序崩溃")
        #Test()
        print('ok')
        time.sleep(inc) 

# N秒 执行一次
re_exe("echo %time%", 1800)

