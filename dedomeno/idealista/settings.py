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

# ------------ DJANGO SETTINGS ------------
# sys.path.insert(0, BASE_DIR+'/dedomeno')
sys.path.append('../dedomeno')
os.environ['DJANGO_SETTINGS_MODULE'] = 'dedomeno.settings'
django.setup()

BOT_NAME = 'idealista'

SPIDER_MODULES = ['idealista.spiders']
NEWSPIDER_MODULE = 'idealista.spiders'


LOG_LEVEL = 'WARNING'


# ------------ CRAWLER SETTINGS ------------
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
    # 'idealista.middlewares.RotatorProxy': 100,
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
CUSTOM_PROXY_LIST = [
    'http://accounts1:YM5wTvgN@157.52.158.2:60099',
    'http://accounts1:YM5wTvgN@157.52.158.3:60099',
    'http://accounts1:YM5wTvgN@157.52.158.6:60099',
    'http://accounts1:YM5wTvgN@157.52.158.13:60099',
    'http://accounts1:YM5wTvgN@157.52.158.15:60099',
    'http://accounts1:YM5wTvgN@157.52.158.16:60099',
    'http://accounts1:YM5wTvgN@157.52.158.17:60099',
    'http://accounts1:YM5wTvgN@157.52.158.19:60099',
    'http://accounts1:YM5wTvgN@157.52.158.20:60099',
    'http://accounts1:YM5wTvgN@157.52.158.26:60099',
    'http://accounts1:YM5wTvgN@157.52.158.32:60099',
    'http://accounts1:YM5wTvgN@157.52.158.35:60099',
    'http://accounts1:YM5wTvgN@157.52.158.37:60099',
    'http://accounts1:YM5wTvgN@157.52.158.40:60099',
    'http://accounts1:YM5wTvgN@157.52.158.41:60099',
    'http://accounts1:YM5wTvgN@157.52.158.42:60099',
    'http://accounts1:YM5wTvgN@157.52.158.43:60099',
    'http://accounts1:YM5wTvgN@157.52.158.48:60099',
    'http://accounts1:YM5wTvgN@157.52.158.49:60099',
    'http://accounts1:YM5wTvgN@157.52.158.50:60099',
    'http://accounts1:YM5wTvgN@157.52.158.51:60099',
    'http://accounts1:YM5wTvgN@157.52.158.52:60099',
    'http://accounts1:YM5wTvgN@157.52.158.53:60099',
    'http://accounts1:YM5wTvgN@157.52.158.57:60099',
    'http://accounts1:YM5wTvgN@157.52.158.61:60099'
]


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
GMAIL_USER = 'ginopalazzo@gmail.com'
GMAIL_PASSWORD = '***REMOVED***'
RECIPIENT = 'ginopalazzo@gmail.com'


# ------------ IDEALISTA SETTINGS ------------
# Dictionary with the url scheme of idealista to compose urls
IDEALISTA_URL_SCHEME = {
    'source': 'Idealista',
    'url': 'https://www.idealista.com/',
    'rent': 'alquiler',
    'rent_transaction': {
        'house': 'viviendas',
        'room': 'habitacion',
        'office': 'oficinas',
        'commercial': 'locales',
        'garage': 'garajes',
        'land': 'terrenos',
    },
    'sale': 'venta',
    'sale_transaction': {
        'house': 'viviendas',
        'office': 'oficinas',
        'commercial': 'locales',
        'garage': 'garajes',
        'land': 'terrenos',
    },
    'separator': '-',
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
    }
}
