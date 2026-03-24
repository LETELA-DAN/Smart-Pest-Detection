# app/data/diseases.py

DISEASES = [
    {
        "id": "tomat_late_blight",
        "name": "Tomato Late Blight (Baridi Kali)",
        "crops": ["tomato", "nyanya", "potato", "viazi"],
        "severity": "HIGH",
        # Keywords are used for the scoring logic
        "keywords": [
            "madoa", "meusi", "black", "spots", "brown", "dark", 
            "leaves", "majani", "shina", "stem", "rot", "oza",
            "baridi", "ukungu", "wet", "vlid"
        ],
        "symptoms_en": "Dark, water-soaked spots on leaves and stems. Rapid rotting in humid weather.",
        "symptoms_sw": "Madoa meusi au kahawia kwenye majani na shina. Kunauka kwa haraka wakati wa baridi.",
        "remedy_en": "Spray fungicides containing Mancozeb or Metalaxyl (e.g., Ridomil Gold). Space plants well.",
        "remedy_sw": "Nyunyizia dawa ya ukungu kama Mancozeb au Ridomil Gold. Punguza msongamano wa mimea.",
        "cause_en": "Fungal pathogen (Phytophthora infestans)",
        "cause_sw": "Fangasi unaosababishwa na unyevu mwingi"
    },
    {
        "id": "maize_lethal_necrosis",
        "name": "Maize Lethal Necrosis (MLN)",
        "crops": ["maize", "mahindi", "corn"],
        "severity": "HIGH",
        "keywords": [
            "funza", "yellow", "njano", "drying", "nyauka", 
            "kufa", "death", "stunted", "fupi", "kavu", "streak"
        ],
        "symptoms_en": "Yellowing of leaves from the edges, drying of the plant before maturity.",
        "symptoms_sw": "Majani kugeuka njano kuanzia kando, mmea kukauka kabla ya kukomaa.",
        "remedy_en": "Remove infected plants immediately. Rotate crops with non-cereals (beans).",
        "remedy_sw": "Ng'oa mimea iliyoathirika. Badilisha aina ya zao msimu ujao (panda maharagwe).",
        "cause_en": "Viral combination spread by thrips and aphids",
        "cause_sw": "Virusi vinavyoenezwa na wadudu wadogo"
    },
    {
        "id": "cabbage_black_rot",
        "name": "Cabbage Black Rot",
        "crops": ["cabbage", "sukuma", "kale", "kabichi"],
        "severity": "MEDIUM",
        "keywords": [
            "v-shape", "yellowing", "veins", "black", "harufu", 
            "smell", "oza", "root", "shina"
        ],
        "symptoms_en": "Yellow V-shaped lesions on leaf edges. Blackening of leaf veins.",
        "symptoms_sw": "Madoa ya njano yenye umbo la V kando ya majani. Mishipa ya majani kuwa nyeusi.",
        "remedy_en": "Use certified seeds. Avoid overhead irrigation. Copper-based sprays.",
        "remedy_sw": "Tumia mbegu zilizoidhinishwa. Epuka kumwagilia maji juu ya majani. Tumia dawa ya shaba.",
        "cause_en": "Bacterial infection (Xanthomonas)",
        "cause_sw": "Maambukizi ya bakteria"
    },
    {
        "id": "bean_rust",
        "name": "Bean Rust (Kutu ya Maharagwe)",
        "crops": ["beans", "maharagwe", "kunde"],
        "severity": "LOW",
        "keywords": [
            "kutu", "rust", "pustules", "red", "ekundu", 
            "brown", "powder", "unga", "vumbi"
        ],
        "symptoms_en": "Small, reddish-brown powdery spots (pustules) on the underside of leaves.",
        "symptoms_sw": "Madoa madogo ya rangi ya kahawia au nyekundu (kutu) chini ya majani.",
        "remedy_en": "Plant resistant varieties. Use sulfur-based fungicides.",
        "remedy_sw": "Panda mbegu zinazostahimili magonjwa. Tumia dawa za kuzuia ukungu (Sulfur).",
        "cause_en": "Fungus spread by wind",
        "cause_sw": "Fangasi anayeenezwa na upepo"
    }
]