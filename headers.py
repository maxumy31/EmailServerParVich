def response(self,responseCode,responseEncoded):
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')  # Разрешаем все источники
    self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')  # Разрешенные методы
    self.send_header('Access-Control-Allow-Headers', 'Content-Type, application/json')  # Разрешенные заголовки
    self.end_headers()
    self.wfile.write(responseEncoded)