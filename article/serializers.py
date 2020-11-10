from rest_framework import serializers
from article.models import Beauty


class BeautySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beauty
        fields = ['category', 'score', 'title', 'author', 'date', 'url']
