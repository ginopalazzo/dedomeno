# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
# https://pypi.python.org/pypi/fake-useragent
# https://github.com/alecxe/scrapy-fake-useragent
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
    """
    Create a new random user agent for every proxy if RANDOM_UA_PER_PROXY=True
    of a random user agent for every request if RANDOM_UA_PER_PROXY=False
    """
    def __init__(self, crawler):
        """
        Start the attributes of the RandomUserAgentMiddelware
        :param crawler:
        """
        super(RandomUserAgentMiddleware, self).__init__()
        # start a UserAgent object
        self.ua = UserAgent()
        # loads the user agent backup list (if the UserAgent service is offline)
        module_dir = os.path.dirname(__file__)  # get current directory
        self.uafile = os.path.join(module_dir, 'user_agents.txt')
        self.ua_backup = self.load_user_agents()
        # if RANDOM_UA_PER_PROXY = True, assign random user agent per proxy
        self.per_proxy = crawler.settings.get('RANDOM_UA_PER_PROXY', False)
        self.proxy2ua = {}

    def load_user_agents(self):
        """
        use as a backup if UserAgent() is not online
        uafile : string, path to text file of user agents, one per line
        :return: a shuffle usera agent list
        """
        ua_list = []
        with open(self.uafile, 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    ua_list.append(ua.strip()[1: - 1])
        random.shuffle(ua_list)
        return ua_list

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        """
        Process the spider request setting in the header a random user-agent
        :param request: request to be process
        :param spider: spider that makes the request
        :return: None: will continue processing this request, executing all other middlewares
        """
        # if 'RANDOM_UA_PER_PROXY' in scrapy settings is True
        if self.per_proxy:
            # get the proxy information from the request
            proxy = request.meta.get('proxy')
            # try to add the current proxy if it's not in the proxy2ua dictionary
            if proxy not in self.proxy2ua:
                try:
                    self.proxy2ua[proxy] = self.ua.random
                except Exception:
                    self.proxy2ua[proxy] = random.choice(self.ua_backup)
                log.debug('Assign User-Agent %s to Proxy %s' % (self.proxy2ua[proxy], proxy))
            request.headers.setdefault('User-Agent', self.proxy2ua[proxy])
        else:
            try:
                request.headers.setdefault('User-Agent', self.ua.random)
            except Exception:
                # print('Exception with uafile, %s' % self.uafile)
                request.headers.setdefault('User-Agent', random.choice(self.ua_backup))


# log = logging.getLogger('scrapy.proxies')

class RotatorProxy(object):
    """
    Make every call with a different proxy from the list, making a FIFO operation por the proxy rotation.
    """
    def __init__(self, settings):
        """
        Starts the attributes needed to make a RotatorProxy object
        :param settings: spider settings
        """
        self._num_pages = 0
        self._http_status_codes = settings.get('BLACKLIST_HTTP_STATUS_CODES', [307])
        # get the email data from the settings
        self.gmail_user = settings.get('GMAIL_USER')
        self.gmail_password = settings.get('GMAIL_PASSWORD')
        self.recipient = settings.get('RECIPIENT')
        # create a list of proxies from the settings CUSTOM_PROXY_LIST
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
        """
        Use a proxy to make the request and make the FIFO operation for the proxies list.
        :param request: request to be process
        :param spider: spider that makes the request
        :return: None: will continue processing this request, executing all other middlewares
        """
        if 'proxy' in request.meta:
            if request.meta["exception"] is False:
                return
        request.meta["exception"] = False
        # check if all the proxies are blocked, send an email and raise an error
        if len(self.proxies) == 0:
            reason = 'All proxies are unusable, cannot proceed. Exit at url %s' % request.url
            self._send_mail(reason, "Dedomeno - All proxies are unusable")
            raise ValueError('All proxies are unusable, cannot proceed')
        # make the FIFO operation
        proxy = self.proxies.pop(0)
        self.proxies.append(proxy)
        # get the selected proxy address and password
        proxy_address = proxy[0]
        proxy_user_pass = proxy[1]
        # use the proxy selected
        if proxy_user_pass:
            request.meta['proxy'] = proxy_address
            basic_auth = 'Basic ' + base64.b64encode(proxy_user_pass.encode()).decode()
            request.headers['Proxy-Authorization'] = basic_auth
        else:
            log.debug('Proxy user pass not found')
        log.debug('Using proxy <%s>, %d proxies left' % (proxy_address, len(self.proxies)))

    def process_response(self, request, response, spider):
        """
        Process the response, checking if the server has block an IP.
        :param request: the request that originated the response
        :param response: the response being processed
        :param spider: the spider for which this response is intended
        :return: pass the response to the next layer.
        """
        log.debug('   request: %s %s' % (request.url, request.meta))
        log.debug('   response: %s %s' % (response.url, response.status))
        log.debug('   num_pages: %s' % self._num_pages)
        self._num_pages = self._num_pages + 1
        # check if the server send a block response and delete that IP from the list.
        if response.status in self._http_status_codes:
            del self.proxies[-1]
            reason = '  %d in %s . IP %s deleted. %d proxies left' % (response.status, response.url, request.meta['proxy'], len(self.proxies))
            log.warning(reason)
            raise IgnoreRequest(reason)
        return response

    def process_exception(self, request, exception, spider):
        """
        It process the exception that have been raised in RotatorProxy
        :param request: request that raised the exception
        :param exception: exception raised
        :param spider: spider involve
        :return: None
        """
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
        """
        It stop an sleep the spider.
        - NOT USING IT -
        :param spider: the spider for which this action is intended
        :return: None
        """
        delay = random.randrange(self._sleep_min, self._sleep_max)
        log.info(u'Sleeping {} seconds'.format(delay))
        time.sleep(delay)
        self._num_pages_max = random.randrange(self._pages_min, self._pages_max)
        self._num_pages = 0
        log.info('Waking up... New num_pages_max set to %d' % self._num_pages_max)
    '''

    def _send_mail(self, message, subject):
        """
        Sends an email with the message and subject of the parameters
        :param message: body string of the email
        :param subject: subject string of the email
        :return: None
        """
        log.info("Sending mail with subject: %s to %s ........." % (subject, self.recipient))
        msg = MIMEMultipart()
        msg['From'] = self.gmail_user
        msg['To'] = self.recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        mail_server = smtplib.SMTP('smtp.gmail.com', 587)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(self.gmail_user, self.gmail_password)
        mail_server.sendmail(self.gmail_user, self.recipient, msg.as_string())
        mail_server.close()
        log.info("Mail sent")
