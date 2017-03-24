# -*- coding: utf-8 -*-

from lxml import html
import requests
from houses.models import *
import logging
from .scrapertoolbelt import *
# from multiprocessing import Pool

# Get an instance of a logger
logger = logging.getLogger(__name__)
# generate a random Agents list
uas = loadUserAgents()


def importAllTerritorialEntities(source_name, country_name):
    """
    Will import all provinces from the main page of the source for a choosen country.
    After that will follow through collectEntities method all children recursively
    """
    TerritorialEntity.objects.all().delete()
    logger.info("START Import all Territorial Entities in " + country_name + ' for ' + source_name + '.')
    country = Country.objects.get(country_name=country_name)
    source = Source.objects.get(source_name=source_name)
    # only implemented for Idealista & Spain
    if source.slug == 'id' and country_name == 'Spain':
        try:
            # collect and compose a tree for a url page
            page = requests.get(source.url, headers=getUserAgent(uas))
            tree = html.fromstring(page.content)
            lista1 = tree.xpath('//div[@class="locations-list clearfix"]/ul/li/a/text()')
            lista2 = tree.xpath('//div[@class="locations-list clearfix"]/ul/li/a/@href')
            # check if there´s data (provinces) to iterate
            if len(lista1) == len(lista2) and len(lista1) != 0 and len(lista2) != 0:
                zip_listas = list(zip(lista1, lista2))
                # iterate for every province
                # pool = Pool(8)
                # [pool.apply_async(collectEntitiesParallel, args=(country, source, pair)) for pair in zip_listas]
                # results = pool.map_async(collectEntitiesParallel, zip_listas)
                for pair in zip_listas:
                    provincia = TerritorialEntity.objects.get_or_create(territorial_entity_name=pair[0], depth_number=0, depth_name='provincia', country=country)
                    url_source_territory = URLSourceTerritory.objects.get_or_create(url_source_territory_name=pair[1].split('/')[2], url_source_territory_name_list=pair[1].split('/')[2], source=source, territory=provincia[0])
                    logger.info("START Import all Territorial Entities and Municipalities in " + pair[0] + '.')
                    collectEntities(country, source, provincia[0], url_source_territory[0], 0)
                    collectMunicipality(country, source, provincia[0], url_source_territory[0])
                    logger.info("END Import all Territorial Entities and Municipalities in " + pair[0] + '.')
                logger.info("END Import all Territorial Entities in " + country_name + ' for ' + source_name + '.')
            else:
                logger.error("list are not equal or are null: There are no Provinces in Idealista.com!!!")
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            logger.error('requests.exceptions.Timeout :' + url)
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            logger.error('requests.exceptions.TooManyRedirects: ' + url)
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            logger.error('requests.exceptions.RequestException: ' + url + ', ' + e)
            sys.exit(1)
    else:
        logger.warning('Only Idealista - Spain is implemented')


def collectEntitiesParallel(pair):
    provincia = TerritorialEntity.objects.get_or_create(territorial_entity_name=pair[0], depth_number=0, depth_name='provincia', country=country)
    url_source_territory = URLSourceTerritory.objects.get_or_create(url_source_territory_name=pair[1].split('/')[2], url_source_territory_name_list=pair[1].split('/')[2], source=source, territory=provincia[0])
    logger.info("START Import all Territorial Entities and Municipalities in " + pair[0] + '.')
    collectEntities(country, source, provincia[0], url_source_territory[0], 0)
    collectMunicipality(country, source, provincia[0], url_source_territory[0])
    logger.info("END Import all Territorial Entities and Municipalities in " + pair[0] + '.')


def collectEntities(country, source, territorial_entity, url_source_territory, depth_number):
    """
    Will collect all entities recursively till reach to entities last depth
    Example of web page for collecting childrens: https://www.idealista.com/venta-viviendas/madrid-provincia/
    """
    # compose the url for sale transaction (there are more houses than in rent)
    sale_transaction = Transaction.objects.get(transaction_name='sale', depth_number=0)
    house_transaction = Transaction.objects.get(transaction_name='house', father=sale_transaction)
    url = source.url + SourceTransaction.objects.get(source=source, transaction=sale_transaction).source_transaction_name + source.separator_url  +  SourceTransaction.objects.get(source=source, transaction=house_transaction).source_transaction_name + '/' + url_source_territory.url_source_territory_name_list + '/'
    try:
        # collect and compose a tree for a url page
        page = requests.get(url, headers=getUserAgent(uas))
        tree = html.fromstring(page.content)
        # Try to collect direct children (no municipality)
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
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        logger.error('requests.exceptions.Timeout: ' + url)
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        logger.error('requests.exceptions.TooManyRedirects: ' + url)
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        logger.error('requests.exceptions.RequestException: ' + url + ', ' + e)
        sys.exit(1)


def composeChildren(children_list, country, source, territorial_entity, url_source_territory, depth_number, municipality):
    """
    Compose and create a list of childrens for a territorial_entity father.
    Then, iterate and collect more entities (collectEntities) for every children.
    """
    for entity_tuple in children_list:
        entity_name = entity_tuple[0].strip()
        entity_url_name = (entity_tuple[1]).split('/')[-2].strip()
        entity_url = '/'.join((entity_tuple[1]).split('/')[2:-1])
        entity_id = entity_tuple[2].strip()
        # print(entity_name, entity_url_name, entity_url, entity_id)
        # create territorial entity & url source asociate
        new_territorial_entity = TerritorialEntity.objects.get_or_create(territorial_entity_name=entity_name, depth_number=depth_number+1, country=country, father=territorial_entity)[0]
        new_url = URLSourceTerritory.objects.get_or_create(url_source_territory_name=entity_url_name, url_source_territory_name_list=entity_url, source=source, territory=new_territorial_entity)[0]
        # if is a municipio
        if municipality:
            new_territorial_entity.depth_name = 'municipio'
            new_territorial_entity.save()
        # Llamada recursiva en profundidad
        collectEntities(country, source, new_territorial_entity, new_url, depth_number + 1)


def collectMunicipality(country, source, province, url_source_territory):
    """
    Check and collect all the Municipalities
    """
    # https://www.idealista.com/venta-viviendas/alava/municipios
    sale_transaction = Transaction.objects.get(transaction_name='sale', depth_number=0)
    house_transaction = Transaction.objects.get(transaction_name='house', father=sale_transaction)
    url = source.url + SourceTransaction.objects.get(source=source, transaction=sale_transaction).source_transaction_name + source.separator_url  +  SourceTransaction.objects.get(source=source, transaction=house_transaction).source_transaction_name + '/' + url_source_territory.url_source_territory_name_list + '/' + 'municipios'
    try:
        # collect and compose a tree for a url page
        page = requests.get(url, headers=getUserAgent(uas))
        tree = html.fromstring(page.content)
        municipality_list_name = tree.xpath('//ul[@id="location_list"]/li/ul/li/a/text()')
        municipality_list_url = tree.xpath('//ul[@id="location_list"]/li/ul/li/a/@href')
        # if there is municipality list page
        if len(municipality_list_name) != 0 and len(municipality_list_url) != 0:
            municipality_list = zip(municipality_list_name, municipality_list_url)
            for municipality in municipality_list:
                # url_source_municipality_name
                municipality_query = TerritorialEntity.objects.filter(country=country, territorial_entity_name=municipality[0])
                if len(municipality_query) == 1:
                    municipality_query.update(depth_name="municipio")
                    URLSourceTerritory.objects.filter(source=source, territory=municipality_query[0]).update(url_source_municipality_name=municipality[1].split('/')[2])
                elif len(municipality_query) == 0:
                    print(municipality[0] + ": Not found")
                else:
                    print(municipality[0] + ": More than 1 result")
                    for m in municipality_query:
                        print(m, m.depth_number)
        else:
            logger.warning('No municipality page found for: ' + url)
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        logger.error('requests.exceptions.Timeout: ' + url)
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        logger.error('requests.exceptions.TooManyRedirects: ' + url)
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        logger.error('requests.exceptions.RequestException: ' + url + ', ' + e)
        sys.exit(1)


def collectBrothers(country, source, territorial_entity, url_source_territory, depth_number, collect_brother):
    # https://www.idealista.com/venta-viviendas/madrid-provincia/mapa
    pass


def checkSourceDisponibility(source, page):
    """
    Check if the source reach to the url_max_request for an IP
    """
    if page.url == Source.url_max_request:
        return false
    else:
        logger.error('Reach the max number of request for this IP in ' + source + ' source.')
        return true
    """
    response = requests.get(someurl)
    if response.history:
        print "Request was redirected"
        for resp in response.history:
            print resp.status_code, resp.url
        print "Final destination:"
        print response.status_code, response.url
    else:
        print "Request was not redirected"
    """
