#!/usr/bin/env python3

import sys
import os
import requests
import json
import configparser as ConfigParser

TOGGL_URL = "https://www.toggl.com/api/v8"

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

    def __init__(self):
       result = toggl("/workspaces", "get")
       self.workspaces = json.loads(result)

    def __str__(self):
        result = ""
        for workspace in self.workspaces:
            result += "{}:{}\n".format(workspace['id'], workspace['name'])
        return result

def toggl(url, method, data=None, headers={'content-type' : 'application/json'}):
    """
    Makes an HTTP request to toggl.com. Returns the raw text data received.
    """
    url = "{}{}".format(TOGGL_URL, url)
    try:
        if method == 'get':
            r = requests.get(url, auth=Config().get_auth(), data=data, headers=headers)
        else:
            raise NotImplementedError('HTTP method "{}" not implemented.'.format(method))
        r.raise_for_status() # raise exception on error
        return r.text
    except Exception as e:
        print('Sent: {}'.format(data))
        print(e)
        print(r.text)
        #sys.exit(1)

class CLI():

    def __init__(self, args=None):
        pass

    def execute(self):
        workspaces = Workspaces()
        print(workspaces)

if __name__ == '__main__':
   CLI(sys.argv[1:]).execute()
