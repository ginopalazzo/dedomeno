import scrapy
from idealista.items import RealEstateItem


class RealEstateSpider(scrapy.Spider):
    name = "real_estate"
    custom_settings = {
        'ITEM_PIPELINES': {
            'idealista.pipelines.RealEstatePipeline': 400
        }
    }
    start_urls = [
        'https://www.idealista.com/venta-viviendas/albacete-provincia/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/alava/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/albacete-provincia/?ordenado-por=fecha-publicacion-desc',
    ]

    def parse(self, response):
        '''
        will parse all the RealEstate atributes and return a RealEstateItem object
        '''
        real_estate = RealEstateItem()
        real_estate['name'] = response.xpath('//div[@class="office-title"]/h2/text()').extract_first()
        real_estate['slug'] = 'id-' + response.url.split('/')[4]
        real_estate['logo'] = 'https:' + response.xpath('//div[@class="logo-branding"]/img/@src').extract_first()
        real_estate['web'] = response.xpath('//div[@id="online"]/a/@href').extract_first()
        real_estate['url'] = response.url
        # real_estate['html'] = response.text
        real_estate['desc'] = response.xpath('//p[@class="office-description"]/text()').extract_first()
        real_estate['telephone'] = response.xpath('//*[@class="icon-phone"]/span/text()').extract_first()
        real_estate['address'] = ''.join(response.xpath('//a[@class="showMap icon-location"]/div/span/text()').extract()) + ''.join(response.xpath('//span[@class="regular-address"]/span/text()').extract())
        real_estate['source'] = 'idealista'
        yield real_estate
