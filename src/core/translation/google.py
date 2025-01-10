from google.cloud import translate_v2 as translate
import os
from src.config.logging_config import setup_logging
from src.config.settings import GOOGLE_CREDENTIALS_PATH
from .base import TranslationService

logger = setup_logging()

class GoogleTranslationService(TranslationService):
    def __init__(self):
        logger.info("Initializing Google Translation Service")
        if GOOGLE_CREDENTIALS_PATH:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_CREDENTIALS_PATH
        else:
            logger.warning("GOOGLE_CREDENTIALS_PATH not set!")
        self.client = translate.Client()

    def translate(self, text: str) -> str:
        if not text or text.strip() == "":
            logger.warning("Attempted to translate empty text")
            return ""
        
        logger.info(f"Translating text with Google Translate: {text[:50]}...")
        
        result = self.client.translate(
            text,
            target_language='gn'  # Guarani language code
        )
        
        translated = result['translatedText']
        logger.info(f"Translation result: {translated[:50]}...")
        return translated 