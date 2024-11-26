import pandas as pd
import logging

class ECLErrorGrouper:
    # Comprehensive error group mapping
    ERROR_GROUPS = {
        'Axle Lock Group': [
            'AXLE1_LOCK', 
            'AXLE2_LOCK', 
            'AXLE3_LOCK', 
            'AXLE4_LOCK'
        ],
        'Speed Sensor Error': [
            'E_SENS_FR1', 
            'E_SENS_FR2', 
            'E_SENS_FR3', 
            'E_SENS_FR4'
        ],
        'Dump Valve Errors': [
            'E_DV1_TOUT', 
            'E_DV2_TOUT', 
            'E_DV3_TOUT', 
            'E_DV4_TOUT',
            'E_DV1_OC', 
            'E_DV2_OC', 
            'E_DV3_OC', 
            'E_DV4_OC'
        ],
        'Board Errors': [
            'E_ZERO_SPEED', 
            'E_SPEED_5', 
            'E_SPEED_5_1', 
            'E_SPEED_5_2', 
            'E_SPEED_30', 
            'E_SPEED_45', 
            'E_WSP_FAILURE', 
            'E_DEVICE_ON'
        ],
        'Power On Event': [
            'I_POWER_ON'
        ]
    }

    @classmethod
    def group_errors(cls, df_ecl):
        """
        Group errors based on predefined error groups and add a group column.
        
        Args:
            df_ecl (pd.DataFrame): Input ECL dataframe
        
        Returns:
            pd.DataFrame: Dataframe with added error group column
        """
        try:
            if df_ecl is None or df_ecl.empty:
                logging.warning("Empty dataframe passed to group_errors")
                return pd.DataFrame()

            # Create a mapping of all errors to their groups
            error_to_group = {}
            for group, errors in cls.ERROR_GROUPS.items():
                for error in errors:
                    error_to_group[error] = group

            # Filter out 'GONE' errors
            df_filtered = df_ecl[~df_ecl['Description'].str.contains('GONE', case=False, na=False)].copy()

            # Add error group column
            df_filtered['Error Group'] = df_filtered['Description'].map(error_to_group)

            # For errors not in predefined groups, mark as 'Unclassified'
            df_filtered['Error Group'].fillna('Unclassified', inplace=True)

            return df_filtered

        except Exception as e:
            logging.error(f"Error grouping ECL errors: {e}")
            return pd.DataFrame()

    @classmethod
    def get_error_groups(cls):
        """
        Get the predefined error groups.
        
        Returns:
            dict: Mapping of error groups to their respective errors
        """
        return cls.ERROR_GROUPS

    @classmethod
    def get_all_errors(cls):
        """
        Get a flat list of all errors across groups.
        
        Returns:
            list: All error descriptions
        """
        all_errors = []
        for group_errors in cls.ERROR_GROUPS.values():
            all_errors.extend(group_errors)
        return all_errors