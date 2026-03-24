# app/models/sms_service.py
import africastalking
import os
import ssl
import urllib3
from dotenv import load_dotenv

load_dotenv()

def initialize_sms():
    """Initialize Africa's Talking SDK with SSL fix for Windows."""
    urllib3.disable_warnings()

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    username = os.getenv("AFRICASTALKING_USERNAME", "sandbox")
    api_key = os.getenv("AFRICASTALKING_API_KEY", "")
    africastalking.initialize(username, api_key)
    return africastalking.SMS


def send_sms(phone, message):
    """
    Send a single SMS to a phone number.
    Returns True if successful, False if failed.
    """
    try:
        sms = initialize_sms()
        response = sms.send(message, [phone], enqueue=True)
        print(f"SMS sent to {phone}: {response}")
        return True
    except Exception as e:
        print(f"SMS send error (non-critical): {e}")
        return False


def send_bulk_sms(phone_numbers, message):
    """
    Send the same SMS to multiple phone numbers at once.
    Used for disease outbreak alerts.
    """
    try:
        sms = initialize_sms()
        response = sms.send(message, phone_numbers)
        print(f"Bulk SMS sent to {len(phone_numbers)} farmers: {response}")
        return True
    except Exception as e:
        print(f"Bulk SMS error (non-critical): {e}")
        return False


def escalate_to_officer(farmer_phone, symptoms, disease_name, language="en"):
    """
    Send an alert to the extension officer when
    the system cannot confidently diagnose a disease.
    """
    officer_phone = os.getenv("EXTENSION_OFFICER_PHONE", "")
    if not officer_phone:
        print("No extension officer phone set in .env")
        return False

    message = (
        f"[SMART PEST ALERT]\n"
        f"Farmer: {farmer_phone}\n"
        f"Symptoms: {symptoms}\n"
        f"AI Diagnosis: {disease_name or 'Could not identify'}\n"
        f"Action: Please call this farmer for expert advice."
    )
    return send_sms(officer_phone, message)


def send_outbreak_alert(county, disease_name, farmer_phones, language="en"):
    """
    Send a disease outbreak alert to all farmers in a county
    when 3 or more farmers report the same disease.
    """
    if language == "sw":
        message = (
            f"[TAHADHARI YA UGONJWA]\n"
            f"Ugonjwa wa {disease_name} umeripotiwa na wakulima wengi "
            f"katika kaunti ya {county}.\n"
            f"Angalia mazao yako na piga dawa mapema."
        )
    else:
        message = (
            f"[DISEASE OUTBREAK ALERT]\n"
            f"{disease_name} has been reported by multiple farmers "
            f"in {county} county.\n"
            f"Check your crops and apply treatment early."
        )
    return send_bulk_sms(farmer_phones, message)