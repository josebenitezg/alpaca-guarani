import gradio as gr
from config import init_all, get_logger
from database import populate_db_with_dataset
from state import TranslationState
from ui import create_ui

def main():
    init_all()  # This now includes setting up logging
    logger = get_logger()
    logger.info("Starting Alpaca Translator application")
    populate_db_with_dataset()
    state = TranslationState()
    app = create_ui(state)
    logger.info("Launching Gradio interface")
    app.launch()

if __name__ == "__main__":
    main()