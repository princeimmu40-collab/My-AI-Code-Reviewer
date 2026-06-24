import os
import json
import requests
import google.generativeai as genai

# 1. API Configuration
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('models/gemini-3.5-flash')

# 2. Get GitHub Event Data
event_path = os.environ['GITHUB_EVENT_PATH']
with open(event_path, 'r') as f:
    event_data = json.load(f)

# 3. Fetch PR Diff
diff_url = event_data['pull_request']['diff_url']
response = requests.get(diff_url)
diff_code = response.text

# 4. Generate AI Review
prompt = f"""
మీరు ఒక సీనియర్ కోడ్ రివ్యూవర్. ఈ క్రింది కోడ్ మార్పులను రివ్యూ చేయండి. 
ముఖ్యంగా SQL ఫైల్స్ అయితే అందులో Primary Keys, SQL Injection vulnerabilities లేదా Best Practices ఏమైనా మిస్ అయ్యాయో చూడండి.
రివ్యూను మార్క్‌డౌన్ (Markdown) ఫార్మాట్‌లో ఇవ్వండి:

{diff_code}
"""
ai_response = model.generate_content(prompt)

# 5. Post Comment to PR
comments_url = event_data['pull_request']['comments_url']
headers = {
    "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
    "Accept": "application/vnd.github.v3+json"
}
payload = {"body": ai_response.text}

post_res = requests.post(comments_url, json=payload, headers=headers)

if post_res.status_code == 201:
    print("Review comment posted successfully!")
else:
    print(f"Failed to post comment: {post_res.status_code} - {post_res.text}")
