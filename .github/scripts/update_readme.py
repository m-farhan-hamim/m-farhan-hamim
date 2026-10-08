import os
import requests
import html
import collections
from datetime import datetime, timedelta

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
USERNAME = "m-farhan-hamim"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# ═══════════════════════════════════════════════════════════════
#  API FETCHERS
# ═══════════════════════════════════════════════════════════════

def fetch_user_stats():
    try:
        url = f"https://api.github.com/users/{USERNAME}"
        response = requests.get(url, headers=HEADERS)
        return response.json() if response.status_code == 200 else {}
    except: return {}

def fetch_all_repos():
    try:
        url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
        response = requests.get(url, headers=HEADERS)
        return response.json() if response.status_code == 200 else []
    except: return []

def fetch_recent_activity():
    try:
        url = f"https://api.github.com/users/{USERNAME}/events?per_page=100"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200: return []
        events = response.json()
        repos, seen = [], set()
        for event in events:
            if event["type"] == "PushEvent":
                repo_name = event["repo"]["name"].replace(f"{USERNAME}/", "")
                if repo_name not in seen:
                    seen.add(repo_name)
                    repos.append((repo_name, event["created_at"][:10]))
                    if len(repos) == 3: break
        return repos
    except: return []

def fetch_contributions():
    try:
        url = f"https://github-contributions-api.jogruber.de/v4/{USERNAME}"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
    except: return None

def calculate_streaks(contributions_data):
    if not contributions_data: return 0, 0
    dates = [d["date"] for d in contributions_data["contributions"] if d["count"] > 0]
    dates.sort()
    if not dates: return 0, 0
    current, longest, temp, prev = 0, 0, 0, None
    for date_str in dates:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        temp = 1 if prev is None else (temp + 1 if (date - prev).days == 1 else 1)
        prev = date
        longest = max(longest, temp)
    today = datetime.now().date()
    current = temp if prev == today or prev == today - timedelta(days=1) else 0
    return current, longest

# ═══════════════════════════════════════════════════════════════
#  SVG GENERATORS
# ═══════════════════════════════════════════════════════════════

def generate_wave_svg(filename, height, section, is_header=True):
    color1, color2 = ("#0d1117", "#1f6feb") if is_header else ("#1f6feb", "#0d1117")
    wave_path = f"M0,{height-40} Q200,{height-80} 400,{height-40} T800,{height-40} L800,{height} L0,{height} Z" if is_header else f"M0,40 Q200,80 400,40 T800,40 L800,0 L0,0 Z"
    text_y = 90 if is_header else height - 60
    desc_y = 130 if is_header else height - 30
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}" viewBox="0 0 800 {height}">
  <defs>
    <linearGradient id="waveGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{color1}" />
      <stop offset="100%" stop-color="{color2}" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="#0d1117" />
  <path d="{wave_path}" fill="url(#waveGrad)" opacity="0.8" />
  <text x="400" y="{text_y}" font-family="system-ui, -apple-system, sans-serif" font-size="36" fill="#ffffff" font-weight="bold" text-anchor="middle">M. Farhan Hamim</text>
  <text x="400" y="{desc_y}" font-family="system-ui, -apple-system, sans-serif" font-size="16" fill="#8B949E" text-anchor="middle">CEO @ PSBDx | WordPress Plugin Developer</text>
</svg>'''
    with open(f"assets/{filename}", "w", encoding="utf-8") as f: f.write(svg)

def generate_divider_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="4" viewBox="0 0 800 4">
  <defs>
    <linearGradient id="divGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="50%" stop-color="#1f6feb" />
      <stop offset="100%" stop-color="#0d1117" />
    </linearGradient>
  </defs>
  <rect width="100%" height="4" fill="url(#divGrad)" />
</svg>'''
    with open("assets/divider.svg", "w", encoding="utf-8") as f: f.write(svg)

def generate_social_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="60" viewBox="0 0 800 60">
  <rect x="180" y="10" width="120" height="36" rx="18" fill="#0d1117" stroke="#1f6feb" stroke-width="1.5" />
  <text x="240" y="33" font-family="system-ui, sans-serif" font-size="14" fill="#58A6FF" text-anchor="middle">GitHub</text>
  <rect x="320" y="10" width="160" height="36" rx="18" fill="#0d1117" stroke="#1f6feb" stroke-width="1.5" />
  <text x="400" y="33" font-family="system-ui, sans-serif" font-size="14" fill="#58A6FF" text-anchor="middle">WordPress</text>
  <rect x="500" y="10" width="120" height="36" rx="18" fill="#0d1117" stroke="#1f6feb" stroke-width="1.5" />
  <text x="560" y="33" font-family="system-ui, sans-serif" font-size="14" fill="#58A6FF" text-anchor="middle">PSBDx</text>
</svg>'''
    with open("assets/social.svg", "w", encoding="utf-8") as f: f.write(svg)

def generate_bento_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="120" viewBox="0 0 800 120">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" rx="12" fill="url(#bgGrad)" stroke="#30363d" stroke-width="1" />
  <text x="200" y="45" font-family="system-ui, sans-serif" font-size="16" fill="#58A6FF" text-anchor="middle" font-weight="bold">🏢 Company</text>
  <text x="200" y="75" font-family="system-ui, sans-serif" font-size="14" fill="#8B949E" text-anchor="middle">Founder &amp; CEO</text>
  <text x="400" y="45" font-family="system-ui, sans-serif" font-size="16" fill="#58A6FF" text-anchor="middle" font-weight="bold">📦 Plugins</text>
  <text x="400" y="75" font-family="system-ui, sans-serif" font-size="14" fill="#8B949E" text-anchor="middle">Plugin Developer</text>
  <text x="600" y="45" font-family="system-ui, sans-serif" font-size="16" fill="#58A6FF" text-anchor="middle" font-weight="bold">🌐 Community</text>
  <text x="600" y="75" font-family="system-ui, sans-serif" font-size="14" fill="#8B949E" text-anchor="middle">Contributor</text>
</svg>'''
    with open("assets/bento.svg", "w", encoding="utf-8") as f: f.write(svg)

def generate_tech_stack_svg():
    techs = ["PHP", "WordPress", "JavaScript", "TypeScript", "HTML5", "CSS3", "MySQL", "Git", "GitHub", "Linux", "Docker"]
    colors = ["#777BB4", "#21759B", "#F7DF1E", "#3178C6", "#E34F26", "#1572B6", "#4479A1", "#F05032", "#181717", "#FCC624", "#2496ED"]
    height = 100
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}" viewBox="0 0 800 {height}">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" rx="12" fill="url(#bgGrad)" stroke="#30363d" stroke-width="1" />
  <text x="400" y="35" font-family="system-ui, sans-serif" font-size="18" fill="#58A6FF" text-anchor="middle" font-weight="bold">🛠️ Tech Stack</text>
'''
    x = 40
    for i, tech in enumerate(techs):
        svg += f'''  <rect x="{x}" y="55" width="60" height="30" rx="6" fill="{colors[i]}" opacity="0.15" stroke="{colors[i]}" stroke-width="1" />
  <text x="{x+30}" y="75" font-family="system-ui, sans-serif" font-size="10" fill="{colors[i]}" text-anchor="middle" font-weight="bold">{tech}</text>
'''
        x += 70
    svg += '</svg>'
    with open("assets/tech_stack.svg", "w", encoding="utf-8") as f: f.write(svg)

def generate_wp_badges_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="80" viewBox="0 0 800 80">
  <rect x="100" y="10" width="180" height="36" rx="18" fill="#21759B" />
  <text x="190" y="33" font-family="system-ui, sans-serif" font-size="14" fill="#ffffff" text-anchor="middle" font-weight="bold">Translation Contributor</text>
  <rect x="300" y="10" width="180" height="36" rx="18" fill="#21759B" />
  <text x="390" y="33" font-family="system-ui, sans-serif" font-size="14" fill="#ffffff" text-anchor="middle" font-weight="bold">Translation Editor '26</text>
  <rect x="500" y="10" width="180" height="36" rx="18" fill="#21759B" />
  <text x="590" y="33" font-family="system-ui, sans-serif" font-size="14" fill="#ffffff" text-anchor="middle" font-weight="bold">Plugin Developer</text>
</svg>'''
    with open("assets/wp_badges.svg", "w", encoding="utf-8") as f: f.write(svg)

def generate_stats_svg(stats, total_stars):
    height = 160
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}" viewBox="0 0 800 {height}">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" rx="16" fill="url(#bgGrad)" stroke="#30363d" stroke-width="1" />
  <text x="30" y="40" font-family="system-ui, sans-serif" font-size="20" fill="#58A6FF" font-weight="bold">📊 Developer Stats</text>
  <line x1="20" y1="55" x2="780" y2="55" stroke="#30363d" stroke-width="1" />
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" fill="freeze" begin="0.1s" /><text x="100" y="90" font-family="system-ui, sans-serif" font-size="28" fill="#D29922" font-weight="bold" text-anchor="middle">{total_stars}</text><text x="100" y="115" font-family="system-ui, sans-serif" font-size="14" fill="#8B949E" text-anchor="middle">Total Stars</text></g>
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" fill="freeze" begin="0.2s" /><text x="300" y="90" font-family="system-ui, sans-serif" font-size="28" fill="#58A6FF" font-weight="bold" text-anchor="middle">{stats.get("public_repos", 0)}</text><text x="300" y="115" font-family="system-ui, sans-serif" font-size="14" fill="#8B949E" text-anchor="middle">Public Repos</text></g>
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" fill="freeze" begin="0.3s" /><text x="500" y="90" font-family="system-ui, sans-serif" font-size="28" fill="#3FB950" font-weight="bold" text-anchor="middle">{stats.get("followers", 0)}</text><text x="500" y="115" font-family="system-ui, sans-serif" font-size="14" fill="#8B949E" text-anchor="middle">Followers</text></g>
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" fill="freeze" begin="0.4s" /><text x="700" y="90" font-family="system-ui, sans-serif" font-size="28" fill="#8B5CF6" font-weight="bold" text-anchor="middle">{stats.get("following", 0)}</text><text x="700" y="115" font-family="system-ui, sans-serif" font-size="14" fill="#8B949E" text-anchor="middle">Following</text></g>
</svg>'''
    with open("assets/stats.svg", "w", encoding="utf-8") as f: f.write(svg)

def generate_streak_svg(total_contributions, current_streak, longest_streak):
    height = 160
    dash = 188.5
    offset = dash - (dash * min(current_streak, 30) / 30)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}" viewBox="0 0 800 {height}">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0d1117" /><stop offset="100%" stop-color="#161b22" /></linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="3" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="100%" height="100%" rx="16" fill="url(#bgGrad)" stroke="#30363d" stroke-width="1" />
  <text x="30" y="40" font-family="system-ui, sans-serif" font-size="20" fill="#58A6FF" font-weight="bold">🔥 Contribution Streak</text>
  <line x1="20" y1="55" x2="780" y2="55" stroke="#30363d" stroke-width="1" />
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" fill="freeze" begin="0.1s" /><text x="150" y="100" font-family="system-ui, sans-serif" font-size="32" fill="#58A6FF" font-weight="bold" text-anchor="middle">{total_contributions}</text><text x="150" y="125" font-family="system-ui, sans-serif" font-size="14" fill="#8B949E" text-anchor="middle">Total Contributions</text></g>
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" fill="freeze" begin="0.2s" /><circle cx="400" cy="95" r="30" fill="none" stroke="#30363d" stroke-width="4" /><circle cx="400" cy="95" r="30" fill="none" stroke="#F85149" stroke-width="4" stroke-dasharray="{dash}" stroke-dashoffset="{dash}" filter="url(#glow)"><animate attributeName="stroke-dashoffset" values="{dash};{offset}" dur="1s" fill="freeze" begin="0.5s" /></circle><text x="400" y="100" font-family="system-ui, sans-serif" font-size="22" fill="#F85149" font-weight="bold" text-anchor="middle">{current_streak}</text><text x="400" y="125" font-family="system-ui, sans-serif" font-size="14" fill="#8B949E" text-anchor="middle">Current Streak</text></g>
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" fill="freeze" begin="0.3s" /><text x="650" y="100" font-family="system-ui, sans-serif" font-size="32" fill="#3FB950" font-weight="bold" text-anchor="middle">{longest_streak}</text><text x="650" y="125" font-family="system-ui, sans-serif" font-size="14" fill="#8B949E" text-anchor="middle">Longest Streak</text></g>
</svg>'''
    with open("assets/streak.svg", "w", encoding="utf-8") as f: f.write(svg)

def generate_languages_svg(repos):
    lang_counts = collections.Counter(r["language"] for r in repos if r.get("language"))
    top = lang_counts.most_common(5)
    total = sum(lang_counts.values()) or 1
    height = 100 + (len(top) * 40)
    colors = ["#58A6FF", "#3FB950", "#D29922", "#8B5CF6", "#F85149"]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}" viewBox="0 0 800 {height}">
  <defs><linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0d1117" /><stop offset="100%" stop-color="#161b22" /></linearGradient></defs>
  <rect width="100%" height="100%" rx="16" fill="url(#bgGrad)" stroke="#30363d" stroke-width="1" />
  <text x="30" y="40" font-family="system-ui, sans-serif" font-size="20" fill="#58A6FF" font-weight="bold">💻 Language Breakdown</text>
  <line x1="20" y1="55" x2="780" y2="55" stroke="#30363d" stroke-width="1" />
'''
    y, delay = 85, 0.1
    for i, (lang, count) in enumerate(top):
        pct = (count / total) * 100
        bar_w = (pct / 100) * 500
        color = colors[i % len(colors)]
        svg += f'''  <g><text x="30" y="{y}" font-family="system-ui, sans-serif" font-size="14" fill="#c9d1d9">{lang}</text><text x="780" y="{y}" font-family="system-ui, sans-serif" font-size="14" fill="#8B949E" text-anchor="end">{pct:.1f}%</text><rect x="150" y="{y-10}" width="0" height="12" rx="6" fill="{color}"><animate attributeName="width" values="0;{bar_w}" dur="0.8s" fill="freeze" begin="{delay}s" /></rect></g>
'''
        y += 40; delay += 0.1
    svg += '</svg>'
    with open("assets/languages.svg", "w", encoding="utf-8") as f: f.write(svg)

def generate_activity_svg(repos):
    height = 120 + (len(repos) * 45)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}" viewBox="0 0 800 {height}">
  <defs><linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0d1117" /><stop offset="100%" stop-color="#161b22" /></linearGradient></defs>
  <rect width="100%" height="100%" rx="16" fill="url(#bgGrad)" stroke="#30363d" stroke-width="1" />
  <text x="30" y="40" font-family="system-ui, sans-serif" font-size="20" fill="#58A6FF" font-weight="bold">⚡ Dynamic Activity</text>
  <circle cx="740" cy="35" r="6" fill="#3FB950"><animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite" /></circle>
  <line x1="20" y1="55" x2="780" y2="55" stroke="#30363d" stroke-width="1" />
'''
    y, delay = 85, 0.1
    for repo, date in repos:
        svg += f'''  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" fill="freeze" begin="{delay}s" /><animateTransform attributeName="transform" type="translate" values="-30,0;0,0" dur="0.5s" fill="freeze" begin="{delay}s" /><text x="30" y="{y}" font-family="system-ui, sans-serif" font-size="15" fill="#58A6FF" font-weight="bold">{html.escape(repo)}</text><text x="400" y="{y}" font-family="system-ui, sans-serif" font-size="15" fill="#3FB950">⚡ Pushed commits</text><text x="650" y="{y}" font-family="system-ui, sans-serif" font-size="15" fill="#8B949E">{date}</text></g>
'''
        y += 45; delay += 0.1
    svg += '</svg>'
    with open("assets/activity.svg", "w", encoding="utf-8") as f: f.write(svg)

def generate_starred_svg(repos):
    height = 120 + (len(repos) * 45)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}" viewBox="0 0 800 {height}">
  <defs><linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0d1117" /><stop offset="100%" stop-color="#161b22" /></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="3" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
  <rect width="100%" height="100%" rx="16" fill="url(#bgGrad)" stroke="#30363d" stroke-width="1" />
  <text x="30" y="40" font-family="system-ui, sans-serif" font-size="20" fill="#58A6FF" font-weight="bold">⭐ Top Starred Repositories</text>
  <g transform="translate(740, 35)"><path d="M0,-8 L2.5,-2.5 L8,-2.5 L3.5,1 L5,6.5 L0,3 L-5,6.5 L-3.5,1 L-8,-2.5 L-2.5,-2.5 Z" fill="#D29922" filter="url(#glow)"><animateTransform attributeName="transform" type="rotate" values="0;10;-10;0" dur="4s" repeatCount="indefinite" /></path></g>
  <line x1="20" y1="55" x2="780" y2="55" stroke="#30363d" stroke-width="1" />
'''
    y, delay = 85, 0.1
    for name, stars, desc in repos:
        svg += f'''  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" fill="freeze" begin="{delay}s" /><animateTransform attributeName="transform" type="translate" values="30,0;0,0" dur="0.5s" fill="freeze" begin="{delay}s" /><text x="30" y="{y}" font-family="system-ui, sans-serif" font-size="15" fill="#58A6FF" font-weight="bold">{html.escape(name)}</text><text x="300" y="{y}" font-family="system-ui, sans-serif" font-size="15" fill="#D29922">⭐ {stars}</text><text x="420" y="{y}" font-family="system-ui, sans-serif" font-size="14" fill="#8B949E">{html.escape(desc)}</text></g>
'''
        y += 45; delay += 0.1
    svg += '</svg>'
    with open("assets/starred.svg", "w", encoding="utf-8") as f: f.write(svg)

# ═══════════════════════════════════════════════════════════════
#  MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════

def update_readme():
    os.makedirs("assets", exist_ok=True)
    
    # Generate static assets
    generate_wave_svg("header.svg", 220, "header", True)
    generate_wave_svg("footer.svg", 140, "footer", False)
    generate_divider_svg()
    generate_social_svg()
    generate_bento_svg()
    generate_tech_stack_svg()
    generate_wp_badges_svg()
    
    # Fetch dynamic data
    user_stats = fetch_user_stats()
    all_repos = fetch_all_repos()
    contributions_data = fetch_contributions()
    activity_data = fetch_recent_activity()
    
    # Generate dynamic assets
    if user_stats:
        total_stars = sum(repo.get("stargazers_count", 0) for repo in all_repos)
        generate_stats_svg(user_stats, total_stars)
        
    if contributions_data:
        total_contributions = contributions_data.get("totalContributions", 0)
        current_streak, longest_streak = calculate_streaks(contributions_data)
        generate_streak_svg(total_contributions, current_streak, longest_streak)
        
    if all_repos:
        generate_languages_svg(all_repos)
        all_repos.sort(key=lambda x: x.get("stargazers_count", 0), reverse=True)
        starred_data = []
        for repo in all_repos[:3]:
            name = repo["name"]
            stars = repo["stargazers_count"]
            desc = repo.get("description") or "No description provided."
            if len(desc) > 45: desc = desc[:42] + "..."
            starred_data.append((name, stars, desc))
        if starred_data:
            generate_starred_svg(starred_data)
            
    if activity_data:
        generate_activity_svg(activity_data)

if __name__ == "__main__":
    update_readme()
