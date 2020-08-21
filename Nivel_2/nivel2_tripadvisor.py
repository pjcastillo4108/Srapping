from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.spiders import Spider
from scrapy.selector import Selector 
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader import ItemLoader

class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    amenities = Field()

class TripAdvisor(CrawlSpider):
    name = 'Hoteles'
    custom_settings = {
        'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36' 
    }
    start_urls = ['https://www.tripadvisor.com/Hotels-g294305-Santiago_Santiago_Metropolitan_Region-Hotels.html']

    download_delay = 2
    rules = (
        Rule(
            LinkExtractor(
                allow = r'/Hotel_Review-' #Expresiones regulares, r me permite considerar el string como raw, sin carácteres
            ), follow = True, callback = 'parse_hotel' #callback me permite llamar una función cuando se haga un requerimiento a la URL
        ),
    )

    def parse_hotel(self,response):
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)

        item.add_xpath('nombre','//h1[@id = "HEADING"]/text()')
        item.add_xpath('precio','//div[@class = "CEf5oHnZ"]/text()')
        item.add_xpath('descripcion','//div[@class = "2f_ruteS _1bona3Pu _2-hMril5 _2uD5bLZZ"]/div[1]/text()')
        item.add_xpath('amenities','//div[contains(@class, "_2rdvbNSg")]/text()')


