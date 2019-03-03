#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import mountepy
import port_for

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

class ReportsRepositoryTestCase(unittest.TestCase):

    def test_detailed_report_pagination(self):

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/detailed_report_page1.json'), 'r') as myfile:
            data1 = myfile.read().replace('\n', '')
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/detailed_report_page2.json'), 'r') as myfile:
            data2 = myfile.read().replace('\n', '')
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/detailed_report_page3.json'), 'r') as myfile:
            data3 = myfile.read().replace('\n', '')

        with mountepy.Mountebank() as mb:
            imposter = mb.add_imposter({
                'protocol': 'http',
                'port': port_for.select_random(),
                'stubs': [
                    {
                        'predicates': [
                            {
                                'equals': {
                                    'method': 'GET',
                                    'path': '/details',
                                    'query': { 'page': '1'}
                                }
                            }
                        ],
                        'responses': [
                            {
                                'is': {
                                    'statusCode': 200,
                                    'headers': {'Content-Type': 'application/json'},
                                    'body': data1
                                }
                            }
                        ]
                    },
                    {
                        'predicates': [
                            {
                                'equals': {
                                        'method': 'GET',
                                        'path': '/details',
                                        'query': { 'page': '2'}
                                }
                            }
                        ],
                        'responses': [
                            {
                                'is': {
                                    'statusCode': 200,
                                    'headers': {'Content-Type': 'application/json'},
                                    'body': data2
                                }
                            }
                        ]
                    },
                    {
                        'predicates': [
                            {
                                'equals': {
                                    'method': 'GET',
                                    'path': '/details',
                                        'query': { 'page': '3'}
                                }
                            }
                        ],
                        'responses': [
                            {
                                'is': {
                                    'statusCode': 200,
                                    'headers': {'Content-Type': 'application/json'},
                                    'body': data3
                                }
                            }
                        ]
                    }
                ]
            })

            stub_url = f'http://localhost:{imposter.port}'

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

if __name__ == '__main__':
    unittest.main()
