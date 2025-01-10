import os
import torch
from enum import Enum

class TranslationModel(Enum):
    NLLB = "nllb"
    OPENAI = "openai"
    GOOGLE = "google"

# Device Configuration
DEVICE = 'mps' if torch.backends.mps.is_available() else 'cuda' if torch.cuda.is_available() else 'cpu'

# Model Configuration
CHECKPOINT = "facebook/nllb-200-distilled-600M"
SOURCE_LANG = "esp_Latn"
TARGET_LANG = "grn_Latn"

# Database Configuration
DB_NAME = "alpaca_translations.db"
HF_DATASET_PATH = "bertin-project/alpaca-spanish"
TABLE_NAME = "alpaca-guarani"

# Supabase Configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# OpenAI Configuration
TRANSLATION_MODEL = TranslationModel(os.environ.get("TRANSLATION_MODEL", "google"))
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"
OPENAI_SYSTEM_PROMPT = """You are a professional translator specialized in Spanish to Guarani translations. 
Translate the given text maintaining the original meaning and cultural context.""" 

# Add Google Translate Configuration
GOOGLE_CREDENTIALS_PATH = os.environ.get("GOOGLE_CREDENTIALS_PATH") 