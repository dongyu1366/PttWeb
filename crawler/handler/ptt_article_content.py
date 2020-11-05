# -*- coding: utf-8 -*-
import os
import threading
import re
import requests
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from article.models import ArticleImage
from crawler.handler.ptt_api import PttApi
from crawler.handler.db_handler import Image


class PttBeautyContent:

    @classmethod
    def _fetch_image_url(cls, article_url):
        """
        Get all images url of the article
        """
        source_token = re.compile(r'([^\d]+)([\d]+)').search(article_url).group(2)
        if not ArticleImage.objects.filter(source_token=source_token):
            response = PttApi.get_ptt_beauty_response(url=article_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find_all('span', class_='article-meta-value')[2].text

            image_url_list = list()
            image_data_list = soup.find('div', id='main-content').find_all('a', rel='nofollow')
            for image in image_data_list:
                url = image.get('href')
                if url and not url.endswith('html'):
                    image_url_list.append(url)
            article = {'source_token': source_token, 'title': title, 'url': image_url_list}

            # Insert to database
            Image.insert_to_db(article=article)

    @classmethod
    def run(cls, url_list):
        threads = list()
        for url in url_list:
            thread = threading.Thread(target=cls._fetch_image_url, args=(url,))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        message = f'Insert article contents to database'
        return message


class ImageHandler:

    @classmethod
    def _make_dir(cls, path):
        try:
            os.makedirs(path)
            print(f'Successfully created the directory {path}')
        except OSError:
            print(f'Creation of the directory {path} failed')

    @classmethod
    def _download_image(cls, url, category, dir_name):
        response = requests.get(url=url, stream=True)
        if response.status_code == 200:
            file_name = url.split('/')[-1]
            if not file_name:
                file_name = url.split('/')[-2]
            path = f'{os.getcwd()}/picture/{category}/{dir_name}'
            file = os.path.join(path, file_name)
            if not os.path.exists(path):
                cls._make_dir(path)
            with open(file, 'wb') as f:
                f.write(response.content)

    @classmethod
    def _get_article_data(cls, source_token):
        article = ArticleImage.objects.filter(source_token=source_token)[0]
        category = article.category
        title = article.title
        dir_name = cls._remove_special_char(title, '\/:*?"<>|.')
        url_list_raw = article.url
        url_list = url_list_raw[1:-1].replace("'", '').split(',')
        data = {'category': category,
                'dir_name': dir_name,
                'url_list': url_list}
        return data

    @staticmethod
    def _remove_special_char(words, delete_chars):
        for c in delete_chars:
            words = words.replace(c, '')
        return words

    @classmethod
    def _save_images_to_dir(cls, article_data):
        category = article_data['category']
        dir_name = article_data['dir_name']
        dir_name = cls._remove_special_char(dir_name, '\/:*?"<>|.')
        url_list = article_data['url_list']
        for url in url_list:
            cls._download_image(url=url, category=category, dir_name=dir_name)

    @classmethod
    def run(cls, source_token_list):
        threads = list()
        for source_token in source_token_list:
            article_data = cls._get_article_data(source_token=source_token)
            thread = threading.Thread(target=cls._save_images_to_dir, args=(article_data,))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        print('Completed all download!')
