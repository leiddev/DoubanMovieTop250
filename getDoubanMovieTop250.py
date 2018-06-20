#!/usr/bin/env python
# encoding=utf-8

"""
爬取豆瓣电影TOP250 - 完整示例代码
https://zhuanlan.zhihu.com/p/20423182
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
    soup = BeautifulSoup(html, 'html.parser')
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})

    movie_list = []

    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div', attrs={'class': 'pic'})
        top = detail.find('em').getText()
        link = detail.find('a')['href']

        detail = movie_li.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).getText()

        detail = movie_li.find('div', attrs={'class': 'bd'})
        rating_num = detail.find('span', attrs={'class': 'rating_num'}).getText()
        quote = detail.find('span', attrs={'class': 'inq'})

        if quote != None:
            item = top + ' ' + movie_name + ' ' + rating_num + ' \"' + quote.getText() + '\"\r\n\t' + link
        else:
            item = top + ' ' + movie_name + ' ' + rating_num + '\r\n\t' + link
        
        print(item)
        movie_list.append(item)

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return movie_list, DOWNLOAD_URL + next_page['href']
    return movie_list, None


def main():
    url = DOWNLOAD_URL

    with codecs.open('movies.txt', 'wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            movies, url = parse_html(html)
            fp.write(u'{movies}\r\n\r\n'.format(movies='\r\n'.join(movies)))


if __name__ == '__main__':
    main()
