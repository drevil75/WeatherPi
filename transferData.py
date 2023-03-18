import glob, os, json
from apis.send2influxapi import *
from apis.send2opensensemap import *
from apis.send2openhab import *
from apis.send2buffer import writeBuffer

config = configparser.ConfigParser()
config.read('./config.cfg')
cachedir = config['default']['cachedir']


def getFileContent(file):
    txt = ''
    f = open(file, mode='r', encoding='utf-8')
    txt = f.read()
    f.close
    return txt

def transferOSMdata():
    # read/transfer/delete all OSM Files
    filelist = glob.glob(f'{cachedir}*osm*')
    osmObj = []
    for file in filelist:
        tmpObj = json.loads(getFileContent(file=file))

        for kvp in tmpObj:
            osmObj.append(kvp)

    rc = ''
    rc = postOSMvalues(osmObj)
    if rc == 'ok':
        for file in filelist:
            if os.path.isfile(file):
                os.remove(file)

def transferINFLUXdata():
    # read/transfer/delete all InfluxDB Files
    filelist = glob.glob(f'{cachedir}*influx*')
    data = ''
    for file in filelist:
        data += getFileContent(file=file) + '\n'

    rc = ''
    rc = write2influxapi(data)
    if rc == 'ok':
        for file in filelist:
            if os.path.isfile(file):
                os.remove(file)


if __name__ == "__main__":
    while True:
        transferOSMdata()    
        transferINFLUXdata()
        time.sleep(600)