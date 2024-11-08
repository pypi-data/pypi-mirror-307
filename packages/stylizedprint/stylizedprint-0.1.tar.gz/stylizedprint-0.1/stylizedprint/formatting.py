def justify_text(text, alignment="center", width=50):
    """Justify text to the left, center, or right within a given width."""
    try:
        if alignment not in {"left", "center", "right"}:
            raise ValueError("Alignment must be 'left', 'center', or 'right'.")
        if alignment == "left":
            return text.ljust(width)
        elif alignment == "right":
            return text.rjust(width)
        elif alignment == "center":
            return text.center(width)
    except ValueError as e:
        print(f"Error in text justification: {e}. Defaulting to center alignment.")
        return text.center(width)
