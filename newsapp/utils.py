import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz,re
from django.utils.text import slugify
from .models import NewsArticle
import textwrap
#NewsArticle.objects.all().delete()
cats=['Finance','Entertainment','Sport','World','Technology','Lifestyle']

def formatme(article):
    sentences = article.split('. ')  # Assuming sentences end with periods
    sentence_count = 0
    paragraph_count = 0

    formatted_paragraphs = []
    for sentence in sentences:
        if sentence_count % 2 == 0 and sentence_count > 0:
            formatted_paragraphs.append('\n')  # Add a line break every 2 sentences
        formatted_paragraphs.append(sentence + '. ')  # Add the sentence with a period
        sentence_count += 1

        if sentence_count % 4 == 0:
            formatted_paragraphs.append('\n\n')  # Add a new paragraph every 4 sentences
            paragraph_count += 1

    formatted_article = ''.join(formatted_paragraphs)
    formatted_article = textwrap.fill(formatted_article, width=100) 
    return formatted_article

def getarticletext(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('div', id='story-primary')
    if main_content:
        processed_content = []
        for paragraph in main_content.find_all('p'):
            excluded_content = re.findall(r'"(.*?)"', paragraph.text)
            cleaned_text = re.sub(r'"(.*?)"', '', paragraph.text)
            rewritten_text = cleaned_text.replace('<br>', '\n')
            processed_paragraph = ' '.join([rewritten_text] + excluded_content)
            processed_content.append(processed_paragraph)
        final_content = '\n'.join(processed_content)
        final_content=str(final_content)
        NewsArticle.objects.filter(link=url, story="").update(story=final_content)
        return final_content

def getarticle(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    soup2=soup.find('div', id='story-primary')
    #print(soup)
    if not soup2:return [f"<a href={url}>{url}</a>"]
    content_list = [str(tag) for tag in soup2.find_all(['p', 'img'])]
    #print(content_list)
    newlist=[]
    for i in content_list:
        if i.startswith('<p'):
            if "storyblock_standfirst g_font-body-s" not in i and "footer_apps" not in i:
                newlist.append(i)
        elif i.startswith('<img'):
            if "inline" in i:
                soup = BeautifulSoup(i, 'html.parser')
                img = soup.find('img')
                img['width'] = '100%'
                img['height'] = 'auto'
                newlist.append(str(img))
    #newlist = '\n'.join(newlist)
    NewsArticle.objects.filter(link=url, story="").update(story=newlist)
    return newlist

def fetch_and_store_articles(category):
    url = f'https://www.news.com.au/content-feeds/latest-news-{category.lower()}/'
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'xml')
    articles = soup.find_all('item')
    for article in articles:
        title = article.title.get_text()
        if not NewsArticle.objects.filter(title=title).exists():
            new_article = NewsArticle(
                title=title,
                subtitle=article.subtitle.get_text(),
                tag=article.category.get_text(),
                category=category,
                link=article.link.get_text(),
                image=article.url.get_text().split('?')[0] + '?width=1280',
                date=datetime.now(pytz.timezone('Australia/Sydney')),
                description=article.description.get_text(),
                url=f"article/{slugify(title)}")
            new_article.save()

def update():
    for cat in cats:
        fetch_and_store_articles(category=cat)