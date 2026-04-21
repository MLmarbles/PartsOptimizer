import csv
from pathlib import Path
from sqlalchemy.orm import Session
from app.database import engine, create_db_and_tables
from app.dataload.parsing import parse_price
from app.models.ram import RAM

def parse_speed_and_type(speed_str: str) -> tuple[int, str]:
    try:
        if ',' in speed_str:
            generation, speed_mhz = map(int, speed_str.split(','))
            return speed_mhz, f'DDR{generation}'
        speed_mhz = int(speed_str)
        ram_type = 'DDR5' if speed_mhz >= 4800 else 'DDR4' if speed_mhz >= 2133 else 'DDR3'
        return speed_mhz, ram_type
    except (ValueError, TypeError):
        return 0, 'Unknown'

def load_ram_data():
    csv_path = Path(__file__).parent.parent / 'data' / 'memory.csv'
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
                        speed_mhz, ram_type = parse_speed_and_type(row['speed'])
                        modules, capacity_per_module = map(int, row['modules'].split(','))
                        ram = RAM(
                            name=name,
                            capacity_gb=modules * capacity_per_module,
                            speed_mhz=speed_mhz,
                            type=ram_type,
                            modules=modules,
                            color=row.get('color', '').strip() or 'Unknown',
                            price=parse_price(row.get('price')),
                        )
                        session.add(ram)
                    except Exception:
                        continue
            session.commit()
        except Exception:
            session.rollback()
            raise
