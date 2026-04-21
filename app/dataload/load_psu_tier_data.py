import csv
import re
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import engine, create_db_and_tables
from app.models.psu import PSU


def parse_tier_list_csv():
    csv_path = Path(__file__).parent.parent / 'data' / 'psu-tiers.csv'
    if not csv_path.exists():
        return []
    with csv_path.open('r', encoding='utf-8') as file:
        return [
            {
                'brand': row['brand'],
                'model': row['model'],
                'sub_models': [value for value in (row['sub_model_1'], row['sub_model_2']) if value],
                'tier': row['tier'] or None,
            }
            for row in csv.DictReader(file)
        ]


def normalize(text):
    text = text.lower()
    text = re.sub('(450|500|550|600|650|700|750|800|850|1000|1050|1200|1300|1500|1600)w?', '', text)
    text = re.sub('[^a-z0-9\\s]', '', text)
    text = re.sub('\\s+', ' ', text).strip()
    return text

def match_psu_to_tier(psu_name, tier_entries):
    psu_lower = normalize(psu_name)
    best_match = None
    best_match_score = 0
    for entry in tier_entries:
        brand_norm = normalize(entry['brand'])
        model_norm = normalize(entry['model'])
        if brand_norm not in psu_lower:
            continue
        if not model_norm:
            continue
        model_tokens = model_norm.split()
        matching_tokens = sum((1 for t in model_tokens if t in psu_lower))
        if matching_tokens == 0:
            continue
        score = matching_tokens / len(model_tokens)
        for sub in entry['sub_models']:
            sub_norm = normalize(sub)
            if sub_norm and sub_norm in psu_lower:
                score += 0.3
        if score > best_match_score:
            best_match_score = score
            best_match = entry
    if best_match and best_match_score >= 0.5:
        return best_match['tier']
    return None

def assign_tiers():
    tier_entries = parse_tier_list_csv()
    if not tier_entries:
        return
    create_db_and_tables()
    with Session(engine) as session:
        psus = session.scalars(select(PSU)).all()
        for psu in psus:
            psu.tier = match_psu_to_tier(psu.name, tier_entries) or ''
        session.commit()
