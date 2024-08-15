import gradio as gr
from translation import translate_text
from database import update_translation
from config import get_logger

logger = get_logger()

def create_ui(state):
    def update_and_next(translated_instruction, translated_input, translated_output):
        logger.info("Saving current translation and moving to next")
        if state.current_item:
            update_translation(
                state.current_item['id'],
                translated_instruction,
                translated_input,
                translated_output
            )
        return get_next_item()

    def get_next_item():
        logger.info("Getting next item for translation")
        item = state.get_next_untranslated()
        if item:
            instruction = item['original_instruction']
            input_text = item['original_input']
            output = item['original_output']
            
            logger.info(f"Translating item id: {item['id']}")
            translated_instruction = translate_text(instruction)
            translated_input = translate_text(input_text)
            translated_output = translate_text(output)
            
            progress = state.get_progress()
            return instruction, input_text, output, translated_instruction, translated_input, translated_output, progress
        else:
            logger.info("All items translated")
            return "All items translated!", "", "", "", "", "", "Translation complete!"

    logger.info("Creating Gradio interface")
    with gr.Blocks() as app:
        gr.Markdown("# Alpaca Guarani - Curation Tool")
        
        with gr.Row():
            progress = gr.Textbox(label="Progress")
        
        with gr.Row():
            with gr.Column():
                original_instruction = gr.Textbox(label="Original Instruction")
                original_input = gr.Textbox(label="Original Input")
                original_output = gr.Textbox(label="Original Output")
            
            with gr.Column():
                translated_instruction = gr.Textbox(label="Translated Instruction")
                translated_input = gr.Textbox(label="Translated Input")
                translated_output = gr.Textbox(label="Translated Output")
        
        next_button = gr.Button("Save and Next")
        
        next_button.click(
            update_and_next,
            inputs=[translated_instruction, translated_input, translated_output],
            outputs=[original_instruction, original_input, original_output, 
                     translated_instruction, translated_input, translated_output, progress]
        )
        
        app.load(get_next_item, outputs=[original_instruction, original_input, original_output, 
                                         translated_instruction, translated_input, translated_output, progress])

    logger.info("Gradio interface created")
    return app