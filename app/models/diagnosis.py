# app/models/diagnosis.py
from app.data.diseases import DISEASES

def clean_text(text):
    if not text: return ""
    return text.lower().strip()

def diagnose(symptom_text):
    """Identifies the disease based on keywords."""
    if not symptom_text or len(symptom_text) < 3:
        return None

    text = clean_text(symptom_text)
    scores = []

    for disease in DISEASES:
        score = 0
        # Check crops (High weight)
        for crop in disease.get("crops", []):
            if crop in text: score += 5
        # Check keywords (Medium weight)
        for kw in disease.get("keywords", []):
            if kw in text: score += 2
        
        if score >= 4:
            scores.append((score, disease))

    if not scores:
        return None

    # Sort and pick the best dictionary
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[0][1]

def format_sms_response(disease, user_input):
    """Formats the reply for the farmer."""
    if disease is None:
        return "POLE: Hatujatambua ugonjwa. Tuma: ZAO + DALILI. Example: 'Nyanya madoa'"

    severity_map = {"HIGH": "HATARI/HIGH", "MEDIUM": "TAHADHARI", "LOW": "INFO"}
    level = severity_map.get(disease.get("severity"), "TAHADHARI")

    # Swahili detection
    sw_words = ["na", "ya", "iko", "nyanya", "mahindi", "madoa"]
    is_sw = any(w in user_input.lower() for w in sw_words)

    if is_sw:
        return f"[{level}] UGONJWA: {disease.get('name')}\nDAWA: {disease.get('remedy_sw')}"
    
    return f"[{level}] DISEASE: {disease.get('name')}\nACTION: {disease.get('remedy_en')}"