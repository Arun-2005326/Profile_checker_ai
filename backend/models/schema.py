from pydantic import BaseModel
from typing import Optional, List, Dict


class GitHubRequest(BaseModel):
    username: str


class ScoreBreakdown(BaseModel):
    profile_completeness: int
    repository_count: int
    repository_quality: int
    followers: int
    original_work: int


class GitHubResponse(BaseModel):
    username: str
    name: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    public_repos: int
    followers: int
    score: int
    breakdown: Dict[str, int]
    feedback: List[str]
