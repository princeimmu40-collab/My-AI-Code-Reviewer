import os
import json
import requests
import google.generativeai as genai

# API Setup
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-1.5-flash')

# 1. GitHub PR Data
with open(os.environ['GITHUB_EVENT_PATH'], 'r') as f:
    event_data = json.load(f)

diff_url = event_data['pull_request']['diff_url']
response = requests.get(diff_url)
diff_code = response.text

# 2. తప్పు ఫైల్ అయితే చెక్ చేస్తుంది
if not diff_code.strip():
    comment_body = "మీరు పంపిన ఫైల్‌లో ఎటువంటి కోడ్ మార్పులు లేవు (Empty Diff). దయచేసి ఏదైనా కోడ్ మార్చి ప్రయత్నించండి."
else:
    # 3. AI తో రివ్యూ
    prompt = f"Review this code: {diff_code}"
    comment_body = model.generate_content(prompt).text

# 4. Post Comment
headers = {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}", "Accept": "application/vnd.github.v3+json"}
requests.post(event_data['pull_request']['comments_url'], json={"body": comment_body}, headers=headers)
