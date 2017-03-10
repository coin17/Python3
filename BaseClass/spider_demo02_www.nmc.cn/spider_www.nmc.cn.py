#! /usr/bin/env python
#coding=utf-8
# 定时抓取全国预报图片 
    
import time, os #定时抓取
import requests 
from bs4 import BeautifulSoup
import datetime #精确时间

def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }).content

def parse_html(html, folder):
    soup = BeautifulSoup(html, "html.parser")
    list_soup = soup.find('ul', attrs={'id': 'mycarousel'})

    if os.path.exists(folder) == False:
    	os.makedirs(folder)
   
    for image_li in list_soup.find_all('li'):
        image_name = image_li.find('p', attrs={'class': 'time'}).getText().replace(':','_')
        img_small = image_li.find('p', attrs={'class': 'img'}).find('img')["data-original"]	#小图
        img_big = img_small.replace('small/','')

        img_localhost = folder + '\\' + image_name + '.jpg'
        #如果文件不存在，且大小不为 0 字节，开始下载另存
        if os.path.isfile(img_localhost) == False or os.path.getsize(img_localhost) == 0:
        	try:
	            img_req = requests.get(img_big, timeout=20)
	            with open(img_localhost, 'wb') as f:
	            	f.write(img_req.content)

	        except:
	        	now = datetime.datetime.now()
	        	with open("error.log", 'w') as f:
	        		f.write(now.strftime('%Y-%m-%d %H:%M:%S') + ' 【错误】当前图片无法下载，失效地址为：' + img_big)

        # 	print('【下载】下载成功，下载地址为' + img_big)
        # else:
        # 	print('【重复】图片已存在，下载地址为' + img_big)

#下载清单
DOWNLOAD_URL = [("能见度","seaplatform1","http://www.nmc.cn/publish/sea/seaplatform1.html"),("风","hourly-winds","http://www.nmc.cn/publish/observations/hourly-winds.html"),("气温","hourly-temperature","http://www.nmc.cn/publish/observations/hourly-temperature.html"),("小时降雨量","hourly-precipitation","http://www.nmc.cn/publish/observations/hourly-precipitation.html"),("卫星云图","fy2", "http://www.nmc.cn/publish/satellite/fy2.htm")]


def main():
	now = datetime.datetime.now()
	print("开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

	for title, folder, url in DOWNLOAD_URL:
		#print(title, folder, url)
		html = download_page(url)
		parse_html(html, folder)

	now = datetime.datetime.now()
	print("结束时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  


def re_exe(cmd, inc = 60): 
    while True: 
        os.system(cmd);
        main()
        time.sleep(inc) 

# N秒 执行一次
re_exe("echo %time%", 1800)
