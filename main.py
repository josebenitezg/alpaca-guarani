from src.config.logging_config import setup_logging
from src.core.database.operations import populate_db_with_dataset
from src.utils.state import TranslationState
from src.ui.main_interface import create_ui

def main():
    logger = setup_logging()
    logger.info("Starting Alpaca Translator application")
    
    populate_db_with_dataset()
    state = TranslationState()
    app = create_ui(state)
    
    logger.info("Launching Gradio interface")
    app.launch()

if __name__ == "__main__":
    main()