import os
import google.generativeai as genai
import requests
import json

# API కీ ని సీక్రెట్స్ నుండి తీసుకోవడం
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# మోడల్ సెటప్ - 'gemini-1.5-flash' వాడండి
model = genai.GenerativeModel('gemini-1.5-flash')

# GitHub PR వివరాలు
event_path = os.environ['GITHUB_EVENT_PATH']
with open(event_path, 'r') as f:
    event_data = json.load(f)

diff_url = event_data['pull_request']['diff_url']
response = requests.get(diff_url)
code_diff = response.text

# AI రివ్యూ
response = model.generate_content(f"Review this code: {code_diff}")

# GitHub లో కామెంట్ పోస్ట్ చేయడం
comments_url = event_data['pull_request']['comments_url']
headers = {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
requests.post(comments_url, json={"body": response.text}, headers=headers)
