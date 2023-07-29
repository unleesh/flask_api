# app.py
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

def get_news_titles_with_urls(query, num_pages=10):
    base_url = 'https://search.naver.com/search.naver'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    news_data = []  # news data store list

    for page in range(num_pages):
        params = {
            'where': 'news',
            'query': query,
            'start': page * 10 + 1
        }

        response = requests.get(base_url, headers=headers, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')
        news_links = soup.select('.news_area')

        for link in news_links:
            title = link.select_one('.news_tit').text
            url = link.select_one('.info_group a').get('href')
            news_data.append({'Title': title, 'URL': url})  # add crawl data to the list

    return news_data  # return crawl data

@app.route('/api/news')
def get_news_data():
    query = '블록체인 게임'
    num_pages = 10
    data = get_news_titles_with_urls(query, num_pages)
    return jsonify(data)  # return data within a json format

if __name__ == '__main__':
    app.run(debug=True)
