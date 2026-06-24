import os
import json
import requests
import google.generativeai as genai
import time

# 1. API కీ సెటప్
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-3.5-flash')

# 2. GitHub ఈవెంట్ డేటా పొందడం
event_path = os.environ['GITHUB_EVENT_PATH']
with open(event_path, 'r') as f:
    event_data = json.load(f)

# Diff URL మరియు Comments URL పొందడం
diff_url = event_data['pull_request']['diff_url']
comments_url = event_data['pull_request']['comments_url']

# 3. కోడ్ మార్పులను డౌన్‌లోడ్ చేయడం
response_diff = requests.get(diff_url)
diff_code = response_diff.text

# 4. AI రివ్యూ (Retry లాజిక్ తో)
def generate_review(code):
    for i in range(5):
        try:
            return model.generate_content(f"Review this code: {code}")
        except Exception as e:
            # 20 సెకన్ల విరామం ఇస్తుంది
            time.sleep(20) 
            print(f"Attempt {i+1} failed: {e}")
    return None

review_response = generate_review(diff_code)

# 5. GitHub లో కామెంట్ పోస్ట్ చేయడం
if review_response:
    headers = {
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"body": review_response.text}
    requests.post(comments_url, json=payload, headers=headers)
    print("Review posted successfully!")
else:
    print("Failed to generate review.")
