import pandas as pd
from backend.json_config_loader import JSONConfigReader

def __get_filtered_freqs(source_df: pd.DataFrame, error_list, jcr: JSONConfigReader):
    error_desc_col = jcr.get_error_description()
    if error_desc_col not in source_df.columns or 'Frequency' not in source_df.columns:
        raise ValueError(f"Source DataFrame must contain {error_desc_col} and 'Frequency' columns.")
    
    # Filter and reorder the frequencies based on the given tag list
    result = source_df.set_index(error_desc_col).reindex(error_list)['Frequency'].fillna(0.0).astype(int)
    return result.reset_index(drop=True) 

def get_tables(ecl_freq_summary: pd.DataFrame, jcr: JSONConfigReader) -> dict[str, pd.DataFrame]:
    df_dicts = dict()
    for table_name, table_details in jcr.get_summary_tab().items():
        # print(table_details)
        df = pd.DataFrame(columns=table_details["COLUMNS"])
        for row_name, row_details in table_details.items():
            # print(row_name, row_details)
            if row_name != "COLUMNS":
                df.loc[len(df)] = [row_name] + __get_filtered_freqs(ecl_freq_summary, row_details, jcr).tolist()
        # display(table_name, df)
        df_dicts[table_name] = df
    return df_dicts