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
                font-family: Arial;
                background: #f4f6f8;
                text-align: center;
            }}

            img {{
                width: 500px;
                margin: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }}
        </style>

        <h2>Results for {owner}/{repo}</h2>

        <img src="/static/commit.png"><br>
        <img src="/static/contributors.png"><br>
        <img src="/static/languages.png">
        '''

    return '''
    <style>
        body {
            font-family: Arial;
            background: #f4f6f8;
            text-align: center;
            padding-top: 50px;
        }

        .container {
            background: white;
            padding: 30px;
            margin: auto;
            width: 300px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        input {
            width: 90%;
            padding: 8px;
            margin: 10px 0;
        }

        button {
            padding: 10px 20px;
            background: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }

        button:hover {
            background: #45a049;
        }
    </style>

    <div class="container">
        <h2>GitHub Project Intelligence Tool</h2>

        <form method="post" onsubmit="showLoading()">
            <input name="owner" placeholder="Owner"><br>
            <input name="repo" placeholder="Repository"><br>
            <button type="submit">Analyze</button>
        </form>

        <p id="loading" style="display:none; color:blue;">
            Analyzing repository... ⏳
        </p>
    </div>

    <script>
        function showLoading() {
            document.getElementById("loading").style.display = "block";
        }
    </script>
    '''

if __name__ == "__main__":
    app.run(debug=True)