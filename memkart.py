#!/usr/bin/env python
from service_stub import ServiceStub, ServiceProcedure


ITEMS = {}


def add_item(item, price):
  ITEMS[item] = [price, 0]
  return 0

def add_quantity(item, quantity):
  ITEMS[item][1] += quantity
  return ITEMS[item][1]

def remove_quantity(item, quantity):
  ITEMS[item][1] -= quantity
  return ITEMS[item][1]

def get_price(item):
  return ITEMS[item][0]

def get_quantity(item):
  return ITEMS[item][1]

def service_setup(name=''):
  serv = ServiceStub(name)
  serv.add('int add_item(str item, int price)', add_item)
  serv.add('int add_quantity(str item, int quantity)', add_quantity)
  serv.add('int remove_quantity(str item, int quantity)', remove_quantity)
  serv.add('int get_price(str item)', get_price)
  serv.add('int get_quantity(str item)', get_quantity)
  return serv


addr = ('', 1995)
midw = ('127.0.0.1', 1992)
service = service_setup('memkart')
print('Starting service on %s -> %s' % (addr, midw))
service.start(('', 1995), ('127.0.0.1', 1992))
