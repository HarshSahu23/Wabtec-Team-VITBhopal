import pandas as pd
from backend.json_config_loader import JSONConfigReader

def get_error_groups(jcr: JSONConfigReader, ecl_summary: pd.DataFrame) -> dict[str, pd.DataFrame]:
    grouped_error_dfs = dict()
    for grp_name, error_list in jcr.get_error_log_tab().items():
        grouped_error_dfs[grp_name] = ecl_summary[ecl_summary[jcr.get_error_description()].isin(error_list)].reset_index(drop=True)
    return grouped_error_dfs