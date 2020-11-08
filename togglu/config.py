

import os

import requests
import configparser as ConfigParser

CFG_FILE = '~/.togglrc'


class Config():
    """
    toggl configuration data, read from ~/.togglrc.
    Properties:
        auth - api_token
    """

    # TODO: don't read and write in constructor
    def __init__(self, cfg_file=CFG_FILE):
        """
        Reads configuration data from ~/.togglrc.
        """
        self.cfg_file = cfg_file
        self.cfg = ConfigParser.RawConfigParser({'continue_creates': 'false'})
        if self.cfg.read(os.path.expanduser(self.cfg_file)) == []:
            self._create_empty_config()
            raise IOError("Missing ~/.togglrc. A default has been created for editing.")

    def _create_empty_config(self):
        """
        Creates a blank ~/.togglrc.
        """
        cfg = ConfigParser.RawConfigParser()
        cfg.add_section('auth')
        cfg.set('auth', 'api_token', 'your_api_token')
        with open(os.path.expanduser(self.cfg_file), 'w') as cfgfile:
            cfg.write(cfgfile)
        os.chmod(os.path.expanduser(self.cfg_file), 0o600)

    def get(self, section, key):
        """
        Returns the value of the configuration variable identified by the
        given key within the given section of the configuration file. Raises
        ConfigParser exceptions if the section or key are invalid.
        """
        return self.cfg.get(section, key).strip()

    def get_auth(self):
        return requests.auth.HTTPBasicAuth(self.get('auth', 'api_token'), 'api_token')
