# GitHub-Project-Intelligence-Tool
A tool that analyzes GitHub repositories and generates visual insights on project activity, contributors, frequency and code structure.

## Scoring System

This tool computes a **developer score** based on key GitHub metrics to evaluate profile strength and activity.

### 🧮 Formula
```python
score = (followers * 2) + (public_repos * 1) + (total_stars * 3)