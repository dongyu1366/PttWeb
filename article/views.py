from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from article.models import Beauty
from crawler.handler.ptt_crawler import BeautyCrawler


def index(request):
    return HttpResponse('OK')
