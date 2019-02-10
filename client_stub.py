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
  if typ != type(val):
    raise TypeError(nam+'='+val+' ('+type(val)+'), but expected '+typ)
  return

def validate_args(data, typ, req):
  for k, v in data.items():
    validate_typ(k, v, typ[k])
  for k in req:
    if data[k] is None:
      raise ValueError(k+' is required')
  return

def get_path(srvc, func):
  if srvc is None or len(srvc) == 0:
    return '/'+func
  return '/'+srvc+'/'+func


class ClientStub:
  def __init__(self, sign, srvc=None, host='127.0.0.1', port=1992):
    parts = re.sub(r'[^\w\[\]\=\'\"\-\.]+', ' ', sign.strip()).split()
    (self.args_typ, self.args_req) = parse_args(parts)
    [self.retn_typ, func] = parts[0:2]
    self.path = get_path(srvc, func)
    self.host = host
    self.port = port

  def call(self, data):
    validate_args(data, self.args_typ, self.args_req)
    conn = HTTPConnection(self.host, self.port)
    conn.request('POST', self.path, body=json.dumps(data))
    res = conn.getresponse()
    data = json.loads(res.read())
    validate_typ('return', data, self.retn_typ)
    return data
