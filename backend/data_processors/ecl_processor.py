import pandas as pd
import logging

class ECLProcessor:
    @staticmethod
    def get_frequency_summary(df_ecl_fmtd, jcr):
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

            summary = df_ecl_fmtd.groupby(by=[jcr.get_error_description()])
            summary = summary.size().reset_index(name='Frequency')
            summary['SortKey'] = summary[jcr.get_error_description()].apply(lambda x: (-len(str(x)), str(x).lower()))
            summary = summary.sort_values(by="SortKey", ignore_index=True)
            summary = summary.drop(columns='SortKey')
            
            return summary
        
        except Exception as e:
            logging.error(f"Error generating ECL frequency summary: {e}")
            return pd.DataFrame()
