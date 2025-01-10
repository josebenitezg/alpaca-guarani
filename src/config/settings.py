import os
import torch
from enum import Enum
import json
import base64

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

# Google Cloud Configuration
GOOGLE_CREDENTIALS = {
    "type": os.environ.get("GOOGLE_CREDENTIALS_TYPE", "service_account"),
    "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
    "private_key_id": os.environ.get("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": os.environ.get("GOOGLE_PRIVATE_KEY", "").replace("\\n", "\n"),
    "client_email": os.environ.get("GOOGLE_CLIENT_EMAIL"),
    "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
    "auth_uri": os.environ.get("GOOGLE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
    "token_uri": os.environ.get("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
    "auth_provider_x509_cert_url": os.environ.get("GOOGLE_AUTH_PROVIDER_X509_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
    "client_x509_cert_url": os.environ.get("GOOGLE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.environ.get("GOOGLE_UNIVERSE_DOMAIN", "googleapis.com")
}

def get_google_credentials_json():
    """Convert credentials dict to JSON string"""
    return json.dumps(GOOGLE_CREDENTIALS) 