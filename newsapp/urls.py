from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .views import NewsArticleSitemap

app_name = 'newsapp'  # Set the app namespace

urlpatterns = [
    path('cube.html', views.cube, name='cube'),
    path('test.html', views.test, name='test'),
    path('base.html', views.base, name='base'),
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('article/<slug:url>/', views.single, name='single'),  # Use 'slug' for URL-friendly titles
    path('articles/', views.articles, name='articles'),
    path('articles.html', views.articles, name='articles'),
    path('contact', views.contact, name='contact'),
    path('contact.html', views.contact, name='contact'),
    path('service-worker.js', views.service_worker, name='service_worker'),
    path('category/<category>/', views.catty, name='category'),  # Assuming you have this route in views
    #path('article/<slug:page>.html', views.redir, name='redir'),  # Assuming you have this route in views
    path('cats/', views.seecats, name='seecats'),  # Assuming you have this route in views
    path('category', views.cattyo, name='categoryo'),
    path('category.html', views.cattyo, name='categoryo'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemap}, name='django.contrib.sitemaps.views.sitemap')

]

sitemaps = {
    'articles': NewsArticleSitemap
}

