import scrapy
from idealista.items import GarageItem, RealEstateItem
from houses.models import Date, Price, Garage, RealEstate
from datetime import date


class GarageSpider(scrapy.Spider):
    name = "garage2"
    custom_settings = {
        'ITEM_PIPELINES': {
            'idealista.pipelines.PropertyPipeline': 300,
            'idealista.pipelines.GaragePipeline': 400,
            'idealista.pipelines.DatePipeline': 500,
            'idealista.pipelines.PricePipeline': 600
        }
    }
    start_urls = [
        'https://www.idealista.com/alquiler-garajes/bilbao-vizcaya/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/alava/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/albacete-provincia/?ordenado-por=fecha-publicacion-desc',
    ]

    def parse(self, response):
        # parse every property in the list
        for item in response.xpath('//div[@class="item-info-container"]'):
            item_page = response.urljoin(item.xpath('.//a[@class="item-link "]/@href').extract_first())
            slug = 'id-' + item_page.split("/")[4]
            price = int("".join((item.xpath('.//span[@class="item-price"]/text()')[0].re('(\d)'))))
            garage = Garage.objects.filter(slug=slug).first()
            # check if there is already a garage with that slug
            if garage:
                # check if last price has change
                garage_price = garage.price_set.order_by('-date_start').first()
                if garage_price.value != price:
                    garage_price.date_end = date.today()
                    garage_price.save()
                    Price.objects.create(value=int(price), date_start=date.today(), property_price=garage)
                # check if a property that was offline now is online
                if not garage.online:
                    garage.online = True
                    garage.save()
                    Date.objects.create(online=date.today(), property_date=garage)
                    # new Date
            # if there is not a garage with that slug scrapy it
            else:
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
        # If property has a real estate
        if garage['real_estate_raw']:
            real_estate_slug = 'id-' + garage['real_estate_raw'].split('/')[2]
            real_estate = RealEstate.objects.filter(slug=real_estate_slug)
            # If the real estate is not in de db
            print('AGENCIA1: ' + garage['real_estate_raw'] + ' - ' + str(real_estate))
            if not real_estate:
                real_estate_page = response.urljoin(garage['real_estate_raw'])
                yield scrapy.Request(real_estate_page, callback=self.parse_real_estate, meta={'garage': garage})
                # garage['real_estate'] = request.meta['real_estate']
            else:
                print('ENTRAAAAAAAAAAAAAAAAAAAA')
                garage['real_estate'] = real_estate.first()
                yield garage
        else:
            yield garage

    def parse_real_estate(self, response):
        '''
        will parse all the RealEstate atributes and return a RealEstateItem object
        '''
        real_estate = RealEstateItem()
        real_estate['name'] = response.xpath('//div[@class="office-title"]/h2/text()').extract_first()
        real_estate['slug'] = 'id-' + response.url.split('/')[4]
        logo = response.xpath('//div[@class="logo-branding"]/img/@src').extract_first()
        if logo:
            real_estate['logo'] = 'https:' + logo
        real_estate['web'] = response.xpath('//div[@id="online"]/a/@href').extract_first()
        real_estate['url'] = response.url
        # real_estate['html'] = response.text
        real_estate['desc'] = response.xpath('//p[@class="office-description"]/text()').extract_first()
        real_estate['telephone'] = response.xpath('//*[@class="icon-phone"]/span/text()').extract_first()
        real_estate['address'] = ''.join(response.xpath('//a[@class="showMap icon-location"]/div/span/text()').extract()) + ''.join(response.xpath('//span[@class="regular-address"]/span/text()').extract())
        real_estate['source'] = 'idealista'
        real_estate_ob = real_estate.save()
        garage = response.meta['garage']
        garage['real_estate'] = real_estate_ob
        yield garage
