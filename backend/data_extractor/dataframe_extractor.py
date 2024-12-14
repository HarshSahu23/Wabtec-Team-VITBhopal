import pandas as pd
import numpy as np
# Defning all the methods as static as
# this class is not meant to stay for
# time. It is meant for importing purposes
# only.

class DataFrameExtractor:
    @staticmethod
    def __read_csv_single_column(file_path):
        """
        Read a CSV file as a single column, preserving entire line contents
        and skipping blank lines.

        Parameters:
        file_path (str): Path to the CSV file

        Returns:
        pandas.DataFrame: DataFrame with entire line contents in a single column
        """
        try:
            # Read the file with all columns as text and no parsing
            df = pd.read_csv(file_path,
                             header=None,  # No header
                             names=['single_col'],  # Column name
                             sep='\0',  # Use newline as separator to read full lines
                             skip_blank_lines=True,
                             )

            # Remove any potential whitespace from the beginning and end of lines
            df.iloc[:, 0] = df.iloc[:, 0].str.strip()

            # Remove any completely blank lines that might have remained
            df = df[df.iloc[:, 0] != '']

            return df

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return pd.DataFrame()
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return pd.DataFrame()

    @staticmethod
    def __find_start_index(df):
        """
        Find the first line index that contains ';' or ',' as a delimiter 
        with more than 2 occurrences using pandas single-column DataFrame.

        Parameters:
        file_path (str): Path to the CSV file

        Returns:
        int: Index of the first line with delimiter (0-based), or -1 if not found
        str: The detected delimiter (';' or ',')
        """
        try:
            # Apply delimiter counting
            semicolon_counts = df.iloc[:, 0].str.count(';')
            comma_counts = df.iloc[:, 0].str.count(',')
            # print(semicolon_counts, semicolon_counts)
            # Find first line with more than 2 semicolons
            # An heuristic measure that the header row will
            # contain more than two columns hence, more than
            # two delimiters
            # display(semicolon_counts)
            # display(comma_counts)

            semicolon_index = semicolon_counts[semicolon_counts > 2].index
            if not semicolon_index.empty:
                return semicolon_index[0], ';'

            # Find first line with more than 2 commas
            comma_index = comma_counts[comma_counts > 2].index
            if not comma_index.empty:
                return comma_index[0], ','

            # If no line with delimiter found
            return None, None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None

    @staticmethod
    def __find_end_index(df, delimiter, header_line_idx):
        """
        Efficiently detect the end of the upper section based on column count consistency
        using pandas vectorized operations.

        Parameters:
        df (pandas.DataFrame): DataFrame with single column
        delimiter (str): Delimiter used in the file

        Returns:
        int: Index marking the end of the upper section
        """
        # Get the column count for the header line
        column_count = df.iloc[header_line_idx, 0].count(delimiter) + 1

        # Vectorized column count calculation
        column_counts = df.iloc[header_line_idx+1:, 0].str.count(delimiter) + 1

        # Find indices where column count differs
        different_count_indices = np.where(column_counts != column_count)[0]
    
        # If no different count found, return end of DataFrame
        if len(different_count_indices) == 0:
            return len(df)
        
        # Return the first index where column count differs
        return header_line_idx + different_count_indices[0]

    @staticmethod
    def __extract_main_section(df, file_path):

        delimiter = None
        header_line_idx = None

        # Detect delimiter and header line
        header_line_idx, delimiter = DataFrameExtractor.__find_start_index(df)

        if header_line_idx is None or delimiter is None:
            raise ValueError(
                "Failed to locate a valid header or delimiter in the file.")

        # df = df[header_line_idx:].reset_index(drop=True)

        main_section_end = DataFrameExtractor.__find_end_index(df, delimiter, header_line_idx)
        # Extract the upper section lines
        # df = df[0:upper_section_end]

        # df_ecl_fmtd = df.iloc[:, 0].str.split(delimiter, expand=True)

        # df_ecl_fmtd = df_ecl_fmtd.reset_index(drop=True)

        # # Reassign columns
        # df_ecl_fmtd.columns = df_ecl_fmtd.iloc[0]

        # # Reset the index
        # df_ecl_fmtd = df_ecl_fmtd.iloc[1:].reset_index(drop=True)
        df_ecl_fmtd = pd.read_csv(
                            file_path, 
                            skiprows=range(0, header_line_idx),  # Skip rows before the start line
                            nrows=main_section_end - header_line_idx,     # Read only the specified number of rows
                            delimiter=delimiter
                        )

        return df_ecl_fmtd.dropna(axis=1, how='all')

    @staticmethod
    def __trim_df(df):
        chars_to_trim = ' ;,'

        # Use str.strip() to remove both leading and trailing characters
        df.iloc[:, 0] = df.iloc[:, 0].str.strip(
            chars_to_trim)
        # display(df.head(10))
        return df

    @staticmethod
    def get_df_from_file(file_path):
        df: pd.DataFrame = DataFrameExtractor.__read_csv_single_column(file_path=file_path)
        df = DataFrameExtractor.__trim_df(df)
        df = DataFrameExtractor.__extract_main_section(df, file_path)
        return df
    
# if __name__ == "__main__":
#     df = DataFrameExtractor.get_df_from_file("csv\Error 2.csv")
#     print(df)
