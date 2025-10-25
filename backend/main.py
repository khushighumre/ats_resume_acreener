from fastapi import FastAPI, UploadFile, File, Form
from io import BytesIO
import pdfplumber
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()  # this line creates your backend app

# @app.get("/")
# def home():
#     return {"message": "Hello, Khushi!"}

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

@app.post("/percentage-match")
async def percentage_match(jd: str = Form(...), file: UploadFile = File(...)):
    # Read uploaded file
    file_bytes = await file.read()
    file_stream = BytesIO(file_bytes)
    
    # Extract resume text
    if file.filename.endswith(".docx"):
        resume_text = docx2txt.process(file_stream)
    elif file.filename.endswith(".pdf"):
        resume_text = ""
        with pdfplumber.open(file_stream) as pdf:
            for page in pdf.pages:
                resume_text += page.extract_text() or ""
    else:
        return {"error": "Unsupported file type"}
    
    # Calculate similarity
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([jd, resume_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    
    # Convert to percentage
    percentage = round(similarity * 100, 2)
    
    return {"percentage_match": percentage}