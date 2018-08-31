# -*- coding:utf-8 -*-
from functools import wraps
from flask import Flask, url_for, request, make_response
from wxpy import *

#bot = Bot(cache_path=True)
bot = Bot()

app = Flask(__name__)

#跨域
def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun

@app.route('/')
@allow_cross_domain
def api_root():
    return 'Welcome Wechat Root!'

@app.route('/api_webchat',methods = ['POST'])
@allow_cross_domain
def api_webchat():
	if request.method == "POST":
		m_type = request.form.get('type')
		m_object = request.form.get('name')
		m_content = request.form.get('message')
		print(m_type)

		if(m_type == 'friend'):
			object_list = bot.friends().search(m_object)
		else:
			print(m_object)
			object_list = bot.groups().search(m_object)

		if(len(object_list) == 0):
			return '没有找到用户或群'

		for o in object_list:
			try:
				o.send(m_content)
				print(m_content)
				return 'to send success!'
			except ResponseError as e:
				print(e.err_code, e.err_msg)



if __name__ == '__main__':
    app.run(host='172.16.30.107',port=8080)