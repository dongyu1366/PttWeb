# -*- coding: utf-8 -*-
import requests


class PttApi:
    PTT_DOMAIN = 'https://www.ptt.cc'
    _ASK_OVER_18 = f'{PTT_DOMAIN}/ask/over18'
    BEAUTY_MAIN_PAGE = f'{PTT_DOMAIN}/bbs/Beauty/index.html'
    _HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

    @classmethod
    def _request_handler(cls, url, retried=5, timeout=10):
        response = None
        for _ in range(retried):
            try:
                response = requests.get(url=url, headers=cls._HEADERS, timeout=timeout)
                break
            except AttributeError:
                continue
        return response

    @classmethod
    def _request_session_handler(cls, url, retried=10, timeout=10):
        response = None
        payload = {'form': '/bbs/Beauty/index.html',
                   'yes': 'yes'}
        for _ in range(retried):
            try:
                r = cls._create_session(payload=payload)
                response = r.get(url=url, headers=cls._HEADERS, timeout=timeout)
                break
            except AttributeError:
                continue
        return response

    @classmethod
    def _create_session(cls, payload, retried=5, timeout=10):
        r_session = None
        for _ in range(retried):
            try:
                r_session = requests.session()
                r1 = r_session.post(url=cls._ASK_OVER_18, data=payload, headers=cls._HEADERS, timeout=timeout)
                break
            except AttributeError:
                continue
        return r_session

    @classmethod
    def get_ptt_beauty_response(cls, url):
        return cls._request_session_handler(url=url)

    @classmethod
    def get_url_response(cls, url):
        return cls._request_handler(url=url)
