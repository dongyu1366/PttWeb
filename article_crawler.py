# -*- coding: utf-8 -*-
import logging
import MySQLdb
import threading
import os
import re
import sys
from datetime import datetime
from bs4 import BeautifulSoup
from time import sleep
from crawler.handler.ptt_api import PttApi

# Log setting
LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATE_FORMAT = '%Y%m%d %H:%M:%S'
logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT, datefmt=DATE_FORMAT)


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
                url = f'{url}.jpg'
                image_url_list.append(url)
        return image_url_list

    @classmethod
    def _insert_to_db(cls, article_list):
        for article in article_list:
            source_token = article['source_token']
            score = article['score']

            # Check the article is already in database or not
            if cur.execute(f"SELECT source_token FROM beauty WHERE source_token={source_token}"):
                BeautyDBHandler.update_to_db(source_token=source_token, score=score)
            else:
                BeautyDBHandler.insert_to_db(article=article)

    def get_all_article(self):
        """
        Try to get all articles on th web Beauty
        """
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
            self.get_all_article()

    def get_article(self):
        """
        Only get articles with specified number of pages
        """
        pages = int(input('輸入要爬取頁數: '))
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
            logging.info(f'Page {i + 1} Completed!')
            sleep(2)


class BeautyDBHandler:

    @classmethod
    def insert_to_db(cls, article):
        source_token = article['source_token']
        title = article['title']
        url = article['url']
        author = article['author']
        date = article['date']
        score = article['score']
        images = article['images']
        images_amounts = len(images)
        images = str(images)
        category = cls._create_category(title)
        sql_i = "INSERT INTO beauty(source_token, category, score, title, author, date, url, images_amounts, images) \
                 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql_i, (source_token, category, score, title, author, date, url, images_amounts, images))
        conn.commit()

    @classmethod
    def update_to_db(cls, source_token, score):
        cur.execute(f"UPDATE beauty SET score={score} WHERE source_token={source_token}")
        conn.commit()

    @classmethod
    def _create_category(cls, name):
        try:
            category = re.compile(r'(\[)(.+)(\])').search(name).group(2)
        except AttributeError:
            category = '其他'
        return category


if __name__ == '__main__':
    # Check for environment variable
    if not os.getenv("PASSWORD"):
        raise RuntimeError("PASSWORD is not set: export PASSWORD='your password'")

    # Connect to database
    try:
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd=os.getenv("PASSWORD"),
            db='ptt',
        )
    except MySQLdb.Error as e:
        print(e)
        sys.exit()

    cur = conn.cursor()

    spider = BeautyCrawler()
    spider.get_article()

    cur.close()
    conn.close()
    logging.info('Completed all task!')
