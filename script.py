import os
import json
import requests
import google.generativeai as genai
import time

# 1. API Configuration
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# 2. Model Setup
model = genai.GenerativeModel('gemini-3.5-flash')

# 3. Handle PR data (దీని వల్ల 'diff_code' డిఫైన్ అవుతుంది)
event_path = os.environ['GITHUB_EVENT_PATH']
with open(event_path, 'r') as f:
    event_data = json.load(f)

# PR diff URL పొందడం
diff_url = event_data['pull_request']['diff_url']
response = requests.get(diff_url)
diff_code = response.text  # ఇక్కడ 'diff_code' డిఫైన్ చేయబడింది

# 4. Generate content (Retry logic తో)
def generate_review(diff_text):
    for i in range(3): # 3 సార్లు ప్రయత్నిస్తుంది
        try:
            return model.generate_content(f"Review this code: {diff_text}")
        except Exception as e:
            print(f"Attempt {i+1} failed: {e}")
            time.sleep(10)
    return None

review_response = generate_review(diff_code)

# 5. Post comment
if review_response:
    comments_url = event_data['pull_request']['comments_url']
    headers = {
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"body": review_response.text}
    requests.post(comments_url, json=payload, headers=headers)
    print("Review posted successfully!")
else:
    print("Failed to generate review after retries.")
