def next_ch(text, cursor):
    while cursor < len(text) and text[cursor].isspace():
        cursor += 1
    if cursor >= len(text):
        return '', cursor
    return text[cursor], cursor

def parse_string(text, cursor):
    if text[cursor] != '"':
        raise ValueError("Expected '\"'")
    cursor += 1  # skip opening quote
    start = cursor
    while cursor < len(text) and text[cursor] != '"':
        cursor += 1
    if cursor == len(text):
        raise ValueError("Unterminated string")
    return text[start:cursor], cursor + 1  # skip closing quote

def parse_number(text, cursor):
    start = cursor
    if text[cursor] == '-':
        cursor += 1
    while cursor < len(text) and text[cursor].isdigit():
        cursor += 1
    if start == cursor or (text[start] == '-' and cursor == start + 1):
        raise ValueError("Invalid number")
    return float(text[start:cursor]), cursor

def parse_boolean(text, cursor):
    if text[cursor:].startswith("true"):
        return True, cursor + 4
    elif text[cursor:].startswith("false"):
        return False, cursor + 5
    raise ValueError("Invalid boolean")

def parse_list(text, cursor):
    if text[cursor] != '[':
        raise ValueError("Expected '['")
    cursor += 1
    items = []

    while True:
        ch, cursor = next_ch(text, cursor)
        if ch == ']':
            return items, cursor + 1
        item, cursor = parse_item(text, cursor)
        items.append(item)
        ch, cursor = next_ch(text, cursor)
        if ch == ',':
            cursor += 1
        elif ch == ']':
            continue
        else:
            raise ValueError(f"Expected ',' or ']', got '{ch}'")

def parse_dict(text, cursor):
    if text[cursor] != '{':
        raise ValueError("Expected '{'")
    cursor += 1
    items = {}

    while True:
        ch, cursor = next_ch(text, cursor)
        if ch == '}':
            return items, cursor + 1
        key, cursor = parse_string(text, cursor)
        ch, cursor = next_ch(text, cursor)
        if ch != ':':
            raise ValueError("Expected ':' after key")
        cursor += 1  # skip ':'
        value, cursor = parse_item(text, cursor)
        items[key] = value
        ch, cursor = next_ch(text, cursor)
        if ch == ',':
            cursor += 1
        elif ch == '}':
            continue
        else:
            raise ValueError(f"Expected ',' or '}}', got '{ch}'")

def parse_item(text, cursor):
    ch, _ = next_ch(text, cursor)
    if ch == '"':
        return parse_string(text, cursor)
    elif ch == '{':
        return parse_dict(text, cursor)
    elif ch == '[':
        return parse_list(text, cursor)
    elif ch == '-' or ch.isdigit():
        return parse_number(text, cursor)
    elif text[cursor:].startswith("true") or text[cursor:].startswith("false"):
        return parse_boolean(text, cursor)
    else:
        raise ValueError(f"Unexpected character: {ch}")

def json(text):
    value, cursor = parse_item(text, 0)
    ch, cursor = next_ch(text, cursor)
    if cursor < len(text):
        raise ValueError("Extra data after JSON value")
    return value
