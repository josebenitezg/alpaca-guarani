import os
import torch
import logging
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from supabase import create_client, Client

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

# Logging Configuration
LOG_DIR = "logs"
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Model and Translator Instances
model_nllb = None
tokenizer_nllb = None
translator = None
supabase: Client = None
logger = None

def setup_logging():
    global logger
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    log_filename = f"{LOG_DIR}/app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger('AlpacaTranslator')
    logger.info("Logging initialized")

def init_model():
    global model_nllb, tokenizer_nllb
    model_nllb = AutoModelForSeq2SeqLM.from_pretrained(CHECKPOINT, device_map=DEVICE)
    tokenizer_nllb = AutoTokenizer.from_pretrained(CHECKPOINT, device_map=DEVICE)
    logger.info("Model and tokenizer initialized")

def init_translator():
    global translator, model_nllb, tokenizer_nllb
    if model_nllb is None or tokenizer_nllb is None:
        init_model()
    translator = pipeline("translation", model=model_nllb, tokenizer=tokenizer_nllb,
                          src_lang=SOURCE_LANG, tgt_lang=TARGET_LANG, max_length=5000)
    logger.info("Translator initialized")

def get_translator():
    global translator
    if translator is None:
        init_translator()
    return translator

def init_supabase():
    global supabase
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Supabase URL or key not found in environment variables")
        raise ValueError("Supabase URL and key must be set as environment variables")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client created")

def get_supabase():
    global supabase
    if supabase is None:
        init_supabase()
    return supabase

# Initialize all components
def init_all():
    setup_logging()
    init_model()
    init_translator()
    init_supabase()
    logger.info("All components initialized")

# Getter for logger
def get_logger():
    global logger
    if logger is None:
        setup_logging()
    return logger