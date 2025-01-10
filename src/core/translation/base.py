from abc import ABC, abstractmethod

class TranslationService(ABC):
    @abstractmethod
    def translate(self, text: str) -> str:
        """Translate the given text to the target language"""
        pass 