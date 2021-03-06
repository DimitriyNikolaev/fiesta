# -*- coding: utf-8 -*-
__author__ = 'dimitriy'


# импортируем модуля языка, которые используются
# в этом скрипте
import os, sys, site
# подключаем наш проект в путь python, если index.wsgi
# находится не в корне проекта, то надо указывать
# полный путь до каталога проекта
virtual_env = os.path.expanduser('~/.virtualenvs/fiesta')
activate_this = os.path.join(virtual_env, 'bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert(0, os.path.join(os.path.expanduser('~'),'web/fiesta/fiesta'))
# подключаем виртуальное окружение проекта
#site.addsitedir('/home/e/evesdrearu/.virtualenvs/etoys/lib/python2.7/site-packages')
# указываем через переменную окружения
# название модуля с конфигурацией проекта
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
# передаём управление нашему проекту
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()