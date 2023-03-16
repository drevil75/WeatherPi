import datetime, time



def getTimeDiff(dtStr):
    sy, smo, sd, sh, smi, ss, apiname, sensor = dtStr.split('-')  
    then = datetime.datetime(int(sy), int(smo), int(sd), int(sh), int(smi), int(ss)) 
    now  = datetime.datetime.now()
    duration = now - then                         
    duration_in_s = duration.total_seconds()
    return duration_in_s      

def getTimestampStr():
   now = datetime.datetime.now(datetime.timezone.utc)
   ts = int(datetime.datetime.timestamp(now))
   ts = str(now).replace(' ','-').split('.')[0].replace(':','-').replace('.','-')
   return ts

