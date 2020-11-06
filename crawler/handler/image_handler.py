# -*- coding: utf-8 -*-
import logging
import os
import threading
from article.models import Beauty
from crawler.handler.ptt_api import PttApi


class ImageHandler:

    def __init__(self, dir_path):
        self.dir_path = dir_path

    @classmethod
    def _get_article_data(cls, source_token):
        article = Beauty.objects.filter(source_token=source_token)[0]
        category = article.category
        title = article.title
        dir_name = cls._remove_special_char(title, '\/:*?"<>|.')
        url_list_raw = article.images
        url_list = url_list_raw[1:-1].replace("'", '').split(',')
        data = {'category': category,
                'dir_name': dir_name,
                'url_list': url_list}
        return data

    def _download_article_images(self, article, sema):
        """
        Download all images in the article
        """
        sema.acquire()
        threads = list()
        dir_name = article['dir_name']
        dir_path = f'{self.dir_path}/{dir_name}'
        url_list = article['url_list']
        for url in url_list:
            thread = threading.Thread(target=self._download_image, args=(url, dir_path,))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        logging.info(f'Download Completed: {dir_name}')
        sema.release()

    @classmethod
    def _download_image(cls, url, dir_path):
        """
        Download the image
        """
        if cls._check_url_valid(url=url):
            if cls._is_new_file(url=url, dir_path=dir_path):
                response = PttApi.get_image_response(url=url)
                if response.status_code == 200:
                    file_name = url.split('/')[-1]
                    if not file_name:
                        file_name = url.split('/')[-2]
                    file = os.path.join(dir_path, file_name)
                    if not os.path.exists(dir_path):
                        cls._make_dir(path=dir_path)
                    with open(file, 'wb') as f:
                        f.write(response.content)

    @staticmethod
    def _check_url_valid(url):
        if ('imgur.com/a/' in url) or ('imgur.com/gallery/' in url):
            return False
        else:
            return True

    @staticmethod
    def _make_dir(path):
        try:
            os.makedirs(path)
            logging.info(f'Successfully created the directory {path}')
        except OSError:
            logging.warning(f'Creation of the directory {path} failed')

    @staticmethod
    def _is_new_file(url, dir_path):
        """
        Return file path if the file not exist
        """
        file_name = url.split('/')[-1]
        file_path = os.path.join(dir_path, file_name)
        if not os.path.exists(file_path):
            return file_path

    @staticmethod
    def _remove_special_char(words, delete_chars):
        for c in delete_chars:
            words = words.replace(c, '')
        return words

    def run(self, source_token_list):
        threads = list()
        max_threads = 5
        sema = threading.Semaphore(value=max_threads)
        for source_token in source_token_list:
            article = self._get_article_data(source_token=source_token)
            thread = threading.Thread(target=self._download_article_images, args=(article, sema,))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        logging.info('All Downloads Completed!')
