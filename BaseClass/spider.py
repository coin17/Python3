#encoding:UTF-8

import requests
import json
from bs4 import BeautifulSoup

url = 'https://www.douban.com/'
webPage = requests.get(url).text
soup = BeautifulSoup(webPage,"html.parser")
print(soup.title)



cookies = {}

raw_cookies = 'UM_distinctid=15f4d106f2f190-07138b9823c296-c313760-100200-15f4d106f30402; CNZZDATA1254317176=1304846001-1508822353-https%253A%252F%252Fwww.zq12369.com%252F%7C1508822353; city=%E5%BC%A0%E5%AE%B6%E5%8F%A3'

for line in raw_cookies.split(':'):
    key,value = line.split('=', 1)
    cookies[key] = value

test2 = "https://www.zq12369.com/api/newzhenqiapi.php"
data = {'param': 'VAn1yHFAwh9OyizSIUiAmuy0XCTcDdTGkh5XJiNb3YdnczoPWG5/nmBJNHETGz1t+PVpzSvUHoSt5O1g4U3zSAolEuG/b1FLOFzVc/70JZpNgHZxgBElFUjPXB2DxFKPTMxZsbpWn7Zm1ru86jUJtvCmJztCV0EeM/5yBYtkbAGnI+yWduj+wBjfSj28SHIbteBORXUGUcqGP0+xAY40MBjYO/c3iGw/D4OLSCI1ZEkYiB0Iaomk7w03HGj8YhZu'}

jsonC = requests.post(test2, data=data,headers={
	'Host':'www.zq12369.com',
	'Origin':'https://www.zq12369.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }, timeout=120).text

print(jsonC)

