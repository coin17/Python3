from __future__ import unicode_literals
from threading import Timer
from wxpy import *
import requests
from MSSql_SqlHelp import MSSQL 
import datetime
import time, os 

bot = Bot()

# linux执行登陆请调用下面的这句
#bot = Bot(console_qr=2,cache_path="botoo.pkl")

#MS Sql Server 链接字符串
ms = MSSQL(host="172.16.12.35",user="sa",pwd="sa",db="SmallIsBeautiful_2017-03-15")

def get_messages(city):
    
    #获取最新空气质量数据，天气数据
    sql = "select top(1) * from Space0024A where column_0='%s' order by column_1 desc " %(city)
    data_aqi = ms.ExecQuery(sql.encode('utf-8'))

    city_aqi = data_aqi[0][3]
    city_time = data_aqi[0][2]
    city_quality = data_aqi[0][13]
    city_primary_pollutant = data_aqi[0][14]

    aqi_content = city_time + city + "实时空气质量为" + city_quality + "，指数为"+city_aqi +"，首要污染物为" + city_primary_pollutant

    sql = "select top(1) * from Space0030A where column_2='%s' order by column_0 desc " %(city)
    data_weather = ms.ExecQuery(sql.encode('utf-8'))

    city_humi = data_weather[0][4]
    city_time = data_weather[0][1]
    city_temp = data_weather[0][7]
    city_weather = data_weather[0][11]
    city_wd = data_weather[0][9]
    city_wl = data_weather[0][13]

    weather_content = city_time + city + "天气为" + city_weather + "，" + city_wd + city_wl + "级，体感温度为" + city_temp + "℃，相对湿度为" + city_humi + "%"

    return aqi_content, weather_content


def send_news():
    try:
        contents = get_messages('北京')
        #print(contents[0],contents[1])
        # 你朋友的微信名称，不是备注，也不是微信帐号。
        
        #my_friend = bot.friends().search(u'米线')[0]
        # my_friend = bot.groups().search(u'就是瞎聊吧')[0]
        # my_friend.send(contents[0])
        # my_friend.send(contents[1])
        # my_friend.send(u"自动消息测试!")


        # 找到需要接收日志的群 -- `ensure_one()` 用于确保找到的结果是唯一的，避免发错地方
        group_receiver = ensure_one(bot.groups().search('公众空气质量提醒'))
        group_receiver.send(contents[0])
        group_receiver.send(contents[1])

        # 指定这个群为接收者
        #logger = get_wechat_logger(group_receiver)

        #logger.error('打扰大家了，但这是一条重要的错误日志...')


        # 每86400秒（1天），发送1次
        # t = Timer(60 * 60, send_news)
        # t.start()
    except:
        # 你的微信名称，不是微信帐号。
        my_friend = bot.friends().search('过桥')[0]
        my_friend.send(u"今天消息提醒发送失败了")


def re_exe(cmd, inc = 60): 
    while True: 
        os.system(cmd);
        print("微信消息推送_Start")
        print(datetime.datetime.now().strftime('%H'))  

        now_time = datetime.datetime.now()

        if(now_time.strftime('%H') == "07"):
            send_news()

        print('微信消息推送_End')
        time.sleep(inc) 

# N秒 执行一次
re_exe("echo %time%", 60 * 60 )

