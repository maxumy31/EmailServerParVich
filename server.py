from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import endpoints

HOST = '127.0.0.1'
PORT = 12345

METHOD_POST = 0
METHOD_GET = 1


class Server(BaseHTTPRequestHandler):
    endpoints = {}

    @classmethod
    def add_endpoint(cls, endpoint, method, function):
        if endpoint not in cls.endpoints:
            cls.endpoints[endpoint] = {}
        cls.endpoints[endpoint][method] = function

    def do_POST(self):
        print("POST запрос по ",self.path)
        self.handleEndpoint(self.path,METHOD_POST)

    def do_GET(self):
        print("GET запрос по ",self.path)

        parsed_url = urllib.parse.urlparse(self.path)
        endpoint = parsed_url.path

        self.handleEndpoint(endpoint,METHOD_GET)


    def handleEndpoint(self, endpoint,method):
        self.endpoints[endpoint][method](self)



Server.add_endpoint("/echo",METHOD_GET,endpoints.echo)

httpd = HTTPServer((HOST, PORT), Server)
print(f"Сервер запущен на {HOST}:{PORT}")
httpd.serve_forever()


