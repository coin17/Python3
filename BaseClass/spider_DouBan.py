#!/usr/bin/env python
# encoding=utf-8

"""
爬取豆瓣电影TOP250 
Top 1 肖申克的救赎 / The Shawshank Redemption / 月黑高飞(港)  /  刺激1995(台)
"""

import codecs

import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://movie.douban.com/top250/'


def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }).content


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})

    movie_name_list = []

    print("当前准备解析页码：" + soup.find('span', attrs={'class': 'thispage'}).getText())

    top_num = 1 + (int(soup.find('span', attrs={'class': 'thispage'}).getText())-1) * 25
    movie_name_list.append("## Top " + str(top_num))

    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div', attrs={'class': 'hd'})

        #名称
        movie_name = ""

        for sp in detail.find_all('span', attrs={'class': 'title'}):
        	movie_name += sp.text

        movie_name_other = detail.find('span', attrs={'class': 'other'}).getText()
        
        img = movie_li.find('div', attrs={'class': 'pic'}).find('a').find('img')
        
        try:
            img_req = requests.get(img["src"], timeout=20)
            img_localhost = 'douban_moviesList_top250\\'+str(top_num)+ '.jpg'
            fp = open(img_localhost,'wb')
            fp.write(img_req.content)
            fp.close()
            movie_name_list.append('!['+movie_name+'](douban_moviesList_top250/'+str(top_num)+'.jpg "douban_moviesList_top250")')
            
        except requests.exceptions.ConnectionError:
            print('【错误】当前图片无法下载，失效地址为：' + img["src"])


        movie_name_list.append("### "+ movie_name + movie_name_other)

        #导演、主演
        evaluate = movie_li.find('div', attrs={'class': 'bd'})
        movie_actor_table = evaluate.find('p').getText().strip().splitlines()

        for mat in movie_actor_table :
            movie_name_list.append("* " + mat.strip())

        # 评分
        movie_score = evaluate.find('div', attrs={'class':'star'})

        movie_rating_num = movie_score.find('span', attrs={'class': 'rating_num'}).getText() + " "

        for mess in movie_score.find_all('span', attrs={'class': ''}):
            movie_rating_num += mess.text

        movie_name_list.append("* " + movie_rating_num)

        #评价
        movie_name_list.append("")
        movie_actor_message = evaluate.find('p',attrs={'class': 'quote'})
        if movie_actor_message:
            movie_name_list.append("> " + movie_actor_message.find('span').getText())

        movie_name_list.append("")
        movie_name_list.append("***")
        movie_name_list.append("")
        top_num +=1

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')


    if next_page:
        return movie_name_list, DOWNLOAD_URL + next_page['href']
    return movie_name_list, None


def main():
    url = DOWNLOAD_URL

    with codecs.open('douban_moviesList_top250.md', 'wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            movies, url = parse_html(html)
            fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))


if __name__ == '__main__':
    main()