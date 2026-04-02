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

        # Call your functions
        show_commit_activity(owner, repo, headers)
        show_contributors(owner, repo, headers)
        show_languages(owner, repo, headers)

        return f'''
    <h2>Results for {owner}/{repo}</h2>
    <img src="/static/commit.png"><br><br>
    <img src="/static/contributors.png"><br><br>
    <img src="/static/languages.png">
'''

    return '''
    <h2>GitHub Project Intelligence Tool</h2>
    <form method="post" onsubmit="showLoading()">
        Owner: <input name="owner"><br><br>
        Repo: <input name="repo"><br><br>
        <button type="submit">Analyze</button>
    </form>

    <p id="loading" style="display:none; color:blue;">
        Analyzing repository... please wait ⏳
        Larger repositories can take longer times...
    </p>

    <script>
        function showLoading() {
            document.getElementById("loading").style.display = "block";
        }
    </script>
'''

if __name__ == "__main__":
    app.run(debug=True)