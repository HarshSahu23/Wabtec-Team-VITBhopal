# src/frontend/streamlit_gui.py

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from src.backend.data_handler import DataHandler
import tempfile
import os
from pathlib import Path
from functools import lru_cache
from src.frontend.visualizations import create_bar_chart, create_pie_chart, create_treemap, get_color

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
        # Set custom CSS for better spacing and readability
        st.markdown("""
            <style>
                .stRadio > div {
                    display: flex;
                    justify-content: center;
                    gap: 1rem;
                }
                .stCheckbox > label {
                    word-wrap: break-word;
                    max-width: 300px;
                }
            </style>
        """, unsafe_allow_html=True)
    
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
 
    @lru_cache(maxsize=128)
    def calculate_percentages(self, total, frequencies):
        """Cache percentage calculations for better performance"""
        return [(freq / total) * 100 for freq in frequencies]
    
    def update_chart(self, data_handler, selected_errors, chart_type):
        if not data_handler or len(selected_errors) == 0:
            st.warning("No data to display. Please select errors to visualize.")
            return
        
        filtered_data = data_handler.ecl_freq_summary[
            data_handler.ecl_freq_summary['Description'].isin(selected_errors)
        ]
        
        if not filtered_data.empty:
            # Create metrics for quick insights
            total_errors = filtered_data['Frequency'].sum()
            max_error = filtered_data.loc[filtered_data['Frequency'].idxmax()]
            
            # Display metrics in columns
            col1, col2, col3 = st.columns(3)
            # Adjust font size of metric values using HTML and CSS
            with col1:
                st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="font-size:18px; font-weight: bold;">Total Errors</div>
                        <div style="font-size:24px;">{total_errors:,}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="font-size:18px; font-weight: bold;">Most Common Error</div>
                        <div style="font-size:24px;">{max_error['Description']}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="font-size:18px; font-weight: bold;">Highest Frequency</div>
                        <div style="font-size:24px;">{max_error['Frequency']:,}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Add sorting options
            sort_col1, sort_col2 = st.columns(2)
            with sort_col1:
                sort_by = st.selectbox(
                    "Sort by",
                    ["Description", "Frequency"],
                    key="sort_by_select"
                )
            with sort_col2:
                sort_order = st.selectbox(
                    "Sort order",
                    ["Ascending", "Descending"],
                    key="sort_order_select"
                )
            
            # Apply sorting based on user selection
            sort_ascending = sort_order == "Ascending"
            filtered_data = filtered_data.sort_values(
                by=sort_by,
                ascending=sort_ascending
            )
            
            # Add button columns for chart controls
            btn_col1, btn_col2 = st.columns(2)
            
            # Add axis swap button for bar chart
            if chart_type == "Bar Chart":
                with btn_col1:
                    if st.button("Swap Axes", use_container_width=True):
                        st.session_state.axes_swapped = not st.session_state.axes_swapped
                
                with btn_col2:
                    if st.button(
                        "Change Graph Annotation",
                        help="Changes the annotated value over each element in the graph from percent to respective quantity",
                        use_container_width=True
                    ):
                        st.session_state.show_percentage = not st.session_state.show_percentage
            
            # Create and display the selected chart type
            if chart_type == "Bar Chart":
                fig = create_bar_chart(filtered_data, self.get_color, st.session_state)
            elif chart_type == "Pie Chart":
                fig = create_pie_chart(filtered_data, self.get_color)
            else:  # Treemap
                fig = create_treemap(filtered_data)
            
            # Display the chart with custom config
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                    'toImageButtonOptions': {
                        'format': 'png',
                        'filename': 'error_analysis',
                        'height': 600,
                        'width': 1200,
                        'scale': 2
                    }
                }
            )
            
            # Display data table
            st.subheader("Detailed Data")
            st.dataframe(
                filtered_data,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Description": st.column_config.TextColumn("Description", width="medium"),
                    "Frequency": st.column_config.NumberColumn("Frequency", format="%d")
                }
            )
    
    def show_credits(self):
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
    
    def show_help(self):
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
    
    def render(self):
        # Title and description
        st.title("📊 Error Analyzer")
        st.markdown("""
        Analyze and visualize error frequencies from your CSV files.
        Upload your files to begin the analysis.
        """)
        
        # Sidebar
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
            
            # Show help and credits in sidebar
            self.show_help()
            self.show_credits()
        
        # Main content
        if st.session_state.data_handler and len(st.session_state.data_handler.ecl_freq_summary) > 0:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Error Selection")
                
                # Select/Clear All buttons
                col1_1, col1_2 = st.columns(2)
                with col1_1:
                    if st.button("Select All", use_container_width=True):
                        st.session_state.selected_errors = set(
                            st.session_state.data_handler.ecl_freq_summary['Description']
                        )
                with col1_2:
                    if st.button("Clear All", use_container_width=True):
                        st.session_state.selected_errors.clear()
                
                # Search filter
                search_term = st.text_input("🔍 Search Errors", "")
                
                # Error checkboxes with search filter in a tabular form
                st.markdown("### Select Errors")
                error_data = st.session_state.data_handler.ecl_freq_summary
                filtered_data = error_data[error_data['Description'].str.contains(search_term, case=False)]
                
                # Table headings
                col1_1, col1_2, col1_3 = st.columns([0.1, 0.7, 0.2])
                with col1_1:
                    # st.checkbox("", key="select_all_errors")
                    select_all = st.checkbox("", key="select_all_errors")
                if select_all:
                    st.session_state.selected_errors = set(filtered_data['Description'])
                else:
                    st.session_state.selected_errors.clear()
                with col1_2:
                    st.markdown("**Description**")
                with col1_3:
                    st.markdown("**Frequency**")
                
                # Display errors in a table format
                for _, row in filtered_data.iterrows():
                    error_desc = row['Description']
                    frequency = row['Frequency']
                    col1_1, col1_2, col1_3 = st.columns([0.1, 0.7, 0.2])
                    with col1_1:
                        if st.checkbox(
                            "", key=f"cb_{error_desc}",
                            value=error_desc in st.session_state.selected_errors
                        ):
                            st.session_state.selected_errors.add(error_desc)
                        else:
                            st.session_state.selected_errors.discard(error_desc)
                    with col1_2:
                        st.write(error_desc)
                    with col1_3:
                        st.write(frequency)
            
            with col2:
                st.subheader("Visualization")
                chart_type = st.radio(
                    "Select Chart Type",
                    ["Bar Chart", "Pie Chart", "Treemap"],
                    horizontal=True
                )
                self.update_chart(
                    st.session_state.data_handler,
                    st.session_state.selected_errors,
                    chart_type
                )
        
        elif not uploaded_files:
            st.info("👆 Please upload CSV files to begin analysis")

def main():
    gui = StreamlitGUI()
    gui.render()

if __name__ == "__main__":
    main()