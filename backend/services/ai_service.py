import os
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

# Configure Groq
async def generate_ai_feedback(username, data):
    """
    Generate professional, human-like feedback based on GitHub profile statistics using Groq (Llama 3).
    """
    api_key_local = os.getenv("GROQ_API_KEY")
    if not api_key_local:
        return "Groq API Key missing. Please set GROQ_API_KEY in your .env file to enable AI insights."

    client_local = AsyncGroq(api_key=api_key_local)

    prompt = f"""
    As a senior technical recruiter, analyze this GitHub profile for a student/entry-level developer named {username}.
    
    Profile Metrics:
    - Public Repos: {data.get('repo_count')}
    - Total Stars: {data.get('stars')}
    - Followers: {data.get('followers')}
    - Languages/Tech Stack: {', '.join(data.get('languages', [])[:5])}
    - Documentation Quality Score: {data.get('quality_metrics', {}).get('readme_score', 0)}/10
    
    Provide exactly 3 bullet points of high-level 'Senior Recruiter Insights' about this profile. 
    Focus on their marketability and what stands out professionally. Keep it concise (max 20 words per bullet).
    """

    try:
        chat_completion = await client_local.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior technical recruiter specializing in developer hiring."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=150,
            temperature=0.7,
            timeout=15.0
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"AI Feedback currently unavailable (Groq): {str(e)}"