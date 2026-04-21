import csv
from pathlib import Path
from sqlalchemy.orm import Session
from app.database import engine, create_db_and_tables
from app.dataload.parsing import parse_int, parse_price
from app.models.storage import Storage

def load_storage_data():
    csv_path = Path(__file__).parent.parent / 'data' / 'internal-hard-drive.csv'
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
                        capacity_gb = parse_int(row.get('capacity'))
                        storage_type = row.get('type', '').strip() or 'Unknown'
                        interface = row.get('interface', '').strip() or 'Unknown'
                        price = parse_price(row.get('price'))
                        storage = Storage(name=name, capacity_gb=capacity_gb, type=storage_type, interface=interface, price=price)
                        session.add(storage)
                    except Exception:
                        continue
            session.commit()
        except Exception:
            session.rollback()
            raise
