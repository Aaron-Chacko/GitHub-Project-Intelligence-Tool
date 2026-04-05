import matplotlib
matplotlib.use('Agg')

import mplcursors
import requests
import matplotlib.pyplot as plt


def show_languages(owner, repo, headers):

    url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error:", response.json())
        return

    data = response.json()

    if not data:
        print("No language data found.")
        return

    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

    top_n = 5
    top_languages = sorted_data[:top_n]
    others = sorted_data[top_n:]

    languages = [lang for lang, _ in top_languages]
    sizes = [size for _, size in top_languages]

    if others:
        other_size = sum(size for _, size in others)
        languages.append("Others")
        sizes.append(other_size)

    total = sum(sizes)
    percentages = [(x / total) * 100 for x in sizes]

    plt.figure()

    bars = plt.bar(languages, percentages)

    plt.xlabel("Languages")
    plt.ylabel("Percentage (%)")
    plt.title(f"Language Distribution: {owner}/{repo}")

    plt.xticks(rotation=30)

    cursor = mplcursors.cursor(bars)

    @cursor.connect("add")
    def on_add(sel):
        index = sel.index
        sel.annotation.set_text(f"{languages[index]}: {percentages[index]:.2f}%")

    plt.tight_layout()
    import os

    ROOT_DIR = os.getcwd()
    static_dir = os.path.join(ROOT_DIR, "static")

    os.makedirs(static_dir, exist_ok=True)

    file_path = os.path.join(static_dir, "languages.png")

    plt.savefig(file_path)
    plt.close()

    print("Saved at:", file_path)
    print("Exists?", os.path.exists(file_path))