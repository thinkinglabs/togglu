#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from datetime import date

from .context import togglu

from togglu.timesheet import Timesheet, TimesheetDateEntry, TimesheetClientEntry, TimeEntries, TimeEntry

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

class TimesheetDateEntryTestCase(unittest.TestCase):

    def test_add_time_entry_to_empty_timesheet_date_entry(self):
        timesheet_date_entry = TimesheetDateEntry(date.fromisoformat('2018-11-11'))
        timesheet_date_entry.add('retromm', 123)

        self.assertEqual(timesheet_date_entry, TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 123)]))

    def test_add_time_entry_to_timesheet_date_entry_with_same_client(self):
        timesheet_date_entry = TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 5)])
        timesheet_date_entry.add('retromm', 4)

        self.assertEqual(timesheet_date_entry, TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 9)]))


class TimeEntriesTestCase(unittest.TestCase):

    def test_time_entries_not_equal_to_none(self):
        self.assertNotEquals(TimeEntries(), None)

    def test_time_entries_not_equal_to_non_time_entries(self):
        self.assertNotEquals(TimeEntries(), object)

    def test_empty_time_entries_are_equal(self):
        self.assertEqual(TimeEntries(), TimeEntries())

    def test_time_entries_with_one_time_entry_each_having_the_same_fields_are_equal(self):
        self.assertEqual(TimeEntries([TimeEntry("foo", "2018-12-01", 123)]), TimeEntries([TimeEntry("foo", "2018-12-01", 123)]))

class TimeEntryTestCase(unittest.TestCase):

    def test_time_entries_having_the_same_fields_are_equal(self):
        self.assertEqual(TimeEntry("foo", "2018-12-01", 123), TimeEntry("foo", "2018-12-01", 123))

if __name__ == '__main__':
    unittest.main()
