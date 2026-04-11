# GitHub-Project-Intelligence-Tool
A tool that analyzes GitHub repositories and generates visual insights on project activity, contributors, frequency and code structure.

## Live Demo
🔗 https://github-project-intelligence-tool.onrender.com 
*(Note: May take ~20 seconds to load on first visit due to cold start)*

## Scoring System

This tool computes a **developer score** based on key GitHub metrics to evaluate profile strength and activity.

### Scoring Approach
Instead of raw values, the system uses **logarithmic scaling** to normalize large differences in GitHub metrics.

This prevents high-star accounts from dominating the score and ensures fair comparison across developers.

Final score is scaled to a range of **0–100**.


## Features

- Commit Activity Visualization (time-based trends)
- Contributor Distribution Analysis (top contributors)
- Language Breakdown with interactive hover insights
- Developer Scoring System (based on followers, repos, stars)

## Tech Stack

- Python
- Matplotlib
- Pandas
- GitHub REST API
- mplcursors

## How It Works

1. User inputs a GitHub repository (owner + repo name)
2. The system fetches data using the GitHub REST API
3. Data is processed and visualized using Matplotlib
4. A normalized developer score is computed using logarithmic scaling
5. Results are displayed via a Flask-based web interface

## Future Improvements

- Add percentile-based ranking system
- Include pull request and issue analytics
- Enable multi-repository comparison
- UI upgrade