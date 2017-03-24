# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from idealista.crawlproperty import CrawlPropertyReactor
import logging

logger = logging.getLogger(__name__)
'''
sudo rabbitmq-server
celery -A dedomeno flower
celery -A dedomeno worker --loglevel=INFO
celery -A dedomeno beat -l info -S django

["palencia", "zaragoza", "barcelona", "valladolid", "las palmas", "cuenca", "melilla", "cordoba", "toledo", "lerida", "leon", "badajoz", "granada", "burgos", "soria", "a coruña", "gerona", "lugo", "ciudad real", "tenerife", "asturias", "baleares", "ourense", "tarragona", "avila", "almeria", "malaga", "la rioja", "valencia", "castellon", "cadiz", "albacete", "alicante", "cantabria", "huelva", "pontevedra", "segovia", "navarra", "jaen", "guadalajara", "salamanca", "zamora", "guipuzcoa", "alava", "murcia", "huesca", "caceres", "vizcaya", "sevilla", "madrid", "teruel", "ceuta"]

{"property_type": "garage", "transaction": "sale", "provinces": ["cuenca", "soria"]}
56 35
{"property_type": "garage", "transaction": "sale", "provinces": ["lugo"]}
63
{"property_type": "garage", "transaction": "sale", "provinces": ["segovia", "melilla"}
67 15
{"property_type": "garage", "transaction": "sale", "provinces": ["zamora"]}
80

house rent -{a coruna, alicante, asturias, barcelon, cadiz, granada, madrid, malaga, murcia, sevilla, valencia}
house sale {separate tasks}
rest

room rent all -{madrid, barcelona} = 1
room rent madrid = 1
room rent barcelona = 1

office rent all -{madrid, barcelona} = 1
office rent madrid = 1
office rent barcelona = 1
office sale all = 1

commercial rent all -{madrid, barcelona, alicante, malaga, sevilla, valencia, vizcaya}
commercial sale all -{madrid, barcelona, malaga, sevilla, valencia, vizcaya}
1 rest

garage sale all -{madrid, barcelona, alicante, malaga, valencia, vizcaya}
garage rent all -{madrid, barcelona}
1 rest

land sale all -{madrid, barcelona, alicante, valencia}
land rent all
1 rest

'''


@shared_task
def property(property_type, transaction, provinces):
    #for province in provinces:
    #    CrawlPropertyReactor(property_type=property_type, transaction=transaction, province=province).run()
    spider = CrawlPropertyReactor(property_type=property_type, transaction=transaction, provinces=provinces)
    stats = spider.conf()
    spider.run()
    return stats
    # p = CrawlPropertyReactor(property_type=property_type, transaction=transaction, province=provinces)
    # print(p.getIdealistaProvinces())
    # p.run()
    # p.stop()
