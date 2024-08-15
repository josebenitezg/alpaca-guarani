from datasets import load_dataset
from config import get_logger, get_supabase
from config import TABLE_NAME

supabase = get_supabase()
logger = get_logger()

def populate_db_with_dataset():
    logger.info("Populating database with dataset")
    dataset = load_dataset('bertin-project/alpaca-spanish')
    
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

def update_translation(id, translated_instruction, translated_input, translated_output):
    logger.info(f"Updating translation for id: {id}")
    supabase.table(TABLE_NAME).update({
        "translated_instruction": translated_instruction,
        "translated_input": translated_input,
        "translated_output": translated_output,
        "translated": True
    }).eq("id", id).execute()
    logger.info(f"Translation updated for id: {id}")

def get_next_untranslated():
    logger.info("Fetching next untranslated item")
    response = supabase.table(TABLE_NAME).select("*").eq("translated", False).order("id").limit(1).execute()
    if response.data:
        item = response.data[0]
        logger.info(f"Next untranslated item fetched: id {item['id']}")
        return item
    else:
        logger.info("No untranslated items remaining")
        return None

def get_translation_progress():
    logger.info("Fetching translation progress")
    total = supabase.table(TABLE_NAME).select("id").execute()
    translated = supabase.table(TABLE_NAME).select("id").eq("translated", True).execute()
    total_count = len(total.data)
    translated_count = len(translated.data)
    logger.info(f"Progress: {translated_count}/{total_count}")
    return translated_count, total_count