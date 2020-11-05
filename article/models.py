from django.db import models


class Article(models.Model):
    source_token = models.IntegerField()
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    score = models.CharField(max_length=50, null=True)
    score_value = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class ArticleImage(models.Model):
    source_token = models.IntegerField()
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    images_amounts = models.IntegerField()
    url = models.CharField(max_length=5000)
