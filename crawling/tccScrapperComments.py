#coding: utf-8
import scrapy
import json

class BrickSetSpider(scrapy.Spider):
	name = "brickset_spider"
	start_urls = ['https://www.livrariacultura.com.br/busca?N=102831&Ntt=']

	def parse(self, response):
		SET_SELECTOR = '.product-ev-box'
		for brickset in response.css(SET_SELECTOR):
			IMAGE_SELECTOR = 'div.main-prod-img-ev a ::attr(href)'
			yield response.follow(brickset.css(IMAGE_SELECTOR).extract_first(), callback=self.extractValues)		
		CURRENT_PAGE_SELECTOR = '.pagination li a.selected ::text'			
		CURRENT_PAGE = response.css(CURRENT_PAGE_SELECTOR).extract_first()
		CURRENT_PAGE_NUMBER = int(CURRENT_PAGE, 10)			
		NEXT_PAGE_NUMBER = CURRENT_PAGE_NUMBER + 1			
		NEXT_PAGE_SELECTOR = './/ul[@class="pagination"]/li/a[text()="'+str(NEXT_PAGE_NUMBER)+'"]/@href'
		NEXT_PAGE_LINK = response.xpath(NEXT_PAGE_SELECTOR).extract_first()
		if NEXT_PAGE_LINK:
			yield scrapy.Request(
				response.urljoin('https://www.livrariacultura.com.br/'+NEXT_PAGE_LINK),
				callback=self.parse,				
			)
	def extractValues(self, response):		
		ISBN_CSS = '//section[@id="product-details"]//ul[@class="details-column"]//li[contains(b,"ISBN")]/text()[2]'
		ISBN = response.xpath(ISBN_CSS).extract_first().strip()
		bookUrl = response.url
		token = bookUrl.split('-')
		stream = token[len(token)-1]
		url = 'https://comments.us1.gigya.com/comments.getComments?categoryID=ProductsRatingReview&streamID=' + stream + '&includeSettings=true&sort=dateDesc&threaded=true&includeStreamInfo=true&includeUserOptions=true&includeUserHighlighting=true&lang=pt-br&ctag=comments_v2&APIKey=3_3Mez5cLsMYm3EyiqY7w8i7fsPMonWe3pXEf29pFJTmxgG7pHbKZd0ytLh4KeenVe&cid=&source=showCommentsUI&sourceData=%7B%22categoryID%22%3A%22ProductsRatingReview%22%2C%22streamID%22%3A%221807897%22%7D&sdk=js_latest&authMode=cookie&format=jsonp&callback=gigya.callback&context=R1045086062'
		yield response.follow(url, callback = self.extractComments, meta = {"ISBN" : ISBN})
	def extractComments(self, response):
		parsed_json = json.loads(response.text.replace('"\r\n});','"}').replace('gigya.callback(',''))		
		for comment in parsed_json['comments']:
			try:
			    AVALIADOR_ID = comment['sender']['profileURL']
			except KeyError:
			    AVALIADOR_ID = 'ANONIMO'
			yield{
				'ISBN'         : response.meta["ISBN"],
				'AVALIADOR_ID' : AVALIADOR_ID,
				'NOTA' 	       : comment['ratings']['_overall'],
				'COMENTARIO'   : comment['commentText'],
			}
