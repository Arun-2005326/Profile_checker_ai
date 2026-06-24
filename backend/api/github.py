from fastapi import APIRouter, HTTPException
from services.github_service import GitHubService
from models.schema import GitHubRequest, GitHubResponse

router = APIRouter()
github_service = GitHubService()


@router.post("/analyze", response_model=GitHubResponse)
async def analyze_github_profile(request: GitHubRequest):
    """Analyze a GitHub profile for placement readiness."""
    try:
        result = await github_service.analyze_profile(request.username)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/profile/{username}")
async def get_github_profile(username: str):
    """Fetch raw GitHub profile data."""
    try:
        profile = await github_service.get_profile(username)
        return profile
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"GitHub user '{username}' not found")
