import pandas as pd
import logging

class DMPProcessor:
    @staticmethod
    def read_dmp(file_path):
        """
        Read DMP file with comprehensive error handling.
        
        Args:
            file_path (str): Path to the CSV file
        
        Returns:
            pd.DataFrame: Loaded dataframe or empty dataframe
        """
        try:
            data = pd.read_csv(file_path, low_memory=False)
            
            # Additional validation
            if data.empty:
                logging.warning(f"Empty dataframe from file: {file_path}")
            
            return data
        
        except pd.errors.EmptyDataError:
            logging.error(f"No columns to parse from file: {file_path}")
            return pd.DataFrame()
        except pd.errors.ParserError as e:
            logging.error(f"Parsing error in file {file_path}: {e}")
            return pd.DataFrame()
        except Exception as e:
            logging.error(f"Unexpected error reading DMP file {file_path}: {e}")
            return pd.DataFrame()

    @staticmethod
    def filter_dmp(df_dmp):
        """
        Filter DMP dataframe with robust error handling.
        
        Args:
            df_dmp (pd.DataFrame): Input DMP dataframe
        
        Returns:
            pd.DataFrame: Filtered dataframe
        """
        try:
            if df_dmp is None or df_dmp.empty:
                logging.warning("Empty or None dataframe passed to filter_dmp")
                return pd.DataFrame()

            required_columns = ["FILL_1","VENT_1","FILL_2","VENT_2","FILL_3","VENT_3","FILL_4","VENT_4"]
            
            # Check if all required columns exist
            missing_columns = [col for col in required_columns if col not in df_dmp.columns]
            if missing_columns:
                logging.warning(f"Missing columns in DMP: {missing_columns}")
                return pd.DataFrame()

            f_df_dmp = df_dmp[required_columns]
            f_df_dmp = f_df_dmp.loc[:, (f_df_dmp[required_columns] != 0).any(axis=0)]
            
            return f_df_dmp
        
        except Exception as e:
            logging.error(f"Error filtering DMP dataframe: {e}")
            return pd.DataFrame()

    @staticmethod
    def get_frequency_summary(df_dmp):
        """
        Get DMP frequency summary with error handling.
        
        Args:
            df_dmp (pd.DataFrame): Filtered DMP dataframe
        
        Returns:
            pd.Series: Frequency summary
        """
        try:
            if df_dmp is None or df_dmp.empty:
                logging.warning("Empty or None dataframe passed to get_dmp_freq_summary")
                return pd.Series()

            summary = df_dmp.sum(axis=0)
            return summary
        
        except Exception as e:
            logging.error(f"Error generating DMP frequency summary: {e}")
            return pd.Series()
