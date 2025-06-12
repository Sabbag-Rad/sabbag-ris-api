from datetime import datetime, date, time


def serialize_dates(obj):
    for key, value in obj.items():
        if isinstance(value, (datetime, date, time)):
            obj[key] = value.isoformat()
    return obj
