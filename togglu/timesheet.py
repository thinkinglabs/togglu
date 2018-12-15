
class Timesheet:

    def __init__(self, entries = []):
        self.entries = entries

class TimesheetDateEntry:

    def __init__(self, date, entries = []):
        self.date = date
        self.entries = entries

class TimesheetCustomerEntry:

    def __init__(self, customer_name, hours_worked):
        self.customer_name = customer_name
        self.hours_worked = hours_worked

