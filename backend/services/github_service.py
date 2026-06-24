import httpx

# Unified Language → Domain Map for Skill Radar
DOMAIN_MAP = {
    "JavaScript": "Web", "TypeScript": "Web", "HTML": "Web", "CSS": "Web",
    "Python": "Data/AI", "R": "Data/AI", "Jupyter Notebook": "Data/AI",
    "Java": "System", "C++": "System", "C": "System", "C#": "System", "Go": "System", "Rust": "System",
    "Swift": "Mobile", "Kotlin": "Mobile", "Dart": "Mobile"
}

def get_github_data(username):
    # Fetch user basics for followers
    user_url = f"https://api.github.com/users/{username}"
    # Fetch 100 repos to get a better skill picture
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    
    with httpx.Client() as client:
        try:
            user_res = client.get(user_url)
            repos_res = client.get(repos_url)

            if user_res.status_code != 200 or repos_res.status_code != 200:
                return None

            user_data = user_res.json()
            repos = repos_res.json()
        except:
            return None

    stars = sum(repo["stargazers_count"] for repo in repos)
    
    lang_stats = {}
    domains = {"Web": 0, "Data/AI": 0, "System": 0, "Mobile": 0, "Other": 0}

    # Sort repos by stars to pick "Featured" ones for README check
    top_repos = sorted(repos, key=lambda x: x["stargazers_count"], reverse=True)[:5]
    has_readme = 0
    has_license = 0

    for repo in repos:
        lang = repo["language"]
        if lang:
            lang_stats[lang] = lang_stats.get(lang, 0) + 1
            domain = DOMAIN_MAP.get(lang, "Other")
            domains[domain] += 1
            
    # Quick check for quality in top repos (simulated via API fields where possible)
    for repo in top_repos:
        if repo.get("has_pages") or repo.get("homepage"): has_readme += 1 # Proxies for quality
        if repo.get("license"): has_license += 1

    return {
        "repo_count": len(repos),
        "stars": stars,
        "followers": user_data.get("followers", 0),
        "languages": list(lang_stats.keys()),
        "skill_distribution": domains,
        "quality_metrics": {
            "top_repos_count": len(top_repos),
            "readme_score": has_readme, # simplified proxy
            "license_score": has_license
        }
    }