import os
from flask import Flask, request
import africastalking
import google.generativeai as genai

# This MUST be outside any function so Render/Gunicorn can see it
app = Flask(__name__)

# 1. Setup AI (Gemini 1.5 Flash)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Setup Africa's Talking
# Username is ALWAYS "sandbox" for the simulator
at_username = "sandbox"
at_api_key = os.environ.get("AT_API_KEY")
africastalking.initialize(at_username, at_api_key)
sms = africastalking.SMS

@app.route('/')
def index():
    return "🌱 Smart-Pest-Detection is LIVE!"

@app.route('/incoming-sms', methods=['POST'])
def incoming_sms():
    # AT sends data as form values
    sender = request.values.get("from")
    text = request.values.get("text", "")
    
    # 3. Location & AI Logic
    if "location" in text.lower():
        ai_reply = "To help your crops, please reply with your City or Sub-county (e.g., 'Chuka' or 'Nairobi')."
    else:
        prompt = f"As a Kenyan agronomist, help a farmer who says: '{text}'. Max 140 chars."
        try:
            response = model.generate_content(prompt)
            ai_reply = response.text
        except Exception as e:
            print(f"AI Error: {e}")
            ai_reply = "I'm experiencing a delay. Please try again in 1 minute!"

    # 4. Send response back to Simulator
    try:
        sms.send(ai_reply, [sender])
        return "OK", 200
    except Exception as e:
        print(f"SMS Error: {e}")
        return "Error", 500

if __name__ == "__main__":
    # Local testing only; Render uses the Gunicorn command instead
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)