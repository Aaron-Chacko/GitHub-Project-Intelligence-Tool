from flask import Flask, request
from visualizations.commit_activity import show_commit_activity
from visualizations.contributors import show_contributors
from visualizations.language import show_languages
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {TOKEN}"
}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        owner = request.form["owner"]
        repo = request.form["repo"]

        show_commit_activity(owner, repo, headers)
        show_contributors(owner, repo, headers)
        show_languages(owner, repo, headers)

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
</style>

<h2>📊 Results for {owner}/{repo}</h2>

<div class="grid">
    <div class="card">
        <h4>Commit Activity</h4>
        <img src="/static/commit.png">
    </div>

    <div class="card">
        <h4>Top Contributors</h4>
        <img src="/static/contributors.png">
    </div>

    <div class="card">
        <h4>Language Distribution</h4>
        <img src="/static/languages.png">
    </div>
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