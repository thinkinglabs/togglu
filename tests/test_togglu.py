#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import io
import locale
import sys
import os

from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread
import port_for
from urllib.parse import urlparse, parse_qs

from .context import togglu
from togglu import togglu

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class TestCLI(unittest.TestCase):

    def test_required_subcommand(self):
        actual_output = io.StringIO()
        sys.stderr = actual_output

        try:
            cli = togglu.CLI()
            cli.execute()

        except SystemExit:
            expected_output = \
                'usage: togglu.py [-h] [--toggl-url TOGGL_URL] [--reports-url REPORTS_URL]' \
                ' {workspaces,timesheet} ...\n' \
                'togglu.py: error: the following arguments are required: subcommand\n'

            self.assertEqual(actual_output.getvalue(), expected_output)

        finally:
            sys.stderr = sys.__stderr__

    def test_required_arguments_for_timesheet(self):
        actual_output = io.StringIO()
        sys.stderr = actual_output

        try:
            cli = togglu.CLI(['timesheet'])
            cli.execute()

        except SystemExit:
            expected_output = \
                'usage: togglu.py timesheet [-h] --workspace-id WORKSPACE_ID [--since SINCE]' \
                ' [--until UNTIL] [--client-id CLIENT_ID]' \
                ' [--tag-id TAG_ID]\n' \
                'togglu.py timesheet: error: the following arguments are required: --workspace-id\n'
                
            self.assertEqual(actual_output.getvalue(), expected_output)

        finally:
            sys.stderr = sys.__stderr__

def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port

class WorkspacesRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        with open(os.path.join(THIS_DIR, os.pardir,'tests/workspaces.json'), 'r') as myfile:
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

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/detailed_report_page1.json'), 'r') as myfile:
            data1 = myfile.read().replace('\n', '')
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/detailed_report_page2.json'), 'r') as myfile:
            data2 = myfile.read().replace('\n', '')
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/detailed_report_page3.json'), 'r') as myfile:
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

class TestTogglU(unittest.TestCase):

    def test_workspaces(self):
        mock_server_port = get_free_port()
        mock_server = HTTPServer(('localhost', mock_server_port), WorkspacesRequestHandler)

        # Start running mock server in a separate thread.
        # Daemon threads automatically shut down when the main process exits.
        mock_server_thread = Thread(target=mock_server.serve_forever)
        mock_server_thread.setDaemon(True)
        mock_server_thread.start()

        stub_url = f'http://localhost:{mock_server_port}'

        try:
            actual_output = io.StringIO()
            sys.stdout = actual_output

            cli = togglu.CLI(['--toggl-url', stub_url, 'workspaces'])
            cli.execute()

            expected_output = "1234567:workspace 1\n2345678:workspace 2\n3456789:workspace 3\n\n"
            self.assertEqual(actual_output.getvalue(), expected_output)
        finally:
            sys.stdout = sys.__stdout__

    def test_timesheet(self):
        mock_server_port = get_free_port()
        mock_server = HTTPServer(('localhost', mock_server_port), DetailedReportPaginationRequestHandler)

        # Start running mock server in a separate thread.
        # Daemon threads automatically shut down when the main process exits.
        mock_server_thread = Thread(target=mock_server.serve_forever)
        mock_server_thread.setDaemon(True)
        mock_server_thread.start()

        stub_url = f'http://localhost:{mock_server_port}'

        self.maxDiff = None
        default_time_locale = locale.getlocale(locale.LC_TIME)[0]

        try:
            locale.setlocale(locale.LC_TIME, 'fr_BE')
            actual_output = io.StringIO()
            sys.stdout = actual_output

            cli = togglu.CLI(['--reports-url', stub_url, 'timesheet', '--workspace-id', '123'])
            cli.execute()
            
            expected_output = \
                '06.12.2018 | Kaloo                          |       1.90\n' \
                '05.12.2018 | VooFix                         |       8.14\n' \
                '23.11.2018 | VooFix                         |       8.54\n' \
                '11.11.2018 | Wikimba                        |       0.11\n' \
                '11.11.2018 | Kwimbee                        |       0.05\n' \
                'total hours: 18.74\n' \
                'days worked: 4.00\n'
            self.assertEqual(actual_output.getvalue(), expected_output)
        finally:
            sys.stdout = sys.__stdout__
            locale.setlocale(locale.LC_TIME, default_time_locale)

if __name__ == '__main__':
    unittest.main()
