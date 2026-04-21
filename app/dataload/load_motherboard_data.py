import csv
from pathlib import Path
from sqlalchemy.orm import Session
from app.database import engine, create_db_and_tables
from app.dataload.parsing import parse_int, parse_price
from app.models.motherboard import Motherboard

def load_motherboard_data():
    csv_path = Path(__file__).parent.parent / 'data' / 'motherboard.csv'
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
                        socket = row.get('socket', '').strip() or 'Unknown'
                        form_factor = row.get('form_factor', '').strip() or 'Unknown'
                        memory_slots = parse_int(row.get('memory_slots'))
                        capacity = parse_int(row.get('max_memory'))
                        max_memory_gb = capacity if capacity > 0 else None
                        color = row.get('color', '').strip() or 'Unknown'
                        model = None
                        price = parse_price(row.get('price'))
                        motherboard = Motherboard(
                            name=name, model=model, socket=socket, form_factor=form_factor,
                            color=color, memory_slots=memory_slots,
                            max_memory_gb=max_memory_gb, price=price,
                        )
                        session.add(motherboard)
                    except Exception:
                        continue
            session.commit()
        except Exception:
            session.rollback()
            raise
