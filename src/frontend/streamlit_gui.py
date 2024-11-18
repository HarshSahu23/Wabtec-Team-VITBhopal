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
from src.frontend.css_utils import inject_main_css, inject_column_css, get_metrics_css  # Import CSS utilities
from src.frontend.sidebar_utils import show_help, show_credits  # Import sidebar utilities

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
            
            # Inject metrics CSS
            st.markdown(get_metrics_css(), unsafe_allow_html=True)
            
            # Display metrics in columns
            metric_cols = st.columns(3)
            
            with metric_cols[0]:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">Total Errors</div>
                        <div class="metric-value-large">{total_errors:,}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[1]:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">Most Common Error</div>
                        <div class="metric-value-medium">{max_error['Description']}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[2]:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">Highest Frequency</div>
                        <div class="metric-value-large">{max_error['Frequency']:,}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Close the container card
            st.markdown("</div>", unsafe_allow_html=True)
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
            
            # Remove or comment out the existing 'Detailed Data' section
            # st.subheader("Detailed Data")
            # st.dataframe(...)

            # Add the new 'Get Detailed Data' section
            st.subheader("Get Detailed Data")
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.session_state.selected_errors:
                    # Convert set to list and sort for consistent display
                    all_selected_errors = sorted(list(st.session_state.selected_errors))
                    selected_error = st.selectbox(
                        "🔍 Search/Select Error",
                        options=all_selected_errors,
                        help="Type to search or select an error to view details"
                    )
                    detailed_data = st.session_state.data_handler.ecl[
                        st.session_state.data_handler.ecl['Description'] == selected_error
                    ]
                else:
                    st.write("No errors selected.")
            with col2:
                pass

            # Render detailed data below the columns
            if st.session_state.selected_errors and not detailed_data.empty:
                st.table(detailed_data.T)
            elif st.session_state.selected_errors:
                st.write("No details available for this error.")
           
    
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
            show_help()
            show_credits()
        
        # Main content
        if st.session_state.data_handler and len(st.session_state.data_handler.ecl_freq_summary) > 0:
            
            col1, col2 = st.columns([1, 3])
            # st.markdown(
            #     """
            #     <style>
            #     /* Style the first column */
            #     [data-testid="stHorizontalBlock"] > div:nth-child(1) {
            #         background-color: rgba(200, 200, 200, 0.2);
            #         padding: 15px;
            #         border-radius: 15px;
            #     }
            #     </style>
            #     """,
            #     unsafe_allow_html=True
            # )
            with col1:
                # Inject column CSS styles
                st.subheader("Error Selection")
                
                # Search filter
                search_term = st.text_input("🔍 Search Errors", "")
                
                # Error checkboxes with search filter in a tabular form
                st.markdown("### Select Errors")
                
                error_data = st.session_state.data_handler.ecl_freq_summary
                filtered_data = error_data[error_data['Description'].str.contains(search_term, case=False)]
                
                # Table headings
                col1_1, col1_2, col1_3 = st.columns([0.15, 0.6,0.25])
                
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