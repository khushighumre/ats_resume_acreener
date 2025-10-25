from fastapi import FastAPI, UploadFile, File, Form
from io import BytesIO
import re
import pdfplumber
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()  # this line creates your backend app

# @app.get("/")
# def home():
#     return {"message": "Hello, Khushi!"}
# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],          # allow all HTTP methods
    allow_headers=["*"],          # allow all headers
)

@app.get("/")
def home():
    print("Home endpoint called")
    return {"message": "Backend is working!"}

@app.get("/test")
def test():
    print("Test endpoint called")
    return {"status": "API is working"}

# @app.post("/resume-info")
# async def resume_info(file: UploadFile = File(...)):
#     # Read uploaded file into memory
#     file_bytes = await file.read()
    
#     # Use BytesIO to handle file in memory
#     file_stream = BytesIO(file_bytes)
    
#     # Extract text depending on file type
#     if file.filename.endswith(".docx"):
#         text = docx2txt.process(file_stream)
#     elif file.filename.endswith(".pdf"):
#         text = ""
#         with pdfplumber.open(file_stream) as pdf:
#             for page in pdf.pages:
#                 text += page.extract_text() or ""
#     else:
#         return {"error": "Unsupported file type"}
    
#     # Return first 500 chars for testing
#     return {"filename": file.filename, "text_preview": text[:500]}

@app.post("/resume-info")
async def resume_info(file: UploadFile = File(...)):
    try:
        # Read uploaded file into memory
        file_bytes = await file.read()
        file_stream = BytesIO(file_bytes)

        # Extract text depending on file type
        text = ""
        if file.filename.endswith(".docx"):
            text = docx2txt.process(file_stream)
        elif file.filename.endswith(".pdf"):
            with pdfplumber.open(file_stream) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        else:
            return {"error": "Unsupported file type"}
        
        if not text.strip():
            return {"error": "No text could be extracted from the file"}

        # Split lines and clean
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # Extract basic info
        info = {
            'Name': lines[0] if lines else "Not found",
            'Email': "Not found",
            'Phone': "Not found",
            'Skills': [],
            'Projects': [],
            'Education': [],
            'Experience': []
        }

        # Contact info
        emails = re.findall(r'\b[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}\b', text)
        phones = re.findall(r'[\+]?[1-9]?[0-9]{7,15}', text)
        
        if emails:
            info['Email'] = emails[0]
        if phones:
            info['Phone'] = phones[0]

        # Skills
        SKILLS_DB = ["Python", "JavaScript", "React", "Node.js", "SQL", 
                     "Machine Learning", "TensorFlow", "Pandas", "Numpy",
                     "FastAPI", "Django", "HTML", "CSS", "Java", "C++"]
        
        for skill in SKILLS_DB:
            if skill.lower() in text.lower():
                info['Skills'].append(skill)

        # Education
        for line in lines:
            if re.search(r"(University|Bachelor|Master|College|Degree)", line, re.I):
                info['Education'].append(line)

        return info

    except Exception as e:
        return {"error": "Failed to process resume", "details": str(e)}


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