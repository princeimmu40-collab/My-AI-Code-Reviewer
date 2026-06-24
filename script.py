import os
import json
import requests
import google.generativeai as genai
from tenacity import retry, wait_exponential, stop_after_attempt

# API సెటప్
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('models/gemini-3.5-flash')

# Retry లాజిక్: ఒకవేళ Rate limit వస్తే, ఇది ఆటోమేటిక్‌గా వెయిట్ చేసి మళ్ళీ ట్రై చేస్తుంది
@retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
def generate_review(diff_code):
    return model.generate_content(f"Review this code: {diff_code}")

# GitHub డేటా & రివ్యూ జనరేషన్
event_path = os.environ['GITHUB_EVENT_PATH']
with open(event_path, 'r') as f:
    event_data = json.load(f)

diff_url = event_data['pull_request']['diff_url']
response = requests.get(diff_url)
review = generate_review(response.text)

# పోస్ట్ చేయడం
comments_url = event_data['pull_request']['comments_url']
headers = {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
requests.post(comments_url, json={"body": review.text}, headers=headers)
