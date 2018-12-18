#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from datetime import date

from .context import togglu

from togglu.timesheet import Timesheet, TimesheetDateEntry, TimesheetClientEntry, TimeEntry

class TimesheetTestCase(unittest.TestCase):

    def test_add_time_entry_to_empty_timesheet(self):
        timesheet = Timesheet()
        timesheet.add(TimeEntry('retromm', '2018-11-11T21:02:16+01:00', 123))
        self.assertEqual(timesheet, Timesheet([TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 123)])]))

    def test_add_time_entry_to_timesheet_with_same_date(self):
        timesheet = Timesheet([TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 123)])])
        timesheet.add(TimeEntry('lupicious', '2018-11-11T21:02:16+01:00', 456))
        self.assertEqual(timesheet, Timesheet(
            [
                TimesheetDateEntry(date.fromisoformat('2018-11-11'),
                                   [
                                       TimesheetClientEntry('retromm', 123),
                                       TimesheetClientEntry('lupicious', 456)
                                   ])
            ]))

class TimesheetDateEntryCase(unittest.TestCase):

    def test_add_time_entry_to_empty_timesheet_date_entry(self):
        timesheet_date_entry = TimesheetDateEntry(date.fromisoformat('2018-11-11'))
        timesheet_date_entry.add('retromm', 123)

        self.assertEqual(timesheet_date_entry, TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 123)]))

    def test_add_time_entry_to_timesheet_date_entry_with_same_client(self):
        timesheet_date_entry = TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 5)])
        timesheet_date_entry.add('retromm', 4)

        self.assertEqual(timesheet_date_entry, TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 9)]))


class TimeEntries(unittest.TestCase):

    def test_time_entries_not_equal_to_none(self):
        self.assertNotEquals(TimeEntries(), None)

    def test_time_entries_not_equal_to_non_time_entries(self):
        self.assertNotEquals(TimeEntries, object)

if __name__ == '__main__':
    unittest.main()
