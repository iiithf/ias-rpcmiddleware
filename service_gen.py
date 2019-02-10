#!/usr/bin/env python
from service_stub import ServiceProcedure
import optparse
import re


def parse_addr(addr):
  i = addr.find(':')
  host = '' if i<0 else addr[0:i]
  port = int(addr if i<0 else addr[i+1:])
  return (host, port)

def parse_procs(text):
  procs = []
  for sign in text.split(';'):
    if len(sign.strip()) > 0:
      procs.append(ServiceProcedure(sign, None))
  return procs

def write_head(f):
  f.write('#!/usr/bin/env python\n')
  f.write('from service_stub import ServiceStub, ServiceProcedure\n')

def write_funcs(f, procs):
  for p in procs:
    f.write('\n')
    args = ', '.join(p.args_typ.keys())
    f.write('def %s(%s):\n' % (p.name, args))
    f.write('  return\n')

def write_setup(f, procs):
  f.write('def service_setup(name=\'\'):\n')
  f.write('  serv = ServiceStub(name)\n')
  for p in procs:
    f.write('  serv.add(\'%s\', %s)\n' % (p.sign, p.name))
  f.write('  return serv\n')

def write_start(f, name, addr, midw):
  f.write('addr = %s\n' % str(addr))
  f.write('midw = %s\n' % str(midw))
  f.write('service = service_setup(\'%s\')\n' % name)
  f.write(r"print('Starting service on %s -> %s' % (addr, midw))"+'\n')
  f.write('service.start(%s, %s)\n' % (str(addr), str(midw)))


p = optparse.OptionParser()
p.set_defaults(outp='service.py', head='service.h', name='', addr='127.0.0.1:1992', midw=None)
p.add_option('--output', dest='outp', help='set output filename')
p.add_option('--header', dest='head', help='set input header file')
p.add_option('--name', dest='name', help='set service name')
p.add_option('--address', dest='addr', help='set service address')
p.add_option('--middleware', dest='midw', help='set middleware address')
(o, args) = p.parse_args()

name = o.name
addr = parse_addr(o.addr)
midw = None if o.midw is None else parse_addr(o.midw)
head = open(o.head, 'r')
outp = open(o.outp, 'w')
procs = parse_procs(head.read())
write_head(outp)
outp.write('\n')
write_funcs(outp, procs)
outp.write('\n')
write_setup(outp, procs)
outp.write('\n\n')
write_start(outp, name, addr, midw)
head.close()
outp.close()
