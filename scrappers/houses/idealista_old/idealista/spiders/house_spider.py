import scrapy


class HouseSpider(scrapy.Spider):
    name = "house"

    def start_request(self):
        urls = [
            'https://www.idealista.com/venta-viviendas/albacete-provincia/?ordenado-por=fecha-publicacion-desc',
            # 'https://www.idealista.com/venta-viviendas/alava/?ordenado-por=fecha-publicacion-desc',
            # 'https://www.idealista.com/venta-viviendas/albacete-provincia/?ordenado-por=fecha-publicacion-desc',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # parse every property in the list
        for item in response.xpath('//a["item-link"]/@href'):
            item_page = response.urljoin(item)
            print('item_page: ' + item_page)
            yield scrapy.Request(item_page, callback=self.parse_property_house)
        # next page definition: Siguiente
        # <a class="icon-arrow-right-after" href="/venta-viviendas/albacete-provincia/pagina-2.htm?ordenado-por=fecha-publicacion-desc"><span>Siguiente</span></a>
        next_page = response.xpath('//a[class="icon-arrow-right-after"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            print('next_page: ' + next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_property_house(self, response):
        pass
