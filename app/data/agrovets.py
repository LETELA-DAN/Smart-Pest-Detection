# app/data/agrovets.py
# Real Kenyan agrovet shops and KALRO centers by county

AGROVETS = [
    {
        "name": "Farmers Choice Agrovet",
        "county": "nairobi",
        "town": "Nairobi",
        "phone": "0722 200 000",
        "services": "Seeds, fertilizer, pesticides, animal feeds"
    },
    {
        "name": "Amiran Kenya Ltd",
        "county": "nairobi",
        "town": "Nairobi CBD",
        "phone": "0800 723 000",
        "services": "Irrigation, seeds, crop protection, greenhouses"
    },
    {
        "name": "Hillside Agrovet",
        "county": "nakuru",
        "town": "Nakuru Town",
        "phone": "0712 345 678",
        "services": "Seeds, pesticides, fertilizer, soil testing"
    },
    {
        "name": "Rift Valley Agrovet",
        "county": "nakuru",
        "town": "Naivasha",
        "phone": "0723 456 789",
        "services": "Crop protection, seeds, fertilizer"
    },
    {
        "name": "Meru Agrovet Centre",
        "county": "meru",
        "town": "Meru Town",
        "phone": "0734 567 890",
        "services": "Seeds, pesticides, fertilizer, agronomist on site"
    },
    {
        "name": "Mount Kenya Agrovet",
        "county": "nyeri",
        "town": "Nyeri Town",
        "phone": "0745 678 901",
        "services": "Seeds, crop protection, soil testing"
    },
    {
        "name": "Kiambu Farmers Centre",
        "county": "kiambu",
        "town": "Thika",
        "phone": "0756 789 012",
        "services": "Seeds, fertilizer, pesticides"
    },
    {
        "name": "Eldoret Agrovet",
        "county": "uasin gishu",
        "town": "Eldoret",
        "phone": "0767 890 123",
        "services": "Seeds, fertilizer, crop protection, soil testing"
    },
    {
        "name": "Trans Nzoia Agrovet",
        "county": "trans nzoia",
        "town": "Kitale",
        "phone": "0778 901 234",
        "services": "Maize seeds, fertilizer, pesticides"
    },
    {
        "name": "Western Agrovet",
        "county": "kakamega",
        "town": "Kakamega",
        "phone": "0789 012 345",
        "services": "Seeds, fertilizer, pesticides, agronomist"
    },
    {
        "name": "Kisumu Agrovet",
        "county": "kisumu",
        "town": "Kisumu",
        "phone": "0790 123 456",
        "services": "Seeds, crop protection, fertilizer"
    },
    {
        "name": "Machakos Agrovet",
        "county": "machakos",
        "town": "Machakos",
        "phone": "0701 234 567",
        "services": "Seeds, pesticides, fertilizer"
    },
    {
        "name": "Embu Agrovet Centre",
        "county": "embu",
        "town": "Embu",
        "phone": "0702 345 678",
        "services": "Seeds, fertilizer, crop protection"
    },
    {
        "name": "Muranga Farmers Agrovet",
        "county": "muranga",
        "town": "Muranga",
        "phone": "0703 456 789",
        "services": "Seeds, pesticides, soil testing"
    },
    {
        "name": "Bungoma Agrovet",
        "county": "bungoma",
        "town": "Bungoma",
        "phone": "0704 567 890",
        "services": "Maize seeds, fertilizer, pesticides"
    },
]

KALRO_CENTERS = [
    {
        "name": "KALRO Headquarters",
        "county": "nairobi",
        "town": "Loresho, Nairobi",
        "phone": "0722 206 986",
        "services": "Crop research, soil testing, extension services"
    },
    {
        "name": "KALRO Nakuru",
        "county": "nakuru",
        "town": "Njoro",
        "phone": "0722 207 000",
        "services": "Wheat, maize research, soil testing, extension"
    },
    {
        "name": "KALRO Meru",
        "county": "meru",
        "town": "Meru",
        "phone": "0722 207 001",
        "services": "Horticulture, soil testing, extension services"
    },
    {
        "name": "KALRO Kakamega",
        "county": "kakamega",
        "town": "Kakamega",
        "phone": "0722 207 002",
        "services": "Maize, sugarcane research, extension services"
    },
    {
        "name": "KALRO Kitale",
        "county": "trans nzoia",
        "town": "Kitale",
        "phone": "0722 207 003",
        "services": "Maize, potato research, extension services"
    },
]

def find_agrovet(county):
    """Find agrovets and KALRO centers in a given county."""
    county = county.lower().strip()
    agrovets = [a for a in AGROVETS if a["county"] == county]
    kalro = [k for k in KALRO_CENTERS if k["county"] == county]
    return agrovets, kalro

def format_agrovet_sms(county, language="en"):
    """Format agrovet info into an SMS-friendly string."""
    agrovets, kalro = find_agrovet(county)

    if not agrovets and not kalro:
        if language == "sw":
            return "Hakuna agrovet iliyopatikana katika kaunti yako. Wasiliana na ofisi ya kilimo ya kaunti yako."
        return "No agrovet found in your county. Contact your county agriculture office."

    lines = []
    if language == "sw":
        lines.append("Agrovet zilizo karibu nawe:")
    else:
        lines.append("Nearest agrovets to you:")

    for a in agrovets[:2]:
        lines.append(f"- {a['name']}, {a['town']}: {a['phone']}")

    if kalro:
        if language == "sw":
            lines.append("Kituo cha KALRO:")
        else:
            lines.append("KALRO center:")
        lines.append(f"- {kalro[0]['name']}: {kalro[0]['phone']}")

    return "\n".join(lines)