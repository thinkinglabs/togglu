
from togglu.timesheet import Timesheet

class TimesheetService:

    def __init__(self, detailed_report_repository):
        self.detailed_report_repository = detailed_report_repository

    def timesheet(self, workspace_id, since = None, until = None):
        time_entries = self.detailed_report_repository.detailed_report(workspace_id, since, until)

        timesheet = Timesheet()

        for entry in time_entries:
            timesheet.add(entry)

        return timesheet
