import os
import streamlit as st
import base64
from openai import OpenAI


# =========================================================
# FUNCIÓN PARA CONVERTIR LA IMAGEN
# =========================================================

def encode_image(image_file):
    return base64.b64encode(
        image_file.getvalue()
    ).decode("utf-8")


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Analizador de Fotos con IA",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# DISEÑO
# =========================================================

st.markdown("""
<style>

/* Fondo general */

.stApp {
    background-color: #101214;
}


/* Contenedor principal */

.block-container {
    max-width: 900px;
    padding-top: 35px;
    padding-bottom: 50px;
}


/* Título principal */

h1 {
    color: white !important;
    font-size: 38px !important;
    font-weight: 700 !important;
}

h2 {
    color: white !important;
}

h3 {
    color: white !important;
}


/* Texto general */

p {
    color: #d1d5db;
}


/* Tarjetas */

[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #1b1f24;
    border: 1px solid #30363d;
    border-radius: 16px;
}


/* Input de API */

.stTextInput input {
    background-color: #1b1f24 !important;
    color: white !important;
    border: 1px solid #4b6cb7 !important;
    border-radius: 10px !important;
}


/* Área de texto */

.stTextArea textarea {
    background-color: #1b1f24 !important;
    color: white !important;
    border: 1px solid #4b6cb7 !important;
    border-radius: 10px !important;
}

.stTextArea textarea::placeholder {
    color: #9ca3af !important;
}


/* Cargador */

[data-testid="stFileUploader"] {
    background-color: #1b1f24;
    border: 2px dashed #4b6cb7;
    border-radius: 15px;
    padding: 15px;
}

[data-testid="stFileUploader"] * {
    color: #e5e7eb !important;
}


/* Botón */

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #4b6cb7, #6a8dd8);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 13px;
    font-size: 17px;
    font-weight: bold;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #5b7bc5, #7898df);
}


/* Imagen */

[data-testid="stImage"] {
    border-radius: 15px;
}


/* Resultado */

.resultado {
    background-color: #1b1f24;
    border: 1px solid #30363d;
    border-top: 4px solid #6a8dd8;
    border-radius: 15px;
    padding: 25px;
    margin-top: 20px;
}


/* Alertas */

[data-testid="stAlert"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# ENCABEZADO
# =========================================================

st.markdown(
    "<h1 style='text-align:center;'>🤖 Analizador de Fotos con IA</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; font-size:18px;'>"
    "Sube una imagen y deja que la inteligencia artificial "
    "analice lo que aparece en ella."
    "</p>",
    unsafe_allow_html=True
)

st.markdown("---")


# =========================================================
# INFORMACIÓN
# =========================================================

info = st.container(border=True)

info.subheader("🔍 ¿Qué puedes analizar?")

info.write(
    "Carga una fotografía y obtén una descripción detallada "
    "de su contenido. También puedes agregar una pregunta "
    "específica o contexto para orientar el análisis."
)


# =========================================================
# API KEY
# =========================================================

st.subheader("🔐 Conexión con OpenAI")

ke = st.text_input(
    "Ingresa tu clave de OpenAI",
    type="password",
    placeholder="sk-..."
)

if ke:

    os.environ["OPENAI_API_KEY"] = ke

    st.success("Clave ingresada correctamente")


# =========================================================
# CLIENTE
# =========================================================

if ke:

    api_key = os.environ["OPENAI_API_KEY"]

    client = OpenAI(
        api_key=api_key
    )


# =========================================================
# CARGAR IMAGEN
# =========================================================

st.subheader("📸 Selecciona una fotografía")

uploaded_file = st.file_uploader(
    "Arrastra tu imagen aquí o selecciónala desde tu computador",
    type=["jpg", "png", "jpeg"]
)


# =========================================================
# MOSTRAR IMAGEN
# =========================================================

if uploaded_file:

    st.subheader("🖼️ Imagen seleccionada")

    st.image(
        uploaded_file,
        caption=uploaded_file.name,
        use_container_width=True
    )


# =========================================================
# PREGUNTA
# =========================================================

st.subheader("💬 Personaliza el análisis")

show_details = st.toggle(
    "Quiero hacer una pregunta específica sobre la imagen",
    value=False
)

additional_details = ""

if show_details:

    additional_details = st.text_area(
        "¿Qué quieres saber sobre la imagen?",
        placeholder=(
            "Ejemplo: ¿Qué objetos aparecen en la fotografía? "
            "¿Qué tipo de lugar es?"
        ),
        height=120
    )


# =========================================================
# BOTÓN
# =========================================================

st.markdown("---")

analyze_button = st.button(
    "🔎 Analizar imagen",
    type="primary"
)


# =========================================================
# ANÁLISIS
# =========================================================

if uploaded_file is not None and ke and analyze_button:

    with st.spinner(
        "🤖 La inteligencia artificial está analizando la imagen..."
    ):

        base64_image = encode_image(
            uploaded_file
        )

        prompt_text = (
            "Describe lo que ves en la imagen en español. "
            "Sé claro, detallado y objetivo. "
            "Menciona los elementos principales, personas, "
            "objetos, lugares, acciones y cualquier detalle "
            "visual relevante que puedas identificar."
        )

        if show_details and additional_details:

            prompt_text += (
                "\n\nPregunta específica del usuario:\n"
                + additional_details
            )


        messages = [
            {
                "role": "user",

                "content": [

                    {
                        "type": "text",
                        "text": prompt_text
                    },

                    {
                        "type": "image_url",

                        "image_url": {
                            "url": (
                                "data:image/jpeg;base64,"
                                + base64_image
                            )
                        }
                    }

                ]
            }
        ]


        try:

            full_response = ""

            message_placeholder = st.empty()


            for completion in client.chat.completions.create(

                model="gpt-4o",

                messages=messages,

                max_tokens=1200,

                stream=True

            ):

                if completion.choices[0].delta.content is not None:

                    full_response += (
                        completion.choices[0].delta.content
                    )

                    message_placeholder.markdown(
                        full_response + "▌"
                    )


            message_placeholder.empty()


            # =============================================
            # RESULTADO
            # =============================================

            st.subheader("🤖 Análisis de la imagen")

            resultado = st.container(border=True)

            resultado.write(
                full_response
            )


        except Exception as e:

            st.error(
                "Ocurrió un error al analizar la imagen: "
                + str(e)
            )


# =========================================================
# MENSAJES
# =========================================================

if analyze_button and not uploaded_file:

    st.warning(
        "📸 Primero debes cargar una imagen."
    )


if analyze_button and not ke:

    st.warning(
        "🔐 Primero debes ingresar tu clave de OpenAI."
    )
