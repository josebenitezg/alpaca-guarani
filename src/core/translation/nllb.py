from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from src.config.settings import CHECKPOINT, DEVICE, SOURCE_LANG, TARGET_LANG
from src.config.logging_config import setup_logging
from .base import TranslationService

logger = setup_logging()

class NLLBTranslationService(TranslationService):
    def __init__(self):
        logger.info("Initializing NLLB Translation Service")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(CHECKPOINT, device_map=DEVICE)
        self.tokenizer = AutoTokenizer.from_pretrained(CHECKPOINT, device_map=DEVICE)
        self.translator = pipeline(
            "translation",
            model=self.model,
            tokenizer=self.tokenizer,
            src_lang=SOURCE_LANG,
            tgt_lang=TARGET_LANG,
            max_length=5000
        )

    def translate(self, text: str) -> str:
        if not text or text.strip() == "":
            logger.warning("Attempted to translate empty text")
            return ""
        
        logger.info(f"Translating text with NLLB: {text[:50]}...")
        translated = self.translator(text)[0]['translation_text']
        logger.info(f"Translation result: {translated[:50]}...")
        return translated 