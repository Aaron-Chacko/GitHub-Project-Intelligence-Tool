import matplotlib
matplotlib.use('Agg')

import requests
import matplotlib.pyplot as plt


def show_contributors(owner, repo, headers):

    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error:", response.json())
        return

    data = response.json()

    if not data:
        print("No contributor data found.")
        return

    data = data[:5]

    names = []
    commits = []

    for contributor in data:
        names.append(contributor["login"])
        commits.append(contributor["contributions"])

    plt.figure()

    colors = plt.cm.Pastel1.colors

    plt.pie(
        commits,
        labels=names,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors
    )

    plt.title(f"Top Contributors: {owner}/{repo}", fontsize=14)

    plt.tight_layout()
    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(BASE_DIR, "static")

    # ✅ ensure folder exists
    os.makedirs(static_dir, exist_ok=True)

    file_path = os.path.join(BASE_DIR, "..", "static", "contributors.png")

    plt.savefig(file_path)
    plt.close()