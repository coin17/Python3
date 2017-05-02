#! /usr/bin/env python
#coding=utf-8
# 抓取卫星云图入库
    

import time, os 
import datetime
from MSSql_SqlHelp import MSSQL 

#MS Sql Server 链接字符串
ms = MSSQL(host=".",user="sa",pwd="sa",db="SmallIsBeautiful")

root = "E:\C_Code\learngit\Python3_Test\BaseClass\spider_demo02_www.nmc.cn"

def main():
    now = datetime.datetime.now()
    print(now.strftime('%H%M%S%f'))
    print("开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

    for rt,dirs,files in os.walk(root):
        for f in files:
            #使用find，如果没有找到子串，返回 -1
            #print(f.find('.jpg'))
            #使用index，如果没有找到子串，会直接抛出异常，substring not found
            #print(f.index('.jpg'))
            if f.find(".jpg") != -1:
                #print(os.path.join(rt,f)) #完整文件名
                #print(rt.split('\\')[-1]) #文件夹名
                folder = rt.split('\\')[-1]
                #print(f) #文件名
                image_name = f
                fileTime = image_name.replace(".jpg","")  # 20170502 13_00
                fileTime = time.strptime(fileTime,"%Y%m%d %H_%M") #time.struct_time(tm_year=2017, tm_mon=5, tm_mday=2, tm_hour=13, tm_min=0, tm_sec=0, tm_wday=1, tm_yday=122, tm_isdst=-1)
                fileTime = time.strftime('%Y-%m-%d %H:%M:%S',fileTime)
                #print(time.ctime(os.path.getmtime(os.path.join(rt,f)))) #修改时间
                #print(time.ctime(os.path.getctime(os.path.join(rt,f)))) #创建时间

                sql="select count(id) from Space0014A where column_0='%s' and column_1='%s' and column_2='%s' " %(folder,fileTime,image_name)
                isRepeat = ms.ExecQuery(sql.encode('utf-8'))
                if isRepeat[0][0] == 0:
                    sql = "insert into Space0014A values ('%s','%s','%s') " %(folder,fileTime,image_name)
                    ms.ExecNonQuery(sql.encode('utf-8'))

    now = datetime.datetime.now()
    print("结束时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

def re_exe(cmd, inc = 60): 
    while True: 
        os.system(cmd);
        main()
        time.sleep(inc) 

# N秒 执行一次
re_exe("echo %time%", 1800)

