from transformers import pipeline
import gradio as gr

# Cargar los modelos de traducción
model_es_en = pipeline("translation", model="Helsinki-NLP/opus-mt-es-en")
model_en_es = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es")

def translate_text(text, direction):
    if not text:
        return ""
    
    if direction == "Espanyol → Angles":
        result = model_es_en(text)
    elif direction == "Angles → Espanyol":
        result = model_en_es(text)
    
    return result[0]['translation_text']

def login(user, password):
    if(user == 'iabd' and password == 'iabd'):
        return True
    else:
        return False

with gr.Blocks(title="Traductor") as demo:
    gr.Markdown("# 🌍 Traductor Espanyol ↔ Angles")
    gr.LoginButton()
    with gr.Row():
        direction = gr.Dropdown(
            choices=["Espanyol → Angles", "Angles → Espanyol"],
            label="Idiomas a traduir",
            value="Espanyol → Angles"
        )
    
    with gr.Row():
        input_text = gr.Textbox(label="Texte a traduir")
        output_text = gr.Textbox(label="Traducció", interactive=False)
    
    btn = gr.Button("Traduir")
    
    btn.click(
        fn=translate_text,
        inputs=[input_text, direction],
        outputs=output_text
    )

if __name__ == "__main__":
    demo.launch()