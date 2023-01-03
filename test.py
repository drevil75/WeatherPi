import datetime, time

def getOSMTimestamp():
   now = datetime.datetime.now(datetime.timezone.utc)
   ts = time.mktime(now.timetuple())
   # ts = int(datetime.datetime.timestamp(now))
   # ts = str(now).replace(' ','T').split('.')[0] + '.000Z'
   #time.mktime(ts.timetuple())
   return ts

# 1630424257000000000

print(getOSMTimestamp())