from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from article.models import Beauty
from article.serializers import BeautySerializer


def index(request):
    return HttpResponse('OK')


class ArticleViewSet(ListAPIView):
    """
    API endpoint that allows article to be viewed.
    """
    queryset = Beauty.objects.all().order_by('-date')
    serializer_class = BeautySerializer
