import os
from datetime import datetime, timedelta
from typing import Callable, Dict, Tuple

import matplotlib.pyplot as plt


def generate_and_save_profiles(
    save_dir: str,
    start_time: str | datetime,
    time_resolution: str | timedelta,
    num_observations: int,
    generator_func: Callable,
    generator_args: Tuple = (),
    generator_kwargs: Dict = None,
):
    generator_kwargs = generator_kwargs or {}
    gen = generator_func(
        start_time=start_time,
        time_resolution=time_resolution,
        *generator_args,
        **generator_kwargs,
    )

    times, usages = zip(*[next(gen) for _ in range(num_observations)])

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(times, usages, label="CPU Usage")
    plt.xlabel("Time")
    plt.ylabel("CPU Usage (%)")
    plt.title(
        f"{generator_func.__name__} (Plot t_r: {time_resolution} | n_o: {num_observations})"
    )
    plt.legend()
    plt.grid(True)

    # Save the plot
    plot_filename = f"plot_{time_resolution}_{num_observations}.png"
    plot_path = os.path.join(save_dir, plot_filename)
    plt.savefig(plot_path)
    plt.close()
