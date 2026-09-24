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
# CONFIGURACIÓN DE LA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Analizador de Fotos con IA",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# ESTILOS
# =========================================================

st.markdown("""
<style>

/* FONDO GENERAL */

.stApp {
    background-color: #101214;
    color: white;
}


/* CONTENEDOR PRINCIPAL */

.main {
    padding-top: 20px;
}


/* ENCABEZADO */

.header {
    background: linear-gradient(
        135deg,
        #182848,
        #4b6cb7
    );

    padding: 35px 25px;
    border-radius: 20px;

    text-align: center;

    margin-bottom: 25px;

    box-shadow:
        0px 8px 25px rgba(0,0,0,0.35);
}

.header h1 {
    color: white !important;
    font-size: 38px;
    margin-bottom: 8px;
}

.header p {
    color: #e5e7eb !important;
    font-size: 17px;
    margin: 0;
}


/* TARJETAS */

.card {
    background-color: #1b1f24;

    padding: 24px;

    border-radius: 16px;

    margin-top: 20px;
    margin-bottom: 20px;

    border: 1px solid #30363d;

    box-shadow:
        0px 5px 18px rgba(0,0,0,0.25);
}

.card-title {
    color: #8ab4ff !important;

    font-size: 21px;

    font-weight: bold;

    margin-bottom: 10px;
}

.card-text {
    color: #d1d5db !important;

    font-size: 15px;

    line-height: 1.6;
}


/* CARGADOR DE IMAGEN */

[data-testid="stFileUploader"] {
    background-color: #1b1f24;

    border: 2px dashed #4b6cb7;

    border-radius: 15px;

    padding: 15px;

    margin-top: 10px;
}

[data-testid="stFileUploader"] * {
    color: #e5e7eb !important;
}


/* IMAGEN */

.image-container {
    background-color: #181b20;

    border-radius: 15px;

    padding: 15px;

    border: 1px solid #30363d;

    margin-top: 20px;
}


/* TEXT AREA */

.stTextArea textarea {
    background-color: #1b1f24 !important;

    color: white !important;

    border: 1px solid #4b6cb7 !important;

    border-radius: 10px;

    font-size: 15px;
}

.stTextArea textarea::placeholder {
    color: #9ca3af !important;
}


/* API KEY */

.stTextInput input {
    background-color: #1b1f24 !important;

    color: white !important;

    border: 1px solid #4b6cb7 !important;

    border-radius: 10px;
}

.stTextInput input::placeholder {
    color: #9ca3af !important;
}


/* BOTÓN */

.stButton > button {
    width: 100%;

    background: linear-gradient(
        135deg,
        #4b6cb7,
        #6a8dd8
    );

    color: white !important;

    border: none;

    border-radius: 12px;

    padding: 13px;

    font-size: 17px;

    font-weight: bold;

    box-shadow:
        0px 4px 12px rgba(75,108,183,0.35);

    transition: 0.2s;
}

.stButton > button:hover {
    background: linear-gradient(
        135deg,
        #5b7bc5,
        #7898df
    );

    transform: translateY(-1px);
}


/* RESULTADO */

.result-header {
    background: linear-gradient(
        135deg,
        #182848,
        #263b69
    );

    padding: 18px 22px;

    border-radius: 15px 15px 0px 0px;

    border-top: 4px solid #6a8dd8;
}

.result-header h3 {
    color: #ffffff !important;

    margin: 0;

    font-size: 21px;
}

.result-body {
    background-color: #1b1f24;

    padding: 25px;

    border-radius: 0px 0px 15px 15px;

    border: 1px solid #30363d;

    border-top: none;

    color: #f3f4f6 !important;

    font-size: 17px;

    line-height: 1.7;

    box-shadow:
        0px 5px 18px rgba(0,0,0,0.3);
}

.result-body p {
    color: #f3f4f6 !important;
}

.result-body strong {
    color: #8ab4ff !important;
}


/* TEXTO GENERAL */

.stApp p {
    color: #d1d5db;
}

.stApp label {
    color: #e5e7eb !important;
}


/* EXPANDER */

.streamlit-expanderHeader {
    background-color: #1b1f24 !important;

    color: white !important;

    border-radius: 10px;
}


/* MENSAJES */

div[data-testid="stAlert"] {
    border-radius: 10px;
}


/* SEPARADOR */

hr {
    border-color: #30363d;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# ENCABEZADO
# =========================================================

st.markdown("""
<div class="header">

    <h1>🤖 Analizador de Fotos con IA</h1>

    <p>
        Sube una imagen y deja que la inteligencia artificial
        analice lo que aparece en ella
    </p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# DESCRIPCIÓN
# =========================================================

st.markdown("""
<div class="card">

    <div class="card-title">
        🔍 ¿Qué puedes analizar?
    </div>

    <div class="card-text">
        Carga una fotografía y obtén una descripción detallada
        de su contenido. También puedes agregar una pregunta
        específica o contexto para orientar el análisis.
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# API KEY
# =========================================================

st.markdown("### 🔐 Conexión con OpenAI")

ke = st.text_input(
    "Ingresa tu clave de OpenAI",
    type="password",
    placeholder="sk-..."
)

if ke:

    os.environ["OPENAI_API_KEY"] = ke

    st.success("Clave ingresada correctamente")


# =========================================================
# CLIENTE OPENAI
# =========================================================

if ke:

    api_key = os.environ["OPENAI_API_KEY"]

    client = OpenAI(
        api_key=api_key
    )


# =========================================================
# CARGAR IMAGEN
# =========================================================

st.markdown("### 📸 Selecciona una fotografía")

uploaded_file = st.file_uploader(
    "Arrastra tu imagen aquí o selecciónala desde tu computador",
    type=["jpg", "png", "jpeg"]
)


# =========================================================
# MOSTRAR IMAGEN
# =========================================================

if uploaded_file:

    st.markdown("""
    <div class="card">

        <div class="card-title">
            🖼️ Imagen seleccionada
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.image(
        uploaded_file,
        caption=uploaded_file.name,
        use_container_width=True
    )


# =========================================================
# PREGUNTA ESPECÍFICA
# =========================================================

st.markdown("### 💬 Personaliza el análisis")

show_details = st.toggle(
    "Quiero hacer una pregunta específica sobre la imagen",
    value=False
)

additional_details = ""

if show_details:

    additional_details = st.text_area(
        "¿Qué quieres saber sobre la imagen?",
        placeholder="Ejemplo: ¿Qué objetos aparecen en la fotografía? ¿Qué tipo de lugar es?",
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

    with st.spinner("🤖 La inteligencia artificial está analizando la imagen..."):

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


            # =================================================
            # RESULTADO FINAL
            # =================================================

            st.markdown("""
            <div class="result-header">
                <h3>🤖 Análisis de la imagen</h3>
            </div>
            """, unsafe_allow_html=True)


            st.markdown(
                '<div class="result-body">' +
                full_response.replace("\n", "<br>") +
                '</div>',
                unsafe_allow_html=True
            )


        except Exception as e:

            st.error(
                "Ocurrió un error al analizar la imagen: "
                + str(e)
            )


# =========================================================
# MENSAJES DE AYUDA
# =========================================================

if analyze_button and not uploaded_file:

    st.warning(
        "📸 Primero debes cargar una imagen."
    )


if analyze_button and not ke:

    st.warning(
        "🔐 Primero debes ingresar tu clave de OpenAI."
    )
