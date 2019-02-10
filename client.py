#!/usr/bin/env python
from client_stub import ClientStub


class Service:
  def __init__(self, srvc, host, port):
    self.test1_stub = ClientStub('int test1(int a, int b)', srvc, host, port)
    self.test2_stub = ClientStub('float test2(float a, float b)', srvc, host, port)

  def test1(self, a, b):
    self.test1_stub.call({'a': a, 'b': b})

  def test2(self, a, b):
    self.test2_stub.call({'a': a, 'b': b})


service = Service('', '127.0.0.1', 1992)
# service.test2(a, b)
