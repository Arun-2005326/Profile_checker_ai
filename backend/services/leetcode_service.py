import requests

HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
    "Origin": "https://leetcode.com",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
}

def get_leetcode_data(username: str):
    """Fetch solved-problem stats for a LeetCode user via the public GraphQL API."""
    url = "https://leetcode.com/graphql"

    query = {
        "query": """
        query getUserProfile($username: String!) {
            matchedUser(username: $username) {
                submitStats: submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
            }
        }
        """,
        "variables": {"username": username},
    }

    try:
        response = requests.post(url, json=query, headers=HEADERS, timeout=10)
        response.raise_for_status()

        body = response.json()

        # User not found on LeetCode
        matched = body.get("data", {}).get("matchedUser")
        if not matched:
            return None

        stats = matched["submitStats"]["acSubmissionNum"]
        # stats[0] = All, [1] = Easy, [2] = Medium, [3] = Hard
        return {
            "total_solved": stats[0]["count"],
            "easy":         stats[1]["count"],
            "medium":       stats[2]["count"],
            "hard":         stats[3]["count"],
        }

    except requests.exceptions.Timeout:
        raise RuntimeError("LeetCode API timed out — please try again.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"LeetCode API error: {e.response.status_code}")
    except Exception as e:
        raise RuntimeError(f"Could not fetch LeetCode data: {e}")