import configparser
import json
from apis.datetimes import getTimestampStr


config = configparser.ConfigParser()
config.read('./config.cfg')
cachedir = int(config['default']['cachedir'])



def writeBuffer(apiname, data):
    try:
        ts = getTimestampStr()

        f = open(f'{cachedir}{ts}-{apiname}.csv', mode='a', encoding='utf-8')
        f.write(data)
        f.close
    except:
        pass

