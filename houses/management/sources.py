# -*- coding: utf-8 -*-

from houses.models import *
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def importAllSources(source_name):
    source = Source.objects.get(source_name=source_name)
    logger.info('START: Import all ' + source_name + ' source logic')
    if source.slug == 'id':
        # Transaction
        source.url_max_request = "https://www.idealista.com/checkvalidation"
        transaction_list = (('rent', 'aquiler'), ('sale', 'venta'))
        for transaction in transaction_list:
            t0 = Transaction.objects.get_or_create(transaction_name=transaction[0], depth_number=0, depth_name='transaction')
            s0 = SourceTransaction.objects.get_or_create(source_transaction_name=transaction[1], source=source, transaction=t0[0])
            # Property
            property_list = (('new construction','obranueva'), ('house', 'viviendas'), ('office', 'oficinas'), ('commercial', 'locales'), ('parking', 'garajes'), ('land', 'terrenos'), ('holliday', 'vacacional'), ('share', 'habitacion'))
            if transaction[0] == 'sale':
                property_list = property_list[:-2]
            for property_name in property_list:
                t1 = Transaction.objects.get_or_create(transaction_name=property_name[0], depth_number=1, depth_name='property', father=t0[0])
                s2 = SourceTransaction.objects.get_or_create(source_transaction_name=property_name[1], source=source, transaction=t1[0])
                # House Type
                house_list = (('flat', 'pisos'), ('chalets', 'chalets'), ('rustic', 'casas-de-pueblo'), ('duplex', 'duplex'), ('attic', 'aticos'), ('locales', 'locales'), ('naves','naves'))
                if property_name[0] == 'office' or property_name[0] == 'parking' or property_name[0] == 'land' or property_name[0] == 'holliday' or property_name[0] == 'share':
                    house_list = ()
                elif property_name[0] == 'house':
                    house_list = house_list[:-2]
                elif property_name[0] == 'new construction':
                    house_list = house_list[:-5]
                elif property_name[0] == 'commercial':
                    house_list = house_list[5:]
                for house_name in house_list:
                    t2 = Transaction.objects.get_or_create(transaction_name=house_name[0], depth_number=2, depth_name='house_type', father=t1[0])
                    s2 = SourceTransaction.objects.get_or_create(source_transaction_name=house_name[1], source=source, transaction=t2[0])
        logger.info('END: Import all ' + source_name + ' source logic')
    else:
        logger.warning('Only Idealista is implemented')
