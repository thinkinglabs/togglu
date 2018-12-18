
import requests

from togglu import REPORTS_URL

class ReportsRepository:

    def __init__(self, base_url = REPORTS_URL, config = None):
        self.base_url = base_url
        self.config = config

    def detailed_report(workspace_id, since = None, until = None):
        """
        Makes an HTTP request to toggl.com. Returns the raw text data received.
        """
        params = {}
        url = "{}{}".format(base_url, "details")
        try:
            r = requests.get(url, auth=config.get_auth(), params=params, data=data, headers=headers)
            r.raise_for_status()  # raise exception on error
            return json.loads(r.text)
        except Exception as e:
            print('Sent: {}'.format(data))
            print(e)
            print(r.text)
            sys.exit(1)