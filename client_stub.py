from http.client import HTTPConnection
import json


class ClientStub:
  def call(self, name, data):
    conn = HTTPConnection('127.0.0.1', port=1992)
    data = {'begin':1, 'end': 2}
    conn.request('POST', '/json', body=json.dumps(data))
    res = conn.getresponse()
    print(json.loads(res.read()))

a = ClientStub()
a.call('a', {})
