import os
import re
import streamlit as st
from pydub import AudioSegment
from dotenv import load_dotenv
import google.generativeai as genai
import wave
import json
from vosk import Model, KaldiRecognizer

# ======================================
# CONFIGURAÇÃO DA INTERFACE
# ======================================
st.set_page_config(
    page_title="AudioTranscript - Transcrição Inteligente",
    page_icon="🎙️",
    layout="centered"
)

# CSS personalizado
st.markdown("""
<style>
    :root {
        --primary: #2563EB;
        --primary-dark: #1E40AF;
        --secondary: #7C3AED;
        --dark: #0F172A;
        --darker: #020617;
        --light: #F8FAFC;
        --accent: #00D4FF;
    }
    
    .stApp {
        background: linear-gradient(152deg, var(--darker) 0%, var(--dark) 100%);
        color: var(--light);
    }
    
    h1, h2, h3 {
        color: var(--light) !important;
    }
    
    h1 {
        background: linear-gradient(90deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4) !important;
    }
    
    audio {
        width: 100% !important;
        border-radius: 12px !important;
        filter: sepia(20%) saturate(120%) hue-rotate(190deg);
    }
</style>
""", unsafe_allow_html=True)

# ======================================
# FUNCIONALIDADES PRINCIPAIS
# ======================================

def transcribe_audio_offline(audio_path):
    if not os.path.exists("model"):
        return "❌ Modelo Vosk não encontrado. Coloque a pasta 'model' no diretório do projeto."

    wf = wave.open(audio_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() > 48000:
        return "❌ O áudio deve estar em mono, 16-bit e até 48kHz."

    model = Model("model")
    rec = KaldiRecognizer(model, wf.getframerate())

    transcription = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            transcription += result.get("text", "") + " "

    result = json.loads(rec.FinalResult())
    transcription += result.get("text", "")
    return transcription.strip().capitalize()

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def limpar_texto(text):
    return re.sub(r"[^\x00-\x7F]+", "", text)

def translate_text_gemini(text, target_language):
    text = limpar_texto(text)
    if not text.strip():
        return "Texto para tradução está vazio."

    prompt = f"Traduza o seguinte texto para {target_language} de forma natural e precisa:\n\n{text}"

    try:
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash",
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                top_p=1,
                top_k=40,
                max_output_tokens=1024
            ),
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error("❌ Erro durante a tradução:")
        st.exception(e)
        return "Erro na tradução."

# ======================================
# INTERFACE SIMPLIFICADA
# ======================================

st.markdown("# 🎙️ AudioTranscript")
st.markdown("### Transforme áudio em texto e traduza para múltiplos idiomas")

uploaded_file = st.file_uploader(
    "Envie seu arquivo de áudio (formato MP3)",
    type=["mp3"]
)

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")

    with st.spinner("Processando áudio para transcrição..."):
        mp3 = AudioSegment.from_file(uploaded_file, format="mp3")
        mp3 = mp3.set_channels(1).set_sample_width(2).set_frame_rate(16000)
        mp3.export("temp.wav", format="wav")
        transcricao = transcribe_audio_offline("temp.wav")
        
        st.subheader("Transcrição:")
        st.write(transcricao)

    idioma_destino = st.selectbox(
        "Selecione o idioma de destino",
        ["English", "Spanish", "French", "German", "Italian"]
    )

    if st.button("Traduzir Texto", type="primary"):
        with st.spinner(f"Traduzindo para {idioma_destino}..."):
            traducao = translate_text_gemini(transcricao, idioma_destino)
        
        st.subheader(f"Tradução ({idioma_destino}):")
        st.write(traducao)