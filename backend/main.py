from fastapi import FastAPI, UploadFile, File
from io import BytesIO
import pdfplumber
import docx2txt

app = FastAPI()  # this line creates your backend app

@app.get("/")
def home():
    return {"message": "Hello, Khushi!"}

@app.post("/resume-info")
async def resume_info(file: UploadFile = File(...)):
    # Read uploaded file into memory
    file_bytes = await file.read()
    
    # Use BytesIO to handle file in memory
    file_stream = BytesIO(file_bytes)
    
    # Extract text depending on file type
    if file.filename.endswith(".docx"):
        text = docx2txt.process(file_stream)
    elif file.filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_stream) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    else:
        return {"error": "Unsupported file type"}
    
    # Return first 500 chars for testing
    return {"filename": file.filename, "text_preview": text[:500]}
