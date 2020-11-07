#!/usr/bin/env python3

import sys
import os
import argparse

import requests
import configparser as ConfigParser

from togglu.constants import TOGGL_URL, REPORTS_URL
from togglu.timesheet_console_renderer import TimesheetConsoleRenderer
from togglu.workspaces_console_renderer import WorkspacesConsoleRenderer
from togglu.list_timesheet import ListTimesheet
from togglu.timesheet_service import TimesheetService
from togglu.reports_repository import ReportsRepository
from togglu.toggl_repository import TogglRepository


class Config(object):
    """
    toggl configuration data, read from ~/.togglrc.
    Properties:
        auth - api_token.
        options - (timezone, time_format, continue_creates) tuple
    """

    def __init__(self):
        """
        Reads configuration data from ~/.togglrc.
        """
        self.cfg = ConfigParser.RawConfigParser({'continue_creates': 'false'})
        if self.cfg.read(os.path.expanduser('~/.togglrc')) == []:
            self._create_empty_config()
            raise IOError("Missing ~/.togglrc. A default has been created for editing.")

    def _create_empty_config(self):
        """
        Creates a blank ~/.togglrc.
        """
        cfg = ConfigParser.RawConfigParser()
        cfg.add_section('auth')
        cfg.set('auth', 'api_token', 'your_api_token')
        cfg.add_section('options')
        cfg.set('options', 'timezone', 'UTC')
        cfg.set('options', 'time_format', '%I:%M%p')
        cfg.set('options', 'continue_creates', 'true')
        with open(os.path.expanduser('~/.togglrc'), 'w') as cfgfile:
            cfg.write(cfgfile)
        os.chmod(os.path.expanduser('~/.togglrc'), 0o600)

    def get(self, section, key):
        """
        Returns the value of the configuration variable identified by the
        given key within the given section of the configuration file. Raises
        ConfigParser exceptions if the section or key are invalid.
        """
        return self.cfg.get(section, key).strip()

    def get_auth(self):
        return requests.auth.HTTPBasicAuth(self.get('auth', 'api_token'), 'api_token')


class CLI():

    def __init__(self, args=[]):
        self.arguments = args
        self.parser = argparse.ArgumentParser(prog='togglu.py', description='Toggl commandline tool')
        self.parser.add_argument('--toggl-url', default=TOGGL_URL)
        self.parser.add_argument('--reports-url', default=REPORTS_URL)
        subparsers = self.parser.add_subparsers(title='available subcommands', dest='subcommand', required=True)
        parser_workspaces = subparsers.add_parser('workspaces')
        parser_workspaces.set_defaults(func=self.workspaces)
        parser_timesheet = subparsers.add_parser('timesheet')
        parser_timesheet.set_defaults(func=self.timesheet)
        parser_timesheet.add_argument('--workspace-id', required=True)
        parser_timesheet.add_argument('--since')
        parser_timesheet.add_argument('--until')
        parser_timesheet.add_argument('--client-id')
        parser_timesheet.add_argument('--tag-id')

    def execute(self):
        args = self.parser.parse_args(self.arguments)
        args.func(args)

    def workspaces(self, args):
        renderer = WorkspacesConsoleRenderer(
            TogglRepository(args.toggl_url, Config())
        )
        renderer.render()

    def timesheet(self, args):
        renderer = TimesheetConsoleRenderer(
            ListTimesheet(
                TimesheetService(
                    ReportsRepository(args.reports_url, Config())
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


if __name__ == '__main__':
    cli = CLI(sys.argv[1:])
    cli.execute()
