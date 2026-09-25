import pandas as pd

def load_jobs(path="data/jobs.csv"):
    return pd.read_csv(path)

def parse_skills(value):
    return {x.strip() for x in str(value).split(",") if x.strip()}

def match_jobs(user_skills, jobs):
    user = set(user_skills)
    rows = []
    for _, job in jobs.iterrows():
        required = parse_skills(job["skills"])
        matched = sorted(user & required)
        missing = sorted(required - user)
        score = round(len(matched) / len(required) * 100, 1) if required else 0
        rows.append({
            "job_id": job["job_id"],
            "title": job["title"],
            "company": job["company"],
            "match_percent": score,
            "matched_skills": matched,
            "missing_skills": missing
        })
    return pd.DataFrame(rows).sort_values("match_percent", ascending=False)
