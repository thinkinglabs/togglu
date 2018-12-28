

class TimesheetConsoleRenderer():

    def __init__(self, list_timesheet):
        self.list_timesheet = list_timesheet
    
    def render(self):

        result = self.list_timesheet.execute()
        
        for date_entry in result.entries:
            for client_entry in date_entry.entries:
                print(f'{date_entry.date.strftime("%x"):<10} | {client_entry.client_name:<30} | {client_entry.duration / 1000/60/60:=10.1f}')
        