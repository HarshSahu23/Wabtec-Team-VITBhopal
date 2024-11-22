import pandas as pd
import logging
from backend.utils.exceptions import FileProcessingError

class ECLProcessor:
    @staticmethod
    def format_ecl(df_ecl):
        """
        Format ECL dataframe with robust error handling.
        
        Args:
            df_ecl (pd.DataFrame): Input dataframe
        
        Returns:
            pd.DataFrame: Formatted dataframe
        
        Raises:
            FileProcessingError: If formatting fails
        """
        try:
            if df_ecl is None or df_ecl.empty:
                raise ValueError("Input dataframe is empty or None")
            
            # Skip some rows that are not required
            df_ecl_fmtd = df_ecl.iloc[8:].reset_index(drop=True)

            # Validate split operation
            try:
                df_ecl_fmtd = df_ecl_fmtd.iloc[:, 0].str.split(';', expand=True)
            except Exception as e:
                raise FileProcessingError(f"Failed to split ECL dataframe: {e}")

            # Ensure columns exist
            if df_ecl_fmtd.empty or len(df_ecl_fmtd.columns) < 2:
                raise FileProcessingError("Insufficient columns after splitting")

            # Reassign columns
            df_ecl_fmtd.columns = df_ecl_fmtd.iloc[0]

            # Drop unrequired columns
            df_ecl_fmtd = df_ecl_fmtd.drop(df_ecl_fmtd.columns[[0, -1]], axis=1)

            # Reset the index
            df_ecl_fmtd = df_ecl_fmtd.iloc[1:].reset_index(drop=True)

            return df_ecl_fmtd
        
        except (ValueError, FileProcessingError) as e:
            logging.error(f"ECL formatting error: {e}")
            return pd.DataFrame()

    @staticmethod
    def get_frequency_summary(df_ecl_fmtd):
        """
        Get ECL frequency summary with error handling.
        
        Args:
            df_ecl_fmtd (pd.DataFrame): Formatted ECL dataframe
        
        Returns:
            pd.DataFrame: Summary dataframe
        """
        try:
            if df_ecl_fmtd is None or df_ecl_fmtd.empty:
                logging.warning("Empty or None dataframe passed to get_ecl_freq_summary")
                return pd.DataFrame()

            summary = df_ecl_fmtd.groupby(by=["Description"])
            summary = summary.size().reset_index(name='Frequency')
            summary['SortKey'] = summary['Description'].apply(lambda x: (-len(str(x)), str(x).lower()))
            summary = summary.sort_values(by="SortKey", ignore_index=True)
            summary = summary.drop(columns='SortKey')
            
            return summary
        
        except Exception as e:
            logging.error(f"Error generating ECL frequency summary: {e}")
            return pd.DataFrame()
