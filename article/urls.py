from django.urls import path
from article import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api/article-list/', views.get_article_list, name='article-list'),
]
