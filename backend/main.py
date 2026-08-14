
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()


# React runs on port 5173.
# FastAPI runs on port 8000.
# Since these are different origins, CORS permission is required.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
         "https://askmynotes-app-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    question: str
    answer: str


@app.get("/")
def home():
    return {
        "message": "FastAPI backend is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

import joblib
model = joblib.load("askmynotes_classifier.pkl")
@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    cleaned_question = request.question.strip()

    if not cleaned_question:
        return QuestionResponse(
            question="",
            answer="Please enter a question.",
        )

    category = model.predict([cleaned_question])[0]

    return QuestionResponse(
        question=cleaned_question,
        answer=f"Your question belongs to the category: {category}",
    )