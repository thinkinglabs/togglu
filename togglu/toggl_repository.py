
import json

import requests

from togglu.constants import TOGGL_URL
from togglu.workspace import Workspace


class TogglRepository:

    def __init__(self, base_url=TOGGL_URL, config=None):
        self.base_url = base_url
        self.config = config

    def workspaces(self):
        workspaces = []

        response = self._toggl(self.base_url, 'workspaces', 'GET')

        for item in response:
            workspaces.append(Workspace(item['id'], item['name']))

        return workspaces

    def _toggl(self, base_url, request_uri, method, params={},
               headers={'content-type': 'application/json'}):
        """
        Makes an HTTP request to the Toggle API of toggl.com. Returns a dictionary.
        """
        url = "{}/{}".format(base_url, request_uri)
        params["user_agent"] = "togglu"
        auth = self.config.get_auth() if self.config else None
        try:
            if method == 'GET':
                response = requests.get(url, auth=auth, params=params, headers=headers)
            else:
                raise NotImplementedError('HTTP method "{}" not implemented.'.format(method))
            response.raise_for_status()  # raise exception on error
            result = json.loads(response.text)
            return result
        except requests.exceptions.RequestException as e:
            print(e)
            print(response.text)
