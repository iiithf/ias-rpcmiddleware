#!/usr/bin/env python
from service_stub import ServiceStub, ServiceProcedure


def test1(a, b):
  return a+b

def test2(a, b):
  return

def service_setup(name=''):
  serv = ServiceStub(name)
  serv.add('int test1(int a, int b)', test1)
  serv.add('float test2(float a, float b)', test2)
  return serv


service = service_setup('')
service.start(('127.0.0.1', 1992), None)
