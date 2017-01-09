import scrapy
from idealista.items import OfficeItem


class OfficeSpider(scrapy.Spider):
    name = "office"
    custom_settings = {
        'ITEM_PIPELINES': {
            'idealista.pipelines.PropertyPipeline': 300,
            'idealista.pipelines.OfficePipeline': 400
        }
    }
    start_urls = [
        'https://www.idealista.com/alquiler-oficinas/madrid-provincia/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/alava/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/albacete-provincia/?ordenado-por=fecha-publicacion-desc',
    ]

    def parse(self, response):
        # parse every property in the list
        for item in response.xpath('//a[@class="item-link "]/@href').extract():
            item_page = response.urljoin(item)
            yield scrapy.Request(item_page, callback=self.parse_property_office)
        # next page definition: Siguiente. Follow each page
        next_page = response.xpath('//a[@class="icon-arrow-right-after"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_property_office(self, response):
        ''' Will parse all the office atributes and return a officeItem object.
        '''
        office = OfficeItem()
        title = response.xpath('//span[@class="txt-bold"]/text()')
        # PROPERTY fields
        office['title'] = title.extract_first()
        office['price_raw'] = int("".join((response.xpath('//p[@class="price"]/text()')[0].re('(\d)'))))
        office['source'] = 'idealista'
        office['url'] = response.url
        office['slug'] = 'id-' + response.url.split("/")[4]
        office['transaction'] = title.re('(Alquiler|venta)')[0].lower()
        # office['html'] = response.text
        office['desc'] = response.xpath('//div[@class="adCommentsLanguage expandable"]/text()').extract_first()
        office['name'] = response.xpath('//div[@class="advertiser-data txt-soft"]/p/text()').extract_first()
        office['phones'] = response.xpath('//p[@class="txt-big txt-bold _browserPhone"]/text()').extract()
        office['address_raw'] = ".".join(response.xpath('//div[@id="addressPromo"]/ul/li/text()').extract())
        office['real_estate_raw'] = response.xpath('//a[@class="about-advertiser-name"]/@href').extract_first()
        # OFFICE fields
        # Basic
        basic = response.xpath('//div[h2/text()="Características básicas"]/ul/li/text()')
        office['m2_total'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sconstruidos')
        office['m2_to_use'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sútiles')
        office['m2_terrain'] = basic.re('Parcela de (.+) m²')
        office['num_of_floors'] = basic.re('Oficina\sde\s([0-9]*[.]?[0-9]+)\spiso')
        office['distribution'] = "".join(basic.re('Distribución\s(.+)')).strip().lower()
        office['kitchen'] = bool(basic.re('ocina'))
        office['wc'] = basic.re('([0-9]*[.]?[0-9]+)\s[ba][as][ñe]')
        office['wc_location'] = "".join(basic.re('(dentro|fuera)'))
        office['orientation'] = basic.re('(norte|sur|este|oeste)')
        office['garage'] = bool(basic.re('(garaje incluid)'))
        office['preservation'] = "".join(basic.re('(buen estado|para reformar)'))
        # Building
        building = response.xpath('//div[h2/text()="Edificio"]/ul/li/text()')
        office['floor_num'] = "".join(building.re('Planta\s(\d+)|(Bajo)|(Sótano)|(Semi-Sótano)|(Entreplanta)'))
        office['outside'] = "".join(building.re('(exterior|interior)'))
        office['elevators'] = building.re('([0-9]*[.]?[0-9]+)\sascensor')
        office['office_type'] = "".join(building.re('(mixto|exclusivo)'))
        office['janitor'] = bool(building.re('(Conserje)'))
        office['access_control'] = bool(building.re('(ontrol de accesos)'))
        office['security_system'] = bool(building.re('(istema de seguridad)'))
        office['security_door'] = bool(building.re('(uerta de seguridad)'))
        office['fire_extinguishers'] = bool(building.re('(xtintores)'))
        office['fire_detectors'] = bool(building.re('(etectores de incendios)'))
        office['sprinklers'] = bool(building.re('(spersores)'))
        office['fire_door'] = bool(building.re('(uerta cortafuegos)'))
        office['emergency_exit'] = bool(building.re('(alida de emergencia)'))
        office['emergency_exit_lights'] = bool(building.re('(uces de salida emergencia)'))
        # Equipment
        equipment = response.xpath('//div[h2/text()="Equipamiento"]/ul/li/text()')
        office['store_room'] = bool(equipment.re('(archivo)'))
        office['hot_water'] = bool(equipment.re('(gua caliente)'))
        office['heating'] = bool(equipment.re('(alefacción)'))
        office['air_conditioning_cold'] = bool(equipment.re('(de frío)'))
        office['air_conditioning_hot'] = bool(equipment.re('(calor)'))
        office['double_glazed_windows'] = bool(equipment.re('(doble acristalamiento)'))
        office['false_ceiling'] = bool(equipment.re('(also techo)'))
        office['false_floor'] = bool(equipment.re('(also suelo)'))
        yield office

    '''
    100 m² construidos
    50 m² construidos, 45 m² útiles
    Oficina de 3 pisos

    Segunda mano/buen estado
    Distribución diáfana
    Distribución tabicada
    Cocina/office
    4 baños y aseos completos fuera de la oficina
    1 aseos completos dentro de la oficina
    1 baños
    2 baños o aseos completos
    Orientación norte, sur, este, oeste
    1 plaza de garaje incluida en el precio

    # Edificio
    Planta 3ª
    Bajo exterior
    Bajo interior
    Entreplanta exterior
    Planta 1ª exterior
    Edificio de 21 plantas
    Edificio de 7 plantas
    2 ascensores
    1 ascensor
    Uso mixto oficina
    Uso exclusivo de oficinas
    Conserje
    Conserje y control de accesos
    Sistema de seguridad
    Puerta de seguridad
    Extintores
    Detectores de incendios
    Aspersores
    Puerta cortafuegos
    Salida de emergencia
    Luces de salida emergencia
    Certificación energética:  (IPE no indicado)
    #Equipamiento
    Agua caliente
    Calefacción
    Aire acondicionado de frío
    Aire acondicionado de frío/calor
    Ventanas con doble acristalamiento
    Falso techo
    Falso suelo

    '''
