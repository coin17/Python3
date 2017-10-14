#!/usr/bin/env python
# encoding=utf-8

"""
爬取真气网空气质量数据，页面直接解析
https://www.zq12369.com/index.php?city=北京&tab=city
"""

import requests #数据抓取
import time, os 
import datetime
from bs4 import BeautifulSoup
from MSSql_SqlHelp import MSSQL 
import pymongo

#所有城市列表
city_list = ["阿坝州","安康","阿克苏地区","阿里地区","阿拉善盟","阿勒泰地区","安庆","安顺","鞍山","克孜勒苏州","安阳","蚌埠","白城","保定","北海","北京","毕节","宝鸡","博州","保山","百色","白山","包头","本溪","白银","巴彦淖尔","亳州","巴中","滨州","长春","承德","成都","常德","昌都地区","赤峰","昌吉州","五家渠","重庆","常熟","长沙","楚雄州","朝阳","沧州","长治","常州","池州","潮州","滁州","崇左","郴州","丹东","东莞","德宏州","大连","大理州","大庆","大同","定西","大兴安岭地区","东营","德阳","黔南州","达州","德州","鄂尔多斯","恩施州","鄂州","防城港","佛山","抚顺","阜新","阜阳","富阳","福州","抚州","广安","贵港","桂林","果洛州","甘南州","贵阳","广元","固原","赣州","甘孜州","广州","淮安","淮北","海北州","鹤壁","河池","海东地区","邯郸","哈尔滨","合肥","黄冈","鹤岗","黑河","红河州","怀化","呼和浩特","海口","呼伦贝尔","葫芦岛","哈密地区","海门","海南州","黄南州","淮南","黄山","衡水","黄石","和田地区","海西州","河源","衡阳","杭州","汉中","菏泽","湖州","贺州","惠州","吉安","晋城","金昌","景德镇","金华","西双版纳州","九江","吉林","荆门","即墨","江门","佳木斯","济宁","胶南","济南","酒泉","句容","湘西州","金坛","鸡西","嘉兴","揭阳","江阴","嘉峪关","晋中","焦作","胶州","荆州","锦州","库尔勒","开封","黔东南州","克拉玛依","昆明","昆山","喀什地区","六安","临安","来宾","临沧","聊城","娄底","临汾","廊坊","漯河","丽江","吕梁","陇南","六盘水","拉萨","凉山州","丽水","乐山","莱芜","临夏州","莱西","辽阳","洛阳","辽源","龙岩","溧阳","临沂","连云港","莱州","泸州","林芝地区","兰州","柳州","马鞍山","牡丹江","茂名","眉山","绵阳","梅州","宁波","南昌","南充","宁德","南京","内江","怒江州","南宁","南平","那曲地区","南通","南阳","平度","平顶山","普洱","盘锦","平凉","蓬莱","莆田","萍乡","濮阳","攀枝花","青岛","秦皇岛","曲靖","齐齐哈尔","七台河","黔西南州","清远","庆阳","衢州","钦州","泉州","荣成","日喀则地区","乳山","日照","寿光","韶关","上海","绥化","石河子","石家庄","商洛","三明","三门峡","山南地区","遂宁","四平","宿迁","商丘","上饶","汕头","汕尾","绍兴","松原","沈阳","邵阳","十堰","三亚","双鸭山","苏州","朔州","随州","深圳","宿州","石嘴山","泰安","铜川","太仓","塔城地区","通化","天津","铁岭","通辽","铜陵","吐鲁番地区","铜仁地区","天水","唐山","太原","泰州","台州","文登","潍坊","瓦房店","武汉","芜湖","乌海","威海","吴江","乌兰察布","乌鲁木齐","渭南","文山州","武威","无锡","梧州","温州","吴忠","兴安盟","西安","宣城","许昌","襄阳","孝感","迪庆州","锡林郭勒盟","厦门","西宁","咸宁","湘潭","邢台","新乡","咸阳","信阳","新余","徐州","忻州","雅安","延安","宜宾","延边州","银川","伊春","运城","宜春","宜昌","盐城","云浮","阳江","营口","榆林","玉林","伊犁哈萨克州","阳泉","玉树州","鹰潭","烟台","义乌","宜兴","玉溪","岳阳","益阳","扬州","永州","淄博","自贡","珠海","诸暨","镇江","湛江","张家港","张家界","张家口","周口","驻马店","肇庆","章丘","舟山","中山","昭通","中卫","遵义","资阳","张掖","招远","郑州","枣庄","漳州","株洲"]
#测试城市列表
#city_list = ["博州"]

# 空气质量
url_temp = 'https://www.zq12369.com/index.php?city={tempCity}&tab=city'

def download_page(url):
    try:
        return requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
                }, timeout=120).content
    except Exception as e:
        print("download_page抓取异常：" + url)
        time.sleep(30) #延迟N秒再抓取
        main()

def start_spider(city):
    html = download_page(url_temp.replace('{tempCity}',city))
    soup = BeautifulSoup(html, "html.parser")

    weather = soup.find('div', class_='weather').getText().strip().splitlines()
    aqi = soup.find('div', class_='aqi').getText()
    aqirank = soup.find('div', class_='aqirank').getText()
    status = soup.find('div', class_='status').getText()
    statustip = soup.find('div', class_='statustip').getText().strip().splitlines()
    aqidetail = soup.find('div', class_='aqidetail').getText().strip().splitlines()
    # 按列赋值
    Time_Point = statustip[1].replace('年','-').replace('月','-').replace('日',' ').replace('时发布',':00:00')
    City_Name = city
    AQI = aqi
    AQI_Rank = aqirank
    Quality = status
    Primary_Pollutant = statustip[0].replace('首要污染物：','')
    PM2_5 = aqidetail[1]
    PM10 = aqidetail[5]
    SO2 = aqidetail[9]
    NO2 = aqidetail[13]
    CO = aqidetail[17]
    O3 = aqidetail[21]
    Weather = ''
    Temperature = ''
    Somatosensory_Temperature = ''
    Humidity = ''
    Wind_Direction = ''
    Wind_Speed = ''
    Visibility = ''
    for w in weather:
        if "体感" in w:
            Somatosensory_Temperature = w.split(' ')[1]
        elif "湿度" in w:
            Humidity =  w.split(' ')[1]
        elif "风" in w:
            Wind_Direction =  w.split(' ')[0]
            Wind_Speed =  w.split(' ')[1]
        elif "能见度" in w:
            Visibility =  w.split(' ')[1]
        elif "  " in w:
            Weather = w.split('  ')[0]
            Temperature = w.split('  ')[1]

    sql = "select count(id) from Space0023A where column_0='%s' and column_1='%s' " %(Time_Point,City_Name)
    isRepeat = ms.ExecQuery(sql.encode('utf-8'))

    if isRepeat[0][0] == 0:
        try:
            sql = "insert into Space0023A values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " %(Time_Point,City_Name,AQI,AQI_Rank,Quality,Primary_Pollutant,PM2_5,PM10,SO2,NO2,CO,O3,Weather,Temperature,Somatosensory_Temperature,Humidity,Wind_Direction,Wind_Speed,Visibility)
            ms.ExecNonQuery(sql.encode('utf-8'))
        except Exception as e:
            print("执行异常SQL：" + sql)



#MS Sql Server 链接字符串
ms = MSSQL(host="172.16.12.35",user="sa",pwd="sa",db="SmallIsBeautiful_2017-03-15")


#主程序
def main():
    now = datetime.datetime.now()
    print("spider_demo10_www.zq12369.com 开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

    for city in city_list:
        print(city)
        start_spider(city)

    now = datetime.datetime.now()
    print("spider_demo10_www.zq12369.com 结束时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  


def re_exe(cmd, inc = 60): 
    while True: 
        os.system(cmd);
        main()
        time.sleep(inc) 

# N秒 执行一次
re_exe("echo %time%", 60 * 10)