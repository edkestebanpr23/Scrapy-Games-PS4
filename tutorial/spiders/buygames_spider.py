import scrapy

class QuotesSpider(scrapy.Spider):
    name = "buygames"

    def start_requests(self):
        url = 'https://www.buygames.ps/en/ps4-games'
        yield scrapy.Request(url, self.parse)
        

    def parse(self, response):
        
        for quote in response.css('li.ajax_block_product'): # Iterando sobre el array de todos los juegos de una pagina
            urlGame = quote.css('div.product-container div.left-block div.product-image-container a::attr(href)').get()
            title = quote.css('div.right-block h2 a::attr(title)').get()
            if urlGame is not None:
                # yield scrapy.Request(str(urlGame), self.page)
                yield {
                    'url': urlGame,
                    'title' : title
                }

        next_page = 'https://www.buygames.ps' + response.css('li#pagination_next a::attr(href)').get()
        print(next_page)
        if next_page is not None:
            yield response.follow(next_page)

   