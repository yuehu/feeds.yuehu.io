# coding: utf-8

import os
# set timezone
os.environ['TZ'] = 'Asia/Shanghai'
import json
import datetime
now = datetime.datetime.now()
stamp = now.strftime('%H:%M')

rootdir = os.path.abspath(os.path.dirname(__file__))
public = os.path.join(rootdir, 'public')


def fetch(item):
    from burglar import Burglar
    Burglar(public)(item)


def parse_weixin():
    with open(os.path.join(public, 'weixin.json')) as f:
        data = json.load(f)

    keys = list(filter(lambda o: stamp in o['time'], data))
    for key in keys:
        item = data[key]
        item['type'] = 'weixin'
        item['name'] = key
        fetch(item)


def parse_zhuanlan():
    with open(os.path.join(public, 'zhuanlan.json')) as f:
        data = json.load(f)

    keys = list(filter(lambda o: stamp in o['time'], data))
    for key in keys:
        item = data[key]
        item['type'] = 'zhuanlan'
        item['name'] = key
        fetch(item)


def parse_daily():
    if stamp not in ['8:00', '10:00', '12:00', '16:00', '20:00', '24:00']:
        return
    fetch({'type': 'daily'})


if __name__ == '__main__':
    parse_weixin()
    parse_zhuanlan()
    parse_daily()
