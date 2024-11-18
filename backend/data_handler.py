import pandas as pd
import glob
from tqdm import tqdm

class DataHandler:
    # __folder_path = ""
    # ecl = pd.DataFrame()
    # ecf = pd.DataFrame()
    # ecl_freq_summary = pd.DataFrame()

    def __format_ecl(self, df_ecl):
        # Skip some rows that are not required
        df_ecl_fmtd = df_ecl.iloc[8:].reset_index(drop=True)

        # Split the text into separate with ';' as delimiter
        df_ecl_fmtd = df_ecl_fmtd.iloc[:, 0].str.split(';', expand=True)

        # Reassign columns
        df_ecl_fmtd.columns = df_ecl_fmtd.iloc[0]

        # Drop unrequired columns
        df_ecl_fmtd = df_ecl_fmtd.drop(df_ecl_fmtd.columns[[0, -1]], axis=1)

        # Reset the index
        df_ecl_fmtd = df_ecl_fmtd.iloc[1:].reset_index(drop=True)

        return df_ecl_fmtd

    def __format_ecf(self, df_ecf):
        # Skip some rows that are not required
        df_ecf_fmtd = df_ecf.iloc[1:].reset_index(drop=True)

        # Split the text into separate with ';' as delimiter
        df_ecf_fmtd = df_ecf_fmtd.iloc[:, 0].str.split(';', expand=True)

        # Reassign columns
        df_ecf_fmtd.columns = df_ecf_fmtd.iloc[0]

        # Drop unrequired columns
        df_ecf_fmtd = df_ecf_fmtd.drop(df_ecf_fmtd.columns[-1], axis=1)

        # Reset the index
        df_ecf_fmtd = df_ecf_fmtd.iloc[1:].reset_index(drop=True)

        return df_ecf_fmtd

    # Read and format dataframe from file_path provided
    def read_csv_from_file(self, file_path):
        data = pd.read_csv(file_path)

        ecf_index = data[data.iloc[:, 0].str.contains(
            "ERROR CODE FREQUENCY")].index[0]

        df_ecl = data.iloc[0:ecf_index, ]
        df_ecf = data.iloc[ecf_index:, ]

        df_ecl = self.__format_ecl(df_ecl)
        df_ecf = self.__format_ecf(df_ecf)

        return df_ecl, df_ecf

    # Read, format and merge dataframe from files under folder_path provided
    def read_csv_from_folder(self, folder_path):
        csv_files = glob.glob(f"{folder_path}/*.csv")
        # print("Printing csv files", csv_files)
        merged_df_ecl = pd.DataFrame()
        merged_df_ecf = pd.DataFrame()

        for csv_file_path in tqdm(csv_files, desc="Reading Files"):
            df_ecl, df_ecf = self.read_csv_from_file(csv_file_path)
            merged_df_ecl = pd.concat(
                [merged_df_ecl, df_ecl])  # Default axis = 0
            merged_df_ecf = pd.concat(
                [merged_df_ecf, df_ecf])  # Default axis = 0

        merged_df_ecf.reset_index(drop=True, inplace=True)
        merged_df_ecl.reset_index(drop=True, inplace=True)

        return merged_df_ecl, merged_df_ecf

    def get_ecl_freq_summary(self, df_ecl_fmtd):
        summary = df_ecl_fmtd.groupby(by=["Description"])
        summary = summary.size().reset_index(name='Frequency')
        summary['SortKey'] = summary['Description'].apply(lambda x: (-len(x), x.lower()))
        summary = summary.sort_values(by="SortKey", ignore_index=True)
        summary = summary.drop(columns='SortKey')
        return summary

    def get_folder(self):
        return self.__folder_path

    def set_folder(self, folder_path):
        self.__folder_path = folder_path
        self.ecl = pd.DataFrame()
        self.ecf = pd.DataFrame()
        self.ecl, self.ecf = self.read_csv_from_folder(self.__folder_path)
        self.ecl_freq_summary = self.get_ecl_freq_summary(self.ecl)

    def __init__(self, folder_path):
        self.set_folder(folder_path)
