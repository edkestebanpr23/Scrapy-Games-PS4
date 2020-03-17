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

                yield scrapy.Request(urlGame, self.parse2, title, urlGame)
                
                # yield {
                #     'title': title,
                #     'url' : urlGame,
                #     'otro' : x
                # # 'author': quote.css('small.author::text').get(),
                # }

        # next_page = response.css('a.next::attr(href)')[0].get()
        # print(next_page)
        # if next_page is not None:
        #     yield response.follow(next_page)
    # def callback(title):


    def parse2(self, response, title, urlGame):
        # title = response.css('div.product-name h1::text').get()
        # return title
        yield {
            'title': title,
            'url' : urlGame,
            'otro' : 'Hola'
        # 'author': quote.css('small.author::text').get(),
        }