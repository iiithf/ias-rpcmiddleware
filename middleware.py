#!/usr/bin/env python
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection
import optparse
import json
import re


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
    handler = self.server.handler
    self.send_json(200, handler.addrs)

  def do_POST(self):
    handler = self.server.handler
    if self.path.startswith('/service'):
      return handler.handle_service(self)
    return handler.handle_forward(self)


class ServiceHandler:
  addrs = {}

  def add(self, name, addr):
    if self.addrs.get(name) is not None:
      return 'Service %s already added!' % name
    self.addrs[name] = addr
    return None

  def remove(self, name, addr):
    if self.addrs.get(name) != addr:
      return 'Not allowed to remove service %s!' % name
    self.addrs[name] = None
    return None

  def handle_service(self, http):
    path = http.path[8:]
    addr = http.request.getpeername()
    msg = 'Unknown request %s!' % http.path
    if path.startswith('/add/'):
      msg = self.add(path[5:], addr)
    elif path.startswith('/remove/'):
      msg = self.remove(path[8:], addr)
    return http.send_json(200 if msg is None else 400, msg)
  
  def handle_forward(self, http):
    name = re.sub(r'\/.*', '', http.path[1:])
    path = http.path[len(name)+1:]
    if self.addrs[name] is None:
      return http.send_json(400, 'Unknown request %s!' % http.path)
    (host, port) = self.addrs[name]
    conn = HTTPConnection(host, port)
    conn.request('POST', path, http.body(), http.headers)
    resp = conn.getresponse()
    return http.send(resp.code, resp.read(), resp.headers)

  def start(self, addr):
    httpd = HTTPServer(addr, RequestHandler)
    httpd.handler = self
    httpd.serve_forever()


p = optparse.OptionParser()
p.set_defaults(host='', port=1992)
p.add_option('--host', dest='host', help='set middleware host address')
p.add_option('--port', dest='port', help='set middleware port number', type='int')
(o, args) = p.parse_args()

addr = (o.host, o.port)
middleware = ServiceHandler()
print('Starting middleware on',addr)
middleware.start(addr)
