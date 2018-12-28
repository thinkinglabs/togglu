#!/usr/bin/env python3

import unittest
from unittest.mock import patch

import sys
import io
import locale
from datetime import date

from togglu.timesheet_console_renderer import TimesheetConsoleRenderer
from togglu.timesheet_response import TimesheetResponse, TimesheetDateEntryResponse, TimesheetClientEntryResponse

class TestTimesheetConsoleRendererTest(unittest.TestCase):

    @patch('togglu.list_timesheet.ListTimesheet')
    def test_render(self, list_timesheet):
        
        default_time_locale = locale.getlocale(locale.LC_TIME)[0]

        try:
            locale.setlocale(locale.LC_TIME, 'fr_BE')
            actual_output = io.StringIO()
            sys.stdout = actual_output
            list_timesheet.execute.return_value = TimesheetResponse([
                TimesheetDateEntryResponse(date.fromisoformat("2018-12-27"), [
                    TimesheetClientEntryResponse("enicious", 2.5 * 1000*60*60)
                ])
            ])

            sut = TimesheetConsoleRenderer(list_timesheet)
            sut.render()

            expected_output = \
                "27.12.2018 | enicious                       |        2.5\n"
            self.assertEqual(actual_output.getvalue(), expected_output)

        finally:
            sys.stdout = sys.__stdout__

            locale.setlocale(locale.LC_TIME, default_time_locale)
