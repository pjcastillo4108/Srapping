
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    amenities = Field()

# CLASE CORE - Al querer hacer extraccion de multiples paginas, heredamos de CrawlSpider
class TripAdvisor(CrawlSpider):
    name = 'hotelestripadvisor'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = ['tripadvisor.com']

    # Url semilla a la cual se hara el primer requerimiento
    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    # Tiempo de espera entre cada requerimiento. Nos ayuda a proteger nuestra IP.
    download_delay = 2

    # Tupla de reglas para direccionar el movimiento de nuestro Crawler a traves de las paginas
    rules = (
        Rule( # Regla de movimiento VERTICAL hacia el detalle de los hoteles
            LinkExtractor(
                allow=r'/Hotel_Review-' # Si la URL contiene este patron, haz un requerimiento a esa URL
            ), follow=True, callback="parse_hotel"), # El callback es el nombre de la funcion que se va a llamar con la respuesta al requerimiento hacia estas URLs
    )

    # Funcion a utilizar con MapCompose para realizar limpieza de datos
    def quitarDolar(self, texto):
        return texto.replace("$", "")

    # Callback de la regla
    def parse_hotel(self, response):
        sel = Selector(response)

        item = ItemLoader(Hotel(), sel)
        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('precio', './/div[@class="hotels-hotel-offers-DominantOffer__price--D-ycN"]/text()',
                        MapCompose(self.quitarDolar))
        # Utilizo Map Compose con funciones anonimas
        # PARA INVESTIGAR: Que son las funciones anonimas en Python?
        item.add_xpath('descripcion', '//div[contains(@class, "hotel-review-about-csr-Description__description")]/div/text()',
                       MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
        item.add_xpath('amenities',
                       '//div[contains(@class, "hotels-hr-about-amenities-Amenity__amenity--3fbBj")]/text()')
        yield item.load_item()

# EJECUCION
# scrapy runspider 1_tripadvisor.py -o tripadvisor.csv -t csv
