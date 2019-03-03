

class TimesheetResponse:
    def __init__(self, entries=[], days_worked=0):
        self.days_worked = days_worked
        self.entries = entries
    
    def get_days_worked(self):
        return self.days_worked

    def __eq__(self, other) -> bool:
        return self.entries == other.entries

    def __repr__(self):
        return ','.join([str(item) for item in self.entries])

class TimesheetDateEntryResponse:
    def __init__(self, date, entries=[]):
        self.date = date
        self.entries = entries

    def __eq__(self, other):
        return self.date == other.date and \
               self.entries == other.entries

    def __repr__(self):
        return "{" + str(self.date) + ", " + ','.join([str(item) for item in self.entries]) + "}"

class TimesheetClientEntryResponse:
    def __init__(self, client_name, duration):
        self.client_name = client_name
        self.duration = duration

    def __eq__(self, other):
        return self.client_name == other.client_name and \
               self.duration == other.duration

    def __repr__(self):
        return "{"+self.client_name + ":" + str(self.duration) + "}"