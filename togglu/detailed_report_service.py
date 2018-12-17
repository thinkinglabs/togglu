
from togglu.timesheet import Timesheet

class DetailedReportService:

    def __init__(self, detailed_report_repository):
        self.detailed_report_repository = detailed_report_repository

    def timesheet(self, api_token, workspace_id, since = None, until = None):
        time_entries = self.detailed_report_repository.report(api_token, workspace_id, since, until)

        timesheet = Timesheet()

        for entry in time_entries:
            timesheet.add(entry)

        return timesheet
