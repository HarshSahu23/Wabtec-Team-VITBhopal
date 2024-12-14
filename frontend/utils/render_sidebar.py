from functools import lru_cache
import os
from pathlib import Path
import re
import streamlit as st
import tkinter as tk
from tkinter import filedialog

from backend.data_handler import DataHandler
from frontend.utils.sidebar_utils import show_credits, show_help

@lru_cache(maxsize=32)
def process_folder(folder_path: str):
    """Cache folder processing to avoid recomputing"""
    return DataHandler(folder_path,"config.json")

def get_csv_files(folder_path: str) -> list:
    """Efficiently get CSV files using pathlib"""
    return [f for f in Path(folder_path).glob('*.csv')]

def render_sidebar():
        st.header("Settings")

        # Function to open folder selection dialog
        def select_folder():
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            root.attributes('-topmost', True)  # Bring the dialog to the front
            folder_selected = filedialog.askdirectory()
            root.destroy()
            return folder_selected

        # Replace file uploader with 'Upload Folder' button
        if st.button("Upload Folder"):
            folder_path = select_folder()
            if folder_path:
                with st.spinner('Processing files...'):
                    csv_files = get_csv_files(folder_path)
                    if csv_files:
                        try:
                            # Parse folder name
                            folder_name = os.path.basename(folder_path)
                            match = re.match(r'(\d{2}-\d{2}-\d{4})_(.+)_(.+)', folder_name)
                            if match:
                                st.session_state.folder_date = match.group(1)
                                st.session_state.depot_name = match.group(2)
                                st.session_state.coach_name = match.group(3)
                                print(st.session_state.folder_date, "##",st.session_state.depot_name,"##", st.session_state.coach_name)
                            else:
                                st.warning("Folder name does not match the expected pattern")

                            # Use cached processing
                            st.session_state.data_handler = process_folder(folder_path)
                            
                            if len(st.session_state.data_handler.ecl_freq_summary) == 0:
                                st.error("No data found in the CSV files!")
                            else:
                                st.success("Files processed successfully")
                                with st.expander("Processed Files"):
                                    for file in csv_files:
                                        st.write(file.name)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.error("No CSV files found in folder")
            else:
                st.info("👆 Please select a folder")

        show_help()
        show_credits()