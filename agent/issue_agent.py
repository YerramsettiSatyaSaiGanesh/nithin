import json
import os
import requests

# Load GitHub event data
event_path = os.environ["GITHUB_EVENT_PATH"]
with open(event_path, "r") as f:
    event = json.load(f)

issue = event["issue"]
title = issue["title"].lower()
body = (issue["body"] or "").lower()

repo = event["repository"]["full_name"]
issue_number = issue["number"]

labels = []
assignee = "YOUR_GITHUB_USERNAME"


# ----------- LOGIC TABLE -----------

if "ai" in title or "ai" in body:
    labels.append("AI Service")
    assignee = issue["user"]["login"]

elif "dse" in title or "data" in body:
    labels.append("DSE")
    assignee = issue["user"]["login"]

elif "consult" in title or "help" in body:
    labels.append("Consultation")
    assignee = issue["user"]["login"]

# ----------- APPLY TO GITHUB -----------





headers = {
    "Authorization": f"token {os.environ['GITHUB_TOKEN']}",
    "Accept": "application/vnd.github+json"
}

print("Repo:", repo)
print("Issue #:", issue_number)
print("Labels to add:", labels)
print("Assignee:", assignee)

if labels:
    r = requests.post(
        f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels",
        headers=headers,
        json={"labels": labels}
    )
    print("Label API status:", r.status_code)
    print("Label API response:", r.text)
    r.raise_for_status()

if assignee:
    r = requests.post(
        f"https://api.github.com/repos/{repo}/issues/{issue_number}/assignees",
        headers=headers,
        json={"assignees": [assignee]}
    )
    print("Assign API status:", r.status_code)
    print("Assign API response:", r.text)
    r.raise_for_status()
