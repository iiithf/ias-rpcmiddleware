#!/usr/bin/env python
import optparse


parser = optparse.OptionParser()
parser.set_defaults(signs='service.h', srvc='', host='127.0.0.1', port=1992)
parser.add_option('--header', dest='signs', help='set header file')
parser.add_option('--service', dest='srvc', help='set service name')
parser.add_option('--host', dest='host', help='set middleware host address')
parser.add_option('--port', dest='port', help='set middleware port number')
(options, args) = parser.parse_args()

file = open(options.signs, 'r')
signs = file.read()

