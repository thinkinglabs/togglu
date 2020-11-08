
import argparse

from togglu.config import Config, CFG_FILE
from togglu.constants import TOGGL_URL, REPORTS_URL
from togglu.timesheet_console_renderer import TimesheetConsoleRenderer
from togglu.workspaces_console_renderer import WorkspacesConsoleRenderer
from togglu.list_timesheet import ListTimesheet
from togglu.timesheet_service import TimesheetService
from togglu.reports_repository import ReportsRepository
from togglu.toggl_repository import TogglRepository


class CLI():

    def __init__(self, args=[]):
        self.arguments = args
        self.parser = argparse.ArgumentParser(prog='togglu', description='Toggl commandline tool',
                                              formatter_class=self.formatter)
        self.parser.add_argument('--config', default=CFG_FILE)
        self.parser.add_argument('--toggl-url', default=TOGGL_URL)
        self.parser.add_argument('--reports-url', default=REPORTS_URL)
        subparsers = self.parser.add_subparsers(title='available subcommands', dest='subcommand', required=True)
        parser_workspaces = subparsers.add_parser('workspaces')
        parser_workspaces.set_defaults(func=self.workspaces)
        parser_timesheet = subparsers.add_parser('timesheet', formatter_class=self.formatter)
        parser_timesheet.set_defaults(func=self.timesheet)
        parser_timesheet.add_argument('--workspace-id', required=True)
        parser_timesheet.add_argument('--since')
        parser_timesheet.add_argument('--until')
        parser_timesheet.add_argument('--client-id')
        parser_timesheet.add_argument('--tag-id')

    def formatter(self, prog):
        return argparse.HelpFormatter(prog, width=80)

    def execute(self):
        args = self.parser.parse_args(self.arguments)
        args.func(args)

    def workspaces(self, args):
        renderer = WorkspacesConsoleRenderer(
            TogglRepository(args.toggl_url, Config(args.config))
        )
        renderer.render()

    def timesheet(self, args):
        renderer = TimesheetConsoleRenderer(
            ListTimesheet(
                TimesheetService(
                    ReportsRepository(args.reports_url, Config(args.config))
                )
            )
        )
        renderer.render(
            args.workspace_id,
            args.since if hasattr(args, 'since') else None,
            args.until if hasattr(args, 'until') else None,
            args.client_id if hasattr(args, 'client_id') else None,
            args.tag_id if hasattr(args, 'tag_id') else None
        )
