# encoding: utf-8
import calendar
import datetime
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """
    Get the environment variable or return exception.
    """
    try:
      return os.environ[var_name]
    except KeyError:
      error_msg = "Set the %s environment variable" % var_name
      raise ImproperlyConfigured(error_msg)


def last_day_of_month(year, month):
    """
    Returns last day of the month for a year and month.
    """
    return calendar.monthrange(year, month)[1]


def num_months_between(start, end):
    """
    Returns number  of months between two dates.

    Ignores day of month.
    """
    m1 = start.year * 12 + (start.month - 1)
    m2 = end.year * 12 + (end.month - 1)
    return m2 - m1


def months_between(start, end):
    """
    Returns a list of datetimes for the first day of each month between two
    dates, inclusive of the start and end dates.
    """
    start_month = start.month
    end_months = (end.year - start.year) * 12 + end.month + 1
    dates = [datetime.datetime(year=yr, month=mn, day=1) for (yr, mn) in (
              ((m - 1) / 12 + start.year, (m - 1) % 12 + 1) for m in range(
                start_month, end_months))]
    return dates


def previous_month(year, month):
    """
    Returns a tuple of the month prior to the year and month provided.
    """
    month = month - 1
    if month == 0:
        month = 12
        year = year - 1
    else:
        year = year
    return year, month


def next_month(year, month):
    """
    Returns a tuple of the month following the year and month provided.
    """
    month = month + 1
    if month == 13:
        month = 1
        year = year + 1
    else:
        year = year
    return year, month


def remove_query_string(url):
    """
    Returns url without any query string parameters.
    """
    return url.split('?')[0]


def to_unix_timestamp(dt, epoch=datetime.datetime(1970, 1, 1)):
    """
    Return number of seconds since epoch for the given datetime.
    """
    return int((dt - epoch).total_seconds())


def from_unix_timestamp(ts):
    """
    Return datetime object for the given timestamp.
    """
    return datetime.datetime.fromtimestamp(int(ts))
