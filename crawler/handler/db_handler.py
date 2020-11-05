# -*- coding: utf-8 -*-
import re
from article.models import Beauty


class BeautyDBHandler:

    @classmethod
    def insert_to_db(cls, article):
        source_token = article['source_token']
        title = article['title']
        url = article['url']
        author = article['author']
        date = article['date']
        score = article['score']
        images = article['images']
        images_amounts = len(images)
        category = cls._create_category(title)
        a = Beauty(source_token=source_token,
                   category=category,
                   score=score,
                   title=title,
                   author=author,
                   date=date,
                   url=url,
                   images_amounts=images_amounts,
                   images=images
                   )
        a.save()

    @classmethod
    def update_to_db(cls, source_token, score):
        a = Beauty.objects.filter(source_token=source_token)[0]
        if score != a.score:
            a.score = score
            a.save()

    @classmethod
    def _create_category(cls, name):
        try:
            category = re.compile(r'(\[)(.+)(\])').search(name).group(2)
        except:
            category = '其他'
        return category
