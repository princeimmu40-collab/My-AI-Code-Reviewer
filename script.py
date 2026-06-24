import os
import requests
import google.generativeai as genai

# 1. Configure with your NEW API Key (AIza...)
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# 2. Use the current supported model
model = genai.GenerativeModel('gemini-3.5-flash')

# 3. Handle PR data
# ... (same as before)

# 4. Generate content (Note: parameters like top_p/temp removed)
response = model.generate_content(f"Review this code: {diff_code}")

# 5. Post comment
# ... (same as before)
