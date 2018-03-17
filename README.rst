========
dedomeno
========


.. image:: https://img.shields.io/pypi/v/dedomeno.svg
        :target: https://pypi.python.org/pypi/dedomeno

.. image:: https://img.shields.io/travis/ginopalazzo/dedomeno.svg
        :target: https://travis-ci.org/ginopalazzo/dedomeno

.. image:: https://readthedocs.org/projects/dedomeno/badge/?version=latest
        :target: https://dedomeno.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



A Spanish real estate (Idealista) python scraper


* Free software: MIT license
* Documentation: https://dedomeno.readthedocs.io.


Features
--------

First untest alpha version.

Use crawlpropery.py to make manual crawls, just modify the CrawlPropertyReactor parameters to yours needs::

    dedomeno/idealista/crawlproperty.py

    if __name__ == "__main__":
        spider = CrawlPropertyReactor(property_type='land', transaction='sale', provinces=['salamanca'])
        spider.conf()
        spider.run()


Use django + celery + flower + scrapy to do programmatic crawls and visualize the output::

    # 1. start django server, http://127.0.0.1:8000/
    python manage.py runserver
    # 2. remove all tasks from queue: celery. (Only works when RabbitMQ is up)
    celery -A proj purge
    # Enter admin http://127.0.0.1:8000/admin and change django-celery-beat to schedule the periodic task in the db
    # 3. Run the RabbitMQ message broker
    sudo rabbitmq-server
    # 4. Celery:
    # 4.1 Start the celery worker
    celery -A dedomeno worker --loglevel=INFO
    # 4.2 Run Flower, a web based tool for monitoring and administrating Celery clusters
    celery -A dedomeno flower
    # 4.3 Start the celery beat (schedule tasks)
    celery -A dedomeno beat -l info -S django

Built With
--------

* Django_ - Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design
* Scrapy_ - An open source and collaborative framework for extracting the data you need from websites.
* Celery_ - An asynchronous task queue/job queue based on distributed message passing


Credits
-------

* Gino Palazzo ginopalazzo@gmail.com
* This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _Django: https://www.djangoproject.com/
.. _Scrapy: https://scrapy.org/
.. _Celery: http://www.celeryproject.org/
