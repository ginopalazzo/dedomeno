# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from fake_useragent import UserAgent
from scrapy.exceptions import IgnoreRequest
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import random
import re
import base64
import logging

log = logging.getLogger(__name__)


class RandomUserAgentMiddleware(object):
    ''' Create a new random user agent for every proxy
        if RANDOM_UA_PER_PROXY=True
    '''
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_backup = self.loadUserAgents()
        self.per_proxy = crawler.settings.get('RANDOM_UA_PER_PROXY', False)
        self.proxy2ua = {}

    def loadUserAgents(self):
        """
        uafile : string
            path to text file of user agents, one per line
            use as a backup if UserAgent() is not online
        """
        module_dir = os.path.dirname(__file__)  # get current directory
        uafile = os.path.join(module_dir, 'user_agents.txt')
        uas = []
        with open(uafile, 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    uas.append(ua.strip()[1: - 1 - 1])
        random.shuffle(uas)
        return uas

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        if self.per_proxy:
            proxy = request.meta.get('proxy')
            if proxy not in self.proxy2ua:
                try:
                    self.proxy2ua[proxy] = self.ua.random
                except Exception:
                    print('HELLOOOOOOOOOO')
                    self.proxy2ua[proxy] = random.choice(self.ua_backup)
                log.debug('Assign User-Agent %s to Proxy %s' % (self.proxy2ua[proxy], proxy))
            request.headers.setdefault('User-Agent', self.proxy2ua[proxy])
        else:
            try:
                request.headers.setdefault('User-Agent', self.ua.random)
            except Exception:
                print('BYEEEEEEE')
                request.headers.setdefault('User-Agent', random.choice(self.ua_backup))


# log = logging.getLogger('scrapy.proxies')

class RotatorProxy(object):
    def __init__(self, settings):
        self._num_pages = 0
        self._http_status_codes = settings.get('BLACKLIST_HTTP_STATUS_CODES', [307])
        custom_proxy_list = settings.get('CUSTOM_PROXY_LIST')
        self.proxies = []
        for line in custom_proxy_list:
            parts = re.match('(\w+://)(\w+:\w+@)?(.+)', line.strip())
            if not parts:
                continue
            # Cut trailing @
            if parts.group(2):
                user_pass = parts.group(2)[:-1]
            else:
                user_pass = ''
            self.proxies.append((parts.group(1) + parts.group(3), user_pass))
        log.info('proxies: %s' % str(self.proxies))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if 'proxy' in request.meta:
            if request.meta["exception"] is False:
                return
        request.meta["exception"] = False
        # check if all the proxies are blocked
        if len(self.proxies) == 0:
            reason = 'All proxies are unusable, cannot proceed. Exit at url %s' % request.url
            self._send_mail(reason, "Dedomeno - All proxies are unusable")
            raise ValueError('All proxies are unusable, cannot proceed')
        # make the FIFO operation
        proxy = self.proxies.pop(0)
        self.proxies.append(proxy)
        proxy_address = proxy[0]
        proxy_user_pass = proxy[1]
        # use the proxy selected
        if proxy_user_pass:
            request.meta['proxy'] = proxy_address
            basic_auth = 'Basic ' + base64.b64encode(proxy_user_pass.encode()).decode()
            request.headers['Proxy-Authorization'] = basic_auth
        else:
            log.debug('Proxy user pass not found')
        log.debug('Using proxy <%s>, %d proxies left' % (
            proxy_address, len(self.proxies)))

    def process_response(self, request, response, spider):
        print('   request: %s %s' % (request.url, request.meta))
        print('   response: %s %s' % (response.url, response.status))
        print('   num_pages: %s' % self._num_pages)
        self._num_pages = self._num_pages + 1
        if response.status in self._http_status_codes:
            del self.proxies[-1]
            reason = '  %d in %s . IP %s deleted. %d proxies left' % (response.status, response.url, request.meta['proxy'], len(self.proxies))
            log.warning(reason)
            raise IgnoreRequest(reason)
        return response

    def process_exception(self, request, exception, spider):
        if 'proxy' not in request.meta:
            return
        proxy = request.meta['proxy']
        try:
            if len(self.proxies) is not 0:
                del self.proxies[-1]
        except KeyError:
            pass
        request.meta["exception"] = True
        log.info('Removing failed proxy <%s>, %d proxies left' % (
            proxy, len(self.proxies)))
    '''
    def _stop_and_sleep(self, spider):
        delay = random.randrange(self._sleep_min, self._sleep_max)
        log.info(u'Sleeping {} seconds'.format(delay))
        time.sleep(delay)
        self._num_pages_max = random.randrange(self._pages_min, self._pages_max)
        self._num_pages = 0
        log.info('Waking up... New num_pages_max set to %d' % self._num_pages_max)
    '''
    def _send_mail(self, message, title):
        gmailUser = 'ginopalazzo@gmail.com'
        gmailPassword = '***REMOVED***'
        recipient = 'ginopalazzo@gmail.com'
        log.info("Sending mail with subject: %s to %s ........." % (title, recipient))
        msg = MIMEMultipart()
        msg['From'] = gmailUser
        msg['To'] = recipient
        msg['Subject'] = title
        msg.attach(MIMEText(message))
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, recipient, msg.as_string())
        mailServer.close()
        log.info("Mail sent")
