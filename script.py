import os
import json
import requests
from openai import OpenAI

# 1. GitHub Actions నుండి PR వివరాలను పొందడం
# GitHub ఆటోమేటిక్‌గా ఈ ఫైల్ పాత్‌ను సెట్ చేస్తుంది
event_path = os.getenv('GITHUB_EVENT_PATH')
with open(event_path, 'r') as f:
    event_data = json.load(f)

# PR సమాచారాన్ని సేకరించడం
pull_request = event_data.get('pull_request', {})
diff_url = pull_request.get('diff_url')
comments_url = pull_request.get('comments_url')
token = os.getenv('GITHUB_TOKEN')

if not diff_url or not comments_url:
    print("PR సమాచారం అందలేదు.")
    exit(0)

# 2. GitHub నుండి కోడ్ మార్పులను (Diff) డౌన్‌లోడ్ చేయడం
response = requests.get(diff_url)
diff_code = response.text

# 3. OpenAI ద్వారా కోడ్ రివ్యూ చేయడం
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a senior developer. Review the code diff provided and provide constructive, specific feedback in Markdown format."},
        {"role": "user", "content": diff_code}
    ]
)

review_text = completion.choices[0].message.content

# 4. రివ్యూని GitHub PR లో కామెంట్‌గా పోస్ట్ చేయడం
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}

post_response = requests.post(comments_url, json={"body": review_text}, headers=headers)

if post_response.status_code == 201:
    print("రివ్యూ సక్సెస్‌ఫుల్‌గా పోస్ట్ చేయబడింది!")
else:
    print(f"ఎర్రర్ వచ్చింది: {post_response.status_code} - {post_response.text}")
