from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector 
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class Noticia(Item):
    titular = Field()
    descripcion = Field()

class EluniversoSpider(Spider):
    name = "MiSegundoSpider"
    custom_settings = {
        'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36' 
    }
    start_urls = ["https://www.eluniverso.com/deportes"]
    
    def parse(self, response):
        sel = Selector(response)
        noticias = sel.xpath('//div[@class = "view-content"]/div[@class = "posts"]') #Lista
        for noticia in noticias:
            item = ItemLoader(Noticia(), noticia)
            item.add_xpath('titular','.//h2/a/text()')
            item.add_xpath('descripcion','.//p/text()')

            yield item.load_item()
