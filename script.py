import os
import json
import requests
import google.generativeai as genai

# 1. GitHub Action నుండి PR వివరాలను పొందడం
event_path = os.getenv('GITHUB_EVENT_PATH')
with open(event_path, 'r') as f:
    event_data = json.load(f)

pull_request = event_data.get('pull_request', {})
diff_url = pull_request.get('diff_url')
comments_url = pull_request.get('comments_url')
token = os.getenv('GITHUB_TOKEN')

# 2. కోడ్ మార్పులను (Diff) డౌన్‌లోడ్ చేయడం
if diff_url:
    response = requests.get(diff_url)
    diff_code = response.text
else:
    diff_code = "No diff available."

# 3. Gemini AI సెటప్ (కొత్త మోడల్‌తో)
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# లాగ్స్‌లో కనిపించిన మోడల్‌ను ఇక్కడ వాడుతున్నాము
model = genai.GenerativeModel('models/gemini-3.1-flash')

# 4. రివ్యూ జనరేషన్
prompt = f"You are a senior developer. Review the following code diff and provide constructive feedback in Markdown format:\n\n{diff_code}"
response = model.generate_content(prompt)
review_text = response.text

# 5. GitHub లో కామెంట్ పోస్ట్ చేయడం
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}
payload = {"body": review_text}

if comments_url:
    post_response = requests.post(comments_url, json=payload, headers=headers)
    if post_response.status_code == 201:
        print("రివ్యూ సక్సెస్‌ఫుల్‌గా పోస్ట్ చేయబడింది!")
    else:
        print(f"ఎర్రర్: {post_response.status_code} - {post_response.text}")
