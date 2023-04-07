from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import BaseServer
import ssl

httpd = HTTPServer(("localhost", 443), SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(
    httpd.socket, certfile="./localhost.pem", server_side=True
)
httpd.serve_forever()
