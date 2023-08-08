import requests
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz,re
from django.utils.text import slugify
import json


link="https://www.news.com.au/sport/afl/nrl-linked-to-afl-grand-final-rejection-as-mindblowing-saviour-firms/news-story/5713c317268985ba1777496d1d9d2e7d"
def getarticle(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    soup2=soup.find('div', id='story-primary')
    #print(soup)
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
    for i in newlist:
        print(i)
    return newlist

def getarticle2(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    soup2=soup.find('div', id='story-primary')
    #print(soup)
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
    #NewsArticle.objects.filter(link=url, story="").update(story=newlist)
    return newlist

def getvideo(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'lxml')
    soup2=soup.find('script',type="application/ld+json")
    #print(soup2)
    script_content = soup2.string.strip()
    json_data = json.loads(script_content)
    main_entity_id = json_data["mainEntityOfPage"]["@id"]
    return(main_entity_id)
    #print(soup)
 
def getvideo2(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'lxml')
    #print(soup2)
    print(soup)
    return 
    script_content = soup2.string.strip()
    json_data = json.loads(script_content)
    main_entity_id = json_data["mainEntityOfPage"]["@id"]
    return(main_entity_id)
    #print(soup)   


link=(getvideo(link))
print(link)
print(getvideo2(link))
exit()

def format(article):
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
    return formatted_article

testtext="""More than $500 million worth of Sydney housing development projects are set to hit the market as fugitive property developer Jean Nassif’s empire crumbles. The Sydney Morning Herald reports thousands of apartment owners living in Toplace buildings are concerned that there will be no money left to fix millions of dollars worth of defects as major lenders move to sell Toplace assets to recoup their losses. “The owners’ worst fear … is that any legitimate claim or opportunity to claw back funds for defective work is gobbled up by secured creditors,” said a source close to one of the owner’s corporations told the publication. According to the SMH, court documents revealed Mr Nassif’s collapsed property empire has debts of more than $1.24 billion, including $88.5 million to suppliers and tradespeople. A source close to one of the lenders told the publication that, having taken control of the assets, the receivers are preparing to go to sale and “that process is expected to commence soon”. The lenders are also concerned that they will be charged default penalty interest rates of up to 30 per cent now that Toplace has gone into administration. In March, insolvency firm KordaMentha was appointed as the receiver and manager of the firms run by Jean Nassif. The companies are responsible for the giant Skyview apartment complex in Sydney’s north west. Tenants were initially barred from moving into the 900 unit block built by Mr Nassif in Castle Hill after signs of cracking were found in the complex’s basement. Mr Nassif is listed as a director of both 51 OCHR and JKN Finance which are the owners and developers of the Skyview towers. Toplace was the builder of Skyview. Last month it was revealed, Mr Nassif’s building firm Toplace Pty Ltd had collapsed into administration with ASIC. The company filed for voluntary administration through lawyers in contact with Mr Nassif. Antony Resnick and Suelen McCallum of insolvency firm DVT Group are the appointed administrators. They are only in charge of the building arm of Toplace Group, not any of the other streams of the business. News.com.au contacted them for comment. Toplace Pty Ltd has been in operation since 1992 and claims to have built 30,000 abodes over those years, including residential houses and apartments, shopping centres and commercial offices. The firm reportedly has not been able to function as a company for some time after losing its building licence due to failing to fix serious defects at a Sydney apartment complex. The NSW Civil and Administrative Tribunal (NCAT) stripped it of its licence after failing to comply with a court order. In June, NSW Police issued an arrest warrant for Mr Nassif in relation to fraud-related charges. Mr Nassif is understood to be living overseas. Police believe the 55-year-old has not been in the country for months, since at least December. Strike Force Calool was established in April 2021 to investigate his alleged financial crimes. Detective Superintendent Peter Faux said in June that police were yet to engage overseas governments or law enforcement agencies in their search, but would do so after there was more clarity on where he could be. “If he is offshore and overseas then we’ll commence the appropriate conversations with those people in relation to that,” he said. “We’ve only just applied for the arrest warrant. We’re now looking at those options in relation to if he is offshore.” Meanwhile, Mr Nassif’s daughter, Ashlyn Nassif, has had her legal practising certificate suspended while she fights allegations she used fake contracts to secure a $150m loan. The 29-year-old is accused of falsifying $10.5m in pre-sale contracts for the development of the $900m Sky View apartment complex in northwest Sydney. The partner of law firm EA Legal was charged with dishonestly obtaining financial advantage by deception and publishing false or misleading material. She was granted bail in March with $2.6m secured by her family. Earlier this year, Mr Nassif was called to front a NSW parliamentary inquiry into allegations of impropriety at Hills Shire Council, but declined to attend as he said he would be in a remote part of Lebanon conducting business and recuperating from a medical procedure, and had intended to be overseas until March 2023. - with NCA Newswire As the fallout from the PwC scandal continues, the federal government has announced a raft of major changes in response to crackdown on tax misconduct. China’s decision to repeal costly tariffs is ‘mutually beneficial’, but wasn’t a transaction for a visit from Albo, the government says. After three years of tension and challenges, Beijing will immediately wind back its tariffs on a major Australian export.. """
print(format(testtext))


# Create an SQLite database
engine = create_engine('sqlite:///news_articles2.db', echo=True)

# Define a base class for declarative models
Base = declarative_base()

# Define the NewsArticle model
class NewsArticle(Base):
    __tablename__ = 'news_article4'
    title = Column(String(255),primary_key=True)
    subtitle = Column(Text)
    tag = Column(String(50))
    category = Column(String(50))
    link = Column(String(255))
    image = Column(String(255))
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)
    url = Column(Text,default='#')
    

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

server_articles = session.query(NewsArticle).all()
title_list = session.query(NewsArticle.title).all()

category="Finance"
tags=set()
myarticles=[]
query = category
url = f'https://www.news.com.au/content-feeds/latest-news-{category.lower()}/'
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, 'xml')
articles=soup.find_all('item')

# Create a new NewsArticle instance and add it to the session
for article in articles:
	print(article)
	article = NewsArticle(
    title=article.title.get_text(),
    subtitle=article.subtitle.get_text(),
    tag=article.category.get_text(),
    category=category,
    link=article.link.get_text(),
    image=article.url.get_text().split('?')[0]+'?width=1280',
    date=datetime.now(pytz.timezone('Australia/Sydney')),
    description=article.description.get_text(),
    url=f"article/{article.title.get_text().replace(' ','_')}"
	)
	if article.title not in str(title_list):
		session.add(article)
		session.commit()
	else: 
		print('already loaded')
		continue

# Query and print all articles from the database
articles = session.query(NewsArticle).all()
for article in articles:
    print(article.link)

# Close the session
session.close()

