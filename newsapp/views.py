from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.serializers import serialize
from .models import NewsArticle
from .utils import getarticle,formatme  # Assuming you have a utils module for getarticle function
from .utils import update
from django.utils.text import slugify  # Import slugify function
import base64,random,math
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
Finance= NewsArticle.objects.filter(category="Finance").order_by('-date')
Technology=  NewsArticle.objects.filter(category="Technology").order_by('-date')
Entertainment=  NewsArticle.objects.filter(category="Entertainment").order_by('-date')
Sport= NewsArticle.objects.filter(category="Sport").order_by('-date')
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
    #categories=[cats[0],cats[1],cats[2],cats[3]]

    Finance = NewsArticle.objects.filter(category='Finance').order_by('-date')
    Entertainment=  NewsArticle.objects.filter(category='Entertainment').order_by('-date')
    Sport=  NewsArticle.objects.filter(category='Sport').order_by('-date')
    Technology= NewsArticle.objects.filter(category="Technology").order_by('-date')
    lifestyle= NewsArticle.objects.filter(category="Lifestyle").order_by('-date')
    world=NewsArticle.objects.filter(category="world").order_by('-date')
    articles = NewsArticle.objects.all().order_by('-date')
    featured_items=Sport
    latest=articles

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
        'articles':articles,
        'latest':latest
    })

def updater(request):
    update()
    return HttpResponse(f"DB updated")

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
        categories += NewsArticle.objects.filter(category=cat).order_by('-date')
    return render(request, 'test.html',{'articles':articles,'categories':categories})

def cattyo(request):
    categories=[]
    articles = NewsArticle.objects.all()
    for cat in cats:
        categories += NewsArticle.objects.filter(category=cat).order_by('-date')
    return render(request, 'category.html',{'articles':articles,'categories':categories})

def articles(request):
    page_number = request.GET.get('page', 1)
    page_number=int(page_number)
    articles = NewsArticle.objects.order_by('-date')
    artamount=len(articles)
    maxpages=artamount/16
    maxpages= math.ceil(maxpages)

    articles=articles[(int(page_number)-1)*16:]
    pages=[]
    for p in range(1,maxpages):
        pages.append({"number":str(p),"active":"page-item"})
    pages[int(page_number)-1]["active"]="page-item active"
    print(request)

    return render(request, 'allarticles.html',{'articles':articles,'categories':categories,'cats':cats,'featured_items':featured_items,'pages':pages,"maxpages":10})

def articleslist(request):
    articles = NewsArticle.objects.all().order_by('-date')
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
    page_number = request.GET.get('page', 1)
    page_number=int(page_number)
    tags=set()

    articles = NewsArticle.objects.filter(category=category).order_by('-date')
    artamount=len(articles)
    maxpages=artamount/16
    maxpages= math.ceil(maxpages)

    articles=articles[(int(page_number)-1)*16:]
    pages=[]
    for p in range(1,maxpages):
        pages.append({"number":str(p),"active":"page-item"})
    pages[int(page_number)-1]["active"]="page-item active"
    print(request)

    return render(request, 'category.html', {
        'cats': cats,
        'articles': articles,
        'category':category,
        'pages':pages,
        'page_number':int(page_number)
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

