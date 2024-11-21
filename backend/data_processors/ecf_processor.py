import pandas as pd
import logging
from backend.utils.exceptions import FileProcessingError

class ECFProcessor:
    @staticmethod
    def format_ecf(df_ecf):
        """
        Format ECF dataframe with robust error handling.
        
        Args:
            df_ecf (pd.DataFrame): Input dataframe
        
        Returns:
            pd.DataFrame: Formatted dataframe
        
        Raises:
            FileProcessingError: If formatting fails
        """
        try:
            if df_ecf is None or df_ecf.empty:
                raise ValueError("Input dataframe is empty or None")
            
            # Skip some rows that are not required
            df_ecf_fmtd = df_ecf.iloc[1:].reset_index(drop=True)

            # Validate split operation
            try:
                df_ecf_fmtd = df_ecf_fmtd.iloc[:, 0].str.split(';', expand=True)
            except Exception as e:
                raise FileProcessingError(f"Failed to split ECF dataframe: {e}")

            # Ensure columns exist
            if df_ecf_fmtd.empty or len(df_ecf_fmtd.columns) < 2:
                raise FileProcessingError("Insufficient columns after splitting")

            # Reassign columns
            df_ecf_fmtd.columns = df_ecf_fmtd.iloc[0]

            # Drop unrequired columns
            df_ecf_fmtd = df_ecf_fmtd.drop(df_ecf_fmtd.columns[-1], axis=1)

            # Reset the index
            df_ecf_fmtd = df_ecf_fmtd.iloc[1:].reset_index(drop=True)

            return df_ecf_fmtd
        
        except (ValueError, FileProcessingError) as e:
            logging.error(f"ECF formatting error: {e}")
            return pd.DataFrame()

