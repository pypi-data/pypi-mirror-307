from rich.text import Text

def apply_style(text, bold=False, italic=False, underline=False, strikethrough=False):
    """Apply text style (bold, italic, underline, strikethrough) using rich."""
    styled_text = Text(text)
    try:
        if bold:
            styled_text.stylize("bold")
        if italic:
            styled_text.stylize("italic")
        if underline:
            styled_text.stylize("underline")
        if strikethrough:
            styled_text.stylize("strike")
    except Exception as e:
        print(f"Error applying style: {e}")
    return styled_text
