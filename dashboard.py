import gradio as gr
import sqlite3
import pandas as pd
import plotly.express as px

DB_NAME = "alpaca_translations.db"

def load_translated_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM translations WHERE translated = 1", conn)
    conn.close()
    return df

def create_dashboard():
    df = load_translated_data()
    
    # Basic statistics
    total_translations = len(df)
    avg_instruction_length = df['translated_instruction'].str.len().mean()
    avg_input_length = df['translated_input'].str.len().mean()
    avg_output_length = df['translated_output'].str.len().mean()
    
    # Create a bar chart of translation lengths
    fig = px.bar(
        x=['Instruction', 'Input', 'Output'],
        y=[avg_instruction_length, avg_input_length, avg_output_length],
        title="Average Length of Translated Text"
    )
    
    stats = (f"Total Translations: {total_translations}\n"
             f"Avg. Instruction Length: {avg_instruction_length:.2f}\n"
             f"Avg. Input Length: {avg_input_length:.2f}\n"
             f"Avg. Output Length: {avg_output_length:.2f}")
    
    return stats, fig, df

def filter_dataframe(df, min_length, max_length):
    return df[(df['translated_instruction'].str.len() >= min_length) & 
              (df['translated_instruction'].str.len() <= max_length)]

with gr.Blocks() as app:
    gr.Markdown("# Alpaca Guarani - Translation Dashboard")
    
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
    
    def update_dashboard():
        stats_text, fig, df = create_dashboard()
        return stats_text, fig, df, df
    
    refresh_button.click(
        update_dashboard,
        outputs=[stats, plot, dataframe, dataframe]  # dataframe is output twice: once for display, once for internal state
    )
    
    min_length.change(filter_dataframe, inputs=[dataframe, min_length, max_length], outputs=[dataframe])
    max_length.change(filter_dataframe, inputs=[dataframe, min_length, max_length], outputs=[dataframe])
    
    app.load(update_dashboard, outputs=[stats, plot, dataframe, dataframe])

if __name__ == "__main__":
    app.launch()