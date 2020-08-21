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

class Tripadvisor(CrawlSpider):
    name = "Hoteles"
    custom_settings = {
        'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36' 
    }
    start_urls = ["https://www.tripadvisor.com/Hotels-g294305-Santiago_Santiago_Metropolitan_Region-Hotels.html"]
    download_delay = 2

    allowed_domains = ['tripadvisor.com']

    rules = (
        Rule(
            LinkExtractor(
                allow = r'/Hotel_Review-'
            ), follow = True, callback = "parse_hotel"
        ),
    )

    def quitarsimbolopeso(self, texto):
        nuevo_texto = texto.replace("\u00a0", " ").replace("\n","").replace("\t","").strip()
        return nuevo_texto 

    def parse_hotel(self, response):
        sel = Selector(response)
        item = ItemLoader(Hotel(),sel)

        item.add_xpath("nombre", 
         "//h1[@id = 'HEADING']/text()")
        item.add_xpath("precio",
         ".//div[contains(@class, '_36QMXqQj')]/text()",
         MapCompose(self.quitarsimbolopeso))
        item.add_xpath("descripcion",
         "//div[contains(@class, '_2f_ruteS _1bona3Pu _2-')]/div[1]/text()" )
        #item.add_xpath("amenities",
        #  "//div[@class = '_1nAmDotd'][1]//div[@class = '_2rdvbNSg0]/text()")

        yield item.load_item()


