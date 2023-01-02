import configparser
# import sendvaluesapi

config = configparser.ConfigParser()
config.read('./config.cfg')

url2 = config['influxdb']['url2']

test = 'weather'
urln = f'{url2}'

print(url2)
