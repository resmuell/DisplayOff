# -*- coding: utf-8 -*-
import xmlrpc.server as xmlrpc_server
import configparser
import dispctrl
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
from types import Final

# serverShutdown=False # flag whether stop this server.

config = configparser.SafeConfigParser()
config.read("./config.ini")

HOST: Final[str] = config.get('Server', 'Host')
PORT: Final[int] = int(config.get('Server', 'Port'))


class MyHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        url = urlparse(self.path)
        body = bytes('''<h1>DisplayOff</h1><hr>
        Usage: http://{0}:{1}/(on|off)[?wait seconds]<br>
        <br>
        Quick link:<br>
        <a href=http://{0}:{1}/off>Turn off now</a><br>
        <a href=http://{0}:{1}/on>Turn on now</a><br>
        '''.format(HOST, PORT), 'ascii')
        wait = 0

        if url.query.isdigit() and int(url.query) > 0:
            wait = int(url.query)

        if url.path == '/on':
            dispctrl.DispOn(wait)
            body = bytes('''<h1>DisplayOff</h1><hr>
            Turning on succeeded.<br>
            <br>
            <a href=http://{0}:{1}/>Back to top page</a><br>
            '''.format(HOST, PORT), 'ascii')
        elif url.path == '/off':
            dispctrl.DispOff(wait)
            body = bytes('''<h1>DisplayOff</h1><hr>
            Turning off succeeded.<br>
            <br>
            <a href=http://{0}:{1}/>Back to top page</a><br>
            '''.format(HOST, PORT), 'ascii')

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-length', len(body))
        self.end_headers()
        self.wfile.write(body)


def main():
    httpd = HTTPServer((HOST, PORT), MyHandler)
    print('Server started... Press Ctrl+C to exit.')
    httpd.serve_forever()


if __name__ == '__main__':
    main()
