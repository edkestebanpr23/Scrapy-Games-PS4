import scrapy

class QuotesSpider(scrapy.Spider):
    name = "games" # Nombre de la araña, es un id

    def start_requests(self):
        url = 'https://www.gamesmen.com.au/video-games/ps4/games/'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        
        for quote in response.css('li.item'): # Iterando sobre el array de todos los juegos de una pagina
            if quote.css('p.product-name a::text').get() is not None:
                urlGame = quote.css('p.product-name a::attr(href)').get() # Se obtiene el url de cada juego de una pagina

                yield scrapy.Request(str(urlGame), self.page) # Invocando el metodo page para que lea la página enviada

        # Este bloque hace que se pueda iterar entre todas las paginas (1, 2, 3, ... , n) que tenga la "pagina web"
        next_page = response.css('a.next::attr(href)')[0].get()
        print(next_page)
        if next_page is not None:
            yield response.follow(next_page) # Esto le indica que el mismo contenido continúa en otra página

    def page(self, response):
        # Obtener genero
        datosGenero = response.css('tbody > tr > th::text').getall()
        indexGenre = datosGenero.index('Genre')
        
        genre = str(response.css('tbody > tr > td::text').getall()[indexGenre]).strip()

        # Obtener otros datos
        datos = response.css('div.attributelinkscontainer > div > div.gmdividerred h2::text').getall()
        valores = response.css('div.attributelinkscontainer > div > div.attributelinks')


        classification = None
        publisher = None

        if 'Classification' in datos:
            indexCla = datos.index('Classification')
            classification = valores[indexCla].css('span > img::attr(title)').get()

        if 'Publisher' in datos:
            indexPub = datos.index('Publisher')
            publisher = valores[indexPub].css('a > img::attr(title)').get()

        # Este yield es quien va concatenando los datos y los va metiendo en un json
        yield {
            'title': response.css('div.product-name h1::text').get(),
            'url' : response.url,
            'developer' : response.css('div.attributelinkscontainer > div > div.attributelinks a::attr(title)').get(),
            'genre' : genre,
            'classification' : classification,
            'publisher' : publisher
        }


    