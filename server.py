from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import urllib.parse
import endpoints
import database

HOST = '127.0.0.1'
PORT = 12345

METHOD_POST = 0
METHOD_GET = 1

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class Server(BaseHTTPRequestHandler):
    endpoints = {}

    @classmethod
    def add_endpoint(cls, endpoint, method, function):
        if endpoint not in cls.endpoints:
            cls.endpoints[endpoint] = {}
        cls.endpoints[endpoint][method] = function
        print("added" + endpoint)

    def do_POST(self):
        print("POST запрос по ",self.path)

        parsed_url = urllib.parse.urlparse(self.path)
        endpoint = parsed_url.path

        self.handleEndpoint(self.path,METHOD_POST)

    def do_GET(self):
        print("GET запрос по ",self.path)

        parsed_url = urllib.parse.urlparse(self.path)
        endpoint = parsed_url.path

        self.handleEndpoint(endpoint,METHOD_GET)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def handleEndpoint(self, endpoint,method):
        try:
            self.endpoints[endpoint][method](self)
        except Exception as e:
            print(e)
            print("Endpoint " + endpoint + " is not valid")



def main():
    database.register_db()

    Server.add_endpoint("/email",METHOD_POST,endpoints.create_email)
    Server.add_endpoint("/email_send",METHOD_POST,endpoints.send_mail)

    Server.add_endpoint("/echo",METHOD_GET,endpoints.echo)
    Server.add_endpoint("/email_exists",METHOD_GET,endpoints.check_email_exists)
    Server.add_endpoint("/email_recieve",METHOD_POST,endpoints.read_mail)
    
    httpd = ThreadingHTTPServer((HOST, PORT), Server)
    print(f"Сервер запущен на {HOST}:{PORT}")
    httpd.serve_forever()

main()
