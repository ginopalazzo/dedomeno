import scrapy
from idealista.items import GarageItem


class GarageSpider(scrapy.Spider):
    name = "garage"
    custom_settings = {
        'ITEM_PIPELINES': {
            'idealista.pipelines.PropertyPipeline': 300,
            'idealista.pipelines.GaragePipeline': 400
        }
    }
    start_urls = [
        'https://www.idealista.com/alquiler-garajes/bilbao-vizcaya/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/alava/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/albacete-provincia/?ordenado-por=fecha-publicacion-desc',
    ]

    def parse(self, response):
        # parse every property in the list
        for item in response.xpath('//a[@class="item-link "]/@href').extract():
            item_page = response.urljoin(item)
            yield scrapy.Request(item_page, callback=self.parse_property_garage)
        # next page definition: Siguiente. Follow each page
        next_page = response.xpath('//a[@class="icon-arrow-right-after"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_property_garage(self, response):
        ''' Will parse all the garage atributes and return a garageItem object.
        '''
        garage = GarageItem()
        title = response.xpath('//span[@class="txt-bold"]/text()')
        # PROPERTY fields
        garage['title'] = title.extract_first()
        garage['price_raw'] = int("".join((response.xpath('//p[@class="price"]/text()')[0].re('(\d)'))))
        garage['source'] = 'idealista'
        garage['url'] = response.url
        garage['slug'] = 'id-' + response.url.split("/")[4]
        garage['transaction'] = title.re('(Alquiler|venta)')[0].lower()
        # garage['html'] = response.text
        garage['desc'] = response.xpath('//div[@class="adCommentsLanguage expandable"]/text()').extract_first()
        garage['name'] = response.xpath('//div[@class="advertiser-data txt-soft"]/p/text()').extract_first()
        garage['phones'] = response.xpath('//p[@class="txt-big txt-bold _browserPhone"]/text()').extract()
        garage['address_raw'] = ".".join(response.xpath('//div[@id="addressPromo"]/ul/li/text()').extract())
        garage['real_estate_raw'] = response.xpath('//a[@class="about-advertiser-name"]/@href').extract_first()
        # GARAGE fields
        # Características básicas
        basic = response.xpath('//div[h2/text()="Características básicas"]/ul/li/text()')
        garage['garage_type'] = "".join(basic.re('Plaza\spara\s(.+)')).strip().lower()
        garage['garage_number'] = basic.re('Plaza\snúmero\s([0-9]*[.]?[0-9]+)')
        garage['covered'] = bool(basic.re('(ubierta)'))
        garage['elevator'] = bool(basic.re('(on ascensor)'))
        # Extras
        extra = response.xpath('//div[h2/text()="Extras"]/ul/li/text()')
        garage['automatic_door'] = bool(extra.re('(rta automática de ga)'))
        garage['security_cameras'] = bool(extra.re('(aras de seguridad)'))
        garage['alarm'] = bool(extra.re('(larm)'))
        garage['security_guard'] = bool(extra.re('(al de seguridad)'))
        yield garage
