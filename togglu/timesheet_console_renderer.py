

class TimesheetConsoleRenderer():

    def __init__(self, list_timesheet):
        self.list_timesheet = list_timesheet
    
    def render(self):

        result = self.list_timesheet.execute()
        
        for date_entry in result.entries:
            for client_entry in date_entry.entries:
                print("%s      %s      %d" % (date_entry.date, client_entry.client_name, client_entry.duration / 1000/60/60))
        