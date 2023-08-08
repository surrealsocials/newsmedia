from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet
from .views import SportArticleList,FinanceArticleList,EntertainmentArticleList,ArticleList

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sport/', SportArticleList.as_view(), name='sport-article-list'),
    path('finance/', FinanceArticleList.as_view(), name='finance-article-list'),
    path('entertainment/', EntertainmentArticleList.as_view(), name='entertainment-article-list'),
    path('articles/', ArticleList.as_view(), name='article-list'),
]
