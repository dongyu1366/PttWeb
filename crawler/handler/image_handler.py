# -*- coding: utf-8 -*-
import os
import threading
import requests
from article.models import Beauty


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
        article = Beauty.objects.filter(source_token=source_token)[0]
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
