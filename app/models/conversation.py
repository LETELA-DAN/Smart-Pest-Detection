# app/models/conversation.py
# Handles multi-turn symptom-guided conversations

from app.models.database import db, Session
from app.models.diagnosis import diagnose, format_sms_response
from app.data.agrovets import format_agrovet_sms
from datetime import datetime

CROP_MENU = {
    "en": (
        "Welcome to Smart Pest Detection!\n"
        "Which crop has a problem?\n"
        "1. Maize\n2. Tomato\n3. Beans\n4. Potato\n5. Cabbage/Kale\n"
        "Reply with the number."
    ),
    "sw": (
        "Karibu Smart Pest Detection!\n"
        "Ni zao gani lina tatizo?\n"
        "1. Mahindi\n2. Nyanya\n3. Maharagwe\n4. Viazi\n5. Sukuma/Kabichi\n"
        "Jibu na nambari."
    ),
}

CROP_MAP = {
    "1": "maize", "2": "tomato", "3": "beans",
    "4": "potato", "5": "cabbage",
    "maize": "maize", "mahindi": "maize",
    "tomato": "tomato", "nyanya": "tomato",
    "beans": "beans", "maharagwe": "beans",
    "potato": "potato", "viazi": "potato",
    "cabbage": "cabbage", "sukuma": "cabbage", "kale": "cabbage",
}

SYMPTOM_PROMPT = {
    "en": (
        "Describe the symptoms you see.\n"
        "For example: yellow leaves, brown spots, holes, wilting, white powder.\n"
        "Be as detailed as possible."
    ),
    "sw": (
        "Elezea dalili unazoziona.\n"
        "Mfano: majani ya njano, madoa ya kahawia, mashimo, kunyauka, unga mweupe.\n"
        "Toa maelezo ya kina iwezekanavyo."
    ),
}

COUNTY_PROMPT = {
    "en": "Which county are you in? (e.g. Nakuru, Meru, Kiambu)",
    "sw": "Uko katika kaunti gani? (mfano: Nakuru, Meru, Kiambu)",
}


def get_or_create_session(phone):
    """Get existing session or create a new one."""
    session = Session.query.filter_by(phone=phone).first()
    if not session:
        session = Session(phone=phone, step="start")
        db.session.add(session)
        db.session.commit()
    return session


def reset_session(phone):
    """Reset a farmer's conversation to the beginning."""
    session = Session.query.filter_by(phone=phone).first()
    if session:
        session.step = "start"
        session.crop = None
        session.symptoms = None
        session.last_active = datetime.utcnow()
        db.session.commit()


def handle_conversation(phone, message, language="en"):
    """
    Main conversation handler.
    Routes the farmer through a step-by-step diagnosis flow.
    Returns the reply SMS string.
    """
    message = message.strip().lower()
    session = get_or_create_session(phone)
    session.language = language
    session.last_active = datetime.utcnow()

    # Allow farmer to restart anytime
    if message in ["restart", "start", "reset", "menu", "anza", "upya"]:
        reset_session(phone)
        return CROP_MENU.get(language, CROP_MENU["en"])

    # Step 1: Ask which crop
    if session.step == "start":
        session.step = "waiting_for_crop"
        db.session.commit()
        return CROP_MENU.get(language, CROP_MENU["en"])

    # Step 2: Receive crop selection
    elif session.step == "waiting_for_crop":
        crop = CROP_MAP.get(message)
        if not crop:
            if language == "sw":
                return "Tafadhali jibu na nambari 1-5 au jina la zao.\n" + CROP_MENU["sw"]
            return "Please reply with a number 1-5 or crop name.\n" + CROP_MENU["en"]
        session.crop = crop
        session.step = "waiting_for_symptoms"
        db.session.commit()
        return SYMPTOM_PROMPT.get(language, SYMPTOM_PROMPT["en"])

    # Step 3: Receive symptoms and diagnose
    elif session.step == "waiting_for_symptoms":
        full_query = f"{session.crop} {message}"
        session.symptoms = message
        disease, detected_lang = diagnose(full_query)
        reply = format_sms_response(disease, language)

        # Ask for county to suggest agrovet
        session.step = "waiting_for_county"
        db.session.commit()

        return (
            reply +
            "\n---\n" +
            COUNTY_PROMPT.get(language, COUNTY_PROMPT["en"])
        )

    # Step 4: Receive county and suggest agrovet
    elif session.step == "waiting_for_county":
        county = message.strip()
        agrovet_info = format_agrovet_sms(county, language)
        reset_session(phone)

        if language == "sw":
            closing = "\nAndika ANZA kuanza upya au elezea tatizo jipya."
        else:
            closing = "\nType RESTART to start again or describe a new problem."

        return agrovet_info + closing

    # Fallback — restart
    reset_session(phone)
    return CROP_MENU.get(language, CROP_MENU["en"])