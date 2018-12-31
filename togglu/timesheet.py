
from datetime import datetime

class Timesheet:

    def __init__(self, entries = []):
        self.entries = {}
        for date_entry in entries:
            self.entries[date_entry.date] = date_entry

    def add(self, time_entry):
        self._add(datetime.fromisoformat(time_entry.start_date).date(), time_entry.client_name, time_entry.duration)

    def _add(self, time_entry_date, client_name, duration):

        date_entry = self.entries.get(time_entry_date)
        if date_entry is None:
            self.entries[time_entry_date] = TimesheetDateEntry(time_entry_date)

        date_entry = self.entries[time_entry_date]
        date_entry.add(client_name, duration)

    def __eq__(self, other) -> bool:
        return self.entries == other.entries

    def __repr__(self):
        return "Timesheet(entries=%r)" % (self.entries)

class TimesheetDateEntry:

    def __init__(self, date, entries = []):
        self.date = date
        self.entries = {}
        for entry in entries:
            self.add(entry.client_name, entry.duration)

    def add(self, client_name, duration):
        client_entry = self.entries.get(client_name)
        if client_entry is None:
            self.entries[client_name] = TimesheetClientEntry(client_name)
        client_entry = self.entries[client_name]

        client_entry.duration += duration

    def __eq__(self, other):
        return self.date == other.date and \
               self.entries == other.entries

    def __repr__(self):
        return "TimesheetDateEntry(date=%r, entries=%r)" % (self.date, self.entries)

class TimesheetClientEntry:

    def __init__(self, client_name, duration = 0):
        self.client_name = client_name
        self.duration = duration

    def __eq__(self, other):
        return self.client_name == other.client_name and \
               self.duration == other.duration

    def __repr__(self):
        return "TimesheetClientEntry(client_name=%r, duration=%r)" % (self.client_name, self.duration)

class TimeEntries:

    def __init__(self, entries=None):
        self.entries = [] if entries is None else entries

    def append(self, time_entry):
        self.entries.append(time_entry)

    def __eq__(self, other):
        return other is not None and \
            other.__class__.__name__ == 'TimeEntries' and \
            self.entries == other.entries

    def __iter__(self):
        return iter(self.entries)

    def __repr__(self):
        return "TimeEntries(entries=%r)" % (self.entries)

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
        return "TimeEntry(client_name=%r, start_date=%r, duration=%r)" % (self.client_name, self.start_date, self.duration)
