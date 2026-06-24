from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from services.github_service import get_github_data
from utils.scorer import calculate_github_score
from fastapi.middleware.cors import CORSMiddleware
from services.leetcode_service import get_leetcode_data
from utils.scorer import calculate_leetcode_score
from services.ai_service import generate_ai_feedback # NEW

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Serve Frontend Static Files ──────────────────────────────────────────
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Also mount script.js, index.css etc.
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/github/{username}")
async def analyze_github(username: str):
    import time
    start_time = time.time()
    try:
        print(f"INFO: Fetching GitHub data for {username}...")
        data = get_github_data(username)
        print(f"INFO: GitHub data fetched in {time.time() - start_time:.2f}s")
    except Exception as e:
        print(f"ERROR: GitHub Fetch failed: {str(e)}")
        raise HTTPException(status_code=502, detail=str(e))

    if not data:
        raise HTTPException(status_code=404, detail=f"GitHub user '{username}' not found")

    score = calculate_github_score(data)
    
    # NEW: Informative AI feedback
    print(f"INFO: Generating AI feedback for {username}...")
    ai_start = time.time()
    ai_feedback = await generate_ai_feedback(username, data)
    print(f"INFO: AI feedback generated in {time.time() - ai_start:.2f}s (Total: {time.time() - start_time:.2f}s)")

    return {
        "username": username,
        "repos": data["repo_count"],
        "stars": data["stars"],
        "followers": data["followers"],
        "languages": data["languages"],
        "skill_distribution": data["skill_distribution"],
        "quality_metrics": data["quality_metrics"],
        "feedback": data["feedback"],
        "ai_feedback": ai_feedback, # NEW
        "score": score
    }

@app.get("/leetcode/{username}")
def analyze_leetcode(username: str):
    try:
        data = get_leetcode_data(username)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Unexpected error: {e}")

    if not data:
        raise HTTPException(status_code=404, detail=f"LeetCode user '{username}' not found")

    score = calculate_leetcode_score(data)

    return {
        "username": username,
        "total_solved": data["total_solved"],
        "easy_solved":   data["easy"],
        "medium_solved": data["medium"],
        "hard_solved":   data["hard"],
        "score": score
    }

from services.hackerrank_service import get_hackerrank_data
from utils.scorer import calculate_hackerrank_score

@app.get("/hackerrank/{username}")
def analyze_hackerrank(username: str):
    try:
        data = get_hackerrank_data(username)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    score = calculate_hackerrank_score(data)

    return {
        "username": username,
        "badges": data.get("badges", 0),
        "certifications": data.get("certifications", 0),
        "score": score
    }

@app.get("/full/{username}")
def full_analysis(username: str):
    github = get_github_data(username)
    leetcode = get_leetcode_data(username)
    hackerrank = get_hackerrank_data(username)

    g_score = calculate_github_score(github) if github else 0
    l_score = calculate_leetcode_score(leetcode) if leetcode else 0
    h_score = calculate_hackerrank_score(hackerrank)

    final_score = (g_score + l_score + h_score) // 3

    return {
        "github_score": g_score,
        "leetcode_score": l_score,
        "hackerrank_score": h_score,
        "final_score": final_score
    }