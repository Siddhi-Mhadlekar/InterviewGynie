# InterviewGynie
# Conversational Interview Bot with Audio Support

## Objective
The Conversational Interview Bot simulates an interview scenario where users can answer questions via audio input and receive feedback. The bot uses OpenAI’s Whisper for transcription and GPT-4 for response evaluation.

## Features
- **Audio Input**: Record your response as audio, which is transcribed into text using Whisper.
- **Text-to-Speech**: The chatbot asks questions both in text and via audio (using gTTS).
- **Automated Evaluation**: Using GPT-4, the bot evaluates candidate responses and provides:
  - A score (1-10)
  - Detailed feedback
  - Suggestions for improvement
- **Streamlit Interface**: A clean and user-friendly interface for recording responses and viewing feedback.

## Project Structure
- `app.py`: Backend using FastAPI for handling audio transcription and response evaluation.
- `chatbot.py`: Streamlit frontend for user interaction.
- `requirements.txt`: Python dependencies.
  
## Setup Instructions
1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/conversational-interview-bot.git
    cd conversational-interview-bot
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Start FastAPI Backend**:
    ```bash
    uvicorn app:app --reload
    ```

4. **Run the Streamlit Frontend**:
    ```bash
    streamlit run chatbot.py
    ```

## How it Works
- **Backend**: FastAPI receives audio responses, transcribes them using Whisper, and evaluates the responses using GPT-4.
- **Frontend**: Streamlit records audio, transcribes, and displays evaluation feedback interactively.


