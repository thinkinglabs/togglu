#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from datetime import date

from .context import togglu  # noqa: F401
from togglu.list_timesheet import TimesheetQuery
from togglu.timesheet import Timesheet, TimesheetDateEntry, TimesheetClientEntry
from togglu.timesheet_response import TimesheetResponse
from togglu.timesheet_response import TimesheetDateEntryResponse
from togglu.timesheet_response import TimesheetClientEntryResponse
from togglu.list_timesheet import ListTimesheet


class ListTimesheetTestCase(unittest.TestCase):

    @patch('togglu.timesheet_service.TimesheetService')
    def test_execute(self, detailed_report_service):

        detailed_report_service.timesheet.return_value = Timesheet(
            [
                TimesheetDateEntry(
                    date.fromisoformat('2018-12-16'),
                    [TimesheetClientEntry('sylent', 8.5)]),
                TimesheetDateEntry(
                    date.fromisoformat('2018-12-17'),
                    [TimesheetClientEntry('euronoodle', 2.5), TimesheetClientEntry('sylent', 4)])
            ])

        sut = ListTimesheet(detailed_report_service)
        actual = sut.execute(TimesheetQuery('workspace_id'))

        self.assertEqual(actual, TimesheetResponse(
            [
                TimesheetDateEntryResponse(
                    date.fromisoformat("2018-12-16"),
                    [TimesheetClientEntryResponse('sylent', 8.5)]),
                TimesheetDateEntryResponse(
                    date.fromisoformat("2018-12-17"),
                    [TimesheetClientEntryResponse('euronoodle', 2.5), TimesheetClientEntryResponse('sylent', 4)])
            ]))
        self.assertEqual(actual.get_days_worked(), 2, 'number of days worked should be 2')


if __name__ == '__main__':
    unittest.main()
