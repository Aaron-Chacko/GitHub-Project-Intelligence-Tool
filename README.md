# GitHub-Project-Intelligence-Tool
A tool that analyzes GitHub repositories and generates visual insights on project activity, contributors, frequency and code structure.

## Scoring System

This tool computes a **developer score** based on key GitHub metrics to evaluate profile strength and activity.

### Formula
```python
score = (followers * 2) + (public_repos * 1) + (total_stars * 3)

### Explanation
The score is calculated by combining three key factors:
- Followers are multiplied by 2 to represent a developer’s reputation.
- Public repositories are multiplied by 1 to show overall activity.
- Total stars are multiplied by 3 to emphasize the quality and impact of the developer’s work.

Higher scores indicate stronger and more influential GitHub profiles.