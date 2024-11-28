import urllib.parse

def parse_post_data(server,content_length):
    return server.rfile.read(content_length)

def parse_get_data(server):
    return urllib.parse.parse_qs(urllib.parse.urlparse(server.path).query)

def get_content_length(server):
    content_length = 0
    if 'Content-Length' in server.headers and server.headers['Content-Length'] is not None:
        content_length = int(server.headers['Content-Length'])
    return content_length
