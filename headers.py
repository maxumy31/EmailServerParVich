def response(self,responseCode,responseEncoded):
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.end_headers()
    self.wfile.write(responseEncoded)