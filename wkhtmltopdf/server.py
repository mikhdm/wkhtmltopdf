#!/usr/bin/env python3

import os
import io
import signal
import sys
import traceback
from datetime import datetime

from urllib.parse import urljoin
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

from utils import htmltopdf, get_temp_filename


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handling requests in separate threads."""


try:
    host, port = sys.argv[1:][0].split(":")
except Exception:
    host, port = "0.0.0.0", 8000

SERVER_HOST = host


def _makepdf(blob):
    if blob:
        fname = get_temp_filename(strlen=16)
        htmlpath = os.path.join("/tmp", "{0}.html".format(fname))

        with open(htmlpath, "wb") as f:
            f.write(blob)
        data = htmltopdf(htmlpath, delete_html=True)
        return data
    return bytes()


class HTMLToPDFHandler(BaseHTTPRequestHandler):
    OK = 200
    SERVER_ERROR = 500

    def _link(self, filename):
        base = "http://{0}".format(
            ":".join([SERVER_HOST, str(self.server.server_port)])
        )
        return urljoin(base, filename)

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        length = self.headers.get("Content-Length")
        blob = self.rfile.read(int(length))
        try:
            data = _makepdf(blob)  # pdf bin data
        except Exception:
            # make trace to send as a response to a client
            with io.StringIO() as buff:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback, file=buff)
                buff.seek(0)
                data = bytes(buff.read(), encoding="utf-8")

            self.send_response(self.__class__.SERVER_ERROR)
            self.send_header("Content-Type", "text/plain")
        else:
            self.send_response(self.__class__.OK)
            self.send_header("Content-Type", "application/pdf")
        finally:
            self.end_headers()
            self.wfile.write(data)


def run(server=ThreadedHTTPServer, handler=BaseHTTPRequestHandler, host="", port=8005):
    addr = (
        host,
        int(port),
    )
    httpd = server(addr, handler)

    signal.signal(signal.SIGINT, lambda s, frame: sys.exit(0))
    signal.signal(signal.SIGTERM, lambda s, frame: sys.exit(0))

    print(datetime.now().strftime("%m-%d-%Y, %H:%M:%S"))
    print("HTML to PDF Converter is running on {0}:{1}".format(host, port))
    print("Press Ctrl-C to exit...")
    httpd.serve_forever()


if __name__ == "__main__":
    run(handler=HTMLToPDFHandler, host=host, port=int(port))
