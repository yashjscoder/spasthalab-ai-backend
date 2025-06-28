from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import os
import google.generativeai as genai

# Load Gemini API key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    content = await file.read()
    with open("temp.pdf", "wb") as f:
        f.write(content)

    doc = fitz.open("temp.pdf")
    full_text = "".join([page.get_text() for page in doc])

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Summarize this medical report in simple terms:\n\n{full_text}")

    return {"summary": response.text}
