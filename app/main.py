from __future__ import annotations
import tempfile
from fastapi import FastAPI, File, Form, UploadFile
from app.extractor import extract_resume

app = FastAPI(title="AI Resume Extraction Service")

@app.get("/")
def root():
    return {"message": "AI Resume Extraction Service is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/extract")
async def extract_endpoint(
    file: UploadFile = File(...),
    model: str = Form("gpt"),
    cache: bool = Form(False),
    use_ocr: bool = Form(True),
):
    suffix = ".pdf" if file.filename and file.filename.lower().endswith(".pdf") else ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    return extract_resume(tmp_path, model=model, cache=cache, use_ocr=use_ocr)
