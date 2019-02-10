#!/usr/bin/env python
from client_stub import ClientStub


class MemkartService:
  def __init__(self, addr=('127.0.0.1', 1992), serv=''):
    self.add_item_stub = ClientStub('int add_item(str item, int price)', addr, serv)
    self.add_quantity_stub = ClientStub('int add_quantity(str item, int quantity)', addr, serv)
    self.remove_quantity_stub = ClientStub('int remove_quantity(str item, int quantity)', addr, serv)
    self.get_price_stub = ClientStub('int get_price(str item)', addr, serv)
    self.get_quantity_stub = ClientStub('int get_quantity(str item)', addr, serv)

  def add_item(self, item, price):
    print('Adding %s at price %d ...' % (item, price))
    self.add_item_stub.call({'item': item, 'price': price})
    print('Added %s.\n' % item)

  def add_quantity(self, item, quantity):
    print('Adding %d %s(s) ...' % (quantity, item))
    quantity = self.add_quantity_stub.call({'item': item, 'quantity': quantity})
    print('%d %s(s) in stock.\n' % (quantity, item))

  def remove_quantity(self, item, quantity):
    print('Purchasing %d %s(s) ...' % (quantity, item))
    quantity = self.remove_quantity_stub.call({'item': item, 'quantity': quantity})
    print('%d %s(s) in stock.\n' % (quantity, item))

  def get_price(self, item):
    print('Checking price of %s ...' % item)
    price = self.get_price_stub.call({'item': item})
    print('%s is priced at %d.\n' % (item, price))

  def get_quantity(self, item):
    print('Checking quantity of %s ...' % item)
    quantity = self.get_quantity_stub.call({'item': item})
    print('%d %s(s) in stock.\n' % (quantity, item))


service = MemkartService(('127.0.0.1', 1992), 'memkart')
print('Memkart inventory demo:\n')
service.add_item('guava', 60)
input('[enter]')
service.add_item('pumpkin', 30)
input('[enter]')
service.add_item('peanuts', 125)
input('[enter]')
service.add_quantity('guava', 300)
input('[enter]')
service.add_quantity('pumpkin', 200)
input('[enter]')
service.add_quantity('peanuts', 100)
input('[enter]')
service.remove_quantity('guava', 30)
input('[enter]')
service.remove_quantity('pumpkin', 20)
input('[enter]')
service.remove_quantity('peanuts', 10)
input('[enter]')
service.get_price('guava')
input('[enter]')
service.get_price('pumpkin')
input('[enter]')
service.get_price('peanuts')
input('[enter]')
service.get_quantity('guava')
input('[enter]')
service.get_quantity('pumpkin')
input('[enter]')
service.get_quantity('peanuts')
input('[enter]')
print('Thanks for participating.')
