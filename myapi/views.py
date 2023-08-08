from django.shortcuts import render
from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

from rest_framework import generics
from newsapp.models import NewsArticle  # Import your NewsArticle model
from .serializers import NewsArticleSerializer  # Create this serializer

class EntertainmentArticleList(generics.ListAPIView):
    queryset = NewsArticle.objects.filter(category='Entertainment')
    serializer_class = NewsArticleSerializer
    
class FinanceArticleList(generics.ListAPIView):
    queryset = NewsArticle.objects.filter(category='Finance')
    serializer_class = NewsArticleSerializer

class SportArticleList(generics.ListAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer

class ArticleList(generics.ListAPIView):
    queryset = NewsArticle.objects.filter(category='Sport')
    serializer_class = NewsArticleSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
