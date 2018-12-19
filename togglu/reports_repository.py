
import requests
import json
import math
import sys

from togglu.togglu import REPORTS_URL
from togglu.timesheet import TimeEntries, TimeEntry

class ReportsRepository:

    def __init__(self, base_url = REPORTS_URL, config = None):
        self.base_url = base_url
        self.config = config

    def detailed_report(self, workspace_id, since = None, until = None):
        params = {"workspace_id": workspace_id, "since": since, "until": until}

        time_entries = TimeEntries()

        detailed_report = self._reports(self.base_url, "details", "get", params)

        number_of_pages = math.ceil(detailed_report['total_count'] / detailed_report['per_page'])

        for entry in detailed_report['data']:
            time_entries.append(to_time_entry(entry))

        for page in range(2, number_of_pages + 1):
            params['page'] = page
            detailed_report = self._reports(self.base_url, "details", "get", params)
            for entry in detailed_report['data']:
                time_entries.append(to_time_entry(entry))

        return time_entries


    def _reports(self, base_url, request_uri, method, params=None, data=None, headers={'content-type': 'application/json'}):
        """
        Makes an HTTP request to toggl.com. Returns the raw text data received.
        """
        url = "{}/{}".format(base_url, request_uri)
        params["user_agent"] = "togglu"
        auth = self.config.get_auth() if self.config else None
        try:
            if method == 'get':
                r = requests.get(url, auth=auth, params=params, data=data, headers=headers)
            else:
                raise NotImplementedError('HTTP method "{}" not implemented.'.format(method))
            r.raise_for_status()  # raise exception on error
            return json.loads(r.text)
        except Exception as e:
            print('Sent: {}'.format(data))
            print(e)
            print(r.text)
            sys.exit(1)

def to_time_entry(detailed_report_entry):
    return TimeEntry(detailed_report_entry['client'], detailed_report_entry['start'], detailed_report_entry['dur'])