#!/usr/bin/env python3

import unittest

from datetime import date

from .context import togglu  # noqa: F401
from togglu.timesheet import Timesheet, TimesheetDateEntry, TimesheetClientEntry, TimeEntries, TimeEntry


class TimesheetTestCase(unittest.TestCase):

    def test_add_time_entry_to_empty_timesheet(self):
        timesheet = Timesheet()
        timesheet.add(TimeEntry('retromm', '2018-11-11T21:02:16+01:00', 123))

        expected = Timesheet(
            [TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 123)])]
        )
        self.assertEqual(timesheet, expected)

    def test_add_time_entry_to_timesheet_with_same_date(self):
        timesheet = Timesheet(
            [TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 123)])]
        )
        timesheet.add(TimeEntry('lupicious', '2018-11-11T21:02:16+01:00', 456))
        self.assertEqual(timesheet, Timesheet(
            [
                TimesheetDateEntry(
                    date.fromisoformat('2018-11-11'),
                    [
                        TimesheetClientEntry('retromm', 123),
                        TimesheetClientEntry('lupicious', 456)
                    ])
            ])
        )

    def test_add_time_entry_to_timesheet_with_same_and_same_client(self):
        timesheet = Timesheet(
            [TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 123)])]
        )
        timesheet.add(TimeEntry('retromm', '2018-11-11T21:02:16+01:00', 456))
        self.assertEqual(timesheet, Timesheet(
            [
                TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 579)])
            ])
        )

    def test_days_worked(self):
        timesheet = Timesheet(
            [
                TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 123)]),
                TimesheetDateEntry(date.fromisoformat('2018-11-12'), [TimesheetClientEntry('retromm', 123)]),
                TimesheetDateEntry(date.fromisoformat('2018-11-13'), [TimesheetClientEntry('retromm', 123)])
            ]
        )

        self.assertEqual(3, timesheet.days_worked())

    def test_duration(self):
        timesheet = Timesheet(
            [
                TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 123)]),
                TimesheetDateEntry(date.fromisoformat('2018-11-12'), [TimesheetClientEntry('retromm', 123)]),
                TimesheetDateEntry(date.fromisoformat('2018-11-13'), [TimesheetClientEntry('retromm', 123)])
            ]
        )

        self.assertEqual(369, timesheet.duration())


class TimesheetDateEntryTestCase(unittest.TestCase):

    def test_add_time_entry_to_empty_timesheet_date_entry(self):
        timesheet_date_entry = TimesheetDateEntry(date.fromisoformat('2018-11-11'))
        timesheet_date_entry.add('retromm', 123)

        expected = TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 123)])
        self.assertEqual(timesheet_date_entry, expected)

    def test_add_time_entry_to_timesheet_date_entry_with_same_client(self):
        timesheet_date_entry = TimesheetDateEntry(
            date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 5)])
        timesheet_date_entry.add('retromm', 4)

        expected = TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 9)])
        self.assertEqual(timesheet_date_entry, expected)

    def test_duration(self):
        timesheet_date_entry = TimesheetDateEntry(date.fromisoformat('2018-11-11'))
        timesheet_date_entry.add('retromm', 123)
        timesheet_date_entry.add('lupicious', 456)

        self.assertEqual(579, timesheet_date_entry.duration())


class TimeEntriesTestCase(unittest.TestCase):

    def test_new_empty_timeentries_has_zero_entries(self):
        time_entries = TimeEntries()
        self.assertEqual(0, len(time_entries.entries), 'time_entries should have 0 entries')

    def test_new_empty_timeentries_should_always_be_empty(self):
        time_entries1 = TimeEntries()
        time_entries1.append(TimeEntry('retromm', '2018-11-11T21:02:16+01:00', 123))
        time_entries1.append(TimeEntry('lupicious', '2018-11-12T21:02:16+01:00', 456))

        time_entries2 = TimeEntries()
        self.assertEqual(0, len(time_entries2.entries), 'time_entries2 should have 0 entries')

    def test_time_entries_not_equal_to_none(self):
        self.assertNotEquals(TimeEntries(), None)

    def test_time_entries_not_equal_to_non_time_entries(self):
        self.assertNotEquals(TimeEntries(), object)

    def test_empty_time_entries_are_equal(self):
        self.assertEqual(TimeEntries(), TimeEntries())

    def test_time_entries_with_one_time_entry_each_having_the_same_fields_are_equal(self):
        self.assertEqual(TimeEntries(
            [TimeEntry("foo", "2018-12-01", 123)]), TimeEntries([TimeEntry("foo", "2018-12-01", 123)])
        )


class TimeEntryTestCase(unittest.TestCase):

    def test_time_entries_having_the_same_fields_are_equal(self):
        self.assertEqual(TimeEntry("foo", "2018-12-01", 123), TimeEntry("foo", "2018-12-01", 123))


if __name__ == '__main__':
    unittest.main()
