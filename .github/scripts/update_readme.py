import os
import requests
import re
import html

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
USERNAME = "m-farhan-hamim"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def fetch_recent_activity():
    url = f"https://api.github.com/users/{USERNAME}/events?per_page=100"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return []
    
    events = response.json()
    repos = []
    seen = set()
    
    for event in events:
        if event["type"] == "PushEvent":
            repo_name = event["repo"]["name"].replace(f"{USERNAME}/", "")
            if repo_name not in seen:
                seen.add(repo_name)
                date = event["created_at"][:10]
                repos.append((repo_name, date))
                if len(repos) == 3:
                    break
    return repos

def fetch_top_starred():
    url = f"https://api.github.com/users/{USERNAME}/repos?sort=stars&per_page=3"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return []
        
    repos = response.json()
    data = []
    for repo in repos:
        name = repo["name"]
        stars = repo["stargazers_count"]
        desc = repo.get("description") or "No description provided."
        if len(desc) > 45:
            desc = desc[:42] + "..."
        data.append((name, stars, desc))
    return data

def generate_activity_svg(repos):
    height = 120 + (len(repos) * 40)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" rx="12" fill="url(#bg)" stroke="#1f6feb" stroke-width="1.5" />
  <text x="30" y="40" font-family="Fira Code, monospace" font-size="20" fill="#58A6FF" font-weight="bold">⚡ Dynamic Activity</text>
  <text x="30" y="75" font-family="Fira Code, monospace" font-size="14" fill="#8B949E">Repository</text>
  <text x="450" y="75" font-family="Fira Code, monospace" font-size="14" fill="#8B949E">Activity</text>
  <text x="650" y="75" font-family="Fira Code, monospace" font-size="14" fill="#8B949E">Date</text>
  <line x1="20" y1="85" x2="780" y2="85" stroke="#30363d" stroke-width="1" />
'''
    y = 115
    for repo, date in repos:
        svg += f'''  <text x="30" y="{y}" font-family="Fira Code, monospace" font-size="15" fill="#58A6FF" font-weight="bold">{html.escape(repo)}</text>
  <text x="450" y="{y}" font-family="Fira Code, monospace" font-size="15" fill="#3FB950">⚡ Pushed commits</text>
  <text x="650" y="{y}" font-family="Fira Code, monospace" font-size="15" fill="#8B949E">{date}</text>
'''
        y += 40
    svg += '</svg>'
    return svg

def generate_starred_svg(repos):
    height = 120 + (len(repos) * 40)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" rx="12" fill="url(#bg)" stroke="#1f6feb" stroke-width="1.5" />
  <text x="30" y="40" font-family="Fira Code, monospace" font-size="20" fill="#58A6FF" font-weight="bold">⭐ Top Starred Repositories</text>
  <text x="30" y="75" font-family="Fira Code, monospace" font-size="14" fill="#8B949E">Repository</text>
  <text x="300" y="75" font-family="Fira Code, monospace" font-size="14" fill="#8B949E">Stars</text>
  <text x="420" y="75" font-family="Fira Code, monospace" font-size="14" fill="#8B949E">Description</text>
  <line x1="20" y1="85" x2="780" y2="85" stroke="#30363d" stroke-width="1" />
'''
    y = 115
    for name, stars, desc in repos:
        svg += f'''  <text x="30" y="{y}" font-family="Fira Code, monospace" font-size="15" fill="#58A6FF" font-weight="bold">{html.escape(name)}</text>
  <text x="300" y="{y}" font-family="Fira Code, monospace" font-size="15" fill="#D29922">⭐ {stars}</text>
  <text x="420" y="{y}" font-family="Fira Code, monospace" font-size="14" fill="#8B949E">{html.escape(desc)}</text>
'''
        y += 40
    svg += '</svg>'
    return svg

def update_readme():
    os.makedirs("assets", exist_ok=True)
    
    activity_data = fetch_recent_activity()
    activity_svg = generate_activity_svg(activity_data)
    with open("assets/activity.svg", "w", encoding="utf-8") as f:
        f.write(activity_svg)
        
    starred_data = fetch_top_starred()
    starred_svg = generate_starred_svg(starred_data)
    with open("assets/starred.svg", "w", encoding="utf-8") as f:
        f.write(starred_svg)
        
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
        
    content = re.sub(
        r"<!-- RECENT_ACTIVITY:start -->.*?<!-- RECENT_ACTIVITY:end -->",
        f"<!-- RECENT_ACTIVITY:start -->\n\n<!-- RECENT_ACTIVITY:end -->",
        content,
        flags=re.DOTALL
    )
    
    content = re.sub(
        r"<!-- TOP_STARRED:start -->.*?<!-- TOP_STARRED:end -->",
        f"<!-- TOP_STARRED:start -->\n\n<!-- TOP_STARRED:end -->",
        content,
        flags=re.DOTALL
    )
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()
