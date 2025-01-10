from src.config.logging_config import setup_logging
from src.core.database.operations import get_next_untranslated, get_translation_progress

logger = setup_logging()

class TranslationState:
    def __init__(self):
        logger.info("Initializing TranslationState")
        self.current_item = None
        self.update_progress()

    def get_next_untranslated(self):
        logger.info("Getting next untranslated item")
        self.current_item = get_next_untranslated()
        self.update_progress()
        return self.current_item

    def update_progress(self):
        logger.info("Updating progress")
        self.translated, self.total = get_translation_progress()

    def get_progress(self):
        progress = f"Progress: {self.translated}/{self.total}"
        logger.info(f"Current progress: {progress}")
        return progress 