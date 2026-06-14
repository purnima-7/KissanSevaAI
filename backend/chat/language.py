from langdetect import detect, LangDetectException

def detect_language(text: str) -> str:
    """
    Detects language of input text.
    Returns ISO code like: en, hi, gu, mr, etc.
    Defaults to English if detection fails.
    """
    try:
        lang = detect(text)
        return lang
    except LangDetectException:
        return "en"
