import gradio as gr
import plotly.express as px
import pandas as pd
from src.core.database.operations import get_translation_progress, get_dashboard_data
from src.config.logging_config import setup_logging

logger = setup_logging()

def create_dashboard():
    def filter_dataframe(df, min_len, max_len):
        return df[df['original_instruction'].str.len().between(min_len, max_len)]
    
    def update_dashboard():
        translated, total = get_translation_progress()
        
        # Create statistics text
        stats_text = f"""
        Total Items: {total}
        Translated: {translated}
        Remaining: {total - translated}
        Progress: {(translated/total)*100:.2f}%
        """
        
        # Create visualization
        fig = px.pie(
            values=[translated, total-translated],
            names=['Translated', 'Remaining'],
            title='Translation Progress'
        )
        
        # Get data for table
        data = get_dashboard_data()  # You'll need to implement this function in database/operations.py
        df = pd.DataFrame(data)
        
        return stats_text, fig, df
    
    with gr.Row():
        stats = gr.Textbox(label="Statistics")
    
    with gr.Row():
        plot = gr.Plot(label="Visualization")
    
    with gr.Row():
        min_length = gr.Slider(minimum=0, maximum=1000, step=10, label="Min Instruction Length")
        max_length = gr.Slider(minimum=0, maximum=1000, step=10, value=1000, label="Max Instruction Length")
    
    with gr.Row():
        dataframe = gr.Dataframe(
            headers=["id", "original_instruction", "original_input", "original_output",
                     "translated_instruction", "translated_input", "translated_output"],
            datatype=["number", "str", "str", "str", "str", "str", "str"],
            col_count=(7, "fixed"),
        )
    
    refresh_button = gr.Button("Refresh Dashboard")
    
    refresh_button.click(
        update_dashboard,
        outputs=[stats, plot, dataframe]
    )
    
    min_length.change(filter_dataframe, inputs=[dataframe, min_length, max_length], outputs=[dataframe])
    max_length.change(filter_dataframe, inputs=[dataframe, min_length, max_length], outputs=[dataframe]) 