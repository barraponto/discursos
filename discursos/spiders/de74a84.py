from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from discursos.items import DiscursosItemLoader


class De74a84Spider(CrawlSpider):
    name = 'de74a84'
    allowed_domains = ['camara.gov.br']
    start_urls = ['http://www.camara.gov.br/internet/SitaqWeb/'
                  'PesquisaDiscursosAvancada.asp']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'CurrentPage'),
             callback='parse_item', follow=True),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.initial_query)

    def initial_query(self, response):
        # Fix a typo in the original markup
        response = response.replace(
            body=response.body.replace('"name="', 'name="'))
        return FormRequest.from_response(
            response, formname='PesqDiscursos',
            formdata={'dtInicio': '01/01/1974', 'dtFim': '31/12/1984',
                      'TipoOrdenacao': 'ASC', 'PageSize': '50'})

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        selector = HtmlXPathSelector(response)
        for sel in selector.select('//table[contains(@class, "tabela-1")]'
                                   '/tbody/tr[not(@id)]'):
            loader = DiscursosItemLoader(selector=sel)
            loader.add_xpath('data', 'td[1]/text()')
            loader.add_xpath('sessao', 'td[2]/text()')
            loader.add_xpath('fase', 'td[3]/text()')
            loader.add_xpath('discurso', 'td[4]/text()')
            loader.add_xpath('orador', 'td[6]/text()')
            loader.add_xpath('hora', 'td[7]/text()')
            loader.add_xpath('publicacao', 'td[8]/a/text()')
            loader.add_xpath('sumario', 'string(following-sibling::tr[@id])')
            yield loader.load_item()
