# coding: utf-8

import os
import sys
import json
import logging
import datetime
from burglar import Burglar, logger

# set timezone
os.environ['TZ'] = 'Asia/Shanghai'
now = datetime.datetime.now()
stamp = now.strftime('%H:%M')
os.environ['TZ'] = 'UTC'

rootdir = os.path.abspath(os.path.dirname(__file__))
public = os.path.join(rootdir, 'public')

# setting logging
formatter = logging.Formatter(
    '[%(asctime)s %(levelname)s %(filename)s:%(lineno)d]: %(message)s'
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# init burglar
fetch = Burglar(public)

logger.info('Cron job - %s' % stamp)


def parse_weixin(filtered=True):
    with open(os.path.join(public, 'weixin.json')) as f:
        data = json.load(f)

    if filtered:
        keys = list(filter(lambda o: stamp in o['time'], data))
    else:
        keys = data.keys()

    for key in keys:
        item = data[key]
        item['type'] = 'weixin'
        item['name'] = key
        fetch(item)


def parse_zhuanlan(filtered=True):
    with open(os.path.join(public, 'zhuanlan.json')) as f:
        data = json.load(f)

    if filtered:
        keys = list(filter(lambda o: stamp in o['time'], data))
    else:
        keys = data.keys()

    for key in keys:
        item = data[key]
        item['type'] = 'zhuanlan'
        item['name'] = key
        fetch(item)


def parse_daily(filtered=True):
    valid = ['8:00', '10:00', '12:00', '16:00', '20:00', '24:00']
    if filtered and stamp not in valid:
        return
    fetch({'type': 'daily'})


if __name__ == '__main__':
    if '--init' in sys.argv:
        filtered = False
    else:
        filtered = True
    parse_weixin(filtered)
    parse_zhuanlan(filtered)
    parse_daily(filtered)
