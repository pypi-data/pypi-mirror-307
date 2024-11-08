from datetime import datetime

import pandas as pd


def is_weekend(current_time) -> bool:
    return current_time.weekday() >= 5  # Saturday and Sunday


def is_weekday(current_time) -> bool:
    return current_time.weekday() < 5  # Monday to Friday


def is_working_hour(current_time, job_start_hour=9, job_end_hour=17) -> bool:
    return job_start_hour <= current_time.hour < job_end_hour


def days_in_year(date: datetime) -> int:
    # Determine if it's a leap year
    year = date.year
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return 366
    else:
        return 365


def is_daily_resolution(time_resolution) -> bool:
    return time_resolution >= pd.Timedelta(days=1)
