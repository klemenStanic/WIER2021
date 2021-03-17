import datetime

def getTimestamp():
    return datetime.datetime.now(datetime.timezone.utc).timestamp()