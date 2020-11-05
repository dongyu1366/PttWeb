# -*- coding: utf-8 -*-
import requests


class PttApi:
    PTT_DOMAIN = 'https://www.ptt.cc'
    BEAUTY_MAIN_PAGE = f'{PTT_DOMAIN}/bbs/Beauty/index.html'
    _HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
    _cookies = {'over18': '1'}

    @classmethod
    def _request_handler(cls, url, cookies=None, retried=5, timeout=20):
        response = None
        for _ in range(retried):
            try:
                response = requests.get(url=url, headers=cls._HEADERS, cookies=cookies, timeout=timeout)
                break
            except AttributeError:
                continue
        return response

    @classmethod
    def get_ptt_beauty_response(cls, url):
        return cls._request_handler(url=url, cookies=cls._cookies)

    @classmethod
    def get_url_response(cls, url):
        return cls._request_handler(url=url)
