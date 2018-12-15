#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from datetime import date

from .context import togglu

from togglu.list_timesheet import TimesheetQuery
from togglu.timesheet import Timesheet, TimesheetDateEntry, TimesheetCustomerEntry
from togglu.timesheet_response import TimesheetResponse, TimesheetDateEntryResponse, TimesheetCustomerEntryResponse

from togglu.detailed_report_service import DetailedReportService
from togglu.list_timesheet import ListTimesheet

class ListTimesheetTestCase(unittest.TestCase):

    @patch('togglu.detailed_report_service.DetailedReportService')
    def test_execute(self, detailed_report_service):

        detailed_report_service.overview.return_value=Timesheet(
        [
            TimesheetDateEntry(date.fromisoformat("2018-12-16"), [TimesheetCustomerEntry("sylent", 8.5)]),
            TimesheetDateEntry(date.fromisoformat("2018-12-17"), [TimesheetCustomerEntry("euronoodle", 2.5), TimesheetCustomerEntry("sylent", 4)])
        ])

        sut = ListTimesheet(detailed_report_service)
        actual = sut.execute(TimesheetQuery("api_token", "workspace_id"))

        self.assertEqual(actual, TimesheetResponse(
            [
                TimesheetDateEntryResponse(date.fromisoformat("2018-12-16"), [TimesheetCustomerEntryResponse("sylent", 8.5)]),
                TimesheetDateEntryResponse(date.fromisoformat("2018-12-17"),
                                   [TimesheetCustomerEntryResponse("euronoodle", 2.5), TimesheetCustomerEntryResponse("sylent", 4)])
            ]))


if __name__ == '__main__':
    unittest.main()
