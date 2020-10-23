from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread
import port_for

def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def mock_http_server(request_handler):
    mock_server_port = get_free_port()
    mock_server = HTTPServer(('localhost', mock_server_port), request_handler)

    # Start running mock server in a separate thread.
    # Daemon threads automatically shut down when the main process exits.
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()
    return mock_server_port
