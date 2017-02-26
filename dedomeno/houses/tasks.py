# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def xsum2(numbers):
    return sum(numbers)


@shared_task
def startPropertySpider(property_type, transaction, province):
    spider = CrawlProperty(property_type, transaction, province)
    spider.startPropertySpider()
    return sum(numbers)
