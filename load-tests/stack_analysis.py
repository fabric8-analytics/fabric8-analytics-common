"""Stack Analysis Load test."""

import os
import datetime
import time
from requests_futures.sessions import FuturesSession

start_time = datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y")
print("TEST START TIME: {}".format(start_time))


three_scale_token = os.getenv('THREE_SCALE_PREVIEW_USER_KEY', '')
api_url = os.getenv('F8A_API_V2_URL')
api_suffix = ''


def close_fps(fp_arr):
    """Close all the file pointers."""
    for file_p in fp_arr:
        file_p.close()


fp_array = []
futures = []
ecosystem_file_mapping = {'npm': 'npmlist.json', 'pypi': 'pylist.json', 'maven': 'dependencies.txt'}

params = {'x-3scale-account-secret': three_scale_token}

session = FuturesSession(max_workers=3)

try:

    for i in range(0, 15):
        for ecosystem in ['npm', 'maven', 'pypi']:
            file_name = ecosystem_file_mapping[ecosystem]
            fp = open('data/{}'.format(file_name), 'rb')
            fp_array.append(fp)
            file_path = os.path.abspath(os.path.dirname('data/{}'.format(file_name)))
            future = session.post('{}/api/v2/stack-analyses{}'.format(api_url, api_suffix),
                                  files={'manifest': (file_name, fp)},
                                  data={'file_path': file_path, 'ecosystem': ecosystem},
                                  headers=params)

            futures.append(future)
        time.sleep(4)
        i += 1

except Exception as e:
    print(e)
    pass

for future in futures:
    print('The response details are {}'.format(future.result().text))
close_fps(fp_array)
