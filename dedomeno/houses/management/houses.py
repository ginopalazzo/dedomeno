# -*- coding: utf-8 -*-

from lxml import html
import requests
from houses.models import *
import logging
import re
from .scrapertoolbelt import *
from .agencies import *


# Get an instance of a logger
logger = logging.getLogger(__name__)
uas = loadUserAgents()


def importAllhouses(source_name, country_name):
    """
    Will import all the houses for the last depth Territorial Entity
    """
    # https://www.idealista.com/venta-viviendas/castelldefels/el-poal/con-pisos/pagina-2.htm?ordenado-por=fecha-publicacion-desc
    # source + transaction.depth=0 + - + transaction.depth=1 + / + url_source_territory + / con- + transaction.depth=2 + /pagina- + page_num +.htm + ?ordenado-por=fecha-publicacion-desc
    House.objects.all().delete()
    logger.info("START Import all Houses in " + country_name + ' for ' + source_name + '. This will take a while...')
    country = Country.objects.get(country_name=country_name)
    source = Source.objects.get(source_name=source_name)
    # only implemented for Idealista & Spain
    if source.slug == 'id' and country_name == 'Spain':
        territorial_leaves_list = TerritorialEntity.objects.filter(depth_last=True, country=country)
        for territorial_leaf in territorial_leaves_list:
            for transaction1 in Transaction.objects.filter(depth_number=0):
                for transaction2 in Transaction.objects.filter(father=transaction1):
                    # if houses
                    for transaction3 in Transaction.objects.filter(father=transaction2):
                        url_transaction1 = SourceTransaction.objects.filter(source=source, transaction=transaction1).first().source_transaction_name
                        url_transaction2 = SourceTransaction.objects.filter(source=source, transaction=transaction2).first().source_transaction_name
                        url_transaction3 = SourceTransaction.objects.filter(source=source, transaction=transaction3).first().source_transaction_name
                        url_territorial_leaf = URLSourceTerritory.objects.get(source=source, territory=territorial_leaf).url_source_territory_name_list
                        url = source.url + url_transaction1 + source.separator_url + url_transaction2 + '/' + url_territorial_leaf + '/' + 'con-' + url_transaction3
                        collectHouses(source, url, transaction3, territorial_leaf, 1)
                    # elif parking
                    # elif terrain ...
        logger.info("END Import all Houses in " + country_name + ' for ' + source_name + '.')
    else:
        logger.warning('Only Idealista - Spain is implemented')


def collectHouses(source, url_base, transaction, territorial_leaf, page_number):
    """
    For every page in the territorial_leafe agency page collect and compose the House
    /pagina- + page_num +.htm + ?ordenado-por=fecha-publicacion-desc
    """
    url = url_base + '/pagina-' + str(page_number) + '.htm' + '?ordenado-por=fecha-publicacion-desc'
    try:
        # collect and compose a tree for a url page
        page = requests.get(url, headers=getUserAgent(uas))
        tree = html.fromstring(page.content)
        # get the list of houses
        house_list = tree.xpath('//a[@class="item-link "]/@href')
        # check if there is houses in the page
        total = cleanTotal(tree.xpath('//span[@class="h1-simulated"]/text()'))
        if len(house_list) > 0 and len(house_list) != total:
            logger.warning('collectHouses is not getting all the houses in url (' + str(len(house_list)) + ' vs ' + str(total) + '): ' + url)
        if len(house_list) > 0:
            # complete all the houses in the house_list
            for house in house_list:
                completeHouse(source, house.split("/")[2], transaction, territorial_leaf)
            # try to get the next page of houses
            collectHouses(source, url_base, transaction, territorial_leaf, page_number + 1)
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        logger.error('requests.exceptions.Timeout : ' + url)
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        logger.error('requests.exceptions.TooManyRedirects: ' + url)
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        logger.error('requests.exceptions.RequestException: ' + url + ', ' + e)
        sys.exit(1)


# get other data from the house
def completeHouse(source, code, transaction, territory):
    # read html page of the house
    url = source.url + "inmueble/" + code
    page = requests.get(url)
    tree = html.fromstring(page.content)
    # get atributes
    title = tree.xpath('//span[@class="txt-bold"]/text()')[0]
    desc = composeDesc(url, tree)
    price = int("".join(re.compile('(\d)', re.IGNORECASE).findall(tree.xpath('//p[@class="price"]/text()')[0])))
    list_phone = composePhone(tree.xpath('//p[@class="txt-big txt-bold _browserPhone"]/text()'))
    agency_location_source = getOrCreateAgencyLocalizationSource(source, tree.xpath('//a[@class="about-advertiser-name"]/@href'), url, territory)
    # search if there is other houses with diferent Transaction
    other_transaction = findOtherHouseTransaction(tree.xpath('//p[@class="more-details"]/a/@href'))
    house = None
    if other_transaction[0]:
        house = house[1]
    else:
        address = ",".join(tree.xpath('//div[@id="addressPromo"]/ul/li/text()'))
        # compose the house for the source
        house = House.objects.create(territorial_entity=territory, address=address)
        composeAtributesHouse(tree.xpath('//section[@id="details"]/div/ul/li/text()'), house)
    source_house = SourceHouse.objects.get_or_create(source=source, price=price, phone=list_phone[0], phone_2=list_phone[1], transaction_type=transaction, page=page.content, house=house, house_source_id=code, url=url, title=title, desc=desc, is_online=True, is_completed=True)[0]
    print(source_house.house_source_id)
    if agency_location_source is not None:
        source_house.agency_location_source.add(agency_location_source)
        source_house.save()
    # building atributes
    # equipment atributes
    # location
    # price = tree.xpath('//span[@class="txt-big txt-bold"]/text()')
    # deposit = tree.xpath('//span[@class="txt-deposit"]/span[1]/text()')[0]
    # c_house = tree.xpath('//section[@id="details"]/div[3]/ul/li/text()')
    # c_building = tree.xpath('//section[@id="details"]/div[4]/ul/li/text()')
    # c_street = tree.xpath('//div[@id="addressPromo"]/ul/li/text()')
    # c_owner_real_state = tr¡ee.xpath('//a[@class="about-advertiser-name"]/text()') #len=0 ->particular, len=1 ->real_state_name


def composePhone(phones):
    phone_list = ["", ""]
    i = 0
    for phone in phones:
        phone_list[i] = phone.strip()
        i = i + 1
    return phone_list


def findOtherHouseTransaction(other_transaction):
    if len(other_transaction) == 1:
        print('other transaction!!' + str(other_transaction))
        house = House.objects.filter(source_house=(SourceHouse.objects.filter(source=source, url=source.url[:-1] + other_transaction).first())).first()
        if house is not None:
            return (True, house)
        else:
            return (False, None)
    else:
        return (False, None)


# ONLY FOR HOUSES!!
def composeAtributesHouse(a_list, house):
    expresion = "".join(a_list)
    print(expresion)
    # House atributes dictionary
    house_atributes_dic = {
        'house.m2_total': ['(\d+)\sm²\sconstruidos', 'composeDefaultInt'],
        'house.m2_to_use': ['(\d+)\sm²\sútiles', 'composeDefaultInt'],
        'house.m2_terrain': ['Parcela de (.+) m²', 'composeTerrain'],
        'house.rooms': ['(\d+)\shabitaci', 'composeDefaultInt'],
        'house.bathrooms': ['(\d+)\swc', 'composeDefaultInt'],
        'house.flat_num': ['Planta\s(\d+)|(Bajo)|(Sótano)', 'composeFlatNum'],
        'house.outside': ['(exterior|interior)', 'composeOutside'],
        'house.conditions': ['(buen estado|para reformar)', 'composeConditions'],
        'house.orientation': ['(norte|sur|este|oeste)', 'composeOrientation']
    }
    # House equipment dictionary
    house_equipment_dic = {
        'Terrace': '(terraza)',
        'Parking': '(garaje)',
        'Wardrobes': '(armarios)',
        'Storeroom': '(trastero)',
        'Garden': '(jardín)',
        'Air Conditioner': '(aire acondicionado)',
        'Swimmingpool': '(piscina)',
        'Lift': '(con ascensor)',
        'Parking': '(garaje)',
        'Parking': '(garaje)',
        'Equipped Kitchen': '(cocina equipada|totalmente amueblado)',
        'Furnished': '(totalmente amueblado)',
    }
    # Fill the atributes in the house object
    for atribute in house_atributes_dic.keys():
        value = house_atributes_dic.get(atribute)
        exec(atribute + '=' + value[1] + '(re.compile(value[0], re.IGNORECASE).findall(expresion))')
        # print(atribute + ": " + "\t" + value[0])
        # exec("print(" + atribute + ")")
    # Add the equipment item in the house object
    for equipment in house_equipment_dic.keys():
        value = house_equipment_dic.get(equipment)
        regex = re.compile(value, re.IGNORECASE).findall(expresion)
        if len(regex) == 1:
            # print('atribute to insert:' + equipment)
            house.equipment.add(Equipment.objects.filter(equipment_name=equipment).first())
    # Save and return the house
    house.save()
    return house


def composeTerrain(terrain):
    print('terrain ' + str(terrain))
    if len(terrain) == 0:
        return 0
    else:
        regex = re.compile('(\d)', re.IGNORECASE).findall(terrain[0])
        join = "".join(regex)
        return int(join)


def composeDesc(url, tree):
    expandable = len(tree.xpath('//a[@class="expander"]/text()'))
    if expandable == 0:
        desc = tree.xpath('//div[@class="adCommentsLanguage expandable"]/text()')
        if len(desc) == 0:
            return None
        else:
            return desc[0]
    else:
        '''
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        driver = webdriver.Firefox()
        driver.get(url)
        driver.find_element_by_css_selector('.expander').click()
        driver.close()
        '''
        return desc[0]


def composeDefaultString(value):
    return value


def composeDefaultInt(value):
    if len(value) == 1:
        return int(value[0])
    else:
        return None


def composeFlatNum(value):
    if value is None or len(value) == 0:
        return None
    else:
        value = value[0]
        value = "".join(value)
        if(value == 'Bajo'):
            return 0
        elif(value == 'Sótano'):
            return -1
        else:
            return int(value)


def composeOrientation(value):
    orientation_dic = {
        'norte': 'N',
        'este': 'E',
        'sur': 'S',
        'oeste': 'W'
    }
    lista = []
    for item in value:
        lista.append(orientation_dic[item])
    return lista


def composeOutside(value):
    if len(value) == 1:
        if value[0] == 'exterior':
            return True
        elif value[0] == 'interior':
            return False
        else:
            return None
    else:
        return None


def composeConditions(value):
    if len(value) == 1:
        if value[0] == 'buen estado':
            return 'good'
        elif value[0] == 'para reformar':
            return 'bad'
        else:
            return None
    else:
        return None


# clean the total number
def cleanTotal(total):
    if len(total) == 0:
        return 0
    else:
        return int(total[0].strip())
