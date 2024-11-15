import os
import pandas as pd
from collections import defaultdict
from colorama import init, Fore, Style

class ErrorAnalyzer:
    def __init__(self):
        init()  # Initialize colorama for Windows support
        self.error_frequencies = defaultdict(int)
        self.error_codes = {}  # To store error code mappings
        
    def get_user_expected_errors(self):
        """Get expected error descriptions from user"""

        """ A) Reading from console """
        # print("Enter expected error descriptions (one per line)")
        # print("Press Enter twice when done:")
        # expected_errors = set()
        # while True:
        #     line = input().strip().upper()
        #     if not line:
        #         break
        #     expected_errors.add(line)
        # return expected_errors

        """ B) Reading from text file """
        expected_errors = set()
        try:
            with open('src\\data\\inputErrorList.txt', 'r') as file:
                for line in file:
                    error = line.strip().upper()
                    if error:  # Skip empty lines
                        expected_errors.add(error)
            
            # Print errors in grid format
            print("\nErrors read from the user input:\n")
            errors_list = sorted(list(expected_errors))
            width = 20
            for i in range(0, len(errors_list), 5):
                chunk = errors_list[i:i+5]
                print(Fore.LIGHTBLACK_EX + ''.join(f"{error:<{width}}" for error in chunk) + Style.RESET_ALL)
            
            return expected_errors
        except FileNotFoundError:
            print("Error: expected_errors.txt not found")
            return set()

    
    def process_csv_file(self, filepath):
        """Process a single CSV file and extract error information"""
        try:
            # Read the file content
            with open(filepath, 'r') as file:
                lines = file.readlines()
            
            # Find the start of error listings
            start_idx = -1
            for idx, line in enumerate(lines):
                if "Nr;Code(hex)" in line:
                    start_idx = idx + 1
                    break
            
            if start_idx == -1:
                print(f"Warning: Could not find error listings in {filepath}")
                return
            
            # Process error entries until empty line or error frequency section
            for line in lines[start_idx:]:
                if line.strip() == '' or '|---' in line:
                    break
                
                parts = line.strip().split(';')
                if len(parts) >= 2:
                    code = parts[1].strip()
                    description = parts[-1].strip().upper()
                    
                    # Store error code mapping
                    self.error_codes[description] = code
                    # Increment frequency
                    self.error_frequencies[description] += 1
                    
        except Exception as e:
            print(f"Error processing {filepath}: {str(e)}")
    
    def analyze_folder(self, folder_path):
        """Process all CSV files in the given folder"""
        print("folder_pat = ",folder_path)
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                filepath = os.path.join(folder_path, filename)
                self.process_csv_file(filepath)
    
    def display_results(self, expected_errors):
        """Display analysis results with color coding"""
        # Prepare categorized results
        expected_seen = []
        expected_not_seen = []
        unexpected_seen = []
        
        # Categorize all errors
        for desc in expected_errors:
            if desc in self.error_frequencies:
                expected_seen.append((self.error_codes.get(desc, 'XXXX'), desc, self.error_frequencies[desc]))
            else:
                expected_not_seen.append(('XXXX', desc, 0))
                
        for desc in self.error_frequencies:
            if desc not in expected_errors:
                unexpected_seen.append((self.error_codes.get(desc, 'XXXX'), desc, self.error_frequencies[desc]))
        
        # Sort each category
        expected_seen.sort(key=lambda x: x[1])
        expected_not_seen.sort(key=lambda x: x[1])
        unexpected_seen.sort(key=lambda x: x[1])
        
        #Output formatting
        code_width = 8
        desc_width = 25
        freq_width = 4
        # Display results
        print("\n===================== Error Analysis Results =====================")
        
        # print("\nExpected and Seen Errors:")
        for code, desc, freq in expected_seen:
            print(f"{Style.NORMAL}{code:<{code_width}} {desc:<{desc_width}} {freq:>{freq_width}}")
            
        # print("\nExpected but Not Seen Errors:")
        for code, desc, freq in expected_not_seen:
            print(f"{Fore.BLUE}{code:<{code_width}} {desc:<{desc_width}} {freq:>{freq_width}}{Style.RESET_ALL}")
            
        # print("\nUnexpected but Seen Errors:")
        for code, desc, freq in unexpected_seen:
            print(f"{Fore.YELLOW}{code:<{code_width}} {desc:<{desc_width}} {freq:>{freq_width}}{Style.RESET_ALL}")
        
        # Print summary
        print(f"\n===================== Summary =====================")
        print(f"Total expected errors:     {len(expected_errors):>3}")
        print(f"Expected errors found:     {len(expected_seen):>3}")
        print(f"{Fore.BLUE}Expected errors not found: {len(expected_not_seen):>3}")
        print(f"{Fore.YELLOW}Unexpected errors found:   {len(unexpected_seen):>3}")

def main():
    # Initialize analyzer
    analyzer = ErrorAnalyzer()
    
    # Get folder path
    folder_path = "D:\\Harsh Data\\Coding\\Hackathon\\Wabtec Team VITBhopal\\resources\\csv\\"
    # folder_path = input("Enter the folder path containing CSV files: ").strip()
    
    # Validate folder path
    if not os.path.exists(folder_path):
        print("Error: Folder path does not exist!")
        return
    
    # Get expected errors from user
    expected_errors = analyzer.get_user_expected_errors()
    
    # Process all CSV files
    analyzer.analyze_folder(folder_path)
    
    # Display results
    analyzer.display_results(expected_errors)

if __name__ == "__main__":
    main()

# >=
# <=
# ==
# ===
# ->
# <->
# !=
# 
