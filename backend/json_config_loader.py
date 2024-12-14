import json

class JSONConfigReader:
    def __init__(self, json_input):
        """
        Initialize the ErrorLogReader with a JSON file path or JSON data as a string/dictionary.
        """
        if isinstance(json_input, str):
            try:
                # Try loading as a file path
                with open(json_input, 'r') as file:
                    self.data = json.load(file)
            except FileNotFoundError:
                # If not a valid file, try parsing as a JSON string
                self.data = json.loads(json_input)
        elif isinstance(json_input, dict):
            self.data = json_input
        else:
            raise ValueError("Input must be a file path, JSON string, or dictionary.")

    def get_error_log_tab(self):
        """
        Retrieve the ERROR_LOG_TAB section.
        """
        return self.data.get("ERROR_LOG_TAB", {})

    def get_summary_tab(self):
        """
        Retrieve the SUMMARY_TAB section.
        """
        return self.data.get("SUMMARY_TAB", {})

    def get_fill_vent_pairs(self):
        """
        Retrieve the FILL_VENT_PAIRS section.
        """
        return self.data.get("FILL_VENT_PAIRS", {})

    def get_error_description(self):
        """
        Retrieve the ERROR_DESCRIPTION section.
        """
        return self.data.get("ERROR_DESCRIPTION", "")

    def get_section(self, section_name):
        """
        Retrieve a specific section by name.
        """
        return self.data.get(section_name, None)


# Example usage
if __name__ == "__main__":
    # Example file path
    json_file_path = "path_to_your_file.json"  # Replace with your actual file path
    
    # Initialize the reader with a file path
    reader = JSONConfigReader(json_file_path)
    
    print("ERROR_LOG_TAB:", reader.get_error_log_tab())
    print("SUMMARY_TAB:", reader.get_summary_tab())
    print("FILL_VENT_PAIRS:", reader.get_fill_vent_pairs())
    print("ERROR_DESCRIPTION:", reader.get_error_description())
