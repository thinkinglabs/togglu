#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from datetime import date

from .context import togglu

from togglu.list_timesheet import TimesheetQuery
from togglu.timesheet import Timesheet, TimesheetDateEntry, TimesheetClientEntry, TimeEntries, TimeEntry
from togglu.timesheet_response import TimesheetResponse, TimesheetDateEntryResponse, TimesheetClientEntryResponse

from togglu.timesheet_service import TimesheetService
from togglu.list_timesheet import ListTimesheet

class DetailedReportServiceTestCase(unittest.TestCase):

    @patch('togglu.reports_repository.ReportsRepository')
    def test_timesheet(self, detailed_report_service):

        detailed_report_service.detailed_report.return_value = TimeEntries(
            [
                TimeEntry('anore', '2018-12-06T14:57:18+01:00', 5),
                TimeEntry('calcile', '2018-12-05T13:18:29+01:00', 1),
                TimeEntry('calcile', '2018-12-05T08:55:26+01:00', 2),
                TimeEntry('anore', '2018-12-04T20:25:24+01:00', 6),
                TimeEntry('lunent', '2018-12-04T20:09:09+01:00', 7),
                TimeEntry('calcile', '2018-12-04T13:36:06+01:00', 3),
                TimeEntry('calcile', '2018-12-04T08:47:14+01:00', 6)
            ])

        sut = TimesheetService(detailed_report_service)
        actual = sut.timesheet('workspace_id')

        self.assertEqual(actual, Timesheet(
            [
                TimesheetDateEntry(date.fromisoformat('2018-12-06'), [
                    TimesheetClientEntry('anore', 5)
                ]),
                TimesheetDateEntry(date.fromisoformat('2018-12-05'), [
                    TimesheetClientEntry('calcile', 3)
                ]),
                TimesheetDateEntry(date.fromisoformat('2018-12-04'), [
                    TimesheetClientEntry('anore', 6),
                    TimesheetClientEntry('lunent', 7),
                    TimesheetClientEntry('calcile', 9)
                ])
            ]))


if __name__ == '__main__':
    unittest.main()
