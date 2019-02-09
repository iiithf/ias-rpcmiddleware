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


class ClientStub:
  def __init__(self, sign, srvc='default', host='127.0.0.1', port=1992):
    parts = re.sub(r'[^\w\[\]]+', ' ', sign).split()
    (self.args_typ, self.args_req) = parse_args(parts)
    [self.retn_typ, self.func] = parts[0:1]
    self.srvc = srvc
    self.host = host
    self.port = port

  def call(self, data):
    validate_args(data, self.args_typ, self.args_req)
    conn = HTTPConnection(self.host, self.port)
    url = '/'+self.srvc+'/'+self.func
    conn.request('POST', url, body=json.dumps(data))
    res = conn.getresponse()
    data = json.loads(res.read())
    validate_typ('return', data, self.retn_typ)
    return data
