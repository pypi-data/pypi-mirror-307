from stylizedprint.colors import apply_color
from stylizedprint.styles import apply_style
from stylizedprint.borders import add_border
from stylizedprint.animations import gradual_print, blinking_text
from stylizedprint.formatting import justify_text
from stylizedprint.utils import print_with_time
from stylizedprint.separator import LineSeparator
from rich.console import Console

console = Console()

class StylizedPrinter:
    def __init__(self, text):
        self.text = text

    def print_colored(self, text_color=None, bg_color=None):
        try:
            colored_text = apply_color(self.text, text_color, bg_color)
            print(colored_text)
        except Exception as e:
            print(f"Error in print_colored: {e}")

    def print_styled(self, bold=False, italic=False, underline=False, strikethrough=False):
        try:
            styled_text = apply_style(self.text, bold, italic, underline, strikethrough)
            console.print(styled_text)
        except Exception as e:
            print(f"Error in print_styled: {e}")

    def print_with_border(self, border_char="*"):
        try:
            bordered_text = add_border(self.text, border_char)
            print(bordered_text)
        except Exception as e:
            print(f"Error in print_with_border: {e}")

    def print_gradually(self, delay=0.1):
        try:
            gradual_print(self.text, delay)
        except Exception as e:
            print(f"Error in print_gradually: {e}")

    def print_blinking(self, times=3, delay=0.5):
        try:
            blinking_text(self.text, times, delay)
        except Exception as e:
            print(f"Error in print_blinking: {e}")

    def print_justified(self, alignment="center", width=50):
        try:
            justified_text = justify_text(self.text, alignment, width)
            print(justified_text)
        except Exception as e:
            print(f"Error in print_justified: {e}")

    def print_with_timestamp(self):
        try:
            print_with_time(self.text)
        except Exception as e:
            print(f"Error in print_with_timestamp: {e}")
            
    def print_with_separator(self, separator_type="plain", *lines, custom_separator=None):
        """
        Prints multiple lines with a chosen separator type.

        Args:
            separator_type (str): Type of separator (plain, html, custom).
            *lines: Lines of text to join and print.
            custom_separator (str): Custom separator if separator_type is "custom".
        """
        separator = LineSeparator(separator_type)
        if custom_separator:
            separator.set_custom_separator(custom_separator)
        joined_text = separator.join_lines(*lines)
        print(joined_text)