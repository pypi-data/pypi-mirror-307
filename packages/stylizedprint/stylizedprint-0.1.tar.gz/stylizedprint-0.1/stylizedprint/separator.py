class LineSeparator:
    def __init__(self, separator_type="plain"):
        """
        Initializes the LineSeparator with a specific type.
        
        Args:
            separator_type (str): Type of separator. Options are:
                                  - "plain": newline character (`\n`)
                                  - "html": HTML line break (`<br>`)
                                  - "custom": custom separator string
        """
        self.separator_type = separator_type
        self.custom_separator = "\n"  # Default custom separator

    def set_custom_separator(self, custom_separator):
        """
        Sets a custom separator string.
        
        Args:
            custom_separator (str): The custom separator string.
        """
        self.custom_separator = custom_separator
        self.separator_type = "custom"

    def get_separator(self):
        """
        Returns the appropriate separator based on the separator type.
        
        Returns:
            str: The line separator.
        """
        if self.separator_type == "plain":
            return "\n"
        elif self.separator_type == "html":
            return "<br>"
        elif self.separator_type == "custom":
            return self.custom_separator
        else:
            raise ValueError(f"Invalid separator type: {self.separator_type}")

    def join_lines(self, *lines):
        """
        Joins multiple lines with the selected separator.
        
        Args:
            *lines: List of lines to join.

        Returns:
            str: The joined string with the specified separator between lines.
        """
        separator = self.get_separator()
        return separator.join(lines)
