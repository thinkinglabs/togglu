
from togglu.list_timesheet import TimesheetQuery

class TimesheetConsoleRenderer():

    def __init__(self, list_timesheet):
        self.list_timesheet = list_timesheet
    
    def render(self, workspace_id, since=None, until=None):

        result = self.list_timesheet.execute(TimesheetQuery(workspace_id, since, until))
        
        for date_entry in result.entries:
            for client_entry in date_entry.entries:
                print(f'{date_entry.date.strftime("%x"):<10} | {client_entry.client_name:<30} | {client_entry.duration / 1000/60/60:=10.1f}')
        
        print(f'days worked: {result.get_days_worked()}')
        