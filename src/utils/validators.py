import re

def validate_form(raw: str) -> bool:
    pattern = r"^(?:1[0-2]|[1-9])-[А-ЯІЇЄҐ]$"
    return bool(re.fullmatch(pattern, raw))

def validate_name(raw: str) -> bool:
    pattern = r"^[А-ЯІЇЄҐ][а-яіїєґ']+ [А-ЯІЇЄҐ][а-яіїєґ']+ [А-ЯІЇЄҐ][а-яіїєґ']+$"
    return bool(re.fullmatch(pattern, raw))

def is_positive_int(value: str) -> bool:
    return value.isdigit()
