from datasets import load_dataset
from src.config.logging_config import setup_logging
from src.config.settings import TABLE_NAME, HF_DATASET_PATH
from .supabase import get_supabase_client

logger = setup_logging()
supabase = get_supabase_client()

def get_next_untranslated():
    response = supabase.table(TABLE_NAME)\
        .select("*")\
        .eq("translated", False)\
        .limit(1)\
        .execute()
    
    return response.data[0] if response.data else None

def get_translation_progress():
    total = supabase.table(TABLE_NAME).select("id", count="exact").execute()
    translated = supabase.table(TABLE_NAME)\
        .select("id", count="exact")\
        .eq("translated", True)\
        .execute()
    
    return translated.count, total.count

def populate_db_with_dataset():
    logger.info("Populating database with dataset")
    dataset = load_dataset(HF_DATASET_PATH)
    
    # Check if the table is empty
    response = supabase.table(TABLE_NAME).select("id").limit(1).execute()
    if not response.data:
        logger.info("Database is empty. Starting population...")
        for idx, item in enumerate(dataset['train']):
            supabase.table(TABLE_NAME).insert({
                "id": idx,
                "original_instruction": item['instruction'],
                "original_input": item['input'],
                "original_output": item['output'],
                "translated": False
            }).execute()
            if idx % 1000 == 0:
                logger.info(f"Populated {idx} items")
        logger.info("Database population completed")
    else:
        logger.info("Database already populated. Skipping population step.") 

def get_dashboard_data():
    """Get all data for dashboard display"""
    response = supabase.table(TABLE_NAME)\
        .select("*")\
        .execute()
    return response.data 