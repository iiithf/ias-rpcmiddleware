#!/usr/bin/env python
from http.server import HTTPServer, BaseHTTPRequestHandler
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


class RequestHandler(BaseHTTPRequestHandler):
  def body(self):
    size = int(self.headers.get('Content-Length'))
    return self.rfile.read(size)

  def send(self, code, body=None, headers=None):
    self.send_response(code)
    for k, v in headers.items():
      self.send_header(k, v)
    self.end_headers()
    if body is not None:
      self.wfile.write(body)
  
  def send_json(self, code, body):
    heads = {'Content-Type': 'application/json'}
    self.send(code, bytes(json.dumps(body), 'utf8'), heads)

  def do_GET(self):
    data = {}
    stub = self.server.stub
    for k, v in stub.procs.items():
      data[k] = v.sign
    self.send_json(200, data)

  def do_POST(self):
    stub = self.server.stub
    stub.handle_call(self)


class ServiceProcedure:
  def __init__(self, sign, func):
    self.sign = re.sub(r'\s+', ' ', sign).strip()
    parts = re.sub(r'[^\w\[\]]+', ' ', self.sign).strip().split(' ')
    (self.retn_typ, self.name) = parts[0:2]
    (self.args_typ, self.args_req) = parse_args(parts)
    self.func = func

  def call(self, args):
    validate_args(args, self.args_typ, self.args_req)
    retn = self.func(**args)
    validate_typ('return', retn, self.retn_typ)
    return retn


class ServiceStub:
  def __init__(self, name=''):
    self.name = name
    self.procs = {}

  def add(self, sign, func):
    proc = ServiceProcedure(sign, func)
    if self.procs.get(proc.name) is not None:
      return 'Procedure %s already added!' % proc.name
    self.procs[proc.name] = proc
    return None
  
  def remove(self, name):
    self.procs[name] = None
    return None

  def handle_call(self, http):
    name = http.path[1:]
    proc = self.procs.get(name)
    if proc is None:
      mesg = 'Unknown procedure %s!' % name
      return http.send_json(400, {'error': mesg})
    try:
      args = json.loads(http.body())
      retn = proc.call(args)
      http.send_json(200, {'return': retn})
    except Exception as e:
      http.send_json(400, {'error': repr(e)})

  def start_add(self, addr, midw):
    (host, port) = midw
    conn = HTTPConnection(host, port, source_address=addr)
    conn.request('POST', '/service/add/'+self.name)
    resp = conn.getresponse()
    if resp.code != 200:
      data = json.loads(resp.read())
      raise NameError(data.get('error'))

  def start(self, addr=('', 1992), midw=None):
    if midw is not None:
      self.start_add(addr, midw)
    httpd = HTTPServer(addr, RequestHandler)
    httpd.stub = self
    httpd.serve_forever()


# def test(a, b):
#   return a+b
# a = ServiceStub()
# a.add('int test(int a, int b)', test)
# a.start()
