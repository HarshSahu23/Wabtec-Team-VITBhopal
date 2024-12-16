import pandas as pd
import logging

class DMPProcessor:
    @staticmethod
    def filter_dmp(df_dmp, jcr):
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

            required_columns = list(jcr.get_fill_vent_pairs().values())
            
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

    @staticmethod
    def process_fill_vent_events(df_dmp):
        """
        Process FILL and VENT events to count VENT transitions during FILL intervals.
        
        Args:
            df_dmp (pd.DataFrame): Input DMP dataframe
        
        Returns:
            dict: Dictionary containing events data for each FILL/VENT pair
        """
        try:
            if df_dmp is None or df_dmp.empty:
                logging.warning("Empty or None dataframe passed to process_fill_vent_events")
                return {}
            
            result = {}
            for i in range(1, 5):
                fill_col = f'FILL_{i}'
                vent_col = f'VENT_{i}'
                time_col = 'Time'
                mod_tick_col = 'MOD_TICK'

                if fill_col not in df_dmp.columns or vent_col not in df_dmp.columns \
                   or time_col not in df_dmp.columns or mod_tick_col not in df_dmp.columns:
                    logging.warning(f"Missing columns: {fill_col}, {vent_col}, {time_col}, or {mod_tick_col}")
                    continue

                # Extract relevant columns
                df_subset = df_dmp[[time_col, mod_tick_col, fill_col, vent_col]]

                # Find where FILL changes
                fill_series = df_subset[fill_col]
                fill_diff = fill_series.diff().fillna(0)
                fill_start_indices = fill_diff[fill_diff == 1].index
                fill_end_indices = fill_diff[fill_diff == -1].index

                events = []
                for idx, start_idx in enumerate(fill_start_indices):
                    # Determine end index
                    if idx < len(fill_end_indices):
                        end_idx = fill_end_indices[idx]
                    else:
                        end_idx = df_subset.index[-1]

                    interval_df = df_subset.loc[start_idx:end_idx]

                    # Adjust vent_series to include previous value
                    vent_start_idx = start_idx - 1 if start_idx > 0 else start_idx
                    vent_series = df_subset[vent_col].iloc[vent_start_idx:end_idx + 1].reset_index(drop=True)
                    vent_diff = vent_series.diff().fillna(vent_series.iloc[0])
                    vent_transitions = (vent_diff == 1).sum()

                    # Record event data
                    event = {
                        'start_time': interval_df.at[start_idx, time_col],
                        'end_time': interval_df.at[end_idx, time_col],
                        'mod_tick_start': interval_df.at[start_idx, mod_tick_col],
                        'mod_tick_end': interval_df.at[end_idx, mod_tick_col],
                        'vent_transition_count': int(vent_transitions)
                    }
                    events.append(event)

                result[f'FILL_{i}_VENT_{i}'] = events

            return result

        except Exception as e:
            logging.error(f"Error processing FILL/VENT events: {e}")
            return {}
