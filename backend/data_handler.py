import glob
import pandas as pd
import logging
from tqdm import tqdm
from backend.utils.logging_config import configure_logging
from backend.utils.exceptions import FileProcessingError
from backend.utils.folder_validator import FolderValidator
from backend.utils.file_classifier import FileClassifier
from backend.utils.file_types import FileClasses
from backend.data_processors.ecl_processor import ECLProcessor
from backend.data_processors.ecf_processor import ECFProcessor
from backend.data_processors.dmp_processor import DMPProcessor
from backend.data_processors.ecl_error_grouper import ECLErrorGrouper

class DataHandler:
    def __init__(self, folder_path):
        """
        Initialize DataHandler with robust folder path validation.
        
        Args:
            folder_path (str): Path to the folder containing CSV files
        
        Raises:
            FileNotFoundError: If the folder does not exist
            PermissionError: If there are permission issues accessing the folder
        """
        configure_logging()
        try:
            # Validate folder path
            FolderValidator.validate_folder(folder_path)
            
            self.__folder_path = folder_path
            self.ecl = pd.DataFrame()
            self.grouped_ecl = pd.DataFrame()  # New attribute for grouped ECL
            self.ecf = pd.DataFrame()
            self.dmp = pd.DataFrame()
            self.ecl_freq_summary = pd.DataFrame()
            self.filtered_dmp = pd.DataFrame()
            self.dmp_freq_summary = pd.Series()
            
            # Set csv folder
            self.set_folder(folder_path)
            
        except (FileNotFoundError, PermissionError, NotADirectoryError) as e:
            logging.error(f"Initialization error: {e}")
            raise

    def __read_csv_from_folder(self, folder_path):
        """
        Read and merge CSV files from folder with comprehensive error handling.
        
        Args:
            folder_path (str): Path to the folder containing CSV files
        
        Returns:
            tuple: Merged ECL, ECF, and DMP dataframes
        """
        merged_df_ecl = pd.DataFrame()
        merged_df_ecf = pd.DataFrame()
        merged_dmp = pd.DataFrame()

        try:
            csv_files = glob.glob(f"{folder_path}/*.csv")
            
            if not csv_files:
                logging.warning(f"No CSV files found in folder: {folder_path}")
                return merged_df_ecl, merged_df_ecf, merged_dmp

            for csv_file_path in tqdm(csv_files, desc="Reading Files"):
                try:
                    file_type = FileClassifier.get_file_class(csv_file_path)
                    
                    if file_type == FileClasses.ECL_ECF:
                        df_ecl, df_ecf = self.__read_ecl_ecf_file(csv_file_path)
                        
                        if not df_ecl.empty:
                            merged_df_ecl = pd.concat([merged_df_ecl, df_ecl])
                        if not df_ecf.empty:
                            merged_df_ecf = pd.concat([merged_df_ecf, df_ecf])
                    
                    elif file_type == FileClasses.DMP_LOG:
                        df_dmp = DMPProcessor.read_dmp(csv_file_path)
                        
                        if not df_dmp.empty:
                            merged_dmp = pd.concat([merged_dmp, df_dmp])
                    
                    else:
                        logging.warning(f"Skipping unrecognized file: {csv_file_path}")

                except Exception as file_error:
                    logging.error(f"Error processing file {csv_file_path}: {file_error}")
                    continue

            # Reset indices
            merged_df_ecf.reset_index(drop=True, inplace=True)
            merged_df_ecl.reset_index(drop=True, inplace=True)
            merged_dmp.reset_index(drop=True, inplace=True)

            return merged_df_ecl, merged_df_ecf, merged_dmp

        except Exception as e:
            logging.error(f"Unexpected error reading CSV files: {e}")
            return merged_df_ecl, merged_df_ecf, merged_dmp

    def __read_ecl_ecf_file(self, file_path):
        """
        Read and format ECL and ECF from CSV with robust error handling.
        
        Args:
            file_path (str): Path to the CSV file
        
        Returns:
            tuple: Formatted ECL and ECF dataframes
        """
        try:
            data = pd.read_csv(file_path, low_memory=False)

            if data.empty:
                logging.warning(f"Empty dataframe from file: {file_path}")
                return pd.DataFrame(), pd.DataFrame()

            ecf_indices = data[data.iloc[:, 0].str.contains("ERROR CODE FREQUENCY", na=False)].index
            if len(ecf_indices) == 0:
                logging.warning(f"No ECF section found in file: {file_path}")
                return pd.DataFrame(), pd.DataFrame()

            ecf_index = ecf_indices[0]

            df_ecl = ECLProcessor.format_ecl(data.iloc[0:ecf_index, ])
            df_ecf = ECFProcessor.format_ecf(data.iloc[ecf_index:, ])

            return df_ecl, df_ecf

        except Exception as e:
            logging.error(f"Error processing ECL/ECF file {file_path}: {e}")
            return pd.DataFrame(), pd.DataFrame()

    def set_folder(self, folder_path):
        """
        Set folder and process files with comprehensive error handling.
        
        Args:
            folder_path (str): Path to the folder containing CSV files
        """
        try:
            self.__folder_path = folder_path
            self.ecl, self.ecf, self.dmp = self.__read_csv_from_folder(self.__folder_path)
            
            if self.ecl.empty:
                logging.warning("No ECL data processed")
            else:
                # Group ECL errors
                self.grouped_ecl = ECLErrorGrouper.group_errors(self.ecl)
                
                # Log grouped ECL data summary
                self._log_grouped_ecl_summary()

            if self.ecf.empty:
                logging.warning("No ECF data processed")
            if self.dmp.empty:
                logging.warning("No DMP data processed")

            self.ecl_freq_summary = ECLProcessor.get_frequency_summary(self.ecl)
            self.filtered_dmp = DMPProcessor.filter_dmp(self.dmp)
            self.dmp_freq_summary = DMPProcessor.get_frequency_summary(self.filtered_dmp)
            self.dmp_freq_summary = DMPProcessor.get_frequency_summary(self.filtered_dmp)
            
        except Exception as e:
            logging.error(f"Error setting folder: {e}")
            self._reset_state()
    
    def _log_grouped_ecl_summary(self):
        """
        Log a summary of grouped ECL errors with detailed statistics.
        """
        try:
            # Error Group Distribution
            print("\n--- Error Group Distribution ---")
            group_counts = self.grouped_ecl['Error Group'].value_counts()
            for group, count in group_counts.items():
                print(f"{group}: {count} errors")

            # Top 10 most frequent errors
            print("\n--- Top 10 Most Frequent Errors ---")
            error_freq = self.grouped_ecl['Description'].value_counts().head(10)
            for error, count in error_freq.items():
                error_group = self.grouped_ecl[self.grouped_ecl['Description'] == error]['Error Group'].iloc[0]
                print(f"{error} (Group: {error_group}): {count} occurrences")

            # Unique error groups
            unique_groups = self.grouped_ecl['Error Group'].unique()
            print(f"\nTotal Unique Error Groups: {len(unique_groups)}")
            print("Error Groups:", ", ".join(unique_groups))

        except Exception as e:
            logging.error(f"Error logging grouped ECL summary: {e}")

    def _reset_state(self):
        """Reset instance variables to empty state."""
        self.ecl = pd.DataFrame()
        self.grouped_ecl = pd.DataFrame()  # Add reset for grouped_ecl
        self.ecf = pd.DataFrame()
        self.dmp = pd.DataFrame()
        self.filtered_dmp = pd.DataFrame()
        self.dmp_freq_summary = pd.Series()

    def get_folder(self):
        """Get current folder path."""
        return self.__folder_path

# main.py
if __name__ == "__main__":
    try:
        folder_path = "csv"
        FolderValidator.validate_folder(folder_path)
        
        dh = DataHandler(folder_path)
        
        # Print processing results
        print("Data processed successfully.")
        print(f"ECL Rows: {len(dh.ecl)}")
        print(f"Grouped ECL Rows: {len(dh.grouped_ecl)}")
        print(f"ECF Rows: {len(dh.ecf)}")
        print(f"DMP Rows: {len(dh.dmp)}")
        
        if not dh.dmp_freq_summary.empty:
            print("\nDMP Frequency Summary:")
            print(f"\tIndices: {dh.dmp_freq_summary.index}")
            print(f"\tValues: {dh.dmp_freq_summary.values}")
        
    except Exception as e:
        logging.error(f"Critical error in main execution: {e}")
        print("Data processing failed. Check logs for details.")
