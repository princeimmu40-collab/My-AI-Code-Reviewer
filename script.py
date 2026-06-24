import os
import json
import requests
import google.generativeai as genai

# 1. GitHub Action నుండి PR వివరాలను పొందడం
event_path = os.getenv('GITHUB_EVENT_PATH')
if not event_path:
    print("GITHUB_EVENT_PATH దొరకలేదు.")
    exit(1)

with open(event_path, 'r') as f:
    event_data = json.load(f)

pull_request = event_data.get('pull_request', {})
diff_url = pull_request.get('diff_url')
comments_url = pull_request.get('comments_url')
token = os.getenv('GITHUB_TOKEN')

if not diff_url or not comments_url:
    print("PR సమాచారం అందలేదు (diff_url లేదా comments_url లేదు).")
    exit(0)

# 2. కోడ్ మార్పులను (Diff) డౌన్‌లోడ్ చేయడం
response = requests.get(diff_url)
diff_code = response.text

# 3. Gemini AI ద్వారా రివ్యూ చేయడం
# ఇక్కడ 'gemini-1.5-flash' లేకపోతే 'gemini-1.5-pro' వాడండి
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

prompt = f"You are a senior developer. Review the following code diff and provide constructive feedback in Markdown format:\n\n{diff_code}"
response = model.generate_content(prompt)
review_text = response.text

# 4. రివ్యూని GitHub PR లో కామెంట్‌గా పోస్ట్ చేయడం
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}
payload = {"body": review_text}

post_response = requests.post(comments_url, json=payload, headers=headers)

if post_response.status_code == 201:
    print("రివ్యూ సక్సెస్‌ఫుల్‌గా పోస్ట్ చేయబడింది!")
else:
    print(f"ఎర్రర్ వచ్చింది: {post_response.status_code} - {post_response.text}")
