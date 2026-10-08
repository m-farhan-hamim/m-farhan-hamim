import os
import requests
import re

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
USERNAME = "m-farhan-hamim"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def fetch_recent_activity():
    url = f"https://api.github.com/users/{USERNAME}/events?per_page=100"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return "| Error fetching activity |"
    
    events = response.json()
    repos = []
    seen = set()
    
    for event in events:
        if event["type"] == "PushEvent":
            repo_name = event["repo"]["name"]
            if repo_name not in seen:
                seen.add(repo_name)
                # Format the date
                date = event["created_at"][:10]
                repos.append((repo_name, date))
                if len(repos) == 3:
                    break
                    
    if not repos:
        return "| No recent activity |"
        
    table = "| 🚀 Repository | 🛠️ Activity | 📅 Date |\n| :--- | :--- | :--- |\n"
    for repo, date in repos:
        table += f"| **[{repo}](https://github.com/{repo})** | ⚡ Pushed commits | {date} |\n"
    return table

def fetch_top_starred():
    url = f"https://api.github.com/users/{USERNAME}/repos?sort=stars&per_page=3"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return "| Error fetching starred repos |"
        
    repos = response.json()
    if not repos:
        return "| No starred repositories |"
        
    table = "| Repository | Stars | Description |\n| :--- | :--- | :--- |\n"
    for repo in repos:
        name = repo["name"]
        stars = repo["stargazers_count"]
        desc = repo.get("description", "No description provided.")
        table += f"| **[{name}]({repo['html_url']})** | ⭐ {stars} | {desc} |\n"
    return table

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Inject Recent Activity
    recent_content = fetch_recent_activity()
    content = re.sub(
        r"<!-- RECENT_ACTIVITY:start -->.*?<!-- RECENT_ACTIVITY:end -->",
        f"<!-- RECENT_ACTIVITY:start -->\n{recent_content}\n<!-- RECENT_ACTIVITY:end -->",
        content,
        flags=re.DOTALL
    )

    # Inject Top Starred
    starred_content = fetch_top_starred()
    content = re.sub(
        r"<!-- TOP_STARRED:start -->.*?<!-- TOP_STARRED:end -->",
        f"<!-- TOP_STARRED:start -->\n{starred_content}\n<!-- TOP_STARRED:end -->",
        content,
        flags=re.DOTALL
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()
