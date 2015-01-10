# coding: utf-8

import os
import sys
import json
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
    with open(os.path.join(public, 'zhihu.json')) as f:
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
    logger.info('Start job - %s' % stamp)
    pool = Pool(processes=4)

    def things():
        for item in parse_weixin(filtered):
            yield item
        for item in parse_zhuanlan(filtered):
            yield item
        for item in parse_daily(filtered):
            yield item

    use_cache = True

    if filtered is not True or now.hour > 22 or now.hour < 5:
        use_cache = False

    rv = pool.map_async(Burglar(public, use_cache), things())
    rv.wait()
    logger.info('End - cache: %s' % use_cache)


if __name__ == '__main__':
    main('--init' not in sys.argv)
