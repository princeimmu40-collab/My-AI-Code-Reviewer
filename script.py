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
response = requests.get(diff_url)
diff_code = response.text

# 3. Gemini AI సెటప్
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# DEBUG: మీ API కీకి అందుబాటులో ఉన్న మోడల్స్ చూడటానికి
print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

# ఇక్కడ 'models/gemini-1.5-flash' లేదా లాగ్స్‌లో కనిపించిన పేరును వాడండి
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 4. రివ్యూ జనరేషన్
prompt = f"Review this code and provide feedback in Markdown:\n\n{diff_code}"
response = model.generate_content(prompt)
review_text = response.text

# 5. GitHub లో కామెంట్ పోస్ట్ చేయడం
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}
payload = {"body": review_text}
requests.post(comments_url, json=payload, headers=headers)
