from datetime import datetime

from metasdk.exceptions import BadParametersError


def check_postgres_datetime_with_tz(value):
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        raise BadParametersError("Datetime should match format '%Y-%m-%dT%H:%M:%S.%f%z': %s" % (value))

def check_postgres_datetime_without_tz(value):
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise BadParametersError("Datetime should match format '%Y-%m-%dT%H:%M:%S': %s" % (value))


def check_postgres_date(value):
    value = value.split("T")[0]
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise BadParametersError("Date should match format '%Y-%m-%d': %s" % (value))