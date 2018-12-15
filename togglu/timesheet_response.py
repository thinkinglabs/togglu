

class TimesheetResponse:
    def __init__(self, entries=[]):
        self.entries = entries

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

class TimesheetCustomerEntryResponse:
    def __init__(self, customer_name, hours_worked):
        self.customer_name = customer_name
        self.hours_worked = hours_worked

    def __eq__(self, other):
        return self.customer_name == other.customer_name and \
               self.hours_worked == other.hours_worked

    def __repr__(self):
        return "{"+self.customer_name+":"+str(self.hours_worked)+"}"