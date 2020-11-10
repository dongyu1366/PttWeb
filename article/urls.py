from django.urls import include, path
from rest_framework import routers
from article import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api/article-list/', views.ArticleViewSet.as_view(), name='article-list')
]
