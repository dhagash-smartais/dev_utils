import os
import json
import argparse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import ipdb

# Argument parsing
parser = argparse.ArgumentParser(
    description="Extract and plot walk durations for each user in the last month."
)
parser.add_argument("root_dir", type=str, help="Root directory containing user folders")
args = parser.parse_args()

root_dir = args.root_dir

# Time window: from 16.06.2025 till today
now = datetime.now()
start_date = datetime.strptime("2025-06-16", "%Y-%m-%d")

# Data structure: list of dicts
all_users_data = []

for user in os.listdir(root_dir):
    print(f"User is {user}")
    user_path = os.path.join(root_dir, user)
    if not os.path.isdir(user_path):
        continue
    walks = {"date": [], "duration": []}
    for walk_folder in os.listdir(user_path):
        if not walk_folder.startswith("walk"):
            continue
        walk_path = os.path.join(user_path, walk_folder)
        if not os.path.isdir(walk_path):
            continue
        metadata_path = os.path.join(walk_path, "metadata.json")
        if not os.path.isfile(metadata_path):
            continue
        try:
            with open(metadata_path, "r") as f:
                meta = json.load(f)
            start_time_str = meta.get("startTime")
            duration = meta.get("duration")
            if not start_time_str or duration is None:
                continue
            # Parse start time
            start_time = datetime.strptime(
                start_time_str.split(" +")[0], "%Y-%m-%d %H:%M:%S"
            )
            if start_time < start_date or start_time > now:
                continue
            walks["date"].append(start_time.date())
            walks["duration"].append(round(duration / 60, 2))
        except Exception as e:
            print(f"Error reading {metadata_path}: {e}")
            continue
    if walks["date"]:
        all_users_data.append({"user": user, "walks": walks})
# Plotting
plt.figure(figsize=(12, 6))
for user_data in all_users_data:
    user = user_data["user"]
    dates = user_data["walks"]["date"]
    durations = user_data["walks"]["duration"]
    # Sort by date
    df = pd.DataFrame({"date": dates, "duration": durations})
    df["date"] = pd.to_datetime(df["date"])  # Ensure date is datetime64
    df = df.sort_values(by=["date"])
    df_numpy = (
        df.groupby("date", as_index=False).sum().to_numpy()
    )  # Sum durations for each date
    print(user)
    plt.plot(df_numpy[:, 0], df_numpy[:, 1], marker="o", label=user)


plt.xlabel("Date")
plt.ylabel("Duration (mins)")
plt.title("Walk Duration per User (Last 1 Month)")
plt.legend(title="User")
plt.tight_layout()
plt.show()
