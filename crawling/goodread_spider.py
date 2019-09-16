#coding: utf-8

import os
import re
import time
import scrapy
import hashlib
from pymongo import MongoClient
from dotenv import load_dotenv

# Carrega as variaves de ambinte.
load_dotenv()

uri = os.environ.get('MONGODB_URI')
client = MongoClient(uri)
database = client.get_database()
db = client['heroku_l5cst43x']
comments = db['books']
ISBN = comments.distinct("ISBN")

REVIRES_STARTS = {"★☆☆☆☆": 1,
                  "★★☆☆☆": 2,
                  "★★★☆☆": 3,
                  "★★★★☆": 4,
                  "★★★★★": 5}

class GoodreadSpider(scrapy.Spider):
  name = "goodread"

  def start_requests(self):
    domain = "https://www.goodreads.com/api/reviews_widget_iframe"
    for isbn in ISBN:
      url = f'{domain}?isbn={isbn}'
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    for review in response.css("div.gr_review_container"):
      avaliador = review.css("span.gr_review_by a::attr(href)").get()
      comment = review.css("div.gr_review_text *::text").getall()
      nota = review.css("span.gr_rating::text").get()
      isbn = re.findall("isbn=(\w*)", response.url)[0]

      data = {
        "AVALIADOR_ID": re.findall("show\/(\w*)\?", avaliador)[0],
        "ISBN": isbn,
        "NOTA": self.nota_parse(nota),
        "COMENTARIO": self.parse_comment(comment),
        "USER_ID": hashlib.md5(avaliador.encode('utf-8')).hexdigest()
      }
      yield data

    time.sleep(2.4)
    print('Dormindo 2.4 sec.')

    # follow the paginate
    for next_href in response.css('a.next_page::attr(href)'):
      yield response.follow(next_href, self.parse)

  def nota_parse(self, nota):
    return REVIRES_STARTS[nota]

  def parse_comment(self, comment):
    list_comments = list(filter(None, map(lambda s: s.strip(), comment)))[0:-1]
    return "\n".join(list_comments)
