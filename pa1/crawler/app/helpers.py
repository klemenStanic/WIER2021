from datetime import datetime, timezone

def getTimestamp():
    return datetime.now(timezone.utc)