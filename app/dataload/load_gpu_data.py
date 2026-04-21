import csv
import re
from pathlib import Path
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import engine, create_db_and_tables
from app.dataload.parsing import parse_int, parse_price
from app.models.gpu import GPU

def infer_brand_from_chipset(chipset: str) -> str:
    first_word = chipset.strip().split(maxsplit=1)[0].lower()
    if first_word in {'geforce', 'rtx', 'gtx', 'nvidia'}:
        return 'NVIDIA'
    if first_word in {'radeon', 'rx', 'amd'}:
        return 'AMD'
    if first_word in {'arc', 'intel'}:
        return 'Intel'
    return first_word.capitalize()

def strip_memory_words(text: str) -> str:
    return ' '.join(
        word for word in text.split()
        if not (word.isdigit() or word.upper().endswith('GB'))
    )

def extract_model_from_name(full_name: str, chipset: str) -> Optional[str]:
    if not full_name or not chipset:
        return None
    full_name = full_name.strip()
    chipset = chipset.strip()
    chipset_words = chipset.split()
    chipset_base = strip_memory_words(chipset)
    name_upper = full_name.upper()
    chipset_base_upper = chipset_base.upper()
    idx = name_upper.find(chipset_base_upper) if chipset_base_upper else -1
    if idx >= 0:
        before = full_name[:idx].strip()
        after = strip_memory_words(full_name[idx + len(chipset_base):])
        model = ' '.join(part for part in (before, after) if part)
        if model:
            return model
    result = full_name
    for word in chipset_words:
        pattern = re.compile('\\b' + re.escape(word) + '\\b', re.IGNORECASE)
        result = pattern.sub('', result, count=1)
    result = ' '.join(result.split()).strip()
    return result if result else None
GPU_TDP_MAP = {
                  'Arc A310': 75,
                  'Arc A380': 75,
                  'Arc A580': 175,
                  'Arc A750': 225,
                  'Arc A770': 225,
                  'Arc B570': 175,
                  'Arc B580': 200,
                  'Arc Pro A40': 50,
                  'Arc Pro A50': 75,
                  'Arc Pro A60': 100,
                  'GeForce RTX 5050': 115,
                  'GeForce RTX 5060': 115,
                  'GeForce RTX 5060 Ti': 165,
                  'GeForce RTX 5070': 220,
                  'GeForce RTX 5070 Ti': 240,
                  'GeForce RTX 5080': 320,
                  'GeForce RTX 5090': 425,
                  'GeForce RTX 4060': 115,
                  'GeForce RTX 4060 Ti': 165,
                  'GeForce RTX 4070': 200,
                  'GeForce RTX 4070 SUPER': 220,
                  'GeForce RTX 4070 Ti': 285,
                  'GeForce RTX 4070 Ti SUPER': 285,
                  'GeForce RTX 4080': 320,
                  'GeForce RTX 4080 SUPER': 320,
                  'GeForce RTX 4090': 450,
                  'GeForce RTX 3050 6GB': 70,
                  'GeForce RTX 3050 8GB': 130,
                  'GeForce RTX 3060 8GB': 170,
                  'GeForce RTX 3060 12GB': 170,
                  'GeForce RTX 3060 Ti': 200,
                  'GeForce RTX 3060 Ti LHR': 200,
                  'GeForce RTX 3070': 220,
                  'GeForce RTX 3070 LHR': 220,
                  'GeForce RTX 3070 Ti': 290,
                  'GeForce RTX 3080 10GB': 320,
                  'GeForce RTX 3080 10GB LHR': 320,
                  'GeForce RTX 3080 12GB LHR': 350,
                  'GeForce RTX 3080 Ti': 350,
                  'GeForce RTX 3090': 350,
                  'GeForce RTX 3090 Ti': 450,
                  'GeForce RTX 2060': 160,
                  'GeForce RTX 2060 12GB': 185,
                  'GeForce RTX 2060 SUPER': 175,
                  'GeForce RTX 2070': 175,
                  'GeForce RTX 2070 SUPER': 215,
                  'GeForce RTX 2080': 215,
                  'GeForce RTX 2080 SUPER': 250,
                  'GeForce RTX 2080 Ti': 250,
                  'GeForce GTX 1630': 75,
                  'GeForce GTX 1650 G5': 75,
                  'GeForce GTX 1650 G6': 75,
                  'GeForce GTX 1650 SUPER': 100,
                  'GeForce GTX 1660': 120,
                  'GeForce GTX 1660 SUPER': 125,
                  'GeForce GTX 1660 Ti': 120,
                  'GeForce GTX 1050': 75,
                  'GeForce GTX 1050 Ti': 75,
                  'GeForce GTX 1060 3GB': 120,
                  'GeForce GTX 1060 6GB': 120,
                  'GeForce GTX 1070': 150,
                  'GeForce GTX 1070 Ti': 180,
                  'GeForce GTX 1080': 180,
                  'GeForce GTX 1080 Ti': 250,
                  'GeForce GTX 950': 90,
                  'GeForce GTX 950 75W': 75,
                  'GeForce GTX 960': 120,
                  'GeForce GTX 970': 145,
                  'GeForce GTX 980': 165,
                  'GeForce GTX 980 Ti': 250,
                  'GeForce GTX 750': 55,
                  'GeForce GTX 750 Ti': 60,
                  'GeForce GTX 760': 170,
                  'GeForce GTX 760 X2': 340,
                  'GeForce GTX 770': 230,
                  'GeForce GTX 780': 250,
                  'GeForce GTX 780 Ti': 250,
                  'GeForce GTX 650': 64,
                  'GeForce GTX 650 Ti': 110,
                  'GeForce GTX 650 Ti Boost': 134,
                  'GeForce GTX 660': 140,
                  'GeForce GTX 660 Ti': 150,
                  'GeForce GTX 670': 170,
                  'GeForce GTX 680': 195,
                  'GeForce GTX 690': 300,
                  'GeForce GTX 550 Ti': 116,
                  'GeForce GTX 560': 150,
                  'GeForce GTX 560 SE': 150,
                  'GeForce GTX 560 Ti': 170,
                  'GeForce GTX 560 Ti 448': 210,
                  'GeForce GTX 560 Ti X2': 340,
                  'GeForce GTX 570': 219,
                  'GeForce GTX 580': 244,
                  'GeForce GTX 580 X2': 488,
                  'GeForce GTX 590': 365,
                  'GeForce GTX 460': 160,
                  'GeForce GTX 460 SE': 150,
                  'GeForce GTX 460 X2': 320,
                  'GeForce GTX 465': 200,
                  'GeForce GTX 470': 215,
                  'GeForce GTX 480': 250,
                  'GeForce GTX 260': 182,
                  'GeForce GTX 275': 219,
                  'GeForce GTX 285': 183,
                  'GeForce GTX 295': 289,
                  'GeForce GTX Titan': 250,
                  'GeForce GTX Titan Black': 250,
                  'GeForce GTX Titan X': 250,
                  'GeForce GTX Titan Z': 375,
                  'Titan X (Pascal)': 250,
                  'Titan Xp': 250,
                  'Titan V': 250,
                  'TITAN RTX': 280,
                  'GeForce GTS 250': 150,
                  'GeForce GTS 450': 106,
                  'GeForce GT 1030': 30,
                  'GeForce GT 1030 DDR4': 20,
                  'GeForce GT 220': 58,
                  'GeForce GT 430': 60,
                  'GeForce GT 440': 65,
                  'GeForce GT 520': 29,
                  'GeForce GT 610': 29,
                  'GeForce GT 620': 30,
                  'GeForce GT 630': 65,
                  'GeForce GT 640': 65,
                  'GeForce GT 710': 19,
                  'GeForce GT 720': 19,
                  'GeForce GT 730': 64,
                  'GeForce GT 740': 64,
                  'GeForce 210': 30,
                  'GeForce 7200 GS': 20,
                  'GeForce 8400 GS': 40,
                  'GeForce 8500 GT': 40,
                  'GeForce 9400 GT': 50,
                  'GeForce 9500 GT': 50,
                  'GeForce 9600 GSO': 84,
                  'GeForce 9600 GT': 95,
                  'GeForce 9800 GT': 125,
                  'GeForce 9800 GTX+': 140,
                  'GeForce FX 5200': 35,
                  'Quadro RTX 4000': 160,
                  'Quadro RTX 5000': 265,
                  'Quadro RTX 6000': 295,
                  'Quadro RTX 8000': 295,
                  'RTX 2000 Ada Generation': 70,
                  'RTX 2000E Ada Generation': 70,
                  'RTX 4000 Ada Generation': 130,
                  'RTX 4000 SFF Ada Generation': 70,
                  'RTX 4500 Ada Generation': 210,
                  'RTX 5000 Ada Generation': 250,
                  'RTX 6000 Ada Generation': 300,
                  'RTX A1000': 50,
                  'RTX A2000 6GB': 70,
                  'RTX A2000 12GB': 70,
                  'RTX A400': 50,
                  'RTX A4000': 140,
                  'RTX A4500': 200,
                  'RTX A5000': 230,
                  'RTX A5500': 230,
                  'RTX A6000': 300,
                  'Quadro P400': 30,
                  'Quadro P600': 25,
                  'Quadro P620': 25,
                  'Quadro P1000': 47,
                  'Quadro P2000': 75,
                  'Quadro P2200': 75,
                  'Quadro P4000': 105,
                  'Quadro P5000': 180,
                  'Quadro P6000': 250,
                  'Quadro M2000': 75,
                  'Quadro M4000': 120,
                  'Quadro M5000': 150,
                  'Quadro M6000': 250,
                  'Quadro K420': 41,
                  'Quadro K600': 41,
                  'Quadro K620': 45,
                  'Quadro K1200': 45,
                  'Quadro K2000': 51,
                  'Quadro K2000D': 51,
                  'Quadro K2200': 68,
                  'Quadro K4000': 80,
                  'Quadro K4000M': 100,
                  'Quadro K4200': 108,
                  'Quadro K5000': 122,
                  'Quadro K5200': 150,
                  'Quadro K6000': 225,
                  'Quadro 400': 32,
                  'Quadro 410': 32,
                  'Quadro 2000D': 62,
                  'Quadro 4000': 142,
                  'Quadro 5000': 152,
                  'Quadro 6000': 204,
                  'Quadro FX 1800': 59,
                  'Quadro GP100': 235,
                  'Quadro GV100': 250,
                  'Quadro NVS 295': 35,
                  'Quadro NVS 420': 35,
                  'Quadro NVS 450': 35,
                  'NVS 810': 68,
                  'T400  2GB': 30,
                  'T400 4GB': 30,
                  'T600': 40,
                  'T1000 4GB': 50,
                  'T1000 8GB': 50,
                  'Radeon RX 9060 XT': 160,
                  'Radeon RX 9070': 220,
                  'Radeon RX 9070 XT': 260,
                  'Radeon RX 7600': 165,
                  'Radeon RX 7600 XT': 190,
                  'Radeon RX 7700 XT': 245,
                  'Radeon RX 7800 XT': 263,
                  'Radeon RX 7900 GRE': 260,
                  'Radeon RX 7900 XT': 315,
                  'Radeon RX 7900 XTX': 355,
                  'Radeon RX 6400': 53,
                  'Radeon RX 6500 XT': 107,
                  'Radeon RX 6600': 132,
                  'Radeon RX 6600 XT': 160,
                  'Radeon RX 6650 XT': 180,
                  'Radeon RX 6700': 175,
                  'Radeon RX 6700 XT': 230,
                  'Radeon RX 6750 XT': 250,
                  'Radeon RX 6800': 250,
                  'Radeon RX 6800 XT': 300,
                  'Radeon RX 6900 XT': 300,
                  'Radeon RX 6950 XT': 335,
                  'Radeon RX 5500 XT': 130,
                  'Radeon RX 5600 XT': 150,
                  'Radeon RX 5700': 180,
                  'Radeon RX 5700 XT': 225,
                  'Radeon RX 550 - 512': 50,
                  'Radeon RX 550 - 640': 50,
                  'Radeon RX 560 - 896': 75,
                  'Radeon RX 560 - 1024': 80,
                  'Radeon RX 570': 150,
                  'Radeon RX 580': 185,
                  'Radeon RX 590': 225,
                  'Radeon RX 460': 75,
                  'Radeon RX 470': 120,
                  'Radeon RX 480': 150,
                  'Radeon RX VEGA 56': 210,
                  'Radeon RX VEGA 64': 295,
                  'Vega Frontier Edition': 300,
                  'Vega Frontier Edition Liquid': 375,
                  'Radeon VII': 300,
                  'Radeon R9 270': 150,
                  'Radeon R9 270X': 180,
                  'Radeon R9 280': 200,
                  'Radeon R9 280X': 250,
                  'Radeon R9 285': 190,
                  'Radeon R9 290': 275,
                  'Radeon R9 290X': 290,
                  'Radeon R9 295X2': 500,
                  'Radeon R9 380': 190,
                  'Radeon R9 380X': 190,
                  'Radeon R9 390': 275,
                  'Radeon R9 390X': 275,
                  'Radeon R9 390X2': 550,
                  'Radeon R9 Fury': 275,
                  'Radeon R9 Fury X': 275,
                  'Radeon R9 Nano': 175,
                  'Radeon R7 240': 30,
                  'Radeon R7 250': 65,
                  'Radeon R7 250X': 95,
                  'Radeon R7 260': 115,
                  'Radeon R7 260X': 115,
                  'Radeon R7 265': 150,
                  'Radeon R7 350': 50,
                  'Radeon R7 360': 100,
                  'Radeon R7 370': 110,
                  'Radeon R5 220': 18,
                  'Radeon R5 230': 19,
                  'Radeon HD 7750': 55,
                  'Radeon HD 7770': 80,
                  'Radeon HD 7770 GHz Edition': 80,
                  'Radeon HD 7790': 85,
                  'Radeon HD 7850': 130,
                  'Radeon HD 7870': 175,
                  'Radeon HD 7870 GHz Edition': 175,
                  'Radeon HD 7870 XT': 185,
                  'Radeon HD 7950': 200,
                  'Radeon HD 7970': 250,
                  'Radeon HD 7970 GHz Edition': 250,
                  'Radeon HD 7990': 375,
                  'Radeon HD 6450': 18,
                  'Radeon HD 6570': 44,
                  'Radeon HD 6670': 66,
                  'Radeon HD 6750': 86,
                  'Radeon HD 6770': 108,
                  'Radeon HD 6790': 150,
                  'Radeon HD 6850': 127,
                  'Radeon HD 6870': 151,
                  'Radeon HD 6870 X2': 302,
                  'Radeon HD 6950': 200,
                  'Radeon HD 6970': 250,
                  'Radeon HD 6990': 375,
                  'Radeon HD 5450': 19,
                  'Radeon HD 5550': 39,
                  'Radeon HD 5570': 39,
                  'Radeon HD 5670': 64,
                  'Radeon HD 5750': 86,
                  'Radeon HD 5770': 108,
                  'Radeon HD 5830': 175,
                  'Radeon HD 5850': 151,
                  'Radeon HD 5870': 188,
                  'Radeon HD 5870 X2': 376,
                  'Radeon HD 5970': 294,
                  'Radeon HD 3450': 30,
                  'Radeon HD 4350': 20,
                  'Radeon HD 4550': 25,
                  'Radeon HD 4650': 48,
                  'Radeon HD 4670': 59,
                  'Radeon HD 4670 X2': 118,
                  'Radeon HD 4830': 110,
                  'Radeon HD 4850': 110,
                  'Radeon HD 4870': 160,
                  'Radeon HD 4890': 190,
                  'Radeon 9550': 20,
                  'Radeon PRO W6400': 50,
                  'Radeon PRO W6600': 100,
                  'Radeon PRO W6800': 250,
                  'Radeon PRO W7500': 70,
                  'Radeon PRO W7600': 130,
                  'Radeon PRO W7700': 190,
                  'Radeon PRO W7800': 260,
                  'Radeon PRO W7900': 295,
                  'Radeon Pro WX 2100': 50,
                  'Radeon Pro WX 3100': 75,
                  'Radeon Pro WX 3200': 50,
                  'Radeon Pro WX 4100': 50,
                  'Radeon Pro WX 5100': 75,
                  'Radeon Pro WX 7100': 230,
                  'Radeon Pro WX 8200': 230,
                  'Radeon Pro WX 9100': 230,
                  'Radeon Pro Duo': 350,
                  'Radeon Pro Duo Polaris': 250,
                  'Radeon Pro VII': 250,
                  'Radeon Pro W5500': 125,
                  'Radeon Pro W5700': 205,
                  'FireGL V7300': 48,
                  'FirePro 2270': 19,
                  'FirePro 2450': 25,
                  'FirePro 2460': 25,
                  'FirePro R5000': 150,
                  'FirePro RG220A': 35,
                  'FirePro S10000': 375,
                  'FirePro S7000': 150,
                  'FirePro S9000': 150,
                  'FirePro S9050': 150,
                  'FirePro S9150': 150,
                  'FirePro V3800': 35,
                  'FirePro V3900': 50,
                  'FirePro V4900': 75,
                  'FirePro V5700': 75,
                  'FirePro V5800': 108,
                  'FirePro V5900': 108,
                  'FirePro V7750': 55,
                  'FirePro V7900': 150,
                  'FirePro V7900 SDI': 150,
                  'FirePro V8750': 150,
                  'FirePro V8800': 150,
                  'FirePro V9800': 225,
                  'FirePro W2100': 26,
                  'FirePro W4100': 50,
                  'FirePro W4300': 50,
                  'FirePro W5000': 75,
                  'FirePro W600': 75,
                  'FirePro W7000': 150,
                  'FirePro W7100': 150,
                  'FirePro W8000': 150,
                  'FirePro W8100': 150,
                  'FirePro W9000': 250,
                  'FirePro W9100': 250,
              }


def get_tdp_from_chipset(chipset: str) -> int:
    chipset_clean = chipset.strip()
    return GPU_TDP_MAP.get(chipset_clean, 150)


def normalize_gpu_name(name: str) -> str:
    return ' '.join(name.upper().split())


def load_gpu_benchmark_data(data_dir: Path) -> dict[str, int]:
    benchmarks = {}
    benchmark_path = data_dir / 'gpu_benchmarks.csv'
    if benchmark_path.exists():
        with open(benchmark_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                gpu_name = row.get('GPU Name', '').strip()
                score_str = row.get('OpenCL Score', '').strip()
                if gpu_name and score_str:
                    try:
                        score = int(score_str)
                        normalized_name = normalize_gpu_name(gpu_name)
                        benchmarks[normalized_name] = score
                    except (ValueError, TypeError):
                        continue
    return benchmarks


def _extract_gpu_core_model(name: str) -> str:
    cleaned = name
    prefixes_to_strip = ['NVIDIA', 'AMD', 'ATI', 'INTEL(R)', 'ARC(TM)', 'RADEON(TM)', 'GEFORCE', 'RADEON', 'QUADRO', 'MESA']
    changed = True
    while changed:
        changed = False
        for prefix in prefixes_to_strip:
            if cleaned.startswith(prefix + ' '):
                cleaned = cleaned[len(prefix):].strip()
                changed = True
    suffixes_to_strip = ['GRAPHICS', 'COMPUTE ENGINE', 'SERIES']
    for suffix in suffixes_to_strip:
        if cleaned.endswith(' ' + suffix):
            cleaned = cleaned[:-(len(suffix) + 1)].strip()
    return cleaned


def find_shortest_benchmark_match(
    name: str, benchmarks: dict[str, int], exclude_mobile: bool = False
) -> Optional[int]:
    pattern = re.compile(r'(?:^|(?<=\s))' + re.escape(name) + r'(?=\s|$)')
    matches = (
        key for key in benchmarks
        if pattern.search(key)
        and not (exclude_mobile and any(tag in key for tag in ('LAPTOP', 'MOBILE', 'MAX-Q')))
    )
    best_match = min(matches, key=len, default=None)
    return benchmarks[best_match] if best_match is not None else None


def find_gpu_benchmark_score(chipset: str, benchmarks: dict[str, int]) -> Optional[int]:
    normalized_chipset = normalize_gpu_name(chipset)
    candidates = [normalized_chipset]
    for prefix in ('NVIDIA ', 'AMD ', 'NVIDIA GEFORCE ', 'AMD RADEON ', 'AMD RADEON RX '):
        candidates.extend((prefix + normalized_chipset, prefix + normalized_chipset + ' GRAPHICS'))
    if normalized_chipset.startswith('ARC '):
        arc_key = 'INTEL(R) ARC(TM) ' + normalized_chipset[4:]
        candidates.extend((arc_key + ' GRAPHICS', arc_key))
    for candidate in candidates:
        if candidate in benchmarks:
            return benchmarks[candidate]

    score = find_shortest_benchmark_match(normalized_chipset, benchmarks)
    if score is not None:
        return score

    chipset_no_mem = re.sub(r'\s+\d+\s*GB$', '', normalized_chipset).strip()
    chipset_no_variant = re.sub(r'\s+(?:LHR|G5|G6)\s*$', '', normalized_chipset).strip()
    chipset_no_variant = re.sub(r'\s+\d+\s*GB\s*(?:LHR)?\s*$', '', chipset_no_variant).strip()
    chipset_core = _extract_gpu_core_model(normalized_chipset)
    variants = []
    if chipset_no_mem != normalized_chipset:
        variants.append(chipset_no_mem)
    if chipset_no_variant not in (normalized_chipset, chipset_no_mem):
        variants.append(normalize_gpu_name(chipset_no_variant))
    if chipset_core and chipset_core != normalized_chipset:
        variants.append(chipset_core)
    for variant in variants:
        score = find_shortest_benchmark_match(variant, benchmarks, exclude_mobile=True)
        if score is not None:
            return score

    for key, value in benchmarks.items():
        if _extract_gpu_core_model(key) in (chipset_core, normalized_chipset):
            return value
    return None


def load_gpu_data():
    csv_path = Path(__file__).parent.parent / 'data' / 'video-card.csv'
    if not csv_path.exists():
        return
    gpu_benchmarks = load_gpu_benchmark_data(csv_path.parent)
    create_db_and_tables()
    with Session(engine) as session:
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        chipset = (row.get('chipset') or '').strip()
                        if not chipset:
                            continue
                        gpu_name = chipset
                        brand = infer_brand_from_chipset(chipset)
                        vram_gb = parse_int(row.get('memory'), strict=True)
                        csv_name = (row.get('name') or '').strip()
                        model = extract_model_from_name(csv_name, chipset) if csv_name else None
                        tdp = get_tdp_from_chipset(chipset)
                        benchmark_score = find_gpu_benchmark_score(chipset, gpu_benchmarks)
                        existing: Optional[GPU] = session.scalars(select(GPU).where(GPU.name == gpu_name)).first()
                        if existing:
                            continue
                        price = parse_price(row.get('price'))
                        gpu = GPU(
                            name=gpu_name,
                            brand=brand,
                            model=model,
                            vram_gb=vram_gb,
                            benchmark_score=benchmark_score,
                            tdp=tdp,
                            price=price,
                        )
                        session.add(gpu)
                    except Exception:
                        continue
            session.commit()
        except Exception:
            session.rollback()
            raise
