from pathlib import Path
from io import BytesIO
import re
from pypdf import PdfReader

SECTION_NAMES = [
    "education", "experience", "work experience", "skills",
    "projects", "certifications", "summary", "objective"
]

def extract_text_from_pdf(path):
    if isinstance(path, (bytes, bytearray, memoryview)):
        reader = PdfReader(BytesIO(path))
    else:
        reader = PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages)

def split_sections(text):
    sections = {}
    current = "general"
    sections[current] = []
    for line in text.splitlines():
        clean = line.strip()
        key = clean.lower().rstrip(":")
        if key in SECTION_NAMES:
            current = key
            sections.setdefault(current, [])
        elif clean:
            sections.setdefault(current, []).append(clean)
    return {k: "\n".join(v).strip() for k, v in sections.items() if v}

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()
