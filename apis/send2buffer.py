import configparser
import json
from apis.datetimes import getTimestampStr


config = configparser.ConfigParser()
config.read('./config.cfg')
cachedir = config['default']['cachedir']



def writeBuffer(apiname, data):
    try:
        ts = getTimestampStr()
        ext = 'txt'
        if 'osm' in apiname: 
            ext = 'json'
        
        f = open(f'{cachedir}{ts}-{apiname}.{ext}', mode='a', encoding='utf-8')
        f.write(data)
        f.close
    except:
        pass

