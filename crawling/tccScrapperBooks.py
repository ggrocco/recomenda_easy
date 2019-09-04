#coding: utf-8
import scrapy

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
				callback=self.parse
			)
	def extractValues(self, response):
		NOME_CSS = 'section.description h1.title ::text'
		AUTOR_CSS = 'ul.info a ::text'
		EDITORA_CSS = '//section[@id="product-details"]//ul[@class="details-column"]//li[contains(b,"Editora")]/a/text()'
		SINOPSE_CSS = '.content ::text'
		ANO_CSS = '//section[@id="product-details"]//ul[@class="details-column"]//li[contains(b,"Ano")]/text()[2]'
		ISBN_CSS = '//section[@id="product-details"]//ul[@class="details-column"]//li[contains(b,"ISBN")]/text()[2]'
		COD_BARRAS_CSS = u'//section[@id="product-details"]//ul[@class="details-column"]//li[contains(b,"Código de Barras")]/text()[2]'
		return{
			'NOME'       : response.css(NOME_CSS).extract_first().strip(),
			'AUTOR'      : response.css(AUTOR_CSS).extract_first().strip(),
			'EDITORA'    : response.xpath(EDITORA_CSS).extract_first().strip(),
			'SINOPSE'    : response.css(SINOPSE_CSS).extract_first().strip(),
			'ANO'        : response.xpath(ANO_CSS).extract_first().strip(),
			'ISBN'       : response.xpath(ISBN_CSS).extract_first().strip(),
			'COD_BARRAS' : response.xpath(COD_BARRAS_CSS).extract_first().strip(),
		}


