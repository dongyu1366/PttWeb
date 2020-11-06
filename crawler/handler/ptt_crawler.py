# -*- coding: utf-8 -*-
import logging
import threading
import re
from datetime import datetime
from bs4 import BeautifulSoup
from time import sleep
from article.models import Beauty
from crawler.handler.ptt_api import PttApi
from crawler.handler.db_handler import BeautyDBHandler


class BeautyCrawler:

    def __init__(self):
        self.current_page = PttApi.BEAUTY_MAIN_PAGE

    def _fetch_article(self, container):
        """
        Get all articles link on current page
        """
        response = PttApi.get_ptt_beauty_response(url=self.current_page)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles_list_data = soup.find('div', id='main-container').find_all('div', class_='r-ent')
        for div in articles_list_data:
            try:
                title = div.find('div', class_='title').text
                title = title.replace('\n', '')
                url = div.a.get('href')
                url = f'{PttApi.PTT_DOMAIN}{url}'

                if '公告' not in title:
                    container.append(url)
            except AttributeError:
                pass
        self.current_page = self._fetch_next_page(soup=soup)

    @classmethod
    def _fetch_article_content(cls, article_url, container):
        """
        Get contents of the article
        """
        try:
            response = PttApi.get_ptt_beauty_response(url=article_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            article_meta = soup.find_all('div', class_='article-metaline')

            source_token = re.compile(r'([^\d]+)([\d]+)').search(article_url).group(2)
            author = article_meta[0].find('span', class_='article-meta-value').text
            title = article_meta[1].find('span', class_='article-meta-value').text
            date_str = article_meta[2].find('span', class_='article-meta-value').text
            date = datetime.strptime(date_str, '%a %b %d %H:%M:%S %Y')
            url = article_url
            score = cls._calculate_score(soup=soup)
            images = cls._fetch_image_url(soup=soup)
            article = {
                'source_token': source_token,
                'score': score,
                'title': title,
                'author': author,
                'date': date,
                'url': url,
                'images': images
            }
            container.append(article)
        except IndexError:
            logging.warning(f'IndexError: {article_url}')

    @staticmethod
    def _fetch_next_page(soup):
        """
        Get the url of next page
        """
        next_page_btn = soup.find('div', class_='btn-group btn-group-paging').find_all('a')[1]
        url = next_page_btn.get('href')
        if url:
            url = f'{PttApi.PTT_DOMAIN}{url}'
        return url

    @staticmethod
    def _calculate_score(soup):
        score = 0
        score_div = soup.find('div', id='main-content').find_all('div', class_='push')
        for div in score_div:
            push_tag = div.find('span', class_='push-tag').text
            if '推' in push_tag:
                score += 1
            elif '噓' in push_tag:
                score -= 1
        return score

    @staticmethod
    def _fetch_image_url(soup):
        image_url_list = list()
        image_data_list = soup.find('div', id='main-content').find_all('a', rel='nofollow')
        for image in image_data_list:
            url = image.get('href')
            if url.endswith(('.jpg', '.png', '.jpeg', '.gif')):
                image_url_list.append(url)
            elif ('imgur' in url) and not (url.endswith('.mp4')):
                url = f'{url}.png'
                image_url_list.append(url)
        return image_url_list

    @staticmethod
    def _insert_to_db(article_list):
        for article in article_list:
            source_token = article['source_token']

            # Check the article is already in database or not
            if Beauty.objects.filter(source_token=source_token):
                score = article['score']
                BeautyDBHandler.update_to_db(source_token=source_token, score=score)
            else:
                BeautyDBHandler.insert_to_db(article=article)

    def get_all(self):
        threads = list()
        article_url_list = list()
        article_list = list()
        self._fetch_article(container=article_url_list)

        # Get the content of each article
        for url in article_url_list:
            thread = threading.Thread(target=self._fetch_article_content, args=(url, article_list))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self._insert_to_db(article_list=article_list)
        sleep(2)

        # Keep fetch or not
        response = PttApi.get_ptt_beauty_response(url=self.current_page)
        soup = BeautifulSoup(response.text, 'html.parser')
        next_page = self._fetch_next_page(soup=soup)
        if next_page:
            self.get_all()

    def update(self, pages):
        for i in range(pages):
            threads = list()
            article_url_list = list()
            article_list = list()
            self._fetch_article(container=article_url_list)

            # Get the content of each article
            for url in article_url_list:
                thread = threading.Thread(target=self._fetch_article_content, args=(url, article_list))
                threads.append(thread)
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            self._insert_to_db(article_list=article_list)
            logging.info(f'Page {i+1} Completed!')
            sleep(2)
