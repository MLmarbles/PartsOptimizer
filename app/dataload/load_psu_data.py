import csv
from pathlib import Path
from sqlalchemy.orm import Session
from app.database import engine, create_db_and_tables
from app.dataload.parsing import parse_int, parse_price
from app.models.psu import PSU

def load_psu_data():
    csv_path = Path(__file__).parent.parent / 'data' / 'power-supply.csv'
    if not csv_path.exists():
        return
    create_db_and_tables()
    with Session(engine) as session:
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        name = row.get('name', '').strip()
                        if not name:
                            continue
                        wattage = parse_int(row.get('wattage'))
                        efficiency_rating = (row.get('efficiency', '').strip() or 'Unknown').capitalize()
                        form_factor = ''
                        tier = ''
                        price = parse_price(row.get('price'))
                        psu = PSU(name=name, wattage=wattage, efficiency_rating=efficiency_rating, tier=tier, form_factor=form_factor, price=price)
                        session.add(psu)
                    except Exception:
                        continue
            session.commit()
        except Exception:
            session.rollback()
            raise
