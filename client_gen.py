#!/usr/bin/env python
from client_stub import ClientStub
import optparse
import re


def parse_addr(addr):
  i = addr.find(':')
  host = '' if i<0 else addr[0:i]
  port = int(addr if i<0 else addr[i+1:])
  return (host, port)

def args_json(typ):
  parts = []
  for k in typ:
    parts.append('\'%s\': %s' % (k, k))
  return '{%s}' % ', '.join(parts)

def parse_stubs(text):
  stubs = []
  for sign in text.split(';'):
    if len(sign.strip()) > 0:
      stubs.append(ClientStub(sign, addr, serv))
  return stubs

def write_head(f):
  f.write('#!/usr/bin/env python\n')
  f.write('from client_stub import ClientStub\n')

def write_init(f, stubs):
  f.write('  def __init__(self, addr=(\'127.0.0.1\', 1992), serv=\'\'):\n')
  for s in stubs:
    f.write('    self.%s_stub = ClientStub(\'%s\', addr, serv)\n' % (s.name, s.sign))

def write_func(f, stubs):
  for s in stubs:
    f.write('\n')
    args = ', '.join(s.args_typ.keys())
    f.write('  def %s(%s):\n' % (s.name, ', '.join(['self', args])))
    f.write('    self.%s_stub.call(%s)\n' % (s.name, args_json(s.args_typ)))

def write_class(f, stubs, serv):
  f.write('class %sService:\n' % serv.title())
  write_init(f, stubs)
  write_func(f, stubs)

def write_sample(f, stubs, addr, serv):
  f.write('service = %sService((\'%s\', %d), \'%s\')\n' % (serv.title(), addr[0], addr[1], serv))
  for s in stubs:
    args = ', '.join(s.args_typ.keys())
    f.write('# service.%s(%s)\n' % (s.name, args))
    break


p = optparse.OptionParser()
p.set_defaults(outp='client.py', head='service.h', serv='', addr='127.0.0.1:1992')
p.add_option('--output', dest='outp', help='set output filename')
p.add_option('--header', dest='head', help='set input header file')
p.add_option('--address', dest='addr', help='set service address')
p.add_option('--service', dest='serv', help='set service name')
(o, args) = p.parse_args()

serv = o.serv
addr = parse_addr(o.addr)
head = open(o.head, 'r')
outp = open(o.outp, 'w')
stubs = parse_stubs(head.read())
write_head(outp)
outp.write('\n\n')
write_class(outp, stubs, serv)
outp.write('\n\n')
write_sample(outp, stubs, addr, serv)
head.close()
outp.close()
