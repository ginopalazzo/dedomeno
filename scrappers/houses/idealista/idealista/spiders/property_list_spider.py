import scrapy
from idealista.items import PropertyListItem
from datetime import date


class PropertyListSpider(scrapy.Spider):
    name = "property_list"
    custom_settings = {
        'ITEM_PIPELINES': {
            'idealista.pipelines.ListPipeline': 300
        }
    }
    start_urls = [
        # 'https://www.idealista.com/venta-garajes/madrid-provincia/?ordenado-por=fecha-publicacion-desc',
    ]

    def parse(self, response):
        # parse every property in the list
        items = response.xpath('//div[@class="item-info-container"]')
        for item in items:
            property_list = PropertyListItem()
            url_ext = item.xpath('.//a[@class="item-link "]/@href').extract_first()
            property_list['slug'] = 'id-' + url_ext.split("/")[2]
            property_list['url'] = response.urljoin(url_ext)
            property_list['price'] = int("".join((item.xpath('.//span[@class="item-price"]/text()').re('(\d)'))))
            property_list['date'] = date.today().strftime("%Y-%m-%d")
            yield property_list
        # next page definition: Siguiente. Follow each page
        next_page = response.xpath('//a[@class="icon-arrow-right-after"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
