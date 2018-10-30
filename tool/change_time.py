import datetime
import pytz
import time
from django.utils import timezone


def time_stamp_to_str(reserve_time):

    time_str = time.strftime("%Y-%m-%d %H:%M:%S", reserve_time)
    return time_str


if __name__ == "__main__":
    pass