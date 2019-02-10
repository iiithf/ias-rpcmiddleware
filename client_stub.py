#!/usr/bin/env python
from http.client import HTTPConnection
import json
import re


def parse_args(parts):
  (typ, req) = ({}, set())
  for i in range(2, len(parts), 2):
    arg = re.sub(r'\W', '', parts[i+1])
    typ[arg] = parts[i]
    if arg == parts[i+1]:
      req.add(arg)
  return (typ, req)

def validate_typ(nam, val, typ):
  if str(type(val)).find(typ) < 0:
    raise TypeError('%s=%s (%s), but expected %s!' % (nam, str(val), type(val), typ))

def validate_args(args, typ, req):
  for k, v in args.items():
    validate_typ(k, v, typ.get(k))
  for k in req:
    if k not in args:
      raise ValueError('%s is required!' % k)


class ClientStub:
  def __init__(self, sign, addr=('127.0.0.1', 1992), serv=''):
    self.sign = re.sub(r'\s+', ' ', sign).strip()
    parts = re.sub(r'[^\w\[\]]+', ' ', self.sign).strip().split(' ')
    (self.retn_typ, self.name) = parts[0:2]
    (self.args_typ, self.args_req) = parse_args(parts)
    (self.addr, self.serv) = (addr, serv)

  def path(self):
    if self.serv is None or len(self.serv) == 0:
      return '/'+self.name
    return '/'+self.serv+'/'+self.name

  def call_post(self, args):
    (host, port) = self.addr
    conn = HTTPConnection(host, port)
    conn.request('POST', self.path(), body=json.dumps(args))
    resp = conn.getresponse()
    data = json.loads(resp.read())
    if 'error' in data:
      raise Exception(data['error'])
    return data['return']


  def call(self, args):
    validate_args(args, self.args_typ, self.args_req)
    retn = self.call_post(args)
    validate_typ('return', retn, self.retn_typ)
    return retn


# a = ClientStub('int test(int a, int b)')
# r = a.call({'a': 1, 'b': 2})
# print(r)
