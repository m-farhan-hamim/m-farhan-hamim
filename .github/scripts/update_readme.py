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
    # FIX: Fetch ALL public repos (up to 100) to ensure we don't miss any
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return []
        
    repos = response.json()
    # Sort in Python to guarantee accurate star ranking
    repos.sort(key=lambda x: x.get("stargazers_count", 0), reverse=True)
    
    data = []
    for repo in repos[:3]:  # Get top 3
        name = repo["name"]
        stars = repo["stargazers_count"]
        desc = repo.get("description") or "No description provided."
        if len(desc) > 45:
            desc = desc[:42] + "..."
        data.append((name, stars, desc))
    return data

def generate_activity_svg(repos):
    height = 120 + (len(repos) * 45)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}" viewBox="0 0 800 {height}">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1f6feb" />
      <stop offset="100%" stop-color="#8b5cf6" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="100%" height="100%" rx="16" fill="url(#bgGrad)" stroke="url(#borderGrad)" stroke-width="2" />
  <text x="30" y="40" font-family="system-ui, -apple-system, sans-serif" font-size="20" fill="#58A6FF" font-weight="bold">⚡ Dynamic Activity</text>
  <circle cx="740" cy="35" r="6" fill="#3FB950">
    <animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite" />
  </circle>
  <text x="30" y="75" font-family="system-ui, -apple-system, sans-serif" font-size="14" fill="#8B949E">Repository</text>
  <text x="450" y="75" font-family="system-ui, -apple-system, sans-serif" font-size="14" fill="#8B949E">Activity</text>
  <text x="650" y="75" font-family="system-ui, -apple-system, sans-serif" font-size="14" fill="#8B949E">Date</text>
  <line x1="20" y1="85" x2="780" y2="85" stroke="#30363d" stroke-width="1" />
'''
    y = 115
    delay = 0.1
    for repo, date in repos:
        svg += f'''  <g opacity="0">
    <animate attributeName="opacity" values="0;1" dur="0.5s" fill="freeze" begin="{delay}s" />
    <animateTransform attributeName="transform" type="translate" values="-30,0;0,0" dur="0.5s" fill="freeze" begin="{delay}s" />
    <text x="30" y="{y}" font-family="system-ui, -apple-system, sans-serif" font-size="15" fill="#58A6FF" font-weight="bold">{html.escape(repo)}</text>
    <text x="450" y="{y}" font-family="system-ui, -apple-system, sans-serif" font-size="15" fill="#3FB950">⚡ Pushed commits</text>
    <text x="650" y="{y}" font-family="system-ui, -apple-system, sans-serif" font-size="15" fill="#8B949E">{date}</text>
  </g>
'''
        y += 45
        delay += 0.1
    svg += '</svg>'
    return svg

def generate_starred_svg(repos):
    height = 120 + (len(repos) * 45)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}" viewBox="0 0 800 {height}">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1f6feb" />
      <stop offset="100%" stop-color="#8b5cf6" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="100%" height="100%" rx="16" fill="url(#bgGrad)" stroke="url(#borderGrad)" stroke-width="2" />
  <text x="30" y="40" font-family="system-ui, -apple-system, sans-serif" font-size="20" fill="#58A6FF" font-weight="bold">⭐ Top Starred Repositories</text>
  <g transform="translate(740, 35)">
    <path d="M0,-8 L2.5,-2.5 L8,-2.5 L3.5,1 L5,6.5 L0,3 L-5,6.5 L-3.5,1 L-8,-2.5 L-2.5,-2.5 Z" fill="#D29922" filter="url(#glow)">
      <animateTransform attributeName="transform" type="rotate" values="0;10;-10;0" dur="4s" repeatCount="indefinite" />
    </path>
  </g>
  <text x="30" y="75" font-family="system-ui, -apple-system, sans-serif" font-size="14" fill="#8B949E">Repository</text>
  <text x="300" y="75" font-family="system-ui, -apple-system, sans-serif" font-size="14" fill="#8B949E">Stars</text>
  <text x="420" y="75" font-family="system-ui, -apple-system, sans-serif" font-size="14" fill="#8B949E">Description</text>
  <line x1="20" y1="85" x2="780" y2="85" stroke="#30363d" stroke-width="1" />
'''
    y = 115
    delay = 0.1
    for name, stars, desc in repos:
        svg += f'''  <g opacity="0">
    <animate attributeName="opacity" values="0;1" dur="0.5s" fill="freeze" begin="{delay}s" />
    <animateTransform attributeName="transform" type="translate" values="30,0;0,0" dur="0.5s" fill="freeze" begin="{delay}s" />
    <text x="30" y="{y}" font-family="system-ui, -apple-system, sans-serif" font-size="15" fill="#58A6FF" font-weight="bold">{html.escape(name)}</text>
    <text x="300" y="{y}" font-family="system-ui, -apple-system, sans-serif" font-size="15" fill="#D29922">⭐ {stars}</text>
    <text x="420" y="{y}" font-family="system-ui, -apple-system, sans-serif" font-size="14" fill="#8B949E">{html.escape(desc)}</text>
  </g>
'''
        y += 45
        delay += 0.1
    svg += '</svg>'
    return svg

def update_readme():
    os.makedirs("assets", exist_ok=True)
    
    activity_data = fetch_recent_activity()
    if activity_data:
        activity_svg = generate_activity_svg(activity_data)
        with open("assets/activity.svg", "w", encoding="utf-8") as f:
            f.write(activity_svg)
        
    starred_data = fetch_top_starred()
    if starred_data:
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
