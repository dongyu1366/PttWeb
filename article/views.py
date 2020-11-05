from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from article.models import Article, ArticleImage
from crawler.handler.ptt_article_list import PttBeauty
from crawler.handler.ptt_article_content import PttBeautyContent, ImageHandler


def index(request):
    # pages = 10
    # PttBeauty.run(pages)
    # print('Stage 1 OK')
    #
    # url_list = []
    # all_article = Article.objects.all()
    # for article in all_article:
    #     url = article.url
    #     url_list.append(url)
    #
    # PttBeautyContent.run(url_list=url_list)
    # print('Stage 2 OK')
    token_list = list()
    images = ArticleImage.objects.filter(category='正妹')
    for image in images:
        token = image.source_token
        token_list.append(token)
    ImageHandler.run(source_token_list=token_list)

    return HttpResponse('OK')
