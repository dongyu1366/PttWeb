from django.urls import path
from article import views

urlpatterns = [
    path('', views.index, name='index')
]
