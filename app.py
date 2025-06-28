from fastapi import FastAPI, UploadFile, File
import fitz  # PyMuPDF for PDF text extraction
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for testing
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

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Summarize this medical report in simple, layman terms."},
            {"role": "user", "content": full_text}
        ],
        max_tokens=1000,
        temperature=0.5,
    )

    return {"summary": response['choices'][0]['message']['content']}
