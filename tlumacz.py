import streamlit as st  # służy do tworzenia interaktywnych aplikacji webowych
import os  #  to moduł pythona umożliwiający interakcje z systemem operacyjnym
from dotenv import dotenv_values
from openai import OpenAI

# conda activate C:\conda\envs\od_zera_do_ai_v2
# streamlit run tlumacz.py

# git init
# git add tlumacz.py
# git add . (dodaje wszystkie pliki)
# git commit -m 'dodano glowny plik'
# git status
# git remote add origin https://github.com/agnes040401/T-umacz.git
# git remote -v
# git push -u origin main (za pierwszym razem)

# i potem cyklicznie
# git add .
# git commit -m 'coś tam'
# git push

# Mój API z pliku .env
# env = dotenv_values(".env")
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.write(st.secrets["OPENAI_API_KEY"])

def translate_text_llm(text, source_lang, target_lang):
    prompt = f"""
    Przetłumacz poniższy tekst z języka {source_lang} na {target_lang}.
    Zachowaj znaczenie, styl i poprawność językową.

    Tekst:
    {text}
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Jesteś profesjonalnym tłumaczem."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()

def generate_speech(prompt, voice, output_audio_path):  # generowanie mowy
    response = openai_client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=prompt,
    )

    response.write_to_file(output_audio_path)
    return output_audio_path

def correct_text(text, style="neutral"):
    """
    style: neutral | formal | informal | academic | business
    """

    prompt = f"""
    Improve the following English text.
    Fix grammar, spelling, and punctuation.
    Make it sound natural to a native speaker.
    Do NOT change the meaning.

    Style: {style}

    Text:
    {text}
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional English editor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()

def main():  #  Funkcja 'main' jest punktem wejściowym dla tej aplikacji. Tutaj jest tworzony interfejs 
             # użytkownika za pomocą 'streamlit'. 
    st.title("🧠 AI Language Studio")
    st.caption("Translation • Proofreading • Text-to-Speech")

    api_key = st.text_input("Wprowadź swój klucz API:", type="password")
    # Użytkownik musi podać swój klucz API, 

    mode = st.selectbox("Wybierz tryb:", ("Tłumaczenie (translate)", "Korekta (correct)"))
    # a następnie wybrać tryb działania aplikacji: tłumaczenie tekstu z języka polskiego na inny lub korekta 
    # tekstu w języku obcym.

    if mode == "Tłumaczenie (translate)":  # Jeśli użytkownik wybierze tryb 'Tłumaczenie z polskiego',
        source_lang = st.selectbox(
        "Język źródłowy",
        ["polski", "angielski", "niemiecki", "francuski", "hiszpański"]
        )

        target_lang = st.selectbox(
        "Język docelowy",
        ["angielski", "polski", "niemiecki", "francuski", "hiszpański"]
        )

        text = st.text_area("Wpisz tekst do tłumaczenia")

        if st.button("Tłumacz") and text:
            with st.spinner("Tłumaczenie w toku..."):
                translated = translate_text_llm(text, source_lang, target_lang)
                st.subheader("Wynik:")
                st.write(translated)

                audio_path = generate_speech(
                    prompt = translated,
                    voice = "alloy",
                    output_audio_path = "speech.mp3"
                )
                st.audio(audio_path)

    elif mode == "Korekta (correct)":  # Jeśli użytkownik wybierze tryb 'Korekta obcego',

        text = st.text_area("Paste your English text:")
        # musi wprowadzić tekst do poprawy. 

        style = st.selectbox(
        "Choose style",
        ["neutral", "formal", "informal", "business", "academic"]
        )

        if st.button("Improve text") and text:
            with st.spinner("Improving text..."):
                improved = correct_text(text, style)
                st.subheader("Improved version:")
                st.write(improved)

                audio_path = generate_speech(
                    prompt = improved,
                    voice = "alloy",
                    output_audio_path = "speech_correct.mp3"
                )
                st.audio(audio_path)

if __name__ == "__main__":
    main()