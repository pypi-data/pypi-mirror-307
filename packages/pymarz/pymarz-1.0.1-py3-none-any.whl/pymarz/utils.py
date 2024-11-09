from datetime import datetime


def datetime_to_str(data: datetime = None):
    return data.strftime("%Y-%m-%dT%H:%M:%S") if data is not None else ""
