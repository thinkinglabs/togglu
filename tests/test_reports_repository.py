#!/usr/bin/env python3

import unittest

from .helpers.http import mock_http_server
from .helpers.http import DetailedReportPaginationRequestHandler
from .helpers.http import DetailedReportFilterRequestHandler
from .helpers.http import HttpGoneRequestHandler

from .context import togglu  # noqa: F401
from togglu.reports_repository import ReportsRepository
from togglu.timesheet import TimeEntries, TimeEntry


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
        time_entries = sut.detailed_report(
            '123', since='2018-11-23', until='2018-11-23', client_id='456', tag_id='123456789')

        expected = TimeEntries([
            TimeEntry("VooFix", "2018-11-23T20:00:18+01:00", 3821000),
            TimeEntry("VooFix", "2018-11-23T13:53:15+01:00", 13576000),
            TimeEntry("VooFix", "2018-11-23T08:56:20+01:00", 13360000)
        ])
        self.assertEqual(time_entries, expected)

    def test_410_gone(self):
        mock_server_port = mock_http_server(HttpGoneRequestHandler)

        stub_url = f'http://localhost:{mock_server_port}'

        sut = ReportsRepository(stub_url)
        with self.assertRaises(Exception):
            sut.detailed_report(
                '123',
                since='2018-11-23',
                until='2018-11-23',
                client_id='456',
                tag_id='123456789'
            )
