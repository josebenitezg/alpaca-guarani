from config import get_translator, get_logger, TranslationModel, TRANSLATION_MODEL
from config import OPENAI_MODEL, OPENAI_SYSTEM_PROMPT
from openai import OpenAI
import os

logger = get_logger()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class TranslationService:
    @staticmethod
    def translate_nllb(text):
        if not text or text.strip() == "":
            logger.warning("Attempted to translate empty text")
            return ""
        translator = get_translator()
        logger.info(f"Translating text with NLLB: {text[:50]}...")
        translated = translator(text)[0]['translation_text']
        logger.info(f"Translation result: {translated[:50]}...")
        return translated

    @staticmethod
    def translate_openai(text):
        if not text or text.strip() == "":
            logger.warning("Attempted to translate empty text")
            return ""
        
        logger.info(f"Translating text with OpenAI: {text[:50]}...")
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": OPENAI_SYSTEM_PROMPT},
                {"role": "user", "content": f"Translate this Spanish text to Guarani: {text}"}
            ],
            model=OPENAI_MODEL,
            temperature=0.3
        )
        
        translated = response.choices[0].message.content.strip()
        logger.info(f"Translation result: {translated[:50]}...")
        return translated

def translate_text(text):
    translation_methods = {
        TranslationModel.NLLB: TranslationService.translate_nllb,
        TranslationModel.OPENAI: TranslationService.translate_openai
    }
    
    translate_method = translation_methods.get(TRANSLATION_MODEL)
    if not translate_method:
        raise ValueError(f"Unsupported translation model: {TRANSLATION_MODEL}")
    
    return translate_method(text)