import urllib.parse
import headers
import json

def echo(self):

    content_length = 0
    if 'Content-Length' in self.headers and self.headers['Content-Length'] is not None:
        content_length = int(self.headers['Content-Length'])

    post_data = self.rfile.read(content_length)
    query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
    print(f"Получено сообщение: {query_params}")
    headers.response(self,200,json.dumps(query_params).encode())