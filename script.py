import os
import json
import requests
import google.generativeai as genai

# API కీ కాన్ఫిగరేషన్
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# గూగుల్ రిటైర్ చేసిన మోడల్స్‌కు బదులుగా లేటెస్ట్ మోడల్ ఉపయోగించడం
# లాగ్స్‌లో కనిపించిన 'models/gemini-3.5-flash' ను ఇక్కడ వాడుతున్నాం
model = genai.GenerativeModel('models/gemini-3.5-flash')

# GitHub PR నుండి సమాచారం
event_path = os.environ['GITHUB_EVENT_PATH']
with open(event_path, 'r') as f:
    event_data = json.load(f)

diff_url = event_data['pull_request']['diff_url']
response = requests.get(diff_url)
diff_code = response.text

# AI రివ్యూ జనరేషన్
prompt = f"Review the following code changes and provide feedback in Markdown:\n\n{diff_code}"
response = model.generate_content(prompt)

# GitHub లో కామెంట్ పోస్ట్ చేయడం
comments_url = event_data['pull_request']['comments_url']
headers = {
    "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
    "Accept": "application/vnd.github.v3+json"
}
payload = {"body": response.text}
requests.post(comments_url, json=payload, headers=headers)
