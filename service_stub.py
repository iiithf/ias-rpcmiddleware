#!/usr/bin/env python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class RequestHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    length = int(self.headers.get('Content-Length'))
    body = self.rfile.read(length).decode('ascii')
    data = json.loads(body)
    response = self.server.stub.call(self.path, data)
    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()
    message = json.dumps(response)
    self.wfile.write(bytes(message, 'utf8'))
    return


class ServiceStub:
  functions = {}

  def add(self, name, details):
    self.functions[name] = details
  
  def remove(self, name):
    self.functions[name] = None

  def call(self, name, data):
    details = self.functions[name]
    return details(**data)

  def start(self, port=1992):
    address = ('', port)
    httpd = HTTPServer(address, RequestHandler)
    httpd.stub = self
    httpd.serve_forever()


def test(begin, end):
  return begin+end


a = ServiceStub()
a.add('/json', test)
a.start()
