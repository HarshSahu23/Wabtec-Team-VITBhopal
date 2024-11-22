import os
import logging
import pandas as pd
from backend.utils.file_types import FileClasses

class FileClassifier:
    @staticmethod
    def get_file_class(file_path):
        """
        Determine file class with more robust type detection.
        
        Args:
            file_path (str): Path to the CSV file
        
        Returns:
            FileClasses: Detected file class
        """
        try:
            # Validate file existence and readability
            if not os.path.exists(file_path):
                logging.warning(f"File does not exist: {file_path}")
                return FileClasses.UNKNOWN
            
            if not os.access(file_path, os.R_OK):
                logging.warning(f"Cannot read file: {file_path}")
                return FileClasses.UNKNOWN

            # Read with error handling
            try:
                df = pd.read_csv(file_path, nrows=50, low_memory=False)
            except Exception as e:
                logging.error(f"Error reading file {file_path}: {e}")
                return FileClasses.UNKNOWN

            file_type_and_col_names = {
                FileClasses.ECL_ECF: ["ERROR CODE LISTING", "Code(hex)", "Ticks(hex)"],
                FileClasses.DMP_LOG: ["MOD_TICK", "MONTIME"]
            }

            # Strict and sensitive column matching
            for column_name in df.columns:
                for file_class, column_list in file_type_and_col_names.items():
                    if any(col in column_name for col in column_list):
                        return file_class
            
            return FileClasses.UNKNOWN

        except Exception as e:
            logging.error(f"Unexpected error in file classification: {e}")
            return FileClasses.UNKNOWN

