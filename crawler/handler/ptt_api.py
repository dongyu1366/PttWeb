# -*- coding: utf-8 -*-
import logging
import requests
from time import sleep


class PttApi:
    PTT_DOMAIN = 'https://www.ptt.cc'
    BEAUTY_MAIN_PAGE = f'{PTT_DOMAIN}/bbs/Beauty/index.html'
    _HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
    _cookies = {'over18': '1'}

    @classmethod
    def _request_handler(cls, url, cookies=None, retried=5, timeout=10):
        response = None
        for i in range(retried):
            try:
                response = requests.get(url=url, headers=cls._HEADERS, cookies=cookies, timeout=timeout)
                break
            except requests.exceptions.Timeout:
                logging.warning(f'Timeout {i + 1} times: {url}')
            except requests.exceptions.ConnectionError:
                logging.warning(f'Connection refused {i + 1} times: {url}')
                sleep(5)
        return response

    @classmethod
    def _request_image_handler(cls, url, cookies=None, retried=5, timeout=10):
        response = None
        for i in range(retried):
            try:
                response = requests.get(url=url, stream=True, headers=cls._HEADERS, cookies=cookies, timeout=timeout)
                break
            except requests.exceptions.Timeout:
                logging.warning(f'Timeout {i + 1} times: {url}')
            except requests.exceptions.ConnectionError:
                logging.warning(f'Connection refused {i + 1} times: {url}')
                sleep(5)
        return response

    @classmethod
    def get_ptt_beauty_response(cls, url):
        return cls._request_handler(url=url, cookies=cls._cookies)

    @classmethod
    def get_url_response(cls, url):
        return cls._request_handler(url=url)

    @classmethod
    def get_image_response(cls, url):
        return  cls._request_image_handler(url=url)
