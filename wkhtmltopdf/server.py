#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import io
import sys
import cgi
import json
import traceback
from datetime import datetime

from urllib.parse import urljoin
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

from utils import htmltopdf, get_temp_filename


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handling requests in a separate threads."""


try:
	host, port = sys.argv[1:][0].split(':')
except:
	host, port = '0.0.0.0', 8005


SERVER_HOST = host


def _makepdf(blob): # TODO async task using asyncio
	if blob:
		fname = get_temp_filename(strlen=16)
		htmlpath = os.path.join('/tmp', "{0}.html".format(fname))

		with open(htmlpath, 'wb') as f:
			f.write(blob)

		data = htmltopdf(htmlpath, delete_html=True)
		return data 
	return bytes()


class HTMLToPDFHandler(BaseHTTPRequestHandler):
	
	OK = 200
	SERVER_ERROR = 500

	def _link(self, filename):
		base = "http://{0}".format(
					":".join([SERVER_HOST, str(self.server.server_port)]))
		return urljoin(base, filename) 
	
	def do_GET(self):
		self.send_response(200)
		self.end_headers()

	def do_POST(self):
		form = cgi.FieldStorage(
				fp=self.rfile,
				headers=self.headers,
				environ={
					'REQUEST_METHOD': 'POST', 
					'CONTENT_TYPE': self.headers['Content-Type']})

		try:
			blob = form.getvalue('html')
			data = _makepdf(blob) # pdf bin data
		except Exception as e:
			# make trace to send as a response to a client
			with io.StringIO() as buff:

				exc_type, exc_value, exc_traceback = sys.exc_info()
				traceback.print_exception(exc_type, exc_value, exc_traceback, file=buff)
				buff.seek(0)

				data = bytes(buff.read(), encoding='utf-8')

			self.send_response(self.__class__.SERVER_ERROR)
			self.send_header("Content-Type", "text/plain")
		else:
			self.send_response(self.__class__.OK)
			self.send_header("Content-Type", "application/pdf")
		finally:
			self.end_headers()
			self.wfile.write(data)


def run(server=ThreadedHTTPServer, handler=BaseHTTPRequestHandler, host='', port=8005):
	addr = (host, int(port),)
	httpd = server(addr, handler)

	print(datetime.now().strftime("%m-%d-%Y, %H:%M:%S"))
	print('HTML to PDF Converter Service on {0}:{1}'.format(host, port))
	print('CTRL-C to quit.')

	httpd.serve_forever()


if __name__ == "__main__":
	run(handler=HTMLToPDFHandler, host=host, port=port)
