# src/frontend/streamlit_gui.py

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from backend.data_handler import DataHandler
import tempfile
import os
from pathlib import Path
from functools import lru_cache
from frontend.compute.visualizations import create_bar_chart, create_pie_chart, create_treemap, get_color
from frontend.utils.css_utils import inject_main_css, inject_column_css, get_metrics_css, inject_tab_css  # Import CSS utilities
from frontend.utils.sidebar_utils import show_help, show_credits  # Import sidebar utilities
from frontend.tabs.render_brakes_log import render_brakes_log;
from frontend.tabs.render_dump_log import render_dump_log;
from frontend.tabs.render_summary import render_summary;

class StreamlitGUI:
    def __init__(self):
        self.init_page_config()
        self.init_session_state()
        # Use the get_color function from visualizations.py
        self.get_color = get_color
    
    def init_page_config(self):
        st.set_page_config(
            page_title="Error Analyzer",
            page_icon="📊",
            layout="wide"
        )
        # Inject CSS styles using the utility function
        inject_main_css()
        inject_tab_css()  # Inject tab CSS
    
    def init_session_state(self):
        # Existing state variables
        if 'data_handler' not in st.session_state:
            st.session_state.data_handler = None
        if 'selected_errors' not in st.session_state:
            st.session_state.selected_errors = set()
        if 'axes_swapped' not in st.session_state:
            st.session_state.axes_swapped = False
        if 'sort_by' not in st.session_state:
            st.session_state.sort_by = None
        if 'sort_ascending' not in st.session_state:
            st.session_state.sort_ascending = True
        # Add new state variable for annotation toggle
        if 'show_percentage' not in st.session_state:
            st.session_state.show_percentage = True  # Default to showing percentages
        if 'selected_tags' not in st.session_state:
            st.session_state.selected_tags = set()
        if 'error_view_mode' not in st.session_state:
            st.session_state.error_view_mode = "Individual Errors"
        if 'tab_badges' not in st.session_state:
            st.session_state.tab_badges = {
                'Brakes Log': {'count': 0, 'color': '#dc3545'},
                'Dump Log': {'count': 0, 'color': '#fd7e14'},
                'Summary': {'count': 0, 'color': '#198754'}
            }
    
    def render(self):
        # Create tabs for navigation
        # Create tabs with plain text labels
        tabs = st.tabs(["Brakes Log", "Dump Log", "Summary"])
        
        # Sidebar content
        with st.sidebar:
            st.header("Settings")
            uploaded_files = st.file_uploader(
                "Upload CSV Files",
                type=['csv'],
                accept_multiple_files=True,
                help="Select one or more CSV files containing error data"
            )
            
            if uploaded_files:
                with st.spinner('Processing files...'):
                    with tempfile.TemporaryDirectory() as temp_dir:
                        for uploaded_file in uploaded_files:
                            temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                            with open(temp_file_path, 'wb') as f:
                                f.write(uploaded_file.getvalue())
                        
                        try:
                            st.session_state.data_handler = DataHandler(temp_dir)
                            if len(st.session_state.data_handler.ecl_freq_summary) == 0:
                                st.error("No data found in the uploaded files or files are empty!")
                        except Exception as e:
                            st.error(f"Failed to load data: {str(e)}")
            elif not uploaded_files:
                st.info("👆 Please upload CSV files to begin analysis")
            show_help()
            show_credits()
        
        # Render content based on active tab
        with tabs[0]:
            render_brakes_log()
        with tabs[1]:
            render_dump_log()
            pass
        with tabs[2]:
            render_summary()
            pass

def main():
    gui = StreamlitGUI()
    gui.render()

if __name__ == "__main__":
    main()