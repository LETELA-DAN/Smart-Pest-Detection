# app/routes/sms.py
from flask import Blueprint, request, Response
from app.models.diagnosis import diagnose, format_sms_response
from app.data.database import log_message

# Initialize the Blueprint
sms_bp = Blueprint('sms', __name__)

@sms_bp.route("/sms/incoming", methods=["POST"])
def incoming_sms():
    """
    Handles incoming SMS from Africa's Talking.
    Uses XML-wrapped Direct HTTP Response to send the reply back to the phone.
    """
    # 1. Extract data from Africa's Talking POST request
    sender = request.values.get("from", "")
    message = request.values.get("text", "")

    print(f"\n--- New Incoming Message ---")
    print(f"📩 From: {sender}")
    print(f"💬 Text: {message}")

    # 2. Process Diagnosis via our logic
    disease = diagnose(message)
    
    # 3. Format the SMS reply (Bilingual)
    reply_text = format_sms_response(disease, message)

    # 4. Log to Database for the Admin Dashboard
    try:
        diagnosis_name = disease['name'] if isinstance(disease, dict) else "Unknown"
        log_message(sender, message, diagnosis_name)
        print(f"💾 Database Logged: {diagnosis_name}")
    except Exception as e:
        print(f"⚠️ Database Logging Error: {e}")

    # 5. THE FINAL FIX: Wrap reply in XML <Response><Say>
    # Africa's Talking requires this specific format to forward the text 
    # back to the user's phone automatically.
    xml_reply = f'<?xml version="1.0" encoding="UTF-8"?><Response><Say>{reply_text}</Say></Response>'

    print(f"📤 XML Sent to AT: {xml_reply}")
    print(f"---------------------------\n")
    
    # Return as application/xml so the AT Gateway processes it correctly
    return Response(xml_reply, mimetype='application/xml')