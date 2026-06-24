import os
import google.generativeai as genai

# మీ AIza కీని ఇక్కడ ఇవ్వండి (టెస్టింగ్ కోసం)
API_KEY = "YOUR_AIza_KEY_HERE"

def test_connection():
    try:
        print("Connecting to Gemini 3.5 Flash...")
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('models/gemini-3.5-flash')
        
        # సింపుల్ టెస్ట్ క్వశ్చన్
        response = model.generate_content("Hi! Are you working?")
        
        print("\n--- సక్సెస్! ---")
        print("AI రెస్పాన్స్:", response.text)
        print("----------------")
        
    except Exception as e:
        print("\n--- ఎర్రర్ వచ్చింది! ---")
        print(f"ఎర్రర్ వివరాలు: {e}")
        print("సలహా: మీ API కీ కరెక్ట్‌గా ఉందో లేదో, 'AIza' తో మొదలవుతుందో లేదో చూడండి.")

if __name__ == "__main__":
    test_connection()
