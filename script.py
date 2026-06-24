import os
import json
from openai import OpenAI

# GitHub Actions నుండి డేటాను తీసుకోవడం
event_path = os.getenv('GITHUB_EVENT_PATH')
with open(event_path, 'r') as f:
    event_data = json.load(f)

# PR URL ని ఇలా పొందాలి
pull_request = event_data.get('pull_request', {})
diff_url = pull_request.get('diff_url')
comments_url = pull_request.get('comments_url')

# మిగతా కోడ్ సేమ్ (OpenAI కాల్స్ మరియు కామెంట్ పోస్ట్ చేయడం)
