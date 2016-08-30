from flask import Flask
from flask import render_template
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import sys
app = Flask(__name__)
app.debug = False

client = MongoClient('localhost', 27017)
db = client.nytimes
collection = db.articles_info
cursor = db.articles_info.find()
all_articles = []
for article in cursor:
  all_articles.append(article)

def get_url_soup_content(url):
  response = requests.get(url)
  if response.ok:
    return BeautifulSoup(response.text)

def find_article(article_id,articles):
  for article in articles:
      if article['id'] == article_id:
          return article

def find_most_similar_articles(article,articles,similar_cnt = 5):
  cnt = 1
  suggestions = []
  sorted_similars = ((k, article['similar_docs'][k]) for k in sorted(article['similar_docs'], key = article['similar_docs'].get, reverse=True))
  for k,v in sorted_similars:
      found_article = find_article(k,articles)
      if found_article['section'] != "Paid Death Notices":
          suggestions.append(found_article)
          cnt += 1
      if cnt == 10:
          break
  return suggestions

@app.route('/')
@app.route('/<article>')
def start(article=None):
  if article is not None:
    displayed_article = article
  else:
    displayed_article = all_articles[0]

  suggestions = find_most_similar_articles(displayed_article, all_articles)
  suggestion1 = suggestions[0]
  suggestion2 = suggestions[1]
  suggestion3 = suggestions[2]
  suggestion4 = suggestions[3]
  suggestion5 = suggestions[4]

  soup = get_url_soup_content(displayed_article['url'])
  #Headline
  headline = soup.body.find('h1',{'id':'story-heading'}).text
  #Author
  author = soup.body.find('span',{'class':'byline-author'}).text
  #Date
  date = soup.body.find('time',{'itemprop':'datePublished'}).text
  #Paragraphs
  paragraphs = soup.body.find_all('p',{'itemprop':'articleBody'})
  new_paragraphs = ''
  for i in range(len(paragraphs)):
      new_paragraphs += ("<p>" + paragraphs[i].text + "</p>")
  
  summary = displayed_article['summary']
  return render_template('index.html',headline = headline, author = author, date = date, article = new_paragraphs, summary = summary, suggestion1 = suggestion1, suggestion2 = suggestion2, suggestion3 = suggestion3, suggestion4 = suggestion4, suggestion5 = suggestion5)
  

@app.route('/<article>')
def call_article(name):
  return re
if __name__ == '__main__':
  app.run()