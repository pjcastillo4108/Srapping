from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector 
from scrapy.loader import ItemLoader

class Pregunta(Item): #Hereda de Item  // #Que a su vez funciona como un diccionario
    id = Field()
    pregunta = Field()
    descripcion = Field()

class StackOverflowSpider(Spider): #Hereda de Spider
    name = 'MiPrimerSpider'
    custom_settings = {
        'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36' 
    }
    start_urls = ['https://stackoverflow.com/questions']
    
    def parse(self, response):
        i = 0
        sel = Selector(response) #Selector me permite hacer consulta a la página
        preguntas = sel.xpath("//div[@id = 'questions']//div[@class = 'question-summary']") #Como son varios valores, se guardan como lista
        for pregunta in preguntas:
            item = ItemLoader(Pregunta(), pregunta) #Clase que recibe como primer parámetro una intancia de mi clase que tiene la abstracción
            item.add_xpath('pregunta', './/h3/a/text()')
            #item.add_xpath('pregunta', ".//div[@class = 'excerpt']/text()")
            item.add_value('id', i)
            i +=1
            yield item.load_item()