import glob
import pandas as pd
import logging
from tqdm import tqdm
from backend.utils.logging_config import configure_logging
from backend.utils.folder_validator import FolderValidator
from backend.data_extractor.dataframe_classifier import DataFrameClassifier, DataFrameClasses
from backend.data_processors.ecl_processor import ECLProcessor
from backend.data_processors.dmp_processor import DMPProcessor
from backend.data_extractor.dataframe_extractor import DataFrameExtractor
from backend.json_config_loader import JSONConfigReader
from backend.data_processors.error_grouper_for_error_log_tab import get_error_groups
from backend.data_processors.table_maker_for_summary_tab import get_tables
from backend.data_processors.detailed_data_for_error_grouper import get_detailed_data_for_error_groups

class DataHandler:
    def __init__(self, folder_path, json_config_path):
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
            self.dmp = pd.DataFrame()
            self.ecl_freq_summary = pd.DataFrame()
            self.filtered_dmp = pd.DataFrame()
            self.dmp_freq_summary = pd.Series()
            self.jcr = JSONConfigReader(json_config_path)
            self.error_grps = dict()
            self.tables = dict()
            self.fill_vent_events = {}
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
            tuple: Merged ECL and DMP dataframes
        """
        merged_ecl = pd.DataFrame()
        merged_dmp = pd.DataFrame()
        try:
            csv_files = glob.glob(f"{folder_path}/*.csv")
            logging.info(f'CSV Files found: {csv_files}')

            if len(csv_files) == 0 or csv_files == None:
                logging.warning(f"No CSV files found in folder: {folder_path}")
                return merged_ecl, merged_dmp

            for csv_file_path in tqdm(csv_files, desc="Reading Files"):
                try:
                    df = DataFrameExtractor.get_df_from_file(csv_file_path)
                    df_type = DataFrameClassifier.get_dataframe_class(df)
                    # print(df)
                    if df_type == DataFrameClasses.ECL:
                        if not df.empty:
                            # print("ECL file Processed")
                            merged_ecl = pd.concat([merged_ecl, df])
                    elif df_type == DataFrameClasses.DMP:
                        if not df.empty:
                            # print("DMP file Processed")
                            merged_dmp = pd.concat([merged_dmp, df])
                    else:
                        logging.warning(f"Skipping unrecognized file: {csv_file_path}")

                except Exception as file_error:
                    logging.error(f"Error processing file {csv_file_path}: {file_error}")
                    continue

            # Reset indices
            merged_ecl.reset_index(drop=True, inplace=True)
            merged_dmp.reset_index(drop=True, inplace=True)

            return merged_ecl, merged_dmp

        except Exception as e:
            logging.error(f"Unexpected error reading CSV files: {e}")
            return merged_ecl, merged_dmp

    def set_folder(self, folder_path):
        """
        Set folder and process files with comprehensive error handling.
        
        Args:
            folder_path (str): Path to the folder containing CSV files
        """
        try:
            FolderValidator.validate_folder(folder_path)
            self.__folder_path = folder_path
            logging.info(f'Reading files from path: {folder_path}')
            self.ecl, self.dmp = self.__read_csv_from_folder(self.__folder_path)
            
            if self.ecl.empty:
                logging.warning("No ECL data processed")
            if self.dmp.empty:
                logging.warning("No DMP data processed")


            self.ecl_freq_summary = ECLProcessor.get_frequency_summary(self.ecl, self.jcr)
            self.filtered_dmp = DMPProcessor.filter_dmp(self.dmp, self.jcr)
            self.dmp_freq_summary = DMPProcessor.get_frequency_summary(self.filtered_dmp)
            self.error_grps = get_error_groups(self.jcr, self.ecl_freq_summary)
            self.error_group_details = get_detailed_data_for_error_groups(self.ecl, self.error_grps)
            self.tables = get_tables(self.ecl_freq_summary, self.jcr)
            self.fill_vent_events = DMPProcessor.process_fill_vent_events(self.dmp)
            # self.print_report()
            # print(self.filtered_dmp)
            
        except Exception as e:
            logging.error(f"Error setting folder: {e}")
            self._reset_state()

    def _reset_state(self):
        """Reset instance variables to empty state."""
        self.ecl = pd.DataFrame()
        self.dmp = pd.DataFrame()
        self.ecl_freq_summary = pd.DataFrame()
        self.filtered_dmp = pd.DataFrame()
        self.dmp_freq_summary = pd.Series()
        # self.jcr = JSONConfigReader(json_config_path)
        self.error_grps = dict()
        self.tables = dict()

    def get_folder(self):
        """Get current folder path."""
        return self.__folder_path

    def print_report(self, output_file='data_processing_report.log'):
        """
        Generate a detailed report of processed data and write it to a text file.

        Args:
            output_file (str): The file path to write the report to.
        """
        report_lines = []
        report_lines.append("=" * 20 + "DATA PROCESSING REPORT" + "=" * 20)
        
        report_lines.append("\nDATA SUMMARY:")
        report_lines.append(f"ECL Dataset: {len(self.ecl)} rows")
        report_lines.append(f"DMP Dataset: {len(self.dmp)} rows")
        report_lines.append(f"Filtered DMP Dataset: {len(self.filtered_dmp)} rows")
        
        if not self.ecl_freq_summary.empty:
            report_lines.append("\nECL FREQUENCY SUMMARY:")
            report_lines.append(str(self.ecl_freq_summary))
        
        if not self.dmp_freq_summary.empty:
            report_lines.append("\nDMP FREQUENCY SUMMARY:")
            report_lines.append(str(self.dmp_freq_summary))
        
        report_lines.append("\nPROCESSING STATUS:")
        status = ""
        status += "\nECL: " + ("SUCCESS" if not self.ecl.empty else "FAIL")
        status += "\nDMP: " + ("SUCCESS" if not self.dmp.empty else "FAIL")
        report_lines.append("OVERALL STATUS")
        report_lines.append(status)
        
        # Add detailed data about fill_vent_events
        report_lines.append("\nFILL VENT EVENTS:")
        if self.fill_vent_events:
            for event, details in self.fill_vent_events.items():
                report_lines.append(f"\nEvent: {event}")
                report_lines.append(str(details))
        else:
            report_lines.append("No fill vent events processed.")
        
        # Write report to file
        try:
            with open(output_file, 'w') as file:
                file.write('\n'.join(report_lines))
            logging.info(f"Report written to {output_file}")
        except Exception as e:
            logging.error(f"Failed to write report to file: {e}")

    def get_detailed_data_for_group(self, group_name):
        return self.error_group_details.get(group_name, pd.DataFrame())


# main.py
if __name__ == "__main__":
    try:
        folder_path = "csv"
        FolderValidator.validate_folder(folder_path)
        
        dh = DataHandler(folder_path)
        
        # Print processing results
        print("Data processed successfully.")
        print(f"ECL Rows: {len(dh.ecl)}")
        print(f"DMP Rows: {len(dh.dmp)}")
        
        if not dh.dmp_freq_summary.empty:
            print("\nDMP Frequency Summary:")
            print(f"\tIndices: {dh.dmp_freq_summary.index}")
            print(f"\tValues: {dh.dmp_freq_summary.values}")
        
        # Generate report
        dh.print_report()
        
    except Exception as e:
        logging.error(f"Critical error in main execution: {e}")
        print("Data processing failed. Check logs for details.")
