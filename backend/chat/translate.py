import os
from dotenv import load_dotenv
from groq import Groq

# ✅ load environment variables FIRST
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("❌ GROQ_API_KEY not found in environment")

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "llama-3.3-70b-versatile"

# Extended Language code to full name mapping
LANGUAGE_MAP = {
    "hi": "Hindi",
    "gu": "Gujarati", 
    "mr": "Marathi",
    "en": "English",
    "pa": "Punjabi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "or": "Odia",
    "as": "Assamese",
    "ur": "Urdu"
}


def translate_text(text: str, target_language: str) -> str:
    """
    Translates given text into target language.
    
    Supports: Hindi, Gujarati, Marathi, Punjabi, Bengali, Tamil, 
              Telugu, Kannada, Malayalam, Odia, Assamese, Urdu, English
    
    Args:
        text: Text to translate
        target_language: ISO language code (e.g., 'en', 'hi', 'pa', 'bn', 'ta') 
                        or full language name
    
    Returns:
        Translated text
    """
    if not text or not text.strip():
        return text
    
    # Convert language code to full name if needed
    if target_language in LANGUAGE_MAP:
        target_lang_name = LANGUAGE_MAP[target_language]
    else:
        target_lang_name = target_language

    # Build translation prompt based on target language
    if target_language == "en" or target_lang_name.lower() == "english":
        direction = "to English"
    else:
        direction = f"to {target_lang_name}"

    prompt = f"""You are a professional translator specializing in agricultural content.

Translate the following text {direction}.

CRITICAL RULES:
1. Translate the language completely
2. Keep all technical terms (pesticide names, chemical names, crop names, disease names) in their original English form - DO NOT translate them
3. Preserve all formatting (bullets, numbers, line breaks)
4. Do NOT add explanations or extra text
5. Return ONLY the translated text, nothing else

Text to translate:
{text}

Translated text:"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=2000
        )

        if response and response.choices:
            translated = response.choices[0].message.content.strip()
            return translated

    except Exception as e:
        print(f"Translation Error: {e}")

    # Fallback: return original text
    return text