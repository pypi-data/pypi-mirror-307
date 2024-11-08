from datetime import datetime

def print_with_time(text):
    """Print text with a timestamp."""
    try:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        print(f"{timestamp} {text}")
    except Exception as e:
        print(f"Error in printing with timestamp: {e}")
        print(text)
