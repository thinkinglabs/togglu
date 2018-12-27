#!/usr/bin/env python3

import unittest
from unittest.mock import patch

import sys
import io
from datetime import date

from togglu.timesheet_console_renderer import TimesheetConsoleRenderer
from togglu.timesheet_response import TimesheetResponse, TimesheetDateEntryResponse, TimesheetClientEntryResponse

class TestTimesheetConsoleRendererTest(unittest.TestCase):

    @patch('togglu.list_timesheet.ListTimesheet')
    def test_render(self, list_timesheet):

        try:
            actual_output = io.StringIO()
            sys.stdout = actual_output
            list_timesheet.execute.return_value = TimesheetResponse([
                TimesheetDateEntryResponse(date.fromisoformat("2018-12-27"), [
                    TimesheetClientEntryResponse("enicious", 4 * 1000*60*60)
                ])
            ])

            sut = TimesheetConsoleRenderer(list_timesheet)
            sut.render()

            expected_output = "2018-12-27      enicious      4\n"
            self.assertEqual(actual_output.getvalue(), expected_output)

        finally:
            sys.stdout = sys.__stdout__
