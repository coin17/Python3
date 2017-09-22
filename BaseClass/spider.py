# coding:UTF-8

#encoding:UTF-8
import requests
import json
from bs4 import BeautifulSoup

url = 'https://www.douban.com/'
webPage = requests.get(url).text
soup = BeautifulSoup(webPage,"html.parser")
print(soup.title)


test = "http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/1.png"
print(test.split("/")[-1])










cookies = {}

raw_cookies = '_ga=GA1.2.533883790.1505975474; _gid=GA1.2.1105338317.1505975474'

for line in raw_cookies.split(':'):
    key,value = line.split('=', 1)
    cookies[key] = value



test2 = "https://www.wmo.int/cpdb/volume_a_observing_stations/list_stations?sEcho=2&iColumns=6&sColumns=station_name,station_id,index_nbr,latitude,longitude,obs_rems&iDisplayStart=0&iDisplayLength=100&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&_=1506043558328"


jsonC = requests.get(test2, headers={
	# 'Host':'www.wmo.int',
	# 'Accept':'application/json, text/javascript, */*; q=0.01',
	# 'Accept-Encoding':'gzip, deflate, br',
	# 'Cache-Control':'no-cache',
	# 'Connection':'keep-alive',
	# 'DNT':'1',
	# 'Pragma':'no-cache',
	'X-Requested-With':'XMLHttpRequest',
	'Referer':'https://www.wmo.int/cpdb/volume_a_observing_stations/list_stations',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }, timeout=120).json()

print(jsonC)