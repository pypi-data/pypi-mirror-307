import time
import sys

def gradual_print(text, delay=0.1):
    """Print text gradually with a delay between characters."""
    try:
        if delay < 0:
            raise ValueError("Delay must be a non-negative value.")
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()  # Newline at the end
    except ValueError as e:
        print(f"Error in gradual print: {e}")
        print(text)

def blinking_text(text, times=3, delay=0.5):
    """Print text with a blinking effect."""
    try:
        if delay < 0:
            raise ValueError("Delay must be a non-negative value.")
        for _ in range(times):
            sys.stdout.write("\r" + text)
            sys.stdout.flush()
            time.sleep(delay)
            sys.stdout.write("\r" + " " * len(text))  # Clear the text temporarily
            sys.stdout.flush()
            time.sleep(delay)
        print("\r" + text)  # Final stable text
    except ValueError as e:
        print(f"Error in blinking text: {e}")
        print(text)
