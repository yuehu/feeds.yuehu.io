# coding: utf-8

import os
import sys
import json
import random
import logging
import datetime
from multiprocessing import Pool
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

logger.info('Cron job - %s' % stamp)


fetch = Burglar(public)


def parse_weixin(filtered=True):
    with open(os.path.join(public, 'weixin.json')) as f:
        data = json.load(f)

    keys = data.keys()
    if filtered:
        keys = list(filter(lambda k: stamp in data[k]['time'], keys))

    for key in keys:
        item = data[key]
        item['type'] = 'weixin'
        item['name'] = key
        yield item


def parse_zhuanlan(filtered=True):
    with open(os.path.join(public, 'zhuanlan.json')) as f:
        data = json.load(f)

    keys = data.keys()
    if filtered:
        keys = list(filter(lambda k: stamp in data[k]['time'], keys))

    for key in keys:
        item = data[key]
        item['type'] = 'zhuanlan'
        item['name'] = key
        yield item


def parse_daily(filtered=True):
    valid = ['8:00', '10:00', '12:00', '16:00', '20:00', '24:00']
    if filtered and stamp not in valid:
        return
    yield {'type': 'daily'}


def main(filtered=True):
    pool = Pool(processes=4)
    rv = []
    rv.append(pool.map_async(fetch, parse_weixin(filtered)))
    rv.append(pool.map_async(fetch, parse_zhuanlan(filtered)))
    rv.append(pool.map_async(fetch, parse_daily(filtered)))
    for result in rv:
        result.wait()


if __name__ == '__main__':
    main('--init' not in sys.argv)
