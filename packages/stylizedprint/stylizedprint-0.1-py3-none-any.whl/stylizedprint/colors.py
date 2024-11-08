from colorama import Fore, Back

def apply_color(text, text_color=None, bg_color=None):
    """Apply color to the text and background using colorama."""
    colors = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "blue": Fore.BLUE,
        "yellow": Fore.YELLOW,
        "cyan": Fore.CYAN,
        "magenta": Fore.MAGENTA,
        "white": Fore.WHITE,
        "black": Fore.BLACK,
    }
    bg_colors = {
        "red": Back.RED,
        "green": Back.GREEN,
        "blue": Back.BLUE,
        "yellow": Back.YELLOW,
        "cyan": Back.CYAN,
        "magenta": Back.MAGENTA,
        "white": Back.WHITE,
        "black": Back.BLACK,
    }

    # Error handling
    try:
        color_text = colors.get(text_color, "")
        color_bg = bg_colors.get(bg_color, "")
        if not color_text and text_color:
            raise ValueError(f"Invalid text color: {text_color}")
        if not color_bg and bg_color:
            raise ValueError(f"Invalid background color: {bg_color}")
        return f"{color_text}{color_bg}{text}"
    except ValueError as e:
        print(f"Error applying color: {e}")
        return text