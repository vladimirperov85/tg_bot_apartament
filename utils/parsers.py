def parse_positive_float(text):
    """Преобразует строку в положительное дробное число"""

    try:
        value = float(text.strip().replace(',', '.'))
    except ValueError:
        return None
    return value if value > 0 else None


def parse_positive_int(text):
    """Преобразует строку в положительное целое число"""

    try:
        value = int(text.strip())
    except ValueError:
        return None
    return value if value > 0 else None