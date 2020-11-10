import logging
import tkinter as tk
from tkinter import filedialog
from article.models import Beauty
from crawler.handler.ptt_crawler import BeautyCrawler
from crawler.handler.image_handler import ImageHandler


LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATE_FORMAT = '%Y%m%d %H:%M:%S'
logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT, datefmt=DATE_FORMAT, filename='myLog.log',
                    filemode='a')


def get_all_beauty_article():
    logging.info('Start to Fetch all Beauty articles')

    spider = BeautyCrawler()
    spider.get_all()

    logging.info('Fetch task complete!')


def update_beauty_article(pages):
    logging.info('Start to Update Beauty articles')

    spider = BeautyCrawler()
    spider.update(pages=pages)

    logging.info('Update task complete!')


def download_images():
    logging.info('Start download task!')
    root = tk.Tk()
    root.withdraw()
    dir_path = filedialog.askdirectory()

    source_token_list = get_token_list()
    a = ImageHandler(dir_path)
    a.run(source_token_list=source_token_list)


def get_token_list():
    source_token_list = list()
    article_list = Beauty.objects.filter(category='正妹')[0:5]
    for article in article_list:
        token = article.source_token
        source_token_list.append(token)
    return source_token_list
