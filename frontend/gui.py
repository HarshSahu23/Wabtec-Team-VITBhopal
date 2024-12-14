# Import backend
from backend.data_handler import DataHandler
# Import frontend tools
from frontend.compute.visualizations import get_color
from frontend.utils.render_sidebar import render_sidebar
from frontend.utils.css_utils import inject_main_css, inject_tab_css  
# Import GUI Tabs
from frontend.tabs.render_brakes_log import render_brakes_log;
from frontend.tabs.render_dump_log import render_dump_log;
from frontend.tabs.render_summary import render_summary;
from frontend.tabs.render_settings import render_settings
# Import core libs
import streamlit as st
import os
from pathlib import Path
from functools import lru_cache
import tkinter as tk
from tkinter import filedialog
import re  
#==============================================

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
        if 'folder_date' not in st.session_state:
            st.session_state.folder_date = None
        if 'depot_name' not in st.session_state:
            st.session_state.depot_name = None
        if 'coach_name' not in st.session_state:
            st.session_state.coach_name = None
        if 'settings_unlocked' not in st.session_state:
            st.session_state.settings_unlocked = False
        if 'pin_attempts' not in st.session_state:
            st.session_state.pin_attempts = 0
        if 'last_attempt_time' not in st.session_state:
            st.session_state.last_attempt_time = 0
    
    def render(self):
        # Create tabs for navigation
        # Update tabs to include Settings
        tabs = st.tabs(["Summary", "Error Log", "WSP Activity Log",  "Settings"])
        
        # Sidebar content
        with st.sidebar:
            render_sidebar()
        
        # Render content based on active tab
        with tabs[0]:
            render_summary()
        with tabs[1]:
            render_brakes_log()
            pass
        with tabs[2]:
            render_dump_log()
            pass
        with tabs[3]:  # Add settings tab
            render_settings()

def main():
    gui = StreamlitGUI()
    gui.render()

if __name__ == "__main__":
    main()