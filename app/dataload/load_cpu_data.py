import csv
import re
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session
from app.database import engine, create_db_and_tables
from app.dataload.parsing import parse_int, parse_price
from app.models.cpu import CPU

INTEL_SOCKETS = {
    2: 'LGA1155',
    3: 'LGA1155',
    4: 'LGA1150',
    5: 'LGA1150',
    6: 'LGA1151',
    7: 'LGA1151',
    8: 'LGA1151',
    9: 'LGA1151',
    10: 'LGA1200',
    11: 'LGA1200',
    12: 'LGA1700',
    13: 'LGA1700',
    14: 'LGA1700',
}


def split_brand_and_name(full_name: str) -> tuple[str, str]:
    parts = full_name.strip().split(maxsplit=1)
    if len(parts) == 1:
        return (parts[0], '')
    return (parts[0], parts[1])

def infer_socket_from_name(name: str) -> str:
    name_upper = name.upper()
    if 'AMD' in name_upper or 'RYZEN' in name_upper:
        return infer_amd_socket(name_upper)
    if 'INTEL' in name_upper or 'CORE' in name_upper:
        return infer_intel_socket(name_upper)
    return 'Unknown'


def infer_amd_socket(name: str) -> str:
    if 'THREADRIPPER' in name or 'TR' in name:
        match = re.search(r'(\d{4})', name)
        if not match:
            return 'sTRX4'
        model = int(match.group(1))
        if model >= 5000:
            return 'sWRX8'
        return 'sTRX4' if model >= 3000 else 'sTR4'

    match = re.search(r'RYZEN\s+\d+\s+(\d{4})', name)
    if not match or int(match.group(1)) < 1000:
        match = re.search(r'(\d{4})', name)
    if not match or int(match.group(1)) < 1000:
        return 'Unknown'
    return 'AM5' if int(match.group(1)) >= 7000 else 'AM4'


def infer_intel_socket(name: str) -> str:
    if 'ULTRA' in name or 'ARROW LAKE' in name:
        return 'LGA1851'
    match = re.search(r'CORE\s+I\d+-(\d{2})\d{3}\b', name)
    if match and int(match.group(1)) >= 10:
        generation = int(match.group(1))
        return INTEL_SOCKETS.get(generation, 'LGA1700')
    match = re.search(r'I\d+-(\d{4})', name)
    if match:
        generation = int(match.group(1)) // 1000
        return INTEL_SOCKETS.get(generation, 'Unknown')
    return 'Unknown'

def normalize_cpu_name(name: str) -> str:
    return ' '.join(name.upper().split())

def load_benchmark_data(data_dir: Path) -> tuple[dict[str, int], dict[str, int]]:
    return (
        load_benchmark_file(data_dir / 'cpu_benchmarks.csv', 'Benchmark Score'),
        load_benchmark_file(data_dir / 'multi_core_benchmarks.csv', 'Multi-Core Score'),
    )


def load_benchmark_file(path: Path, score_column: str) -> dict[str, int]:
    if not path.exists():
        return {}
    benchmarks = {}
    with path.open('r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            name = row.get('CPU Name', '').strip()
            if not name:
                continue
            try:
                benchmarks[normalize_cpu_name(name)] = int(row.get(score_column, ''))
            except (ValueError, TypeError):
                continue
    return benchmarks

def find_benchmark_score(full_name: str, benchmarks: dict[str, int]) -> Optional[int]:
    normalized_full = normalize_cpu_name(full_name)
    if normalized_full in benchmarks:
        return benchmarks[normalized_full]
    normalized_clean = re.sub('\\s+[A-Z]\\s*$', '', normalized_full)
    if normalized_clean in benchmarks:
        return benchmarks[normalized_clean]
    parts = normalized_full.split(maxsplit=1)
    if len(parts) > 1:
        name_only = parts[1]
        for key, value in benchmarks.items():
            if name_only in key or key in name_only:
                return value
    return None

def load_cpu_data():
    csv_path = Path(__file__).parent.parent / 'data' / 'cpu.csv'
    if not csv_path.exists():
        return
    single_core_benchmarks, multi_core_benchmarks = load_benchmark_data(csv_path.parent)
    create_db_and_tables()
    with Session(engine) as session:
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        full_name = row['name']
                        brand, name = split_brand_and_name(full_name)
                        socket = infer_socket_from_name(full_name)
                        cores = parse_int(row.get('core_count'), strict=True)
                        tdp = parse_int(row.get('tdp'), strict=True)
                        integrated_gpu = bool(row.get('graphics', '').strip())
                        single_core_score = find_benchmark_score(full_name, single_core_benchmarks)
                        multi_core_score = find_benchmark_score(full_name, multi_core_benchmarks)
                        price = parse_price(row.get('price'))
                        cpu = CPU(
                            name=name,
                            brand=brand,
                            cores=cores,
                            single_core_score=single_core_score,
                            multi_core_score=multi_core_score,
                            tdp=tdp,
                            socket=socket,
                            integrated_gpu=integrated_gpu,
                            price=price,
                        )
                        session.add(cpu)
                    except Exception:
                        continue
            session.commit()
        except Exception:
            session.rollback()
            raise
