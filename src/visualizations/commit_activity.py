import matplotlib
matplotlib.use('Agg')

import requests
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime


def show_commit_activity(owner, repo, headers):

    all_commits = []
    page = 1

    while True:
        print(f"Fetching page {page}...")

        url = f"https://api.github.com/repos/{owner}/{repo}/commits?page={page}&per_page=100"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Error:", response.json())
            return

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

    if not dates:
        print("No commit data found.")
        return

    date_counts = Counter(dates)

    sorted_dates = sorted(date_counts.keys())
    commit_counts = [date_counts[d] for d in sorted_dates]

    print("Total commits:", len(all_commits))

    plt.figure()
    plt.plot(sorted_dates, commit_counts, marker='o')
    plt.xlabel("Date")
    plt.ylabel("Number of Commits")
    plt.title(f"Commit Activity: {owner}/{repo}")
    plt.xticks(rotation=45)
    plt.tight_layout()

    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(BASE_DIR, "static")

    # ✅ ensure folder exists
    os.makedirs(static_dir, exist_ok=True)

    file_path = os.path.join(static_dir, "commit.png")

    plt.savefig(file_path)
    plt.close()