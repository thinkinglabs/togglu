from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread
import port_for

import os
from urllib.parse import urlparse, parse_qs

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

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

class WorkspacesRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        with open(os.path.join(THIS_DIR, os.pardir, 'data/workspaces.json'), 'r') as myfile:
            data = myfile.read().replace('\n', '')
        
        # Process an HTTP GET request and return a response with an HTTP 200 status.
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        url = urlparse(self.path)
        if url.path == '/workspaces':
            self.wfile.write(bytes(data, "utf-8"))

        return

class DetailedReportPaginationRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        with open(os.path.join(THIS_DIR, os.pardir, 'data/detailed_report_page1.json'), 'r') as myfile:
            data1 = myfile.read().replace('\n', '')
        with open(os.path.join(THIS_DIR, os.pardir, 'data/detailed_report_page2.json'), 'r') as myfile:
            data2 = myfile.read().replace('\n', '')
        with open(os.path.join(THIS_DIR, os.pardir, 'data/detailed_report_page3.json'), 'r') as myfile:
            data3 = myfile.read().replace('\n', '')
        
        # Process an HTTP GET request and return a response with an HTTP 200 status.
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        url = urlparse(self.path)
        if url.path == '/details':
            query = parse_qs(url.query)
            page = query['page'][0]
            
            if page == '1':
                self.wfile.write(bytes(data1, "utf-8"))
            elif page == '2':
                self.wfile.write(bytes(data2, "utf-8"))
            elif page == '3':
                self.wfile.write(bytes(data3, "utf-8"))

        return

class DetailedReportFilterRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        with open(os.path.join(THIS_DIR, os.pardir, 'data/detailed_report_filter.json'), 'r') as myfile:
            data = myfile.read().replace('\n', '')
        
        # Process an HTTP GET request and return a response with an HTTP 200 status.
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        url = urlparse(self.path)
        if url.path == '/details':
            query = parse_qs(url.query)
            page = query['page'][0]
            since = query['since'][0]
            until = query['until'][0]
            client_ids = query['client_ids'][0]
            tag_ids = query['tag_ids'][0]
            
            if (
                page == '1' 
                and since == '2018-11-23'
                and until == '2018-11-23'
                and tag_ids == '123456789'
                and client_ids == '456'
            ):  
                self.wfile.write(bytes(data, "utf-8"))
            
        return