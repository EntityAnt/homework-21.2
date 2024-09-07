import http.server
import socketserver
import urllib.parse

PORT = 8080


class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/contacts':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Чтение содержимого HTML-файла
            with open('html/contacts.html', 'r', encoding='utf-8') as file:
                html_content = file.read()

            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Читаем тело запроса

            # Парсим данные
            data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            # Печатаем данные в консоль
            print("Полученные данные:", data)

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('Данные успешно получены!'.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')


# Запуск сервера
with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Сервер запущен на порту {PORT}")
    httpd.serve_forever()
