#!/usr/bin/env python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class RequestHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    length = int(self.headers.get('Content-Length'))
    body = self.rfile.read(length).decode('ascii')
    data = json.loads(body)
    print(self.path, data)
    self.send_response(200)
    self.send_header('Content-Type', 'text/html')
    self.end_headers()
    message = 'Hello Client!'
    self.wfile.write(bytes(message, 'utf8'))
    return

def server_start():
  address = ('', 1992)
  httpd = HTTPServer(address, RequestHandler)
  httpd.serve_forever()


server_start()
