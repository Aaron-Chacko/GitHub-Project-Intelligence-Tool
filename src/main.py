import pandas as pd
import requests


def extract_username(url):
    return url.rstrip("/").split("/")[-1]


def get_github_data(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "public_repos": data["public_repos"],
            "followers": data["followers"],
            "following": data["following"]
        }
    else:
        return {
            "public_repos": None,
            "followers": None,
            "following": None
        }


def analyze_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code != 200:
        return {"total_stars": 0, "top_language": None}

    repos = response.json()

    total_stars = 0
    languages = {}

    for repo in repos:
        total_stars += repo["stargazers_count"]

        lang = repo["language"]
        if lang:
            languages[lang] = languages.get(lang, 0) + 1

    top_language = max(languages, key=languages.get) if languages else None

    return {
        "total_stars": total_stars,
        "top_language": top_language
    }
    
def calculate_score(row):
    score = 0

    score += row["followers"] * 2
    score += row["public_repos"] * 1
    score += row["total_stars"] * 3

    return score


def main():
    
    df = pd.read_csv("data/input.csv")

    #username
    df["username"] = df["github_url"].apply(extract_username)

    #github data
    df["github_data"] = df["username"].apply(get_github_data)

    df["public_repos"] = df["github_data"].apply(lambda x: x["public_repos"])
    df["followers"] = df["github_data"].apply(lambda x: x["followers"])
    df["following"] = df["github_data"].apply(lambda x: x["following"])

    df.drop(columns=["github_data"], inplace=True)

    #repo analyse
    df["repo_data"] = df["username"].apply(analyze_repos)

    df["total_stars"] = df["repo_data"].apply(lambda x: x["total_stars"])
    df["top_language"] = df["repo_data"].apply(lambda x: x["top_language"])

    df.drop(columns=["repo_data"], inplace=True)
    
    df["score"] = df.apply(calculate_score, axis=1)

    #score highest
    df = df.sort_values(by="score", ascending=False)

    print("\nFinal Data:\n")
    print(df)

    df.to_csv("output/results.csv", index=False)
    print("\nSaved to output/results.csv ✅")


if __name__ == "__main__":
    main()