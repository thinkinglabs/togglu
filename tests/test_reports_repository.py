#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from .helpers import mock_http_server

import os
from datetime import date

from .context import togglu

from togglu.reports_repository import ReportsRepository

from togglu.list_timesheet import TimesheetQuery
from togglu.timesheet import Timesheet, TimesheetDateEntry, TimesheetClientEntry, TimeEntries, TimeEntry
from togglu.timesheet_response import TimesheetResponse, TimesheetDateEntryResponse, TimesheetClientEntryResponse

from togglu.timesheet_service import TimesheetService
from togglu.list_timesheet import ListTimesheet

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

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


class DetailedReportFilterRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/detailed_report_filter.json'), 'r') as myfile:
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

class ReportsRepositoryTestCase(unittest.TestCase):

    def test_detailed_report_pagination(self):
        mock_server_port = mock_http_server(DetailedReportPaginationRequestHandler)

        stub_url = f'http://localhost:{mock_server_port}'

        sut = ReportsRepository(stub_url)
        time_entries = sut.detailed_report('123')

        expected = TimeEntries([
            TimeEntry("Kaloo", "2018-12-06T14:57:18+01:00", 6850000),
            TimeEntry("VooFix", "2018-12-05T13:18:29+01:00", 17932000),
            TimeEntry("VooFix", "2018-12-05T08:55:26+01:00", 11361000),
            TimeEntry("VooFix", "2018-11-23T20:00:18+01:00", 3821000),
            TimeEntry("VooFix", "2018-11-23T13:53:15+01:00", 13576000),
            TimeEntry("VooFix", "2018-11-23T08:56:20+01:00", 13360000),
            TimeEntry("Wikimba", "2018-11-11T21:02:16+01:00", 391000),
            TimeEntry("Kwimbee", "2018-11-11T20:58:23+01:00", 171000)
            ])
        self.assertEqual(time_entries, expected)
    
    def test_detailed_report_filter(self):
        mock_server_port = mock_http_server(DetailedReportFilterRequestHandler)
        
        stub_url = f'http://localhost:{mock_server_port}'

        sut = ReportsRepository(stub_url)
        time_entries = sut.detailed_report('123', since='2018-11-23', until='2018-11-23', client_id='456', tag_id='123456789')

        expected = TimeEntries([
            TimeEntry("VooFix", "2018-11-23T20:00:18+01:00", 3821000),
            TimeEntry("VooFix", "2018-11-23T13:53:15+01:00", 13576000),
            TimeEntry("VooFix", "2018-11-23T08:56:20+01:00", 13360000)
            ])
        self.assertEqual(time_entries, expected)

if __name__ == '__main__':
    unittest.main()
