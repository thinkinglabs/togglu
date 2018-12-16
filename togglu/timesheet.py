
from datetime import datetime, date

class Timesheet:

    def __init__(self, entries = []):
        self.entries = entries

    def add(self, time_entry):
        self.entries.append(TimesheetDateEntry(datetime.fromisoformat(time_entry.start_date).date(), [TimesheetClientEntry(time_entry.client_name, time_entry.duration)]))

    def __eq__(self, other) -> bool:
        return self.entries == other.entries

    def __repr__(self):
        return ','.join([str(item) for item in self.entries])

class TimesheetDateEntry:

    def __init__(self, date, entries = []):
        self.date = date
        self.entries = entries

    def __eq__(self, other):
        return self.date == other.date and \
               self.entries == other.entries

    def __repr__(self):
        return "{" + str(self.date) + ", " + ','.join([str(item) for item in self.entries]) + "}"

class TimesheetClientEntry:

    def __init__(self, client_name, duration):
        self.client_name = client_name
        self.duration = duration

    def __eq__(self, other):
        return self.client_name == other.client_name and \
               self.duration == other.duration

    def __repr__(self):
        return "{" + self.client_name + ":" + str(self.duration) + "}"

class TimeEntries:

    def __init__(self, entries):
        self.entries = entries

    def __eq__(self, other):
        self.entries == other.entries

    def __repr__(self):
        return ','.join([str(item) for item in self.entries])

class TimeEntry:

    def __init__(self, client_name, start_date, duration):
        self.client_name = client_name
        self.start_date = start_date
        self.duration = duration

    def __eq__(self, other):
        return self.client_name == other.client_name and \
            self.start_date == other.start_date and \
            self.duration == other.duration

    def __repr__(self):
        return '{%r, %r, %r}' % self.client_name, self.start_date, self.duration
