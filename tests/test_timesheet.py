#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from datetime import date

from .context import togglu

from togglu.timesheet import Timesheet, TimesheetDateEntry, TimesheetClientEntry, TimeEntry

class TimesheetTestCase(unittest.TestCase):

    def test_add_time_entry_to_empty_timesheet(self):

        timesheet = Timesheet()

        timesheet.add(TimeEntry('retromm', '2018-11-11T21:02:16+01:00', 391000))

        self.assertEqual(timesheet, Timesheet([TimesheetDateEntry(date.fromisoformat('2018-11-11'), [TimesheetClientEntry('retromm', 391000)])]))

if __name__ == '__main__':
    unittest.main()
