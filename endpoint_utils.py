import urllib.parse
import hashlib
import json

def parse_post_data(server,content_length):
    raw = (server.rfile.read(content_length).decode('utf-8'))
    js = json.loads(raw)
    return js

def parse_get_data(server):
    return urllib.parse.parse_qs(urllib.parse.urlparse(server.path).query)

def get_content_length(server):
    content_length = 0
    if 'Content-Length' in server.headers and server.headers['Content-Length'] is not None:
        content_length = int(server.headers['Content-Length'])
    return content_length

def hash_password(password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password

