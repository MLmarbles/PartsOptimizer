def parse_price(value: str | None) -> float | None:
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def parse_int(value: str | None, *, strict: bool = False) -> int:
    try:
        return int(value) if value and value.strip() else 0
    except (ValueError, TypeError):
        if strict:
            raise
        return 0
