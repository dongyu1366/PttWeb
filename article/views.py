import logging
import tkinter as tk
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from article.models import Beauty
from crawler.handler.ptt_crawler import BeautyCrawler
from crawler.handler.image_handler import ImageHandler

LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATE_FORMAT = '%Y%m%d %H:%M:%S'
logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT, datefmt=DATE_FORMAT)


def index(request):
    # root = tk.Tk()
    # root.withdraw()
    # dir_path = tk.filedialog.askdirectory()
    #
    # source_token_list = get_token_list()
    # a = ImageHandler(dir_path)
    # a.run(source_token_list=source_token_list)

    return HttpResponse('ok')


def get_token_list():
    source_token_list = list()
    article_list = Beauty.objects.all()[0:5]
    for article in article_list:
        token = article.source_token
        source_token_list.append(token)
    return source_token_list
