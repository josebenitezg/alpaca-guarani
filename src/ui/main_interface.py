import gradio as gr
from src.config.logging_config import setup_logging
from src.core.translation import OpenAITranslationService, NLLBTranslationService, GoogleTranslationService
from src.config.settings import TranslationModel, TRANSLATION_MODEL, TABLE_NAME
from src.core.database.supabase import get_supabase_client
from .dashboard import create_dashboard

logger = setup_logging()
supabase = get_supabase_client()

def create_ui(state):
    def get_translator():
        if TRANSLATION_MODEL == TranslationModel.OPENAI:
            return OpenAITranslationService()
        elif TRANSLATION_MODEL == TranslationModel.GOOGLE:
            return GoogleTranslationService()
        return NLLBTranslationService()

    def save_translation(instruction, input_text, output):
        if not state.current_item:
            return "No current item to save", {}, {}, {}, {}, {}, {}
        
        logger.info(f"Saving translation for item {state.current_item['id']}")
        supabase.table(TABLE_NAME).update({
            "translated_instruction": instruction,
            "translated_input": input_text,
            "translated_output": output,
            "translated": True
        }).eq("id", state.current_item['id']).execute()
        
        state.update_progress()
        
        # Get next item immediately after saving
        return load_next()

    def translate_and_update():
        if not state.current_item:
            return "No items left to translate"
        
        translator = get_translator()
        translated_instruction = translator.translate(state.current_item['original_instruction'])
        translated_input = translator.translate(state.current_item['original_input'])
        translated_output = translator.translate(state.current_item['original_output'])
        
        return {
            instruction_box: translated_instruction,
            input_box: translated_input,
            output_box: translated_output
        }

    with gr.Blocks() as app:
        gr.Markdown("# Alpaca Guarani - Translation Interface")
        
        with gr.Row():
            progress_box = gr.Textbox(value=state.get_progress(), label="Progress")
        
        with gr.Row():
            with gr.Column():
                original_instruction = gr.Textbox(label="Original Instruction")
                original_input = gr.Textbox(label="Original Input")
                original_output = gr.Textbox(label="Original Output")
            
            with gr.Column():
                instruction_box = gr.Textbox(label="Translated Instruction", lines=3, interactive=True)
                input_box = gr.Textbox(label="Translated Input", lines=3, interactive=True)
                output_box = gr.Textbox(label="Translated Output", lines=3, interactive=True)
        
        with gr.Row():
            translate_btn = gr.Button("Translate")
            next_btn = gr.Button("Next")
            save_btn = gr.Button("Save")
        
        # Add dashboard tab
        with gr.Tab("Dashboard"):
            create_dashboard()
        
        def load_next():
            item = state.get_next_untranslated()
            if not item:
                return {
                    original_instruction: "",
                    original_input: "",
                    original_output: "",
                    instruction_box: "",
                    input_box: "",
                    output_box: "",
                    progress_box: state.get_progress()
                }
            
            return {
                original_instruction: item['original_instruction'],
                original_input: item['original_input'],
                original_output: item['original_output'],
                instruction_box: "",
                input_box: "",
                output_box: "",
                progress_box: state.get_progress()
            }
        
        translate_btn.click(
            translate_and_update,
            outputs=[instruction_box, input_box, output_box]
        )
        
        next_btn.click(
            load_next,
            outputs=[
                original_instruction, original_input, original_output,
                instruction_box, input_box, output_box, progress_box
            ]
        )
        
        app.load(load_next, outputs=[
            original_instruction, original_input, original_output,
            instruction_box, input_box, output_box, progress_box
        ])
        
        save_btn.click(
            save_translation,
            inputs=[instruction_box, input_box, output_box],
            outputs=[
                progress_box,
                original_instruction, original_input, original_output,
                instruction_box, input_box, output_box
            ]
        )
        
        return app 