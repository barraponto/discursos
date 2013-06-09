from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose


class DiscursosItem(Item):
    data = Field()
    sessao = Field()
    fase = Field()
    discurso = Field()
    sumario = Field()
    orador = Field()
    hora = Field()
    publicacao = Field()


class DiscursosItemLoader(XPathItemLoader):
    default_item_class = DiscursosItem
    default_input_processor = MapCompose(lambda value: value.strip())
    default_output_processor = TakeFirst()
