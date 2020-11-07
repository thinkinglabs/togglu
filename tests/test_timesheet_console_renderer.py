#!/usr/bin/env python3

import unittest
from unittest.mock import patch

import sys
import io
import locale
from datetime import date

from .context import togglu  # noqa: F401
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

            one_hour = 1000 * 60 * 60

            list_timesheet.execute.return_value = TimesheetResponse([
                TimesheetDateEntryResponse(date.fromisoformat("2018-12-27"), [
                    TimesheetClientEntryResponse("enicious", 2.5 * one_hour),
                    TimesheetClientEntryResponse("frontile", 4 * one_hour)
                ]),
                TimesheetDateEntryResponse(date.fromisoformat("2018-12-28"), [
                    TimesheetClientEntryResponse("enicious", 1 * one_hour)
                ])
            ], 2, 7.50 * one_hour)

            sut = TimesheetConsoleRenderer(list_timesheet)
            sut.render(1234)

            expected_output = \
                '27.12.2018 | enicious                       |       2.50\n' \
                '27.12.2018 | frontile                       |       4.00\n' \
                '28.12.2018 | enicious                       |       1.00\n' \
                'total hours: 7.50\n' \
                'days worked: 2.00\n'

            self.assertEqual(actual_output.getvalue(), expected_output)

        finally:
            sys.stdout = sys.__stdout__

            locale.setlocale(locale.LC_TIME, default_time_locale)
