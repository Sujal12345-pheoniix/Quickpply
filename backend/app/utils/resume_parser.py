import fitz  # PyMuPDF
import json
import google.generativeai as genai
from app.config import settings

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print("Error extracting PDF text:", e)
        return ""


async def parse_resume_with_gemini(resume_text: str) -> dict:
    if not settings.GOOGLE_AI_API_KEY:
        print("GOOGLE_AI_API_KEY is not set.")
        return {}

    genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
    
    # Using gemini-1.5-flash as the fast, lightweight model for structuring text
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) resume parser.
    Extract key professional details from the following resume text and format them strictly as a raw JSON object.
    Do not output any markdown code fences (like ```json), commentary, or extra characters. Output ONLY the JSON.

    Expected JSON Schema:
    {{
      "full_name": "String or null",
      "headline": "String (e.g. Senior Software Engineer) or null",
      "summary": "String (professional summary) or null",
      "years_experience": Number (total years of professional experience, e.g. 5.5) or null,
      "current_title": "String or null",
      "current_company": "String or null",
      "location": "String (City, State/Country) or null",
      "skills": ["String", "String", ...]
    }}

    Candidate Resume Text:
    {resume_text}
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean any accidental markdown wrap
        if text.startswith("```"):
            # strip leading line
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines).strip()
            
        return json.loads(text)
    except Exception as e:
        print("Error calling Gemini API for resume parsing:", e)
        return {}
