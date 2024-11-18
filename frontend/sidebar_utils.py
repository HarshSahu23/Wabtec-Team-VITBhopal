
import streamlit as st

def show_help():
    with st.sidebar.expander("Help", expanded=False):
        st.markdown("""
        ### Quick Guide
        
        1. **Import Data:**
           - Use the file uploader to select CSV files
           - You can select multiple files at once
        
        2. **Analyze Errors:**
           - Use checkboxes to select errors
           - Choose from multiple visualization types
           - Interact with charts:
             - Zoom in/out
             - Pan
             - Download as PNG
           - Sort data in the table view
        
        3. **Features:**
           - Interactive visualizations
           - Key metrics dashboard
           - Detailed data table
           - Multiple chart types
        """)

def show_credits():
    with st.sidebar.expander("Credits", expanded=False):
        st.markdown("""
        ### Error Analyzer v1.0.0
        
        **Developed by:**
        - Akhand Pratap Tiwari
        - Aryan Rana
        - Harsh Sahu
        - Elson Nag
        
        **Under the guidance of:**  
        Wabtec Corporation
        
        © 2024 Wabtec Corporation
        """)