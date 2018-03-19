#encoding:UTF-8

import requests
import execjs
import json
import time, os 
import datetime
from MSSql_SqlHelp import MSSQL 
import pymongo
# 数据备份至 mongo，需先安装 pymongo
# pip install pymongo

# 因数据缺失，不进行抓取入库操作

#所有城市列表
city_list = ["阿坝州","安康","阿克苏地区","阿里地区","阿拉善盟","阿勒泰地区","安庆","安顺","鞍山","克孜勒苏州","安阳","蚌埠","白城","保定","北海","北京","毕节","宝鸡","博州","保山","百色","白山","包头","本溪","白银","巴彦淖尔","亳州","巴中","滨州","长春","承德","成都","常德","昌都地区","赤峰","昌吉州","五家渠","重庆","常熟","长沙","楚雄州","朝阳","沧州","长治","常州","池州","潮州","滁州","崇左","郴州","丹东","东莞","德宏州","大连","大理州","大庆","大同","定西","大兴安岭地区","东营","德阳","黔南州","达州","德州","鄂尔多斯","恩施州","鄂州","防城港","佛山","抚顺","阜新","阜阳","富阳","福州","抚州","广安","贵港","桂林","果洛州","甘南州","贵阳","广元","固原","赣州","甘孜州","广州","淮安","淮北","海北州","鹤壁","河池","海东地区","邯郸","哈尔滨","合肥","黄冈","鹤岗","黑河","红河州","怀化","呼和浩特","海口","呼伦贝尔","葫芦岛","哈密地区","海门","海南州","黄南州","淮南","黄山","衡水","黄石","和田地区","海西州","河源","衡阳","杭州","汉中","菏泽","湖州","贺州","惠州","吉安","晋城","金昌","景德镇","金华","西双版纳州","九江","吉林","荆门","即墨","江门","佳木斯","济宁","胶南","济南","酒泉","句容","湘西州","金坛","鸡西","嘉兴","揭阳","江阴","嘉峪关","晋中","焦作","胶州","荆州","锦州","库尔勒","开封","黔东南州","克拉玛依","昆明","昆山","喀什地区","六安","临安","来宾","临沧","聊城","娄底","临汾","廊坊","漯河","丽江","吕梁","陇南","六盘水","拉萨","凉山州","丽水","乐山","莱芜","临夏州","莱西","辽阳","洛阳","辽源","龙岩","溧阳","临沂","连云港","莱州","泸州","林芝地区","兰州","柳州","马鞍山","牡丹江","茂名","眉山","绵阳","梅州","宁波","南昌","南充","宁德","南京","内江","怒江州","南宁","南平","那曲地区","南通","南阳","平度","平顶山","普洱","盘锦","平凉","蓬莱","莆田","萍乡","濮阳","攀枝花","青岛","秦皇岛","曲靖","齐齐哈尔","七台河","黔西南州","清远","庆阳","衢州","钦州","泉州","荣成","日喀则地区","乳山","日照","寿光","韶关","上海","绥化","石河子","石家庄","商洛","三明","三门峡","山南地区","遂宁","四平","宿迁","商丘","上饶","汕头","汕尾","绍兴","松原","沈阳","邵阳","十堰","三亚","双鸭山","苏州","朔州","随州","深圳","宿州","石嘴山","泰安","铜川","太仓","塔城地区","通化","天津","铁岭","通辽","铜陵","吐鲁番地区","铜仁地区","天水","唐山","太原","泰州","台州","文登","潍坊","瓦房店","武汉","芜湖","乌海","威海","吴江","乌兰察布","乌鲁木齐","渭南","文山州","武威","无锡","梧州","温州","吴忠","兴安盟","西安","宣城","许昌","襄阳","孝感","迪庆州","锡林郭勒盟","厦门","西宁","咸宁","湘潭","邢台","新乡","咸阳","信阳","新余","徐州","忻州","雅安","延安","宜宾","延边州","银川","伊春","运城","宜春","宜昌","盐城","云浮","阳江","营口","榆林","玉林","伊犁哈萨克州","阳泉","玉树州","鹰潭","烟台","义乌","宜兴","玉溪","岳阳","益阳","扬州","永州","淄博","自贡","珠海","诸暨","镇江","湛江","张家港","张家界","张家口","周口","驻马店","肇庆","章丘","舟山","中山","昭通","中卫","遵义","资阳","张掖","招远","郑州","枣庄","漳州","株洲"]
#city_list = ["北京"]
url = "https://www.zq12369.com/api/newzhenqiapi.php"

def get_js():  
    f = open("des_rsa.js", 'r', encoding='UTF-8')  
    line = f.readline()  
    htmlstr = ''  
    while line:  
        htmlstr = htmlstr + line  
        line = f.readline()  
    return htmlstr  

jsstr = get_js()


def start_spider(city):
    print("开始抓取：" + city)

    #月数据
    obj = {'city': city,'type': 'MONTH','startTime': (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d'),'endTime': (datetime.datetime.now()).strftime('%Y-%m-%d')}
    method = "CETCITYPERIOD"

    key = execjs.compile(jsstr).call("getParam", method, obj)  
    data = {'param': key}

    try:
        json_source = requests.post(url, data=data,headers={
        'Host':'www.zq12369.com',
        'Origin':'https://www.zq12369.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
        }, timeout=120).text
        json_source = execjs.compile(jsstr).call("decryptData", json_source)  
        json_source = execjs.compile(jsstr).call("b.decode", json_source) 
        json_source = json.loads(json_source)
        # 数据不全
        if json_source["result"]["success"] == True:
            print(json_source["result"]["data"]["total"])

        #analysis_json_Day(json_source,city)

        print("完成解析：" + city)
        time.sleep(2) #休息N秒
    except Exception as e:
        print("抓取异常：" + city)
        time.sleep(2) #休息N秒




#MS Sql Server 链接字符串
ms = MSSQL(host="172.16.12.35",user="sa",pwd="sa",db="SmallIsBeautiful_2017-03-15")

#MongoDB 数据库链接
client  = pymongo.MongoClient('172.16.21.232', 27017)
db = client.OriginalData

#主程序
def main():
    now = datetime.datetime.now()
    print("spider_demo10_www.zq12369.com 月数据 开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  

    jsstr = get_js() 

    for city in city_list:
        start_spider(city)

    now = datetime.datetime.now()
    print("spider_demo10_www.zq12369.com 月数据 结束时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  


def re_exe(cmd, inc = 60): 
    while True: 
        os.system(cmd);
        main()
        time.sleep(inc) 

# N秒 执行一次
re_exe("echo %time%", 60 * 60 * 3)

#main()