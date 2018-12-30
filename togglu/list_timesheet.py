
from togglu.timesheet_service import TimesheetService
from togglu.timesheet_response import TimesheetResponse, TimesheetDateEntryResponse, TimesheetClientEntryResponse

class TimesheetQuery:
    def __init__(self, workspace_id, since = None, until = None):
        self.workspace_id = workspace_id
        self.since = since
        self.until = until

class ListTimesheet:

    def __init__(self, detailed_report_service):
        self.detailed_report_service = detailed_report_service


    def execute(self, query):

        timesheet = self.detailed_report_service.timesheet(query.workspace_id, query.since, query.until)

        return to_timesheet_response(timesheet)

def to_timesheet_response(timesheet):
    return TimesheetResponse(list(map(to_date_entry_response, timesheet.entries.values())))

def to_date_entry_response(timesheet_date_entry):
        return TimesheetDateEntryResponse(timesheet_date_entry.date, list(map(to_customer_entry_response, timesheet_date_entry.entries.values())))

def to_customer_entry_response(timesheet_customer_entry):
        return TimesheetClientEntryResponse(timesheet_customer_entry.client_name, timesheet_customer_entry.duration)

