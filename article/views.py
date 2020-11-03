from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from handler.ptt_beauty import PttBeauty


def index(request):
    pages = 20
    message = PttBeauty.run(pages)

    return HttpResponse(message)
