from io import BytesIO

from pypdf import PdfWriter

from src.skill_extractor import extract_skills
from src.matcher import load_jobs, match_jobs
from src.resume_parser import extract_text_from_pdf
from src.roadmap import build_action_plan_markdown

def test_skill_extraction():
    skills = extract_skills("I use Python, SQL, Pandas and scikit-learn.")
    assert "Python" in skills
    assert "SQL" in skills
    assert "Pandas" in skills
    assert "Scikit-learn" in skills

def test_matching():
    jobs = load_jobs()
    result = match_jobs(["Python", "SQL"], jobs)
    assert len(result) == len(jobs)
    assert result["match_percent"].max() > 0

def test_pdf_parser_accepts_in_memory_upload():
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    buffer = BytesIO()
    writer.write(buffer)

    assert extract_text_from_pdf(buffer.getvalue()) == ""

def test_action_plan_explains_score_and_prioritizes_gaps():
    report = build_action_plan_markdown(
        "Data Scientist",
        50.0,
        ["Python"],
        ["Statistics"],
    )

    assert "Current role alignment:** 50.0%" in report
    assert "1 of 2" in report
    assert "Week 1: Statistics" in report
    assert "Days 29-30" in report
