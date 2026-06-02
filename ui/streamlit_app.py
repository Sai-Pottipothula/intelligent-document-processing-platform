from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import streamlit as st

from app.extractor import extract_resume


st.set_page_config(
    page_title="AI Resume Extraction Service",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Extraction Service")
st.write("Upload a resume PDF and extract structured JSON using GPT or Claude.")

uploaded_file = st.file_uploader(
    "Upload resume PDF",
    type=["pdf"]
)

model = st.selectbox(
    "Select model",
    ["gpt", "claude"]
)

use_cache = st.checkbox("Use cache", value=False)
use_ocr = st.checkbox("Use OCR fallback", value=True)

if uploaded_file is not None:
    st.info(f"Uploaded file: {uploaded_file.name}")

    if st.button("Extract Resume Data"):
        with st.spinner("Extracting resume data..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = Path(tmp.name)

            try:
                result = extract_resume(
                    str(tmp_path),
                    model=model,
                    cache=use_cache,
                    use_ocr=use_ocr
                )

                st.success("Extraction complete!")

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Structured JSON")
                    st.json(result)

                with col2:
                    st.subheader("Quick Summary")

                    data = result.get("data", result)

                    st.write(f"**Name:** {data.get('name')}")
                    st.write(f"**Emails:** {', '.join(data.get('emails', []))}")
                    st.write(f"**Phones:** {', '.join(data.get('phones', []))}")
                    st.write(f"**Location:** {data.get('location')}")
                    st.write(f"**Confidence:** {data.get('confidence_score')}")

                    skills = data.get("skills", [])
                    if skills:
                        st.write("**Top Skills:**")
                        st.write(", ".join(skills[:15]))

                json_output = json.dumps(result, indent=2)

                st.download_button(
                    label="Download JSON",
                    data=json_output,
                    file_name="resume_extraction.json",
                    mime="application/json"
                )

            except Exception as e:
                st.error("Extraction failed.")
                st.exception(e)
else:
    st.warning("Upload a PDF resume to begin.")