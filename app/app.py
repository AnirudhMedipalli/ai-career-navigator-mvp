import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import plotly.express as px
import streamlit as st

from src.matcher import load_jobs, match_jobs
from src.resume_parser import extract_text_from_pdf, split_sections
from src.roadmap import build_action_plan_markdown, generate_roadmap
from src.skill_extractor import extract_skills
from src.visuals import CAREER_SCENE


st.set_page_config(page_title="AI Career Navigator", page_icon="🧭", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #0f172a;
        background-image:
            linear-gradient(rgba(166, 184, 214, 0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(166, 184, 214, 0.025) 1px, transparent 1px);
        background-size: 32px 32px;
    }
    [data-testid="stHeader"] { background: rgba(15, 23, 42, 0.88); }
    [data-testid="stMainBlockContainer"] {
        max-width: 1320px;
        padding-top: 1.1rem;
        padding-bottom: 4rem;
    }
    .hero-kicker, .section-kicker {
        color: #8be0c2;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }
    .hero-title {
        color: #f8fafc;
        font-family: "Space Grotesk", "Segoe UI", sans-serif;
        font-size: 3.45rem;
        font-weight: 650;
        line-height: 1.04;
        margin: 1.1rem 0 1rem;
    }
    .hero-title span { color: #b8adff; }
    .hero-copy {
        color: #aab7cc;
        font-size: 1.08rem;
        line-height: 1.65;
        max-width: 34rem;
        margin: 0;
    }
    .hero-meta {
        color: #91a0b8;
        font-size: 0.82rem;
        margin-top: 1.6rem;
    }
    .section-title {
        color: #f8fafc;
        font-size: 1.55rem;
        font-weight: 650;
        margin: 0.25rem 0 0.5rem;
    }
    .section-copy { color: #aab7cc; margin-bottom: 1.1rem; }
    [data-testid="stForm"] {
        background: rgba(30, 41, 59, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 1.1rem 1.2rem 0.8rem;
    }
    [data-testid="stFileUploaderDropzone"] {
        background: rgba(15, 23, 42, 0.56);
        border: 1px dashed rgba(184, 173, 255, 0.46);
        border-radius: 9px;
    }
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 10px;
        min-height: 112px;
        padding: 1rem 1.15rem;
    }
    [data-testid="stMetricLabel"] { color: #aab7cc; }
    [data-testid="stMetricValue"] { color: #f8fafc; }
    [data-testid="stExpander"] {
        background: rgba(30, 41, 59, 0.55);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 9px;
    }
    .roadmap-step {
        color: #8be0c2;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    @media (max-width: 700px) {
        .hero-title { font-size: 2.5rem; }
        .hero-copy { font-size: 1rem; }
        [data-testid="stMainBlockContainer"] { padding-top: 0.6rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


hero_copy, hero_scene = st.columns([1.02, 1.1], gap="large", vertical_alignment="center")
with hero_copy:
    st.markdown('<div class="hero-kicker">Career intelligence / 01</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-title">Map your next<br><span>career move.</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="hero-copy">Turn your experience into a clear read on your strengths, '
        'your next role, and the skills that will get you there.</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="hero-meta">RESUME SIGNALS &nbsp;·&nbsp; ROLE FIT &nbsp;·&nbsp; NEXT STEPS</div>', unsafe_allow_html=True)
with hero_scene:
    CAREER_SCENE(key="career-growth-scene", height=310, width="stretch")

st.space("large")
st.markdown('<div class="section-kicker">Start with your experience</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Build your career snapshot</div>', unsafe_allow_html=True)
st.markdown('<div class="section-copy">Choose a resume and the role you want to grow into.</div>', unsafe_allow_html=True)

target_roles = [
    "Data Scientist",
    "Data Analyst",
    "Machine Learning Engineer",
    "AI Engineer",
    "Data Engineer",
    "Business Intelligence Analyst",
]

with st.form("resume_analysis", border=True):
    upload_column, role_column = st.columns([1.55, 1], gap="large", vertical_alignment="bottom")
    with upload_column:
        uploaded = st.file_uploader("Resume PDF", type=["pdf"], help="PDF format")
    with role_column:
        target = st.selectbox("Target role", target_roles)
    submitted = st.form_submit_button(
        "Analyze my profile",
        type="primary",
        icon=":material/arrow_forward:",
        width="stretch",
    )
st.caption("Your PDF is processed in memory; the app does not save the original file.")

if submitted:
    if uploaded is None:
        st.warning("Add a PDF resume to start your analysis.")
    else:
        project_root = Path(__file__).resolve().parents[1]
        resume_text = extract_text_from_pdf(uploaded.getvalue())
        resume_sections = split_sections(resume_text)
        detected_skills = extract_skills(resume_text)
        jobs = load_jobs(project_root / "data" / "jobs.csv")
        job_results = match_jobs(detected_skills, jobs)
        selected_role = job_results.loc[job_results["title"] == target].iloc[0]
        matched_skills = selected_role["matched_skills"]
        missing_skills = selected_role["missing_skills"]

        st.session_state["career_analysis"] = {
            "filename": Path(uploaded.name).name,
            "target": target,
            "skills": detected_skills,
            "results": job_results,
            "matched": matched_skills,
            "missing": missing_skills,
            "required_count": len(matched_skills) + len(missing_skills),
            "match_percent": selected_role["match_percent"],
            "sections": resume_sections,
        }

analysis = st.session_state.get("career_analysis")
if analysis:
    st.space("large")
    st.markdown('<div class="section-kicker">Your readout</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">A clearer picture of your fit</div>', unsafe_allow_html=True)
    st.caption(f"Based on {analysis['filename']} · Targeting {analysis['target']}")

    metric_columns = st.columns(3, gap="medium")
    metric_columns[0].metric("Skills identified", len(analysis["skills"]))
    metric_columns[1].metric("Role alignment", f"{analysis['match_percent']}%")
    metric_columns[2].metric("Priority skill gaps", len(analysis["missing"]))

    action_plan = build_action_plan_markdown(
        analysis["target"],
        analysis["match_percent"],
        analysis["matched"],
        analysis["missing"],
    )
    st.download_button(
        "Download 30-day action plan",
        data=action_plan,
        file_name="career-action-plan.md",
        mime="text/markdown",
        icon=":material/download:",
    )

    skills_column, gaps_column = st.columns([1, 1], gap="large")
    with skills_column:
        st.markdown("### Skills credited for this role")
        st.caption(f"{len(analysis['matched'])} of {analysis['required_count']} listed skills recognized")
        if analysis["matched"]:
            for skill in analysis["matched"]:
                st.badge(skill, color="green")
        else:
            st.caption("No listed role skills were detected in this resume yet.")
    with gaps_column:
        st.markdown("### Skills to build")
        if analysis["missing"]:
            for skill in analysis["missing"]:
                st.badge(skill, color="orange")
        else:
            st.badge("Role-ready", icon=":material/check:", color="green")

    with st.expander("How role alignment is calculated", icon=":material/analytics:"):
        st.write(
            "The score is the share of this role's listed skill categories found in your resume. "
            "It uses exact matches after known aliases are normalized; it is not a hiring probability."
        )
        st.write(f"Required categories: {analysis['required_count']}")
        st.write(
            "All skills detected: "
            + (", ".join(analysis["skills"]) if analysis["skills"] else "none detected")
        )

    st.space("medium")
    st.markdown('<div class="section-kicker">Explore your options</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Role match overview</div>', unsafe_allow_html=True)
    chart_data = analysis["results"].sort_values("match_percent", ascending=True)
    fig = px.bar(
        chart_data,
        x="match_percent",
        y="title",
        orientation="h",
        text="match_percent",
        range_x=[0, 108],
        color_discrete_sequence=["#8be0c2"],
    )
    fig.update_traces(
        texttemplate="%{x:.0f}%",
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
        hovertemplate="%{y}<br>Role alignment: %{x:.1f}%<extra></extra>",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "sans-serif", "color": "#dce5f2", "size": 13},
        margin={"l": 12, "r": 40, "t": 10, "b": 24},
        xaxis={"title": None, "range": [0, 108], "ticksuffix": "%", "gridcolor": "rgba(148,163,184,0.15)"},
        yaxis={"title": None, "showgrid": False, "tickfont": {"size": 13}},
        showlegend=False,
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    st.markdown('<div class="section-kicker">A plan you can act on</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Your learning roadmap</div>', unsafe_allow_html=True)
    roadmap = generate_roadmap(analysis["missing"])
    if roadmap:
        for index, (skill, action) in enumerate(roadmap.items(), start=1):
            with st.container(border=True):
                st.markdown(f'<div class="roadmap-step">Step {index:02}</div>', unsafe_allow_html=True)
                st.markdown(f"#### {skill}")
                st.write(action)
    else:
        st.success("You already match the listed requirements for this role.")

    with st.expander("Detected resume sections", icon=":material/description:"):
        for name, content in analysis["sections"].items():
            st.markdown(f"**{name.title()}**")
            st.write(content[:3000])
