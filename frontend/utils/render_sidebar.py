from functools import lru_cache
import os
from pathlib import Path
import re
import streamlit as st
import tempfile

from backend.data_handler import DataHandler
from frontend.utils.sidebar_utils import show_credits, show_help

@lru_cache(maxsize=32)
def process_folder(folder_path: str):
    """Cache folder processing to avoid recomputing"""
    return DataHandler(folder_path, "config.json")

def render_sidebar():
    st.header("Settings")
    
    # Add the 'Use sample data' button
    use_sample_data = st.button("Use sample data")
    
    # Use file uploader for multiple CSV files
    uploaded_files = st.file_uploader("Upload CSV Files", type=['csv'], accept_multiple_files=True)
    
    if use_sample_data:
        # User clicked the 'Use sample data' button
        with st.spinner('Processing sample data...'):
            try:
                # Assume 'csv' folder is in the root of the project
                csv_folder = os.path.join(os.getcwd(), 'csv')
                if not os.path.exists(csv_folder):
                    st.error("Sample data folder 'csv' not found!")
                    return
                
                # Get list of all CSV files in the 'csv' folder
                sample_files = [os.path.join(csv_folder, f) for f in os.listdir(csv_folder) if f.endswith('.csv')]
                if not sample_files:
                    st.error("No CSV files found in 'csv' folder!")
                    return
                
                # Get first file's name to extract metadata
                first_file = os.path.basename(sample_files[0])
                folder_match = re.match(r'(\d{2}-\d{2}-\d{4})_(.+)_(.+)\.csv', first_file)
                
                if folder_match:
                    st.session_state.folder_date = folder_match.group(1)
                    st.session_state.depot_name = folder_match.group(2)
                    st.session_state.coach_name = folder_match.group(3)
                else:
                    st.warning("File names should follow pattern: date_depot_coach.csv")
                
                # Process the 'csv' folder containing all sample files
                st.session_state.data_handler = process_folder(csv_folder)
                
                if len(st.session_state.data_handler.ecl_freq_summary) == 0:
                    st.error("No data found in the sample CSV files!")
                else:
                    st.success("Sample data processed successfully")
                    with st.expander("Processed Sample Files"):
                        for file in sample_files:
                            st.write(os.path.basename(file))
            except Exception as e:
                st.error(f"Error: {str(e)}")
                
    elif uploaded_files:
        with st.spinner('Processing files...'):
            # Create a temporary directory to store uploaded files
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save all uploaded files to temp directory
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(file_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                
                try:
                    # Get first file's name to extract metadata
                    first_file = uploaded_files[0].name
                    # Assuming first file name follows pattern: date_depot_coach
                    folder_match = re.match(r'(\d{2}-\d{2}-\d{4})_(.+)_(.+)\.csv', first_file)
                    
                    if folder_match:
                        st.session_state.folder_date = folder_match.group(1)
                        st.session_state.depot_name = folder_match.group(2)
                        st.session_state.coach_name = folder_match.group(3)
                    else:
                        st.warning("File names should follow pattern: date_depot_coach.csv")
                    
                    # Process the temp directory containing all uploaded files
                    st.session_state.data_handler = process_folder(temp_dir)
                    
                    if len(st.session_state.data_handler.ecl_freq_summary) == 0:
                        st.error("No data found in the CSV files!")
                    else:
                        st.success("Files processed successfully")
                        with st.expander("Processed Files"):
                            for file in uploaded_files:
                                st.write(file.name)
                                
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    show_help()
    show_credits()