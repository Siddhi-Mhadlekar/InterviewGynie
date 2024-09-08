from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import openai
import whisper

app = FastAPI()

# Replace with your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Initialize Whisper model for speech-to-text
model = whisper.load_model("base")

# Model for text input
class InterviewRequest(BaseModel):
    candidate_name: str
    question: str
    response: str

class EvaluationResponse(BaseModel):
    score: float
    feedback: str
    suggestions: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Interview Bot API"}

# Endpoint for audio upload and transcription
@app.post("/transcribe_audio")
async def transcribe_audio(file: UploadFile = File(...)):
    audio = await file.read()

    with open("temp_audio.mp3", "wb") as f:
        f.write(audio)

    result = model.transcribe("temp_audio.mp3")
    return {"transcription": result["text"]}

# Endpoint for evaluating text-based interview responses
@app.post("/evaluate_response", response_model=EvaluationResponse)
def evaluate_response(interview_request: InterviewRequest):
    score, feedback, suggestions = evaluate_candidate_response(
        interview_request.question, interview_request.response
    )
    return EvaluationResponse(
        score=score,
        feedback=feedback,
        suggestions=suggestions
    )

def evaluate_candidate_response(question: str, response: str) -> (float, str, str):
    prompt = f"""
    You are an expert interviewer and evaluator. I will give you an interview question and a candidate's response. 
    Please evaluate the response on a scale of 1 to 10 based on the following criteria:
    1. Relevance to the question
    2. Clarity and structure
    3. Completeness of the answer
    Then, provide constructive feedback explaining why the response deserves that score and suggest ways to improve.

    Interview Question: {question}
    Candidate's Response: {response}

    Please provide:
    1. The score (1-10).
    2. Feedback on the response.
    3. Suggestions for improvement.
    """

    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=300,
        temperature=0.7
    )

    gpt_output = response.choices[0].text.strip()

    try:
        lines = gpt_output.split("\n")
        score = float(lines[0].split(":")[1].strip())
        feedback = lines[1].split(":")[1].strip()
        suggestions = lines[2].split(":")[1].strip()
    except Exception as e:
        score = 0
        feedback = "Could not parse GPT response."
        suggestions = "Please try again."

    return score, feedback, suggestions
