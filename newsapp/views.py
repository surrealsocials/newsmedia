from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.serializers import serialize
from .models import NewsArticle
from .utils import getarticle,formatme  # Assuming you have a utils module for getarticle function
from .utils import update
from django.utils.text import slugify  # Import slugify function
import base64,random
from unidecode import unidecode
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.contrib.sitemaps import Sitemap

class NewsArticleSitemap(Sitemap):
    changefreq = "daily"  # How often the content changes
    priority = 0.8  # Priority for search engines

    def items(self):
        return NewsArticle.objects.all()

    def lastmod(self, obj):
        return obj.date


cats=['Finance','Entertainment','Sport','Technology','World','Lifestyle']
tags=set()
Finance= NewsArticle.objects.filter(category="Finance")
Technology=  NewsArticle.objects.filter(category="Technology") 
Entertainment=  NewsArticle.objects.filter(category="Entertainment")
Sport= NewsArticle.objects.filter(category="Sport") 
global categories
categories=[Entertainment,Technology,Finance,Sport]
featured_items=Sport

# views.py
global globallastupdate
globallastupdate=datetime.now()
update()


def my_view(request):
    # Get the 'Referer' header from the request.META dictionary
    referer = request.META.get('HTTP_REFERER', None)
    
    return HttpResponse(f"Referral source: {referer}")


def index(request):
    global globallastupdate
    referer = request.META.get('HTTP_REFERER', None)
    print(referer)
    #update()
    
    most_recent_timestamp = globallastupdate#NewsArticle.objects.order_by('last_update').last().last_update
    current_time = datetime.now(most_recent_timestamp.tzinfo)
    time_difference = current_time - globallastupdate
    if time_difference > timedelta(minutes=30):
        print("More than 30 minute ago",time_difference)
        update()
        print('updating db')
        globallastupdate=datetime.now()
    else:
        #update()
        print("Less than 30 minute ago",time_difference)

    print("globallastupdate:",globallastupdate)

    cats=['Finance','Entertainment','Sport','Technology','World','Lifestyle']
    categories=[cats[0],cats[1],cats[2],cats[3]]


    categories[0] = NewsArticle.objects.filter(category=cats[0]).order_by('?')
    categories[1]=  NewsArticle.objects.filter(category=cats[1]).order_by('?')
    categories[2]=  NewsArticle.objects.filter(category=cats[2]).order_by('?')
    categories[3]= NewsArticle.objects.filter(category=cats[3]).order_by('?')
    featured_items=Sport
    lifestyle=Entertainment
    world=Finance
    articles = NewsArticle.objects.all().order_by('?')

    return render(request, 'index.html', {
        'cats': cats,
        'categories':[Entertainment,Technology,Finance,Sport],
        'featured_items': featured_items,
        'lifestyle': lifestyle,
        'world': world,
        'Finance':Finance,
        'Sport':Sport,
        'Entertainment':Entertainment,
        'Technology':Technology,
        'articles':articles
    })

def single(request, url):
    cats=['Finance','Entertainment','Sport','Technology','World','Lifestyle']

    try:
        article=NewsArticle.objects.filter(url=f'article/{url}')[0]
        story = article.story
        if story == "":
            print('story Empty')
            story=getarticle(article.link)
            print("The story has updated.")
        else:
            #story=getarticle(article.link)
            story=eval(story)
            print("Got Story from DB:")
    except:
        article=NewsArticle.objects.filter(url=f'article/{url}')[0]
        story=getarticle(article.link)
        #story=formatme(story)
        print('exception: fetched story')
    
    return render(request, 'single.html', {
        'categories': cats,
        'cats': cats,
        'article':article,
        'story': story,
        'featured_items':featured_items
    })

def base(request):    
    return render(request, 'base.html')

def cube(request):    
    return render(request, 'cube.html')

def test(request):
    categories=[]
    articles = NewsArticle.objects.all()
    for cat in cats:
        categories += NewsArticle.objects.filter(category=cat)
    return render(request, 'test.html',{'articles':articles,'categories':categories})

def cattyo(request):
    categories=[]
    articles = NewsArticle.objects.all()
    for cat in cats:
        categories += NewsArticle.objects.filter(category=cat)
    return render(request, 'category.html',{'articles':articles,'categories':categories})

def articles(request):
    articles = NewsArticle.objects.all()
    articles = NewsArticle.objects.order_by('?')

    return render(request, 'allarticles.html',{'articles':articles,'categories':categories,'cats':cats,'featured_items':featured_items})

def articleslist(request):
    articles = NewsArticle.objects.all()
    article_dicts = [{
        'title': article.title,
        'summary': article.subtitle,
        'category': article.category,
        'link': article.link,
        'tag': article.tag,
        'date': article.date,
    } for article in articles]
    return JsonResponse(article_dicts, safe=False)

def service_worker(request):
    return render(request, 'service-worker.js', content_type='application/javascript')

def catty(request, category):
    tags=set()
    articles = NewsArticle.objects.filter(category=category)
    return render(request, 'category.html', {
        'cats': cats,
        'articles': articles,
        'category':category
    })

def redir(request, page):
    return redirect(f'/{page}')

def contact(request):
    return render(request, 'contact.html', {
        'cats': cats,
        'featured_items':featured_items
    })


def seecats(request):
    Sport = NewsArticle.objects.filter(category='Sport')
    Finance = NewsArticle.objects.filter(category='Finance')
    Entertainment = NewsArticle.objects.filter(category='Entertainment')
    Technology = NewsArticle.objects.filter(category='Technology')
    return JsonResponse({'Sport': serialize('json', Sport), 'Finance': serialize('json', Finance),
                         'Entertainment': serialize('json', Entertainment), 'Technology': serialize('json', Technology)})

