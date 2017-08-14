#! /usr/bin/env python
#coding=utf-8

#中国气象局气象数据中心调用的key
#KEY：03A179AA86F8A5E120B45F20CE450D5C
#单位实名认证，一天可以调用50次
#http://api.data.cma.cn/api?key=03A179AA86F8A5E120B45F20CE450D5C&&data=SURF_CHN_HOR&timeRange=20170705030000&staIDs=53886,53890 

import json
import time, os 
import requests
import datetime
from MSSql_SqlHelp import MSSQL 

def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }, timeout=120)

def parse_weather(dist_weather):
    print(dist_weather["returnMsg"])
    print(len(dist_weather["DS"]))
    for x in dist_weather["DS"]:
        Station_Id_C = x["Station_Id_C"]
        Year = x["Year"]
        Mon = x["Mon"]
        Day = x["Day"]
        Hour = x["Hour"]
        sql = "select count(id) from Space0018A where column_0='%s' and column_1='%s' and column_2='%s' and column_3='%s' and column_4='%s' " %(Station_Id_C,Year,Mon,Day,Hour)
        isRepeat = ms.ExecQuery(sql.encode('utf-8'))
        print(isRepeat)
        if isRepeat[0][0] == 0:
            PRS = x["PRS"]
            PRS_Sea = x["PRS_Sea"]
            PRS_Max = x["PRS_Max"]
            PRS_Min = x["PRS_Min"]
            TEM = x["TEM"]
            TEM_Max = x["TEM_Max"]
            TEM_Min = x["TEM_Min"]
            RHU = x["RHU"]
            RHU_Min = x["RHU_Min"]
            VAP = x["VAP"]
            PRE_1h = x["PRE_1h"]
            WIN_D_INST_Max = x["WIN_D_INST_Max"]
            WIN_S_Max = x["WIN_S_Max"]
            WIN_D_S_Max = x["WIN_D_S_Max"]
            WIN_S_Avg_10mi = x["WIN_S_Avg_10mi"]
            WIN_D_Avg_10mi = x["WIN_D_Avg_10mi"]
            WIN_S_Inst_Max = x["WIN_S_Inst_Max"]
            sql = "insert into Space0018A values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " %(Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_Max,TEM_Min,RHU,RHU_Min,VAP,PRE_1h,WIN_D_INST_Max,WIN_S_Max,WIN_D_S_Max,WIN_S_Avg_10mi,WIN_D_Avg_10mi,WIN_S_Inst_Max)
            #print(sql)
            ms.ExecNonQuery(sql.encode('utf-8'))


#MS Sql Server 链接字符串
ms = MSSQL(host="172.16.12.35",user="sa",pwd="sa",db="SmallIsBeautiful_2017-03-15")

#邯郸地面站代码
pointCode = '53886,53890,53892,53893,53894,53895,53896,53897,53899,53980,53996'

def main():
    now = datetime.datetime.now()
    print("api.data.cma.cn 开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  
    try:
        url = "http://api.data.cma.cn/api?key=03A179AA86F8A5E120B45F20CE450D5C&&data=SURF_CHN_HOR&times="+(datetime.datetime.now() - datetime.timedelta(days = 1)).strftime('%Y%m%d%H')+"0000&staIDs="+pointCode
        print(url)
        dist_weather = download_page(url)
        print(dist_weather.json())

        parse_weather(dist_weather.json())

    except Exception as e:
        print(dist_weather.content)
        
    now = datetime.datetime.now()
    print("api.data.cma.cn 结束时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

def re_exe(cmd, inc = 60): 
    while True: 
        os.system(cmd);
        main()
        time.sleep(inc) 

# N秒 执行一次
re_exe("echo %time%", 3600)

main()
