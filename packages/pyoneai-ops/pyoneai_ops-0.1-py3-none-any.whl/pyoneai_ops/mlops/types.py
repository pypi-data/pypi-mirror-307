from typing import Literal

SupportedEntities = Literal["virtualmachine", "host"]

SupportedProfiles = Literal[
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
]
