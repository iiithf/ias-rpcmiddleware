#!/usr/bin/env python
from client_stub import ClientStub
import optparse
import re


def args_json(typ):
  parts = []
  for k in typ:
    parts.append('\'%s\': %s' % (k, k))
  return '{%s}' % ', '.join(parts)


parser = optparse.OptionParser()
parser.set_defaults(header='service.h', service='', host='127.0.0.1', port=1992, output='client.py')
parser.add_option('--output', dest='output', help='set output filename')
parser.add_option('--header', dest='header', help='set input header file')
parser.add_option('--service', dest='service', help='set service name')
parser.add_option('--host', dest='host', help='set middleware host address')
parser.add_option('--port', dest='port', help='set middleware port number')
(o, args) = parser.parse_args()

signs = []
stubs = []
hdr = open(o.header, 'r')
out = open(o.output, 'w')
for sign in hdr.read().split(';'):
  text = re.sub(r'\s+', ' ', sign).strip()
  if text == '':
    continue
  signs.append(text)
  stubs.append(ClientStub(sign, o.service, o.host, o.port))
out.write('#!/usr/bin/env python\n')
out.write('from client_stub import ClientStub\n')
out.write('\n\n')
out.write('class %sService:\n' % o.service.title())
out.write('  def __init__(self, srvc, host, port):\n')
for i in range(len(signs)):
  func = re.sub(r'.*\/', '', stubs[i].path)
  out.write('    self.%s_stub = ClientStub(\'%s\', srvc, host, port)\n' % (func, signs[i]))
for stub in stubs:
  out.write('\n')
  func = re.sub(r'.*\/', '', stub.path)
  args = ', '.join(['self', ', '.join(stub.args_typ.keys())])
  out.write('  def %s(%s):\n' % (func, args))
  out.write('    self.%s_stub.call(%s)\n' % (func, args_json(stub.args_typ)))
out.write('\n\n')
out.write('service = %sService(\'%s\', \'%s\', %d)\n' % (o.service, o.service, o.host, o.port))
for stub in stubs:
  func = re.sub(r'.*\/', '', stubs[i].path)
  out.write('# service.%s(%s)\n' % (func, ', '.join(stub.args_typ.keys())))
  break
out.close()
