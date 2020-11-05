# -*- coding: utf-8 -*-
import threading
import re
import requests
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from article.models import Article
from crawler.handler.ptt_api import PttApi
from crawler.handler.db_handler import ArticleList


class PttBeauty:

    @classmethod
    def _fetch_article(cls, current_page, container, counts, pages):
        """
        Get the articles list
        """
        counts += 1
        response = PttApi.get_ptt_beauty_response(url=current_page)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles_list_data = soup.find('div', id='main-container').find_all('div', class_='r-ent')

        for div in articles_list_data:
            try:
                title = div.find('div', class_='title').text
                title = title.replace('\n', '')
                url = div.a.get('href')
                url = f'{PttApi.PTT_DOMAIN}{url}'
                score = div.find('div', class_='nrec').text
                author = div.find('div', class_='author').text
                date = div.find('div', class_='date').text
                id_pattern = re.compile(r'([^\d]+)([\d]+)').search(url)
                source_token = id_pattern.group(2)
                articles_dict = {
                    'source_token': source_token,
                    'title': title,
                    'url': url,
                    'score': score,
                    'author': author,
                    'date': date
                }
                if '公告' not in articles_dict['title']:
                    container.append(articles_dict)
            except AttributeError:
                pass

        # Check if need to fetch articles of next page
        next_page = cls._fetch_next_page(current_page)
        if counts < pages and next_page:
            cls._fetch_article(current_page=next_page, container=container, counts=counts, pages=pages)

        return container

    @classmethod
    def _fetch_next_page(cls, url):
        """
        Get the url of next page
        """
        response = PttApi.get_ptt_beauty_response(url=url)
        soup = BeautifulSoup(response.text, 'html.parser')
        next_page_btn = soup.find('div', class_='btn-group btn-group-paging').find_all('a')[1]
        url = next_page_btn.get('href')
        if url:
            url = f'{PttApi.PTT_DOMAIN}{url}'
        return url

    @classmethod
    def _insert_to_db(cls, article_list):
        for article in article_list:
            source_token = article['source_token']

            # Check the article is already in database or not
            if Article.objects.filter(source_token=source_token):
                score = article['score']
                ArticleList.update_to_db(source_token=source_token, score=score)
            else:
                ArticleList.insert_to_db(article=article)

    @classmethod
    def run(cls, pages):
        articles_list = list()
        counts = 0

        cls._fetch_article(current_page=PttApi.BEAUTY_MAIN_PAGE, container=articles_list, counts=counts, pages=pages)

        message = f'Total articles are: {len(articles_list)}'

        cls._insert_to_db(article_list=articles_list)

        return message


if __name__ == '__main__':
    PttBeauty.run(1)
