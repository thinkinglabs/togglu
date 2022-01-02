
import math
import json

import requests

from togglu.constants import REPORTS_URL
from togglu.timesheet import TimeEntries, TimeEntry


class ReportsRepository:

    def __init__(self, base_url=REPORTS_URL, config=None):
        self.base_url = base_url
        self.config = config

    def detailed_report(self, workspace_id, since=None, until=None, client_id=None, tag_id=None):
        params = {
            "workspace_id": workspace_id, "since": since, "until": until, "client_ids": client_id, "tag_ids": tag_id
        }

        time_entries = TimeEntries()

        number_of_pages = 1
        page = 1
        while 1 <= page <= number_of_pages:
            params['page'] = page
            detailed_report = self._reports(self.base_url, 'details', 'GET', params)

            number_of_pages = math.ceil(detailed_report['total_count'] / detailed_report['per_page'])

            for entry in detailed_report['data']:
                time_entries.append(to_time_entry(entry))

            page += 1

        return time_entries

    def _reports(self, base_url, request_uri, method, params={}, data=None,
                 headers={'content-type': 'application/json'}):
        """
        Makes an HTTP request to the Reports API of toggl.com. Returns a dictionary.
        """
        url = "{}/{}".format(base_url, request_uri)
        params["user_agent"] = "togglu"
        auth = self.config.get_auth() if self.config else None
        try:
            if method == 'GET':
                response = requests.get(url, auth=auth, params=params, data=data, headers=headers)
            else:
                raise NotImplementedError('HTTP method "{}" not implemented.'.format(method))
            response.raise_for_status()  # raise exception on error
            result = json.loads(response.text)
            return result
        except requests.exceptions.RequestException as e:
            print('Sent: {}'.format(data))
            print(e)
            print(response.text)
            raise Exception from e


def to_time_entry(detailed_report_entry):
    return TimeEntry(detailed_report_entry['client'], detailed_report_entry['start'], detailed_report_entry['dur'])
