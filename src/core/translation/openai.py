from openai import OpenAI
from src.config.settings import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_SYSTEM_PROMPT
from src.config.logging_config import setup_logging
from .base import TranslationService

logger = setup_logging()

class OpenAITranslationService(TranslationService):
    def __init__(self):
        logger.info("Initializing OpenAI Translation Service")
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def translate(self, text: str) -> str:
        if not text or text.strip() == "":
            logger.warning("Attempted to translate empty text")
            return ""
        
        logger.info(f"Translating text with OpenAI: {text[:50]}...")
        
        response = self.client.chat.completions.create(
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