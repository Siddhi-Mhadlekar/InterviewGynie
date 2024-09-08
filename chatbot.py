import streamlit as st
import requests
import speech_recognition as sr
from gtts import gTTS
import base64

# FastAPI backend URLs
API_URL_EVALUATION = "http://127.0.0.1:8000/evaluate_response"
API_URL_TRANSCRIBE = "http://127.0.0.1:8000/transcribe_audio"

# Setup Streamlit page
st.set_page_config(page_title="Conversational Interview Bot", layout="centered")

st.title("Conversational Interview Bot")

candidate_name = st.text_input("Enter your name:", "")
questions = [
    "Tell me about yourself.",
    "What are your strengths and weaknesses?",
    "Why should we hire you?",
    "Describe a challenging project you worked on."
]
current_question = st.selectbox("Choose a question:", questions)

# Text-to-Speech for questions
def speak_question(question_text):
    tts = gTTS(text=question_text, lang='en')
    tts.save("question.mp3")

    audio_file = open("question.mp3", "rb")
    audio_bytes = audio_file.read()
    
    st.audio(audio_bytes, format="audio/mp3")

# Record and transcribe user response
def record_audio():
    st.info("Recording... Please respond to the question.")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    
    # Save audio to file
    with open("response.wav", "wb") as f:
        f.write(audio.get_wav_data())
    
    return "response.wav"

# Upload audio for transcription
def transcribe_audio(file_path):
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(API_URL_TRANSCRIBE, files=files)

    if response.status_code == 200:
        return response.json()["transcription"]
    else:
        return None

# Display and read question out loud
st.subheader("Question:")
st.write(current_question)
speak_question(current_question)

# Audio recording and response transcription
if st.button("Record Audio Response"):
    audio_file = record_audio()
    transcription = transcribe_audio(audio_file)

    if transcription:
        st.write(f"**Transcribed Response**: {transcription}")
    else:
        st.write("Could not transcribe the audio response. Please try again.")

# Submit transcribed response for evaluation
if st.button("Submit Response"):
    if candidate_name and transcription:
        payload = {
            "candidate_name": candidate_name,
            "question": current_question,
            "response": transcription
        }

        response = requests.post(API_URL_EVALUATION, json=payload)

        if response.status_code == 200:
            data = response.json()
            st.subheader("Evaluation Results")
            st.write(f"**Score**: {data['score']}/10")
            st.write(f"**Feedback**: {data['feedback']}")
            st.write(f"**Suggestions**: {data['suggestions']}")
        else:
            st.write("There was an issue with the evaluation. Please try again.")
    else:
        st.write("Please record and transcribe a response before submitting.")
