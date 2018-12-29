#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from datetime import date

from .context import togglu

from togglu.list_timesheet import TimesheetQuery
from togglu.timesheet import Timesheet, TimesheetDateEntry, TimesheetClientEntry
from togglu.timesheet_response import TimesheetResponse, TimesheetDateEntryResponse, TimesheetClientEntryResponse

from togglu.timesheet_service import TimesheetService
from togglu.list_timesheet import ListTimesheet

class ListTimesheetTestCase(unittest.TestCase):

    @patch('togglu.timesheet_service.TimesheetService')
    def test_execute(self, detailed_report_service):

        detailed_report_service.overview.return_value=Timesheet(
        [
            TimesheetDateEntry(date.fromisoformat('2018-12-16'), [TimesheetClientEntry('sylent', 8.5)]),
            TimesheetDateEntry(date.fromisoformat('2018-12-17'), [TimesheetClientEntry('euronoodle', 2.5), TimesheetClientEntry('sylent', 4)])
        ])

        sut = ListTimesheet(detailed_report_service)
        actual = sut.execute(TimesheetQuery('workspace_id'))

        self.assertEqual(actual, TimesheetResponse(
            [
                TimesheetDateEntryResponse(date.fromisoformat("2018-12-16"), [TimesheetClientEntryResponse('sylent', 8.5)]),
                TimesheetDateEntryResponse(date.fromisoformat("2018-12-17"),
                                           [TimesheetClientEntryResponse('euronoodle', 2.5), TimesheetClientEntryResponse('sylent', 4)])
            ]))


if __name__ == '__main__':
    unittest.main()
