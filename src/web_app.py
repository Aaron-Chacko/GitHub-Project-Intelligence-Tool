from flask import Flask, request
from visualizations.commit_activity import show_commit_activity
from visualizations.contributors import show_contributors
from visualizations.language import show_languages
from dotenv import load_dotenv
import os
import requests
import time

app = Flask(__name__, static_folder="static")
from flask import send_from_directory

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('src/static', filename)

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {TOKEN}"
}

# -----------------------------
# 🔢 SCORE FUNCTIONS
# -----------------------------
def calculate_score(followers, repos, stars):
    return (followers * 2) + (repos * 1) + (stars * 3)


def get_github_data(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    return None


def analyze_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url, headers=headers)

    total_stars = 0

    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            total_stars += repo["stargazers_count"]

    return total_stars


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        owner = request.form["owner"]
        repo = request.form["repo"]

        commit_img = show_commit_activity(owner, repo, headers)
        contributors_img = show_contributors(owner, repo, headers)
        languages_img = show_languages(owner, repo, headers)

        time.sleep(1)

        # -----------------------------
        # 🔥 SCORE CALCULATION
        # -----------------------------
        user_data = get_github_data(owner)

        followers = user_data["followers"] if user_data else 0
        public_repos = user_data["public_repos"] if user_data else 0
        total_stars = analyze_repos(owner)

        score = calculate_score(followers, public_repos, total_stars)

        return f'''
<style>
    body {{
        font-family: 'Segoe UI', Arial;
        background: #f4f6f8;
        text-align: center;
        padding: 20px;
    }}

    h2 {{
        margin-bottom: 20px;
    }}

    .grid {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
    }}

    .card {{
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}

    img {{
        width: 400px;
        border-radius: 8px;
    }}

    .score-card {{
        margin-top: 40px;
        padding: 20px;
        border-radius: 12px;
        background: #111827;
        color: white;
        display: inline-block;
    }}

    .score-card h1 {{
        font-size: 48px;
        color: #22c55e;
    }}
</style>

<h2>📊 Results for {owner}/{repo}</h2>

<div class="grid">
    <div class="card">
        <h4>Commit Activity</h4>
        <img src="data:image/png;base64,{commit_img}">
    </div>

    <div class="card">
        <h4>Top Contributors</h4>
        <img src="data:image/png;base64,{contributors_img}">
    </div>

    <div class="card">
        <h4>Language Distribution</h4>
        <img src="data:image/png;base64,{languages_img}">
    </div>
</div>

<div class="score-card">
    <h2>🔢 GitHub Account Score</h2>
    <h1>{round(score, 2)}</h1>
    <p>Followers: {followers}</p>
    <p>Repositories: {public_repos}</p>
    <p>Total Stars: {total_stars}</p>
</div>
'''

    return '''
<style>
    body {
        font-family: 'Segoe UI', Arial;
        background: linear-gradient(to right, #667eea, #764ba2);
        margin: 0;
        padding: 0;
    }

    .container {
        background: white;
        padding: 40px;
        margin: 100px auto;
        width: 450px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        text-align: center;
    }

    h2 {
        margin-bottom: 20px;
    }

    input {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border-radius: 6px;
        border: 1px solid #ccc;
    }

    button {
        width: 100%;
        padding: 12px;
        background: #667eea;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-weight: bold;
    }

    button:hover {
        background: #5a67d8;
    }

    #loading {
        margin-top: 15px;
        color: #333;
    }
</style>

<div class="container">
    <h2>GitHub Project Intelligence Tool 🚀</h2>

    <form method="post" onsubmit="showLoading()">
        <input name="owner" placeholder="Enter Owner (e.g. microsoft)">
        <input name="repo" placeholder="Enter Repository (e.g. vscode)">
        <button type="submit">Analyze</button>
    </form>

    <p id="loading" style="display:none;">
        Analyzing... please wait ⏳
        Larger repositories take longer times.
    </p>
</div>

<script>
    function showLoading() {
        document.getElementById("loading").style.display = "block";
    }
</script>
'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)