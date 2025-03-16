from transformers import pipeline
import gradio as gr

# Cargar los modelos de traducción
model_es_en = pipeline("translation", model="Helsinki-NLP/opus-mt-es-en")
model_en_es = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es")

# Función de traducción
def translate_text(text, direction):
    if not text:
        return ""
    
    if direction == "Espanyol → Angles":
        result = model_es_en(text)
    elif direction == "Angles → Espanyol":
        result = model_en_es(text)
    
    return result[0]['translation_text']

# Función de autenticación
def login(user, password):
    if user == 'iabd' and password == 'iabd':
        return True  # Autenticación exitosa
    return False  # Autenticación fallida

# Crear la aplicación con Gradio
with gr.Blocks(title="Traductor") as demo:
    autenticat = gr.State(False)  # Estado para almacenar si el usuario está autenticado

    gr.Markdown("# 🌍 Traductor Espanyol ↔ Angles")

    # Sección de Login
    with gr.Row() as login_ui:
        user_input = gr.Textbox(label="User")
        password_input = gr.Textbox(label="Contrasenya", type="password")
        login_btn = gr.Button("Login")
        error_message = gr.Markdown("", visible=False)  # Mensaje de error oculto al inicio

    # Sección del Traductor (Oculta al inicio)
    with gr.Column(visible=False) as traductor_ui:
        direction = gr.Dropdown(
            choices=["Espanyol → Angles", "Angles → Espanyol"],
            label="Idiomas a traduir",
            value="Espanyol → Angles"
        )
        input_text = gr.Textbox(label="Texte a traduir")
        output_text = gr.Textbox(label="Traducció", interactive=False)
        translate_btn = gr.Button("Traduir")

    # Función que maneja el login
    def handle_login(user, password):
        is_authenticated = login(user, password)  # Verificar credenciales
        
        if is_authenticated:
            return (
                True,  # Actualiza el estado autenticat
                gr.update(visible=False),  # Ocultar la UI de login
                gr.update(visible=True),  # Mostrar la UI del traductor
                gr.update(value="", visible=False)  # Ocultar mensaje de error
            )
        else:
            return (
                False,
                gr.update(visible=True),  # Mantener visible la UI de login
                gr.update(visible=False),  # Mantener oculta la UI del traductor
                gr.update(value="❌ Usuario o contraseña incorrectos", visible=True)  # Mostrar mensaje de error
            )

    # Conectar el botón de login con la función handle_login
    login_btn.click(
        handle_login,
        inputs=[user_input, password_input],
        outputs=[autenticat, login_ui, traductor_ui, error_message]
    )

    # Conectar el botón de traducir con la función de traducción
    translate_btn.click(translate_text, inputs=[input_text, direction], outputs=output_text)

if __name__ == "__main__":
    demo.launch()
