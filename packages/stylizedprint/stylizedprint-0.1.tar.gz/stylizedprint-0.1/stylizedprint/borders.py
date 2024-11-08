def add_border(text, border_char="*"):
    """Add a border around the text with the specified character."""
    try:
        if len(border_char) != 1:
            raise ValueError("Border character must be a single character, e.g. '*' or '#'.")
        border_line = border_char * (len(text) + 4)
        return f"{border_line}\n{border_char} {text} {border_char}\n{border_line}"
    except ValueError as e:
        print(f"Error applying border: {e}. Using '*' as default border character.")
        border_line = "*" * (len(text) + 4)
        return f"{border_line}\n* {text} *\n{border_line}"
