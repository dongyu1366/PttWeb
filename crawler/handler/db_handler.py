# -*- coding: utf-8 -*-
import re
from article.models import Article, ArticleImage


class ArticleList:

    @classmethod
    def insert_to_db(cls, article):
        source_token = article['source_token']
        title = article['title']
        url = article['url']
        author = article['author']
        date = article['date']
        score = article['score']
        score_value = cls._transfer_score(score=score)
        category = cls._create_category(title)
        a = Article(source_token=source_token, category=category, title=title, url=url, author=author, date=date,
                    score=score, score_value=score_value)
        a.save()

    @classmethod
    def update_to_db(cls, source_token, score):
        a = Article.objects.filter(source_token=source_token)[0]
        score_value = cls._transfer_score(score=score)
        if score_value != a.score_value:
            a.score = score
            a.score_value = score_value
            a.save()

    @classmethod
    def _transfer_score(cls, score):
        try:
            score_value = int(score)
        except:
            if score == '爆':
                score_value = 100
            elif score == '':
                score_value = 0
            else:
                score_value = -1

        return score_value

    @classmethod
    def _create_category(cls, name):
        try:
            category = re.compile(r'(\[)(.+)(\])').search(name).group(2)
        except:
            category = '其他'
        return category


class Image:

    @classmethod
    def insert_to_db(cls, article):
        source_token = article['source_token']
        title = article['title']
        url = article['url']
        images_amounts = len(url)
        category = cls._create_category(title)

        a = ArticleImage(source_token=source_token, category=category, title=title, url=url,
                         images_amounts=images_amounts)
        a.save()

    @classmethod
    def _create_category(cls, name):
        try:
            category = re.compile(r'(\[)(.+)(\])').search(name).group(2)
        except:
            category = '其他'
        return category
