import os
import requests
import google.generativeai as genai

# 1. API కీ సెటప్
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

# 2. మోడల్ సెటప్ (ఇక్కడ 'gemini-1.5-flash' వాడండి)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. GitHub డేటా
event_path = os.getenv('GITHUB_EVENT_PATH')
with open(event_path, 'r') as f:
    import json
    event_data = json.load(f)

diff_url = event_data['pull_request']['diff_url']
response = requests.get(diff_url)
diff_code = response.text

# 4. రివ్యూ చేయడం
response = model.generate_content(f"Review this code: {diff_code}")

# 5. పోస్ట్ చేయడం
comments_url = event_data['pull_request']['comments_url']
headers = {"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"}
requests.post(comments_url, json={"body": response.text}, headers=headers)
