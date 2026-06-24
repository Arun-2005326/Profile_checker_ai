def calculate_github_score(data):
    score = 0
    feedback = []

    # 1. Repository Count (Max 20)
    repo_score = min(data["repo_count"] * 1, 20)
    score += repo_score
    if repo_score < 15: feedback.append("Aim for at least 15+ public repositories to show consistency.")

    # 2. Stars/Impact (Max 30)
    star_score = min(data["stars"] * 3, 30)
    score += star_score
    if star_score < 10: feedback.append("Work on 1-2 'pinned' projects to gain more stars and visibility.")

    # 3. Languages/Stack (Max 20)
    lang_score = min(len(data["languages"]) * 4, 20)
    score += lang_score
    if lang_score < 10: feedback.append("Learn and use at least 3 industrial languages (e.g. Java, Python, TS).")

    # 4. Documentation Quality (Max 15) - NEW
    qm = data.get("quality_metrics", {})
    doc_score = min((qm.get("readme_score", 0) * 2) + (qm.get("license_score", 0) * 1), 15)
    score += doc_score
    if doc_score < 10: feedback.append("Add professional READMEs and Licenses to your top 5 most starred repos.")

    # 5. Followers/Social (Max 15)
    follower_score = min(data.get("followers", 0) * 1, 15)
    score += follower_score

    data["feedback"] = feedback
    return int(min(score, 100))

def calculate_leetcode_score(data):
    score = 0
    score += min(data.get("total_solved", 0) * 0.15, 40)
    score += min(data.get("medium", 0) * 1.5, 40)
    score += min(data.get("hard", 0) * 4, 20)
    return int(min(score, 100))

def calculate_hackerrank_score(data):
    score = data.get("badges", 0) * 10 + data.get("certifications", 0) * 20
    return min(score, 100)