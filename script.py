import os
import json
import requests
import google.generativeai as genai

# GitHub ఈవెంట్ డేటాను లోడ్ చేయడం
event_path = os.getenv('GITHUB_EVENT_PATH')
with open(event_path, 'r') as f:
    event_data = json.load(f)

# PR సమాచారం తీసుకోవడం
pull_request = event_data.get('pull_request', {})
diff_url = pull_request.get('diff_url')
comments_url = pull_request.get('comments_url')
token = os.getenv('GITHUB_TOKEN')

# Diff కోడ్‌ని డౌన్‌లోడ్ చేయడం
if diff_url:
    response = requests.get(diff_url)
    diff_code = response.text
else:
    diff_code = "No diff found."

# Gemini API సెటప్
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

# కోడ్ రివ్యూ ప్రాంప్ట్
prompt = f"Review the following code changes and provide constructive feedback in Markdown format:\n\n{diff_code}"
response = model.generate_content(prompt)

# GitHub లో కామెంట్ పోస్ట్ చేయడం
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}
payload = {"body": response.text}

if comments_url:
    requests.post(comments_url, json=payload, headers=headers)
