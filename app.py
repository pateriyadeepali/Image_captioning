# app.py
import streamlit as st
from PIL import Image
from caption_generator import generate_caption
from translator import translate_caption
from gtts import gTTS
import os
import uuid

st.set_page_config(page_title="🖼️ Caption Generator", layout="centered")
st.title("🖼️ Multilingual Image Caption Generator with Audio Controls")

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

language_options = ["Hindi", "Gujarati", "Marathi", "Malayalam", "French", "German"]
selected_langs = st.multiselect("🌐 Choose translation languages", language_options, default=["Hindi"])

lang_codes = {
    "Hindi": "hi",
    "Gujarati": "gu",
    "Marathi": "mr",
    "Malayalam": "ml",
    "French": "fr",
    "German": "de"
}

def speak_text(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    filename = f"temp_audio_{uuid.uuid4().hex}.mp3"
    tts.save(filename)
    return filename

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Generating caption..."):
        caption = generate_caption(image)

    # Tabs for English and Translations
    tab1, tab2 = st.tabs(["📄 English Caption", "🌍 Translations"])

    # --- English Caption Tab ---
    with tab1:
        col1, col2 = st.columns(2)
        if col1.button("📝 Show English Text"):
            st.markdown(f"**Caption**: {caption}")
        if col2.button("🔊 Play English Audio"):
            audio_path = speak_text(caption, 'en')
            st.audio(audio_path, format='audio/mp3')
            os.remove(audio_path)

    # --- Translation Tab ---
    with tab2:
        translations = translate_caption(caption)
        for lang in selected_langs:
            trans_text = translations.get(lang)
            lang_code = lang_codes.get(lang, "en")

            st.markdown(f"### {lang}")
            tcol1, tcol2 = st.columns(2)

            if tcol1.button(f"📝 Show {lang} Text", key=f"text_{lang}"):
                st.markdown(f"**{lang}**: {trans_text}")

            if tcol2.button(f"🔊 Play {lang} Audio", key=f"audio_{lang}"):
                audio_path = speak_text(trans_text, lang_code)
                st.audio(audio_path, format='audio/mp3')
                os.remove(audio_path)
