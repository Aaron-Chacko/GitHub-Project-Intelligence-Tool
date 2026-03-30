import matplotlib
matplotlib.use('TkAgg')

import requests
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")

OWNER = "psf"
REPO = "requests"

headers = {
    "Authorization": f"token {TOKEN}"
}

all_commits = []
page = 1

while True:
    print(f"Fetching page {page}...")

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/commits?page={page}&per_page=100"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error:", response.json())
        break

    data = response.json()

    if not isinstance(data, list) or len(data) == 0:
        break

    all_commits.extend(data)

    if len(data) < 100:
        break

    page += 1

dates = []
for commit in all_commits:
    date_str = commit["commit"]["author"]["date"]
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    dates.append(date_obj.date())

date_counts = Counter(dates)

sorted_dates = sorted(date_counts.keys())
commit_counts = [date_counts[d] for d in sorted_dates]

print("Total commits:", len(all_commits))

plt.figure()
plt.plot(sorted_dates, commit_counts, marker='o')
plt.xlabel("Date")
plt.ylabel("Number of Commits")
plt.title("Commit Activity Over Time (Full Data)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show(block=True)
input("Press Enter to exit...")