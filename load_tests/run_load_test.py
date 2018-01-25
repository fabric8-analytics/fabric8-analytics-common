#!/usr/local/bin/python3

# This script requires refactoring. Another test script with
# locust is being developed

# Usage: ./run_load_test.py <concurrent request count> <API URL>

import os
import sys
import datetime
from requests_futures.sessions import FuturesSession

start_time = datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y")
print ("TEST START TIME: {}".format(start_time))

try:
	total_threads = int(sys.argv[1])
except IndexError as e:
	total_threads = int(os.getenv('TOTAL_THREAD_COUNT', '10'))
	pass

try:
	api_url = sys.argv[2]
except IndexError as e:
	api_url=os.getenv('RECOMMENDER_API_URL')
	pass

user_key=os.getenv('3SCALE_USER_KEY', '')
api_suffix=''
if user_key != '':
	api_suffix = '?user_key={}'.format(user_key)

session = FuturesSession(max_workers=total_threads)

def close_fps(fp_arr):
	if len(fp_arr) >= 50:
		for fp in fp_arr:
			fp.close()

fp_array = []

for i in range(0, total_threads):
	fp1 = open('data/pom-effective.xml', 'r')
	print ('Run %d for %s is in progress' % (i, '/Users/samuzzal/Performance/pom.xml'))
	try:
		resp = session.post('{}/api/v1/stack-analyses{}'.format(api_url, api_suffix),
							files = {'manifest[]': ('pom.xml', fp1)}, data = {'filePath[]':'/home/JohnDoe'},
							headers={'Authorization': 'Bearer {}'.format(os.getenv('RECOMMENDER_API_TOKEN'))})
	except Exception as e:
		print (e)
		pass

	close_fps(fp_array)
	fp_array.append(fp1)

