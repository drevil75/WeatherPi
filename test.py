import datetime

def getOSMTimestamp():
   now = datetime.datetime.now(datetime.timezone.utc)
   ts = int(datetime.datetime.timestamp(now))
   ts = str(now).replace(' ','T').split('.')[0] + '.000Z'
   return ts

print(getOSMTimestamp())