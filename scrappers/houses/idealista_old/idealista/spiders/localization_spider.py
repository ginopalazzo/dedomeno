import scrapy
from houses.models import Source


class LocalizationSpider(scrapy.Spider):
    # name of the spider
    name = "localization"
    # start of the urls: it gets the url from the django db
    start_urls = [
        Source.objects.get(source_name='Idealista').url
    ]

    def parse(self, response):
        provinces = response.xpath('//div[@class="locations-list clearfix"]/ul/li/a')
        for province in provinces:
            name = province.xpath('.//text()').extract_first().strip()
            url_name = province.xpath('.//@href').extract_first().split('/')[2]
            depth_number = 0
            yield {
                'territorial_entity_name': name,
                'depth_number': depth_number,
                'depth_name': 'provincia',
                'depth_last': False,
                'father': None,
                'url_source_territory_name': url_name,
                'url_source_territory_name_list': url_name
            }
            # next page definition: breadcrumbs
            next_page = 'https://www.idealista.com/venta-viviendas/' + url_name + '/'
            yield scrapy.Request(next_page, callback=self.parse_entities)

    def parse_entities(self, response):
        childrens = response.xpath('//div[@class="breadcrumb-subitems"]/ul/li/ul/li/a')
        print(childrens)
        for children in childrens:
            name = children.xpath('.//text()').extract_first().strip()
            url_name = children.xpath('.//@href').extract_first().split('/')[-2].strip()
            url = children.xpath('.//@href').extract_first().split('/')[2:-1]
            print(name)
            print(url_name)
            print(url)
            # yield {
            #    'territorial_entity_name': name,
            #    'depth_number': depth_number,
            #    'depth_name': '',
            #    'depth_last': False,
            #    'father': None,
            #    'url_source_territory_name': url_name,
            #    'url_source_territory_name_list': url
            # }
            # next_page = 'https://www.idealista.com/venta-viviendas/' + url_name + '/'
            # yield scrapy.Request(next_page, callback=self.parse_entities, depth_number)
        '''
        children_list_name = tree.xpath('//div[@class="breadcrumb-subitems"]/ul/li/ul/li/a/text()')
        children_list_url = tree.xpath('//div[@class="breadcrumb-subitems"]/ul/li/ul/li/a/@href')
        children_list_id = tree.xpath('//div[@class="breadcrumb-subitems"]/ul/li/ul/li/a/@data-location-id')
        children_list = zip(children_list_name, children_list_url, children_list_id)
        # if there is no childrens --> Trt to collect all municipalities
        if len(children_list_name) == 0:
            children_list_name = tree.xpath('//li[@class="select-municipality"]/div/ul/li/a/text()')
            children_list_url = tree.xpath('//li[@class="select-municipality"]/div/ul/li/a/@href')
            children_list_id = tree.xpath('//li[@class="select-municipality"]/div/ul/li/a/@data-location-id')
            children_list = zip(children_list_name, children_list_url, children_list_id)
            # if there is no childrens and no municipalities, we reach the last depth of the tree
            if len(children_list_name) == 0:
                territorial_entity.depth_last = True
                territorial_entity.save()
            else:
                # compose and create the children and call again to this function for every children
                composeChildren(children_list, country, source, territorial_entity, url_source_territory, depth_number, True)
        else:
            # compose and create the children and call again to this function for every children
            composeChildren(children_list, country, source, territorial_entity, url_source_territory, depth_number, False)
        '''
