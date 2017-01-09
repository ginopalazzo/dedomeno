import scrapy
from idealista.items import CommercialItem


class CommercialSpider(scrapy.Spider):
    name = "commercial"
    custom_settings = {
        'ITEM_PIPELINES': {
            'idealista.pipelines.PropertyPipeline': 300,
            'idealista.pipelines.CommercialPipeline': 400
        }
    }
    start_urls = [
        'https://www.idealista.com/venta-terrenos/madrid-provincia/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/alava/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/albacete-provincia/?ordenado-por=fecha-publicacion-desc',
    ]

    def parse(self, response):
        # parse every property in the list
        for item in response.xpath('//a[@class="item-link "]/@href').extract():
            item_page = response.urljoin(item)
            yield scrapy.Request(item_page, callback=self.parse_property_commercial)
        # next page definition: Siguiente. Follow each page
        next_page = response.xpath('//a[@class="icon-arrow-right-after"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_property_commercial(self, response):
        ''' Will parse all the commercial atributes and return a commercialItem object.
        '''
        commercial = CommercialItem()
        title = response.xpath('//span[@class="txt-bold"]/text()')
        # PROPERTY fields
        commercial['title'] = title.extract_first()
        commercial['price_raw'] = int("".join((response.xpath('//p[@class="price"]/text()')[0].re('(\d)'))))
        commercial['source'] = 'idealista'
        commercial['url'] = response.url
        commercial['slug'] = 'id-' + response.url.split("/")[4]
        commercial['transaction'] = title.re('(Alquiler|venta)')[0].lower()
        # commercial['html'] = response.text
        commercial['desc'] = response.xpath('//div[@class="adCommentsLanguage expandable"]/text()').extract_first()
        commercial['name'] = response.xpath('//div[@class="advertiser-data txt-soft"]/p/text()').extract_first()
        commercial['phones'] = response.xpath('//p[@class="txt-big txt-bold _browserPhone"]/text()').extract()
        commercial['address_raw'] = ".".join(response.xpath('//div[@id="addressPromo"]/ul/li/text()').extract())
        commercial['real_estate_raw'] = response.xpath('//a[@class="about-advertiser-name"]/@href').extract_first()
        # COMMERCIAL fields
        # Basic
        basic = response.xpath('//div[h2/text()="Características básicas"]/ul/li/text()')
        commercial['transfer_price'] = response.xpath('//div[@class="details-block clearfix"]/p[@class="more-details"]/text()').re('Traspaso\spor\s([0-9]*[.]?[0-9]+)\s€')
        commercial['m2_total'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sconstruidos')
        commercial['m2_to_use'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sútiles')
        commercial['m2_terrain'] = basic.re('Parcela de (.+) m²')
        commercial['num_of_floors'] = basic.re('([0-9]*[.]?[0-9]+)\splanta')
        commercial['distribution'] = "".join(basic.re('Distribución\s(.+)')).strip().lower()
        commercial['location'] = "".join(basic.re('Situado\s(.+)')).strip().lower()
        commercial['corner'] = bool(basic.re('(ace esquina)'))
        commercial['show_windows'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sescaparate')
        commercial['last_activity'] = "".join(basic.re('ltima\sactividad:\s(.+)')).strip().lower()
        commercial['preservation'] = "".join(basic.re('(buen estado|para reformar)'))
        commercial['wc'] = basic.re('([0-9]*[.]?[0-9]+)\saseos\so\sbaños')
        # Building
        building = response.xpath('//div[h2/text()="Edificio"]/ul/li/text()')
        commercial['floor_num'] = "".join(building.re('Planta\s(\d+)|(Bajo)|(Sótano)|(Semi-Sótano)|(Entreplanta)'))
        commercial['facade'] = "".join(building.re('Fachada\sde\s(\.+)'))
        # Equipment
        equipment = response.xpath('//div[h2/text()="Equipamiento"]/ul/li/text()')
        commercial['air_conditioning'] = bool(equipment.re('(ire acondicionado)'))
        commercial['alarm_system'] = bool(equipment.re('(stema de alarma)'))
        commercial['store_room'] = bool(equipment.re('(lmacén)'))
        commercial['heating'] = bool(equipment.re('(alefacci)'))
        commercial['kitchen'] = bool(equipment.re('(ocina)'))
        commercial['security_door'] = bool(equipment.re('(uerta de seguridad)'))
        commercial['smoke_extractor'] = bool(equipment.re('(alida de humos)'))
        yield commercial

    '''
    # Traspaso
    Traspaso por 100.000 €
    # Características básicas
    160 m² construidos, 140 m² útiles
    200 m² construidos
    1 planta
    8 plantas
    Distribución 1-2 estancias
    Distribución 3-5 estancias
    Distribución 5-10 estancias
    Distribución más de 10 estancias
    Distribución diáfana
    Situado en centro comercial
    Situado a pie de calle
    Situado en entreplanta
    Situado en subterráneo
    Hace esquina


    8 escaparates
    1 escaparates

    Última actividad: licencia C-1
    Última actividad: otras
    Última actividad: Bar - Restaurante
    Última actividad: Tienda de alimentación
    Última actividad: automoción

    Segunda mano/buen estado
    Segunda mano/para reformar

    2 aseos o baños
    8 aseos o baños

    # Edificio
    Bajo
    Sótano
    Entreplanta
    Planta 6ª
    Fachada de 1 a 4 m.
    Fachada de 5 a 8 m.
    Fachada de 9 a 12 m.
    Fachada de más de 12 m.

    Certificación energética: en trámite
    Certificación energética:  (218 kwh/m³ año)
    # Equipamiento
    Calefacción
    Salida de humos
    Aire acondicionado
    Almacén/archivo
    Cocina completamente equipada
    Puerta de seguridad
    Sistema de alarma
    '''
