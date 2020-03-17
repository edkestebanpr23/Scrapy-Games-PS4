import scrapy

# class QuotesSpider(scrapy.Spider):
#     name = "games"

#     def start_requests(self):
#         url = 'http://quotes.toscrape.com/'
#         tag = getattr(self, 'tag', None)
#         if tag is not None:
#             url = url + 'tag/' + tag
#         yield scrapy.Request(url, self.parse)

#     def parse(self, response):
#         for quote in response.css('div.quote'):
#             yield {
#                 'text': quote.css('span.text::text').get(),
#                 'author': quote.css('small.author::text').get(),
#             }

#         next_page = response.css('li.next a::attr(href)').get()
#         if next_page is not None:
#             yield response.follow(next_page, self.parse)

class QuotesSpider(scrapy.Spider):
    name = "games"

    def start_requests(self):
        url = 'https://www.gamesmen.com.au/video-games/ps4/games/'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('li.item'): # Iterando sobre el array de todos los juegos de una pagina
            if quote.css('p.product-name a::text').get() is not None:
                urlGame = quote.css('p.product-name a::attr(href)').get()
                title = quote.css('p.product-name a::text').get()

                yield scrapy.Request(str(urlGame), self.page)

        # next_page = response.css('a.next::attr(href)')[0].get()
        # print(next_page)
        # if next_page is not None:
        #     yield response.follow(next_page)

    def page(self, response):
        # Obtener genero
        datosGenero = response.css('tbody > tr > th::text').getall()
        indexGenre = datosGenero.index('Genre')
        # genre = str(response.css('tbody > tr > td::text').getall()[indexGenre]).strip()

        # Obtener otros datos
        # datos = response.css('div.attributelinkscontainer > div > div.gmdividerred h2::text').getall()

        # Desarrollador
        # indexDeveloper = datos.index('Developer')

        yield {
            'title': response.css('div.product-name h1::text').get(),
            'url' : response.url,
            'developer' : response.css('div.attributelinkscontainer > div > div.attributelinks a::attr(title)').get()
        }


    