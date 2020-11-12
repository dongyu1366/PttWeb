from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from article.models import Beauty
from article.serializers import BeautySerializer


def index(request):

    return render(request, "article/index.html")


@api_view(['GET', ])
def get_article_list(request):
    """
    API endpoint that allows article to be viewed.
    """
    category = request.GET.get('category')
    score = request.GET.get('score')
    if category and score:
        articles = Beauty.objects.filter(category=category).filter(score__gt=score).order_by('-score')
    elif category:
        articles = Beauty.objects.filter(category=category).order_by('-date')
    elif score:
        articles = Beauty.objects.filter(score__gt=score).order_by('-score')
    else:
        articles = Beauty.objects.all().order_by('-date')
    serializer = BeautySerializer(articles, many=True)
    article = [dict(a) for a in serializer.data]
    return Response(article)
