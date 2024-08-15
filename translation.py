from config import get_translator
from config import get_logger

logger = get_logger()

def translate_text(text):
    if not text or text.strip() == "":
        logger.warning("Attempted to translate empty text")
        return ""
    translator = get_translator()
    logger.info(f"Translating text: {text[:50]}...")  # Log first 50 characters
    translated = translator(text)[0]['translation_text']
    logger.info(f"Translation result: {translated[:50]}...")  # Log first 50 characters of result
    return translated