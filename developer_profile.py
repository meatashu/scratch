import datetime
import requests
import json
import re

def get_jira_issues(username):
    """Gets a list of Jira issues assigned to the given user in the last 30 days."""
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=30)
    url = "https://your-jira-server/rest/api/2/search?jql=assignee={} AND createdDate > '{}'".format(
        username, start_date.isoformat()
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        issues = data["issues"]
        return issues
    else:
        raise Exception("Failed to get Jira issues")

def get_bitbucket_commits(username):
    """Gets a list of Bitbucket commits made by the given user in the last 30 days."""
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=30)
    url = "https://api.bitbucket.org/2.0/users/{}/commits?q=author:{} AND updatedDate > '{}'".format(
        username, username, start_date.isoformat()
    )
    response = requests.get(url, headers={"Authorization": "Bearer your_bitbucket_token"})
    if response.status_code == 200:
        data = json.loads(response.content)
        commits = data["values"]
        return commits
    else:
        raise Exception("Failed to get Bitbucket commits")

def generate_developer_profile(username):
    """Generates a developer profile for the given user, tracking the last 30 days only, and determining commits made per Jira."""
    issues = get_jira_issues(username)
    commits = get_bitbucket_commits(username)

    profile = {
        "name": username,
        "jira_issues": issues,
        "bitbucket_commits": commits,
        "commits_per_jira": {},
    }

    for issue in issues:
        profile["jira_issues_by_project"].setdefault(issue["project"], []).append(issue)

    for commit in commits:
        commit_message = commit["message"]
        jira_number = re.findall(r"\[JIRA-\d+\]", commit_message)
        if jira_number:
            for jira in jira_number:
                profile["commits_per_jira"].setdefault(jira, []).append(commit)

    return profile

if __name__ == "__main__":
    username = "your_username"
    profile = generate_developer_profile(username)
    print(profile)
