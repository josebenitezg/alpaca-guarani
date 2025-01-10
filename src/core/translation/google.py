from google.cloud import translate_v2 as translate
import json
from src.config.logging_config import setup_logging
from src.config.settings import get_google_credentials_json
from .base import TranslationService
import tempfile
import os

logger = setup_logging()

class GoogleTranslationService(TranslationService):
    def __init__(self):
        logger.info("Initializing Google Translation Service")
        
        # Create temporary credentials file
        credentials_json = get_google_credentials_json()
        
        # Create a temporary file to store credentials
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            temp_file.write(credentials_json)
            temp_credentials_path = temp_file.name
        
        try:
            # Set temporary credentials file path
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_credentials_path
            self.client = translate.Client()
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_credentials_path)
            except Exception as e:
                logger.warning(f"Failed to delete temporary credentials file: {e}")

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