"""Module with synthetic data generators"""

__all__ = [
    "random_workload",
    "high_loads_on_weekdays",
    "high_loads_on_weekends",
    "high_loads_on_working_hours_on_weekdays",
    "high_loads_on_specific_working_hours_on_weekdays",
    "high_usage_during_off_hours",
    "intensive_usage",
    "low_usage",
    "random_usage_with_periodic_spikes",
    "seasonal_workload_variation",
    "continuous_growth",
    "daily_seasonal_exponential",
    "PROFILES",
]
import random
from datetime import datetime, timedelta, timezone
from typing import Callable

import numpy as np
import pandas as pd
from pyoneai.core.metric import Metric

from pyoneai_ops.mlops.generators.utils.date_utils import (
    days_in_year,
    is_daily_resolution,
    is_weekday,
    is_weekend,
    is_working_hour,
)

MIN_CPU_USAGE: float = 0.0
MAX_CPU_USAGE: float = 100.0


def datetime_generator(start_time: str | datetime, delta: str | timedelta):
    if isinstance(start_time, str):
        start_time = datetime.fromisoformat(start_time)
    if isinstance(delta, str):
        delta = pd.Timedelta(delta)

    current_time = start_time
    while True:
        yield current_time
        current_time += delta


def collect_metric_data(
    generator: Callable,
    num_observations: int,
    name: str = "cpu_usage",
):
    datetimes, usages = zip(
        *[next(generator) for _ in range(num_observations)]
    )
    return Metric(time_index=datetimes, data={name: usages})


def random_workload(
    start_time=datetime.now(tz=timezone.utc),
    time_resolution="1h",
    random_seed=42,
):
    random.seed(random_seed)

    datetimes = datetime_generator(start_time, time_resolution)

    while True:
        cpu_usage = random.uniform(MIN_CPU_USAGE, MAX_CPU_USAGE)
        yield next(datetimes), cpu_usage


def high_loads_on_weekdays(
    start_time=datetime.now(tz=timezone.utc),
    time_resolution="1h",
    random_seed=42,
    high_load=(80, 10),
    low_load=(10, 5),
):
    np.random.seed(random_seed)

    datetimes = datetime_generator(start_time, time_resolution)

    while True:
        current_time = next(datetimes)
        if is_weekday(current_time):
            cpu_usage = np.random.normal(
                loc=high_load[0], scale=high_load[1]
            )  # High usage
        else:
            cpu_usage = np.random.normal(
                loc=low_load[0], scale=low_load[1]
            )  # Minimal usage

        cpu_usage = np.clip(cpu_usage, MIN_CPU_USAGE, MAX_CPU_USAGE)
        yield current_time, cpu_usage


def high_loads_on_weekends(
    start_time=datetime.now(tz=timezone.utc),
    time_resolution="1h",
    random_seed=42,
    high_load=(80, 10),
    low_load=(10, 5),
):
    np.random.seed(random_seed)

    datetimes = datetime_generator(start_time, time_resolution)

    while True:
        current_time = next(datetimes)
        if is_weekend(current_time):
            cpu_usage = np.random.normal(
                loc=high_load[0], scale=high_load[1]
            )  # High usage
        else:
            cpu_usage = np.random.normal(
                loc=low_load[0], scale=low_load[1]
            )  # Minimal usage

        cpu_usage = np.clip(cpu_usage, MIN_CPU_USAGE, MAX_CPU_USAGE)
        yield current_time, cpu_usage


def high_loads_on_working_hours_on_weekdays(
    start_time=datetime.now(tz=timezone.utc),
    time_resolution="1h",
    random_seed=42,
    high_load=(80, 10),
    low_load=(10, 5),
):
    np.random.seed(random_seed)

    datetimes = datetime_generator(start_time, time_resolution)

    while True:
        current_time = next(datetimes)
        if is_weekday and is_working_hour(
            current_time, 9, 17
        ):  # Weekdays 9:00-17:00
            cpu_usage = np.random.normal(
                loc=high_load[0], scale=high_load[1]
            )  # High usage
        else:
            cpu_usage = np.random.normal(
                loc=low_load[0], scale=low_load[1]
            )  # Minimal usage

        cpu_usage = np.clip(cpu_usage, MIN_CPU_USAGE, MAX_CPU_USAGE)
        yield current_time, cpu_usage


def high_loads_on_specific_working_hours_on_weekdays(
    start_time=datetime.now(tz=timezone.utc),
    time_resolution="1h",
    random_seed=42,
    high_load=(90, 5),
    medium_load=(60, 10),
    low_load=(10, 5),
):
    np.random.seed(random_seed)

    datetimes = datetime_generator(start_time, time_resolution)

    while True:
        current_time = next(datetimes)
        if is_weekday(current_time):  # Weekdays
            if is_working_hour(current_time, 15, 17):  # 15:00-17:00
                cpu_usage = np.random.normal(
                    loc=high_load[0], scale=high_load[1]
                )  # High usage
            elif is_working_hour(current_time, 9, 15):  # 9:00-15:00
                cpu_usage = np.random.normal(
                    loc=medium_load[0], scale=medium_load[1]
                )  # Medium usage
            else:
                cpu_usage = np.random.normal(
                    loc=low_load[0], scale=low_load[1]
                )  # Minimal usage
        else:
            cpu_usage = np.random.normal(
                loc=low_load[0], scale=low_load[1]
            )  # Minimal usage

        cpu_usage = np.clip(cpu_usage, MIN_CPU_USAGE, MAX_CPU_USAGE)
        yield current_time, cpu_usage


def high_usage_during_off_hours(
    start_time=datetime.now(tz=timezone.utc),
    time_resolution="1h",
    random_seed=42,
    high_load=(80, 10),
    low_load=(10, 5),
):
    np.random.seed(random_seed)

    datetimes = datetime_generator(start_time, time_resolution)

    while True:
        current_time = next(datetimes)
        if is_weekday(current_time):  # Monday to Friday
            if 22 <= current_time.hour or current_time.hour < 6:  # 22:00-6:00
                cpu_usage = np.random.normal(
                    loc=high_load[0], scale=high_load[1]
                )  # High usage
            else:
                cpu_usage = np.random.normal(
                    loc=low_load[0], scale=low_load[1]
                )  # Low usage
        else:
            cpu_usage = np.random.normal(
                loc=low_load[0], scale=low_load[1]
            )  # Low usage

        cpu_usage = np.clip(cpu_usage, MIN_CPU_USAGE, MAX_CPU_USAGE)
        yield current_time, cpu_usage


def intensive_usage(
    start_time=datetime.now(tz=timezone.utc),
    time_resolution="1h",
    random_seed=42,
    high_load=(90, 5),
):
    np.random.seed(random_seed)

    datetimes = datetime_generator(start_time, time_resolution)

    while True:
        current_time = next(datetimes)
        cpu_usage = np.random.normal(
            loc=high_load[0], scale=high_load[1]
        )  # Constant high usage
        cpu_usage = np.clip(cpu_usage, MIN_CPU_USAGE, MAX_CPU_USAGE)
        yield current_time, cpu_usage


def low_usage(
    start_time=datetime.now(tz=timezone.utc),
    time_resolution="1h",
    random_seed=42,
    low_load=(20, 5),
):
    np.random.seed(random_seed)

    datetimes = datetime_generator(start_time, time_resolution)

    while True:
        current_time = next(datetimes)
        cpu_usage = np.random.normal(
            loc=low_load[0], scale=low_load[1]
        )  # Constant low usage
        cpu_usage = np.clip(cpu_usage, MIN_CPU_USAGE, MAX_CPU_USAGE)
        yield current_time, cpu_usage


def random_usage_with_periodic_spikes(
    start_time=datetime.now(tz=timezone.utc),
    time_resolution="1h",
    random_seed=42,
    spike_chance=0.1,
    high_load=(90, 10),
    regular_load=(30, 10),
):
    np.random.seed(random_seed)
    random.seed(random_seed)

    datetimes = datetime_generator(start_time, time_resolution)

    while True:
        current_time = next(datetimes)
        if random.random() < spike_chance:  # Chance of a spike
            cpu_usage = np.random.normal(
                loc=high_load[0], scale=high_load[1]
            )  # High spike
        else:
            cpu_usage = np.random.normal(
                loc=regular_load[0], scale=regular_load[1]
            )  # Regular usage

        cpu_usage = np.clip(cpu_usage, MIN_CPU_USAGE, MAX_CPU_USAGE)
        yield current_time, cpu_usage


def seasonal_workload_variation(
    start_time=datetime.now(tz=timezone.utc),
    time_resolution="1h",
    random_seed=42,
    seasonality_freq=20,
    high_load=(80, 10),
    low_load=(50, 10),
):
    np.random.seed(random_seed)

    datetimes = datetime_generator(start_time, time_resolution)

    sample_counter = 0
    while True:
        current_time = next(datetimes)
        if (
            sample_counter % seasonality_freq == 0
        ):  # Determine peak seasonality
            cpu_usage = np.random.normal(loc=high_load[0], scale=high_load[1])
        else:
            cpu_usage = np.random.normal(loc=low_load[0], scale=low_load[1])

        cpu_usage = np.clip(cpu_usage, MIN_CPU_USAGE, MAX_CPU_USAGE)
        yield current_time, cpu_usage

        sample_counter += 1


def continuous_growth(
    start_time=datetime.now(tz=timezone.utc), time_resolution="1h"
):
    datetimes = datetime_generator(start_time, time_resolution)

    if isinstance(time_resolution, str):
        time_resolution = pd.Timedelta(time_resolution)

    if is_daily_resolution(time_resolution):  # If the resolution is in days
        while True:
            current_time = next(datetimes)
            start_of_year = datetime(
                current_time.year, 1, 1, tzinfo=timezone.utc
            )
            total_seconds_in_year = days_in_year(start_of_year) * 24 * 60 * 60

            seconds_elapsed = (current_time - start_of_year).total_seconds()
            if seconds_elapsed < 0:
                cpu_usage = 0  # Before the start of the year
            else:
                fraction_of_year = seconds_elapsed / total_seconds_in_year
                cpu_usage = (
                    fraction_of_year * 100
                )  # Linear increase from 0% to 100%
                cpu_usage += np.random.normal(loc=0, scale=5)  # Adding noise

            cpu_usage = np.clip(cpu_usage, MIN_CPU_USAGE, MAX_CPU_USAGE)
            yield current_time, cpu_usage

    else:  # Time resolution is in hours or smaller units
        while True:
            current_time = next(datetimes)
            start_of_day = current_time.replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            end_of_day = start_of_day + timedelta(days=1)
            total_seconds_in_day = (end_of_day - start_of_day).total_seconds()
            elapsed_seconds = (current_time - start_of_day).total_seconds()

            day_progress = elapsed_seconds / total_seconds_in_day
            cpu_usage = day_progress * 100.0  # Linear growth from 0% to 100%
            cpu_usage += np.random.normal(loc=0, scale=5)  # Adding noise

            cpu_usage = np.clip(cpu_usage, MIN_CPU_USAGE, MAX_CPU_USAGE)
            yield current_time, cpu_usage


def daily_seasonal_exponential(
    start_time=datetime.now(tz=timezone.utc),
    time_resolution="1h",
    random_seed=42,
    low_load=(10, 5),
):
    np.random.seed(random_seed)

    datetimes = datetime_generator(start_time, time_resolution)

    while True:
        current_time = next(datetimes)
        hour = current_time.hour
        if is_working_hour(current_time, 6, 22):  # 6:00-22:00
            cpu_usage = min(
                MAX_CPU_USAGE, np.exp(hour / 4)
            )  # Exponential growth (divided by 4 to ensure it doesn't grow too fast)
        else:
            cpu_usage = np.random.normal(
                loc=low_load[0], scale=low_load[1]
            )  # Drop at night

        cpu_usage = np.clip(cpu_usage, MIN_CPU_USAGE, MAX_CPU_USAGE)
        yield current_time, cpu_usage


PROFILES = {
    "random_workload": random_workload,
    "high_loads_on_weekdays": high_loads_on_weekdays,
    "high_loads_on_weekends": high_loads_on_weekends,
    "high_loads_on_working_hours_on_weekdays": high_loads_on_working_hours_on_weekdays,
    "high_loads_on_specific_working_hours_on_weekdays": high_loads_on_specific_working_hours_on_weekdays,
    "high_usage_during_off_hours": high_usage_during_off_hours,
    "intensive_usage": intensive_usage,
    "low_usage": low_usage,
    "random_usage_with_periodic_spikes": random_usage_with_periodic_spikes,
    "seasonal_workload_variation": seasonal_workload_variation,
    "continuous_growth": continuous_growth,
    "daily_seasonal_exponential": daily_seasonal_exponential,
}
