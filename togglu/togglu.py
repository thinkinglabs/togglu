#!/usr/bin/env python3

import sys
import os
import argparse
import math
from datetime import datetime

import requests
import json
import configparser as ConfigParser


TOGGL_URL = 'https://www.toggl.com/api/v8'
REPORTS_URL = 'https://www.toggl.com/reports/api/v2/details'

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

class Workspaces:

    def __init__(self, toggl_url = TOGGL_URL):
        self.workspaces = toggl(toggl_url, "/workspaces", "get")

    def __str__(self):
        result = ""
        for workspace in self.workspaces:
            result += "{}:{}\n".format(workspace['id'], workspace['name'])
        return result

class DaysWorked:

    def __init__(self, reports_url = REPORTS_URL):
        self.days_worked = 0

        self.days_worked = self.calculate(reports_url)

    @staticmethod
    def calculate(reports_url = REPORTS_URL):
        days_worked = 0
        page = 1
        previous_date = None

        while True:
            report = reports(reports_url, "/details", "get")
            time_entries = report['data']

            pages = math.ceil(report['total_count'] / report['per_page'])

            (result, previous_date) = DaysWorked.calculate_per_page(time_entries, previous_date)
            days_worked += result

            page += 1
            if page > pages:
                break

        return days_worked

    @staticmethod
    def calculate_per_page(time_entries, date=None):
        days_worked = 0
        previous_date = date
        for time_entry in time_entries:
            start = datetime.fromisoformat(time_entry['start'])
            this_date = start.date()
            days_worked += 0 if previous_date == this_date else 1
            previous_date = this_date
        return (days_worked, previous_date)

    def __str__(self):
        result = str(self.days_worked)
        return result

def toggl(base_url, request_uri, method, params=None, data=None, headers={'content-type' : 'application/json'}):
    """
    Makes an HTTP request to toggl.com. Returns the raw text data received.
    """
    url = "{}{}".format(base_url, request_uri)
    try:
        if method == 'get':
            r = requests.get(url, auth=Config().get_auth(), params=params, data=data, headers=headers)
        else:
            raise NotImplementedError('HTTP method "{}" not implemented.'.format(method))
        r.raise_for_status() # raise exception on error
        return json.loads(r.text)
    except Exception as e:
        print('Sent: {}'.format(data))
        print(e)
        print(r.text)
        sys.exit(1)

def reports(base_url, request_uri, method, params=None, data=None, headers={'content-type': 'application/json'}):
    """
    Makes an HTTP request to toggl.com. Returns the raw text data received.
    """
    url = "{}{}?user_agent=togglu&workspace_id=509982&since=2018-11-01&page=1".format(base_url, request_uri)
    try:
        if method == 'get':
            r = requests.get(url, auth=Config().get_auth(), params=params, data=data, headers=headers)
        else:
            raise NotImplementedError('HTTP method "{}" not implemented.'.format(method))
        r.raise_for_status() # raise exception on error
        return json.loads(r.text)
    except Exception as e:
        print('Sent: {}'.format(data))
        print(e)
        print(r.text)
        sys.exit(1)



class CLI():

    def __init__(self, args=None):
        parser = argparse.ArgumentParser(prog='togglu.py', description='Toggl commandline tool')
        parser.add_argument('--toggl-url', default=TOGGL_URL)
        parser.add_argument('--reports-url', default=REPORTS_URL)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--workspaces', action='store_true')
        group.add_argument('--days-worked', action='store_true')
        args = parser.parse_args(args)
        self.toggl_url = args.toggl_url
        self.reports_url = args.reports_url
        self.workspaces = args.workspaces
        self.days_worked = args.days_worked

    def execute(self):
        if self.workspaces:
            workspaces = Workspaces(self.toggl_url)
            print(workspaces)
        elif self.days_worked:
            print(DaysWorked(self.reports_url))

if __name__ == '__main__':
   CLI(sys.argv[1:]).execute()
