#!/usr/bin/env python3

import time
import requests
import logging
import sys

EXITMSG='''\n
\tRun '$ docker-compose ps -a'
\tand note if any container have an 'Exited' Status
'''

logging.basicConfig(level=20)
starttime = time.time()

status = 0

while status != 200:

    time.sleep(10)

    if (time.time() - starttime > 300) and (status != 200):
        logging.error('Timed out!' + EXITMSG)
        sys.exit(1)

    try:
        r = requests.get('http://localhost:8080')
        status = r.status_code
    except Exception as e:
        logging.info('Waiting for service to come up...')

    if status == 200:
        logging.info('Service Ready!')
