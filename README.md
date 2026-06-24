# ⚡ GitScore AI

> **AI-powered placement readiness analyzer** — Analyze your GitHub, LeetCode, and HackerRank profiles and get a comprehensive score with AI-generated recruiter feedback.

---

## ✨ Features

- 🔍 **GitHub Analysis** — Scores your profile across repos, stars, followers, documentation quality, and original work
- 🧩 **LeetCode Integration** — Tracks total problems solved across Easy, Medium, and Hard difficulties
- 🏆 **HackerRank Integration** — Evaluates badges and certifications
- 🤖 **AI Recruiter Insights** — Powered by Google Gemini / Groq to generate personalized feedback as if from a real recruiter
- 📊 **Visual Score Dashboard** — Animated score rings, metric cards, and skill distribution charts
- 🌐 **All-in-One Server** — Backend serves the frontend; no separate build step needed

---

## 🖥️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, FastAPI, Uvicorn |
| **AI** | Google Gemini (`google-generativeai`), Groq |
| **HTTP Client** | httpx |
| **Validation** | Pydantic v2, pydantic-settings |
| **Frontend** | HTML5, Vanilla CSS (dark theme), Vanilla JavaScript |
| **Charts** | Chart.js |
| **Data Sources** | GitHub REST API v3, LeetCode GraphQL API, HackerRank API |

---

## 📁 Project Structure

```
placementready-ai/
├── backend/
│   ├── main.py                  # FastAPI app — serves frontend + all API routes
│   ├── .env                     # Environment variables (API keys)
│   ├── services/
│   │   ├── github_service.py    # GitHub API integration & data parsing
│   │   ├── leetcode_service.py  # LeetCode GraphQL integration
│   │   ├── hackerrank_service.py# HackerRank profile scraping
│   │   └── ai_service.py        # AI feedback generation (Gemini / Groq)
│   ├── utils/
│   │   └── scorer.py            # Scoring algorithms for all platforms
│   ├── models/
│   │   └── schema.py            # Pydantic request/response models
│   └── core/
│       └── config.py            # App configuration & env settings
├── frontend/
│   ├── index.html               # Main UI (served at /)
│   ├── style.css                # Dark-theme styling (served at /static/style.css)
│   └── script.js                # Frontend logic & API calls (served at /static/script.js)
├── requirements.txt             # Python dependencies
└── README.md
```

---

## ⚙️ Setup & Run

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd placementready-ai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create or edit the `.env` file inside `backend/`:
```env
GITHUB_TOKEN=your_github_personal_access_token
GEMINI_API_KEY=your_google_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```

> **Note:** `GITHUB_TOKEN` is optional but raises the API rate limit from 60 → 5,000 requests/hour. AI feedback requires at least one of `GEMINI_API_KEY` or `GROQ_API_KEY`.

### 4. Start the Server
```bash
cd backend
python -m uvicorn main:app --reload
```

### 5. Open the App
```
http://localhost:8000
```

| URL | Description |
|---|---|
| `http://localhost:8000` | Main app (frontend UI) |
| `http://localhost:8000/docs` | Interactive Swagger API docs |
| `http://localhost:8000/github/{username}` | GitHub analysis API |
| `http://localhost:8000/leetcode/{username}` | LeetCode analysis API |
| `http://localhost:8000/hackerrank/{username}` | HackerRank analysis API |
| `http://localhost:8000/full/{username}` | Combined score API |

---

## 🏆 Scoring Criteria

### GitHub Score (out of 100)

| Category | Max Points |
|---|---|
| Profile Completeness (bio, avatar, location) | 20 |
| Repository Count | 20 |
| Repository Quality (stars, READMEs, descriptions) | 30 |
| Followers | 15 |
| Original Work (non-forked repos) | 15 |
| **Total** | **100** |

### LeetCode Score (out of 100)
Weighted by difficulty: Easy (1pt) · Medium (2pt) · Hard (3pt), normalized to 100.

### HackerRank Score (out of 100)
Based on number of badges and certifications earned.

---

## 🔌 API Reference

### `GET /github/{username}`
Returns GitHub profile analysis with AI feedback.

**Response:**
```json
{
  "username": "torvalds",
  "repos": 8,
  "stars": 10500,
  "followers": 200000,
  "languages": ["C", "Shell"],
  "skill_distribution": { "C": 70, "Shell": 30 },
  "quality_metrics": { "has_readme": true, "avg_stars": 1312 },
  "feedback": ["Add more READMEs", "Pin top repos"],
  "ai_feedback": "Your profile demonstrates exceptional...",
  "score": 94
}
```

### `GET /leetcode/{username}`
Returns LeetCode stats and score.

### `GET /hackerrank/{username}`
Returns HackerRank badges and score.

### `GET /full/{username}`
Returns combined score across all three platforms.

---

## 📄 License

© 2026 **Arunkumar** · GitScore AI · All rights reserved.
