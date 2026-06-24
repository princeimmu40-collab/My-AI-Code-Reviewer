import os
import json
import requests
import google.generativeai as genai

# GitHub నుండి డేటా
with open(os.environ['GITHUB_EVENT_PATH'], 'r') as f:
    event_data = json.load(f)

diff_url = event_data['pull_request']['diff_url']
comments_url = event_data['pull_request']['comments_url']

# Diff డౌన్‌లోడ్
response = requests.get(diff_url)
diff_code = response.text

# Gemini కాన్ఫిగరేషన్
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-1.5-flash') # వేగవంతమైన మరియు ఉచిత మోడల్

# రివ్యూ జనరేషన్
response = model.generate_content(f"Review this code and provide feedback in Markdown: {diff_code}")

# GitHubలో కామెంట్ పోస్ట్ చేయడం
headers = {"Authorization": f"token {os.environ['GITHUB_TOKEN']}", "Accept": "application/vnd.github.v3+json"}
requests.post(comments_url, json={"body": response.text}, headers=headers)
