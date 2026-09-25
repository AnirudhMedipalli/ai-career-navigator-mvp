import re
import pandas as pd

def load_skill_dictionary(path="data/skills.csv"):
    df = pd.read_csv(path)
    aliases = {}
    for _, row in df.iterrows():
        canonical = row["canonical_skill"]
        for alias in str(row["aliases"]).split(","):
            aliases[alias.strip().lower()] = canonical
        aliases[canonical.lower()] = canonical
    return aliases

def extract_skills(text, path="data/skills.csv"):
    aliases = load_skill_dictionary(path)
    found = set()
    text_lower = text.lower()
    for alias, canonical in aliases.items():
        pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
        if re.search(pattern, text_lower):
            found.add(canonical)
    return sorted(found)
