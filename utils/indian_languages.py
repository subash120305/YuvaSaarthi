"""
Supported Indian Languages Configuration
All 22 Official Languages of India + English
"""

# All supported Indian languages
SUPPORTED_INDIAN_LANGUAGES = {
    # English
    "en": {
        "name": "English",
        "native_name": "English",
        "flag": "🇬🇧",
        "google_code": "en"
    },
    
    # Indo-Aryan Languages
    "hi": {
        "name": "Hindi",
        "native_name": "हिंदी",
        "flag": "🇮🇳",
        "google_code": "hi"
    },
    "bn": {
        "name": "Bengali",
        "native_name": "বাংলা",
        "flag": "🇮🇳",
        "google_code": "bn"
    },
    "mr": {
        "name": "Marathi",
        "native_name": "मराठी",
        "flag": "🇮🇳",
        "google_code": "mr"
    },
    "gu": {
        "name": "Gujarati",
        "native_name": "ગુજરાતી",
        "flag": "🇮🇳",
        "google_code": "gu"
    },
    "or": {
        "name": "Odia",
        "native_name": "ଓଡ଼ିଆ",
        "flag": "🇮🇳",
        "google_code": "or"
    },
    "pa": {
        "name": "Punjabi",
        "native_name": "ਪੰਜਾਬੀ",
        "flag": "🇮🇳",
        "google_code": "pa"
    },
    "as": {
        "name": "Assamese",
        "native_name": "অসমীয়া",
        "flag": "🇮🇳",
        "google_code": "as"
    },
    "ur": {
        "name": "Urdu",
        "native_name": "اردو",
        "flag": "🇮🇳",
        "google_code": "ur"
    },
    "ks": {
        "name": "Kashmiri",
        "native_name": "कॉशुर / کٲشُر",
        "flag": "🇮🇳",
        "google_code": "ks"
    },
    "sd": {
        "name": "Sindhi",
        "native_name": "سنڌي / सिन्धी",
        "flag": "🇮🇳",
        "google_code": "sd"
    },
    "sa": {
        "name": "Sanskrit",
        "native_name": "संस्कृतम्",
        "flag": "🇮🇳",
        "google_code": "sa"
    },
    "ne": {
        "name": "Nepali",
        "native_name": "नेपाली",
        "flag": "🇮🇳",
        "google_code": "ne"
    },
    "mai": {
        "name": "Maithili",
        "native_name": "मैथिली",
        "flag": "🇮🇳",
        "google_code": "hi"  # Fallback to Hindi
    },
    "kok": {
        "name": "Konkani",
        "native_name": "कोंकणी",
        "flag": "🇮🇳",
        "google_code": "hi"  # Fallback to Hindi
    },
    "mni": {
        "name": "Manipuri",
        "native_name": "মৈতৈলোন্",
        "flag": "🇮🇳",
        "google_code": "hi"  # Fallback to Hindi
    },
    "doi": {
        "name": "Dogri",
        "native_name": "डोगरी",
        "flag": "🇮🇳",
        "google_code": "hi"  # Fallback to Hindi
    },
    "sat": {
        "name": "Santali",
        "native_name": "ᱥᱟᱱᱛᱟᱲᱤ",
        "flag": "🇮🇳",
        "google_code": "hi"  # Fallback to Hindi
    },
    "bo": {
        "name": "Bodo",
        "native_name": "बड़ो",
        "flag": "🇮🇳",
        "google_code": "hi"  # Fallback to Hindi
    },
    
    # Dravidian Languages
    "te": {
        "name": "Telugu",
        "native_name": "తెలుగు",
        "flag": "🇮🇳",
        "google_code": "te"
    },
    "ta": {
        "name": "Tamil",
        "native_name": "தமிழ்",
        "flag": "🇮🇳",
        "google_code": "ta"
    },
    "kn": {
        "name": "Kannada",
        "native_name": "ಕನ್ನಡ",
        "flag": "🇮🇳",
        "google_code": "kn"
    },
    "ml": {
        "name": "Malayalam",
        "native_name": "മലയാളം",
        "flag": "🇮🇳",
        "google_code": "ml"
    },
}


def get_language_display_name(lang_code: str) -> str:
    """Get display name for language selector"""
    if lang_code not in SUPPORTED_INDIAN_LANGUAGES:
        return lang_code.upper()
    
    lang = SUPPORTED_INDIAN_LANGUAGES[lang_code]
    return f"{lang['flag']} {lang['name']} ({lang['native_name']})"


def get_language_name(lang_code: str) -> str:
    """Get simple language name"""
    if lang_code not in SUPPORTED_INDIAN_LANGUAGES:
        return lang_code.upper()
    return SUPPORTED_INDIAN_LANGUAGES[lang_code]['name']


def get_google_translate_code(lang_code: str) -> str:
    """Get Google Translate language code"""
    if lang_code not in SUPPORTED_INDIAN_LANGUAGES:
        return "en"
    return SUPPORTED_INDIAN_LANGUAGES[lang_code]['google_code']


def get_popular_languages() -> list:
    """Get most commonly used languages for quick access"""
    return ["hi", "en", "bn", "te", "mr", "ta", "gu", "kn", "ml", "or", "pa"]


def get_all_language_codes() -> list:
    """Get list of all supported language codes"""
    return list(SUPPORTED_INDIAN_LANGUAGES.keys())


# Sample queries in different languages
SAMPLE_QUERIES = {
    "en": [
        "What are the JEE exam dates for 2026?",
        "Tell me about NEET eligibility",
        "How to apply for scholarships?",
        "Explain Pythagoras theorem"
    ],
    "hi": [
        "JEE 2026 की परीक्षा कब है?",
        "NEET की पात्रता के बारे में बताएं",
        "छात्रवृत्ति के लिए कैसे आवेदन करें?",
        "पाइथागोरस प्रमेय समझाइए"
    ],
    "bn": [
        "২০২৬ সালে JEE পরীক্ষার তারিখ কী?",
        "NEET যোগ্যতা সম্পর্কে বলুন",
        "বৃত্তির জন্য কীভাবে আবেদন করবেন?",
        "পিথাগোরাসের উপপাদ্য ব্যাখ্যা করুন"
    ],
    "te": [
        "2026 JEE పరీక్ష తేదీలు ఏమిటి?",
        "NEET అర్హత గురించి చెప్పండి",
        "స్కాలర్‌షిప్‌ల కోసం ఎలా దరఖాస్తు చేయాలి?",
        "పైథాగరస్ సిద్ధాంతాన్ని వివరించండి"
    ],
    "mr": [
        "2026 साठी JEE परीक्षेच्या तारखा काय आहेत?",
        "NEET पात्रतेबद्दल सांगा",
        "शिष्यवृत्तीसाठी अर्ज कसा करावा?",
        "पायथागोरसचे प्रमेय समजावून सांगा"
    ],
    "ta": [
        "2026 JEE தேர்வு தேதிகள் என்ன?",
        "NEET தகுதி பற்றி சொல்லுங்கள்",
        "உதவித்தொகைக்கு எப்படி விண்ணப்பிப்பது?",
        "பித்தகோரஸ் தேற்றத்தை விளக்குங்கள்"
    ],
    "gu": [
        "2026 માટે JEE પરીક્ષાની તારીખો શું છે?",
        "NEET લાયકાત વિશે જણાવો",
        "શિષ્યવૃત્તિ માટે કેવી રીતે અરજી કરવી?",
        "પાયથાગોરસ પ્રમેય સમજાવો"
    ],
    "kn": [
        "2026 ರ JEE ಪರೀಕ್ಷಾ ದಿನಾಂಕಗಳು ಯಾವುವು?",
        "NEET ಅರ್ಹತೆ ಬಗ್ಗೆ ಹೇಳಿ",
        "ವಿದ್ಯಾರ್ಥಿವೇತನಕ್ಕೆ ಹೇಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸುವುದು?",
        "ಪೈಥಾಗೋರಸ್ ಪ್ರಮೇಯವನ್ನು ವಿವರಿಸಿ"
    ],
    "ml": [
        "2026-ലെ JEE പരീക്ഷാ തീയതികൾ എന്തൊക്കെയാണ്?",
        "NEET യോഗ്യതയെക്കുറിച്ച് പറയുക",
        "സ്കോളർഷിപ്പിനായി എങ്ങനെ അപേക്ഷിക്കാം?",
        "പൈതഗോറസ് സിദ്ധാന്തം വിശദീകരിക്കുക"
    ],
    "pa": [
        "2026 ਲਈ JEE ਪ੍ਰੀਖਿਆ ਦੀਆਂ ਤਾਰੀਖਾਂ ਕੀ ਹਨ?",
        "NEET ਯੋਗਤਾ ਬਾਰੇ ਦੱਸੋ",
        "ਸਕਾਲਰਸ਼ਿਪ ਲਈ ਕਿਵੇਂ ਅਰਜ਼ੀ ਦੇਣੀ ਹੈ?",
        "ਪਾਇਥਾਗੋਰਸ ਥਿਊਰਮ ਸਮਝਾਓ"
    ],
    "or": [
        "2026 ପାଇଁ JEE ପରୀକ୍ଷା ତାରିଖ କ'ଣ?",
        "NEET ଯୋଗ୍ୟତା ବିଷୟରେ କୁହନ୍ତୁ",
        "ଛାତ୍ରବୃତ୍ତି ପାଇଁ କିପରି ଆବେଦନ କରିବେ?",
        "ପାଇଥାଗୋରସ୍ ଥିଓରେମ୍ ବୁଝାନ୍ତୁ"
    ]
}


def get_sample_queries(lang_code: str) -> list:
    """Get sample queries for a language"""
    return SAMPLE_QUERIES.get(lang_code, SAMPLE_QUERIES["en"])
