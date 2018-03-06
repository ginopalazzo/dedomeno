# -*- coding: utf-8 -*-

# Scrapy settings for idealista project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import sys
import os
import django
from decouple import config, Csv


# ------------ DJANGO SETTINGS ------------
# sys.path.insert(0, BASE_DIR+'/dedomeno')
sys.path.append('../dedomeno')
os.environ['DJANGO_SETTINGS_MODULE'] = 'dedomeno.settings'
django.setup()

BOT_NAME = 'idealista'

SPIDER_MODULES = ['idealista.spiders']
NEWSPIDER_MODULE = 'idealista.spiders'


LOG_LEVEL = 'INFO'


# ------------ CRAWLER SETTINGS ------------
'''
# ----- Polite Idealista crawl settings ----
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'
# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1
# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.8
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 10
# CONCURRENT_REQUESTS_PER_IP = 1
# Disable cookies (enabled by default)
COOKIES_ENABLED = False
# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False
# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#    'Accept-Language': 'en',
# }
# Retry many times since proxies often fail
RETRY_TIMES = 4
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
# Enables o disables the redirect
REDIRECT_ENABLED = False
# Closes the spider if n errors occurred
CLOSESPIDER_ERRORCOUNT = 10
'''

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'
# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1  # !
# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothcdrottle settings and docs
DOWNLOAD_DELAY = 0.04  # With the rotator proxies (DOUBLE CHECK!!) #!
#! DOWNLOAD_DELAY = 0.6
# ---- HOME ----
# CONCURRENT_REQUESTS = 1
# DOWNLOAD_DELAY = 0.6
# --------------
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 10
# CONCURRENT_REQUESTS_PER_IP = 1
# Disable cookies (enabled by default)
COOKIES_ENABLED = False
# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False
# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#    'Accept-Language': 'en',
# }
# Retry many times since proxies often fail
RETRY_TIMES = 4
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
# Enables o disables the redirect
REDIRECT_ENABLED = False
# Closes the spider if n errors occurred
CLOSESPIDER_ERRORCOUNT = 10

# ------------ SPIDER MIDDLEWARES SETTINGS ------------
# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#     'idealista.middlewares.IdealistaSpiderMiddleware': 543,
# }


# ------------ DOWNLOADER MIDDLEWARES SETTINGS ------------
# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    # check if its works without RedirectMiddleware
    # 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    # 'idealista.idealistamiddlewares.redirect.RedirectMiddleware': 1,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 80,
    'idealista.middlewares.RotatorProxy': 90,  #!
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'idealista.middlewares.RandomUserAgentMiddleware': 120,
}
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html


# ------------ EXTENSIONS SETTINGS ------------
# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#     'scrapy.extensions.telnet.TelnetConsole': None,
#     'scrapy.extensions.closespider.CloseSpider': 500,
# }


# ------------ PROXIES SETTINGS ------------
# Proxy mode
# 0 = Every requests have different proxy
# 1 = Take only one proxy from the list and assign it to every requests
# 2 = Put a custom proxy to use in the settings
# 3 = List of custom proxy, every request have different proxy
# PROXY_MODE = 3
# If proxy mode is 2 uncomment this sentence :
# CUSTOM_PROXY = "http://ginopalazzo:***REMOVED***@fr.proxymesh.com:31280"
# If proxy mode is 3 uncomment this sentence :
# PROXY_LIST = '/Users/ginopalazzo/Magic/dedomeno-proyect/scrappers/houses/idealista/idealista/proxy_list.txt'
BLACKLIST_HTTP_STATUS_CODES = [307]

'''
CUSTOM_PROXY_LIST = [
    'http://user:pass@111.111.111.111:00000',
    'http://user:pass@ip:port'
]
'''
CUSTOM_PROXY_LIST = config('SCRAPY_CUSTOM_PROXY_LIST', cast=Csv())


# ------------ PIPELINES SETTINGS ------------
# Configure item pipelines: * Configuration per Spider
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
    # 'idealista.pipelines.RealEstatePipeline': 200,
    # 'idealista.pipelines.HousePipeline': 300,
#}


# ------------ AUTOTHROTTLE SETTINGS ------------
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = False
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 20
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True


# ------------ HTTP CACHING SETTINGS ------------
# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# ------------ EMAIL WARNING SETTINGS ------------
# The gmail account will be use to send the warning emails to the recipient
GMAIL_USER = config('SCRAPY_GMAIL_USER')
GMAIL_PASSWORD = config('SCRAPY_GMAIL_PASSWORD')
RECIPIENT = config('SCRAPY_RECIPIENT')


# ------------ IDEALISTA SETTINGS ------------
# Dictionary with the url scheme of idealista to compose urls
IDEALISTA_URL_SCHEME = {
    'source': 'Idealista',
    'country': 'spain',
    'url': 'https://www.idealista.com/',
    'rent': 'alquiler',
    'rent_transaction': {
        'house': 'viviendas',
        'room': 'habitacion',
        'office': 'oficinas',
        'commercial': 'locales',
        'garage': 'garajes',
        'land': 'terrenos',
        'storeroom': 'trasteros',
        'building': 'edificios',
    },
    'sale': 'venta',
    'sale_transaction': {
        'house': 'viviendas',
        'office': 'oficinas',
        'commercial': 'locales',
        'garage': 'garajes',
        'land': 'terrenos',
        'storeroom': 'trasteros',
        'building': 'edificios',
    },
    'separator': '-',
    'municipality': 'municipios',
    'query_pub_date': '?ordenado-por=fecha-publicacion-desc',
    'pro': 'pro',
    'real estate': 'agencias-inmobiliarias',
    'provinces': {
        'a coruña': 'a-coruna-provincia',
        'alava': 'alava',
        'albacete': 'albacete-provincia',
        'alicante': 'alicante',
        'almeria': 'almeria-provincia',
        'asturias': 'asturias',
        'avila': 'avila-provincia',
        'badajoz': 'badajoz-provincia',
        'baleares': 'balears-illes',
        'barcelona': 'barcelona-provincia',
        'burgos': 'burgos-provincia',
        'caceres': 'caceres-provincia',
        'cadiz': 'cadiz-provincia',
        'cantabria': 'cantabria',
        'castellon': 'castellon',
        'ceuta': 'ceuta-provincia',
        'ciudad real': 'ciudad-real-provincia',
        'cordoba': 'cordoba-provincia',
        'cuenca': 'cuenca-provincia',
        'gerona': 'girona-provincia',
        'granada': 'granada-provincia',
        'guadalajara': 'guadalajara-provincia',
        'guipuzcoa': 'guipuzcoa',
        'huelva': 'huelva-provincia',
        'huesca': 'huesca-provincia',
        'jaen': 'jaen-provincia',
        'la rioja': 'la-rioja',
        'las palmas': 'las-palmas',
        'leon': 'leon-provincia',
        'lerida': 'lleida-provincia',
        'lugo': 'lugo-provincia',
        'madrid': 'madrid-provincia',
        'malaga': 'malaga-provincia',
        'melilla': 'melilla-provincia',
        'murcia': 'murcia-provincia',
        'navarra': 'navarra',
        'ourense': 'ourense-provincia',
        'palencia': 'palencia-provincia',
        'pontevedra': 'pontevedra-provincia',
        'salamanca': 'salamanca-provincia',
        'tenerife': 'santa-cruz-de-tenerife-provincia',
        'segovia': 'segovia-provincia',
        'sevilla': 'sevilla-provincia',
        'soria': 'soria-provincia',
        'tarragona': 'tarragona-provincia',
        'teruel': 'teruel-provincia',
        'toledo': 'toledo-provincia',
        'valencia': 'valencia-provincia',
        'valladolid': 'valladolid-provincia',
        'vizcaya': 'vizcaya',
        'zamora': 'zamora-provincia',
        'zaragoza': 'zaragoza-provincia',
    },
    'provinces_ine': {
        '02': {
            'name_official': 'Albacete',
            'name_dedomeno': 'albacete',
            'name-idealista': 'albacete-provincia',
        },
        '03': {
            'name_official': 'Alicante/Alacant',
            'name_dedomeno': 'alicante',
            'name-idealista': 'alicante',
        },
        '04': {
            'name_official': 'Almería',
            'name_dedomeno': 'almeria',
            'name-idealista': 'almeria-provincia',
        },
        '01': {
            'name_official': 'Araba/Álava',
            'name_dedomeno': 'alava',
            'name-idealista': 'alava',
        },
        '33': {
            'name_official': 'Asturias',
            'name_dedomeno': 'asturias',
            'name-idealista': 'asturias',
        },
        '05': {
            'name_official': 'Ávila',
            'name_dedomeno': 'avila',
            'name-idealista': 'avila-provincia',
        },
        '06': {
            'name_official': 'Badajoz',
            'name_dedomeno': 'badajoz',
            'name-idealista':'badajoz-provincia',
        },
        '07': {
            'name_official': 'Balears, Illes',
            'name_dedomeno': 'baleares',
            'name-idealista': 'balears-illes',
        },
        '08': {
            'name_official': 'Barcelona',
            'name_dedomeno': 'barcelona',
            'name-idealista': 'barcelona-provincia',
        },
        '48': {
            'name_official': 'Bizkaia',
            'name_dedomeno': 'vizcaya',
            'name-idealista': 'vizcaya',
        },
        '09': {
            'name_official': 'Burgos',
            'name_dedomeno': 'burgos',
            'name-idealista': 'burgos-provincia',
        },
        '10': {
            'name_official': 'Cáceres',
            'name_dedomeno': 'caceres',
            'name-idealista': 'caceres-provincia',
        },
        '11': {
            'name_official': 'Cádiz',
            'name_dedomeno': 'cadiz',
            'name-idealista': 'cadiz-provincia',
        },
        '39': {
            'name_official': 'Cantabria',
            'name_dedomeno': 'cantabria',
            'name-idealista': 'cantabria',
        },
        '12': {
            'name_official': 'Castellón/Castelló',
            'name_dedomeno': 'castellon',
            'name-idealista': 'castellon',
        },
        '13': {
            'name_official': 'Ciudad Real',
            'name_dedomeno': 'ciudad real',
            'name-idealista': 'ciudad-real-provincia',
        },
        '14': {
            'name_official': 'Córdoba',
            'name_dedomeno': 'cordoba',
            'name-idealista': 'cordoba-provincia',
        },
        '15': {
            'name_official': 'Coruña, A',
            'name_dedomeno': 'a coruña',
            'name-idealista': 'a-coruna-provincia',
        },
        '16': {
            'name_official': 'Cuenca',
            'name_dedomeno': 'cuenca',
            'name-idealista': 'cuenca-provincia',
        },
        '20': {
            'name_official': 'Gipuzkoa',
            'name_dedomeno': 'guipuzcoa',
            'name-idealista': 'guipuzcoa',
        },
        '17': {
            'name_official': 'Girona',
            'name_dedomeno': 'gerona',
            'name-idealista': 'girona-provincia',
        },
        '18': {
            'name_official': 'Granada',
            'name_dedomeno': 'granada',
            'name-idealista': 'granada-provincia',
        },
        '19': {
            'name_official': 'Guadalajara',
            'name_dedomeno': 'guadalajara',
            'name-idealista': 'guadalajara-provincia',
        },
        '21': {
            'name_official': 'Huelva',
            'name_dedomeno': 'huelva',
            'name-idealista': 'huelva-provincia',
        },
        '22': {
            'name_official': 'Huesca',
            'name_dedomeno': 'huesca',
            'name-idealista': 'huesca-provincia',
        },
        '23': {
            'name_official': 'Jaén',
            'name_dedomeno': 'jaen',
            'name-idealista': 'jaen-provincia',
        },
        '24': {
            'name_official': 'León',
            'name_dedomeno': 'leon',
            'name-idealista': 'leon-provincia',
        },
        '25': {
            'name_official': 'Lleida',
            'name_dedomeno': 'lerida',
            'name-idealista': 'lleida-provincia',
        },
        '27': {
            'name_official': 'Lugo',
            'name_dedomeno': 'lugo',
            'name-idealista': 'lugo-provincia',
        },
        '28': {
            'name_official': 'Madrid',
            'name_dedomeno': 'madrid',
            'name-idealista': 'madrid-provincia',
        },
        '29': {
            'name_official': 'Málaga',
            'name_dedomeno': 'malaga',
            'name-idealista': 'malaga-provincia',
        },
        '30': {
            'name_official': 'Murcia',
            'name_dedomeno': 'murcia',
            'name-idealista': 'murcia-provincia',
        },
        '31': {
            'name_official': 'Navarra',
            'name_dedomeno': 'navarra',
            'name-idealista': 'navarra',
        },
        '32': {
            'name_official': 'Ourense',
            'name_dedomeno': 'ourense',
            'name-idealista': 'ourense-provincia',
        },
        '34': {
            'name_official': 'Palencia',
            'name_dedomeno': 'palencia',
            'name-idealista': 'palencia-provincia',
        },
        '35': {
            'name_official': 'Palmas, Las',
            'name_dedomeno': 'las palmas',
            'name-idealista': 'las-palmas',
        },
        '36': {
            'name_official': 'Pontevedra',
            'name_dedomeno': 'pontevedra',
            'name-idealista': 'pontevedra-provincia',
        },
        '26': {
            'name_official': 'Rioja, La',
            'name_dedomeno': 'la rioja',
            'name-idealista': 'la-rioja',
        },
        '37': {
            'name_official': 'Salamanca',
            'name_dedomeno': 'salamanca',
            'name-idealista': 'salamanca-provincia',
        },
        '38': {
            'name_official': 'Santa Cruz de Tenerife',
            'name_dedomeno': 'tenerife',
            'name-idealista': 'santa-cruz-de-tenerife-provincia',
        },
        '40': {
            'name_official': 'Segovia',
            'name_dedomeno': 'segovia',
            'name-idealista': 'segovia-provincia',
        },
        '41': {
            'name_official': 'Sevilla',
            'name_dedomeno': 'sevilla',
            'name-idealista': 'sevilla-provincia',
        },
        '42': {
            'name_official': 'Soria',
            'name_dedomeno': 'soria',
            'name-idealista': 'soria-provincia',
        },
        '43': {
            'name_official': 'Tarragona',
            'name_dedomeno': 'tarragona',
            'name-idealista': 'tarragona-provincia',
        },
        '44': {
            'name_official': 'Teruel',
            'name_dedomeno': 'teruel',
            'name-idealista': 'teruel-provincia',
        },
        '45': {
            'name_official': 'Toledo',
            'name_dedomeno': 'toledo',
            'name-idealista': 'toledo-provincia',
        },
        '46': {
            'name_official': 'Valencia/València',
            'name_dedomeno': 'valencia',
            'name-idealista': 'valencia-provincia',
        },
        '47': {
            'name_official': 'Valladolid',
            'name_dedomeno': 'valladolid',
            'name-idealista': 'valladolid-provincia',
        },
        '49': {
            'name_official': 'Zamora',
            'name_dedomeno': 'zamora',
            'name-idealista': 'zamora-provincia',
        },
        '50': {
            'name_official': 'Zaragoza',
            'name_dedomeno': 'zaragoza',
            'name-idealista': 'zaragoza-provincia',
        },
        '51': {
            'name_official': 'Ceuta',
            'name_dedomeno': 'ceuta',
            'name-idealista': 'ceuta-provincia',
        },
        '52': {
            'name_official': 'Melilla',
            'name_dedomeno': 'melilla',
            'name-idealista': 'melilla-provincia',
        },
    },
}
