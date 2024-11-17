# src/frontend/streamlit_gui.py

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from src.backend.data_handler import DataHandler
import tempfile
import os
from pathlib import Path

class StreamlitGUI:
    def __init__(self):
        self.init_page_config()
        self.init_session_state()
        self.color_sequence = px.colors.qualitative.Set3  # Colorful but professional palette
    
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
        if 'data_handler' not in st.session_state:
            st.session_state.data_handler = None
        if 'selected_errors' not in st.session_state:
            st.session_state.selected_errors = set()
    
    def create_bar_chart(self, filtered_data):
        """Create an interactive bar chart using Plotly"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=filtered_data['Description'],
            y=filtered_data['Frequency'],
            marker_color=self.color_sequence[:len(filtered_data)],
            hovertemplate='<b>Error:</b> %{x}<br>' +
                         '<b>Frequency:</b> %{y}<br>' +
                         '<extra></extra>'  # Removes trace name from hover
        ))
        
        fig.update_layout(
            title={
                'text': 'Error Frequency Distribution',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Error Description',
            yaxis_title='Frequency',
            showlegend=False,
            xaxis_tickangle=-45,
            margin=dict(t=100, l=50, r=50, b=100),
            height=600,
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )
        
        # Add percentage annotations on top of bars
        total = filtered_data['Frequency'].sum()
        for i, value in enumerate(filtered_data['Frequency']):
            percentage = (value / total) * 100
            fig.add_annotation(
                x=i,
                y=value,
                text=f'{percentage:.1f}%',
                showarrow=False,
                yshift=10
            )
        
        return fig
    
    def create_pie_chart(self, filtered_data):
        """Create an interactive pie chart using Plotly"""
        fig = go.Figure()
        
        fig.add_trace(go.Pie(
            labels=filtered_data['Description'],
            values=filtered_data['Frequency'],
            textinfo='label+percent',
            textposition='outside',
            hovertemplate='<b>Error:</b> %{label}<br>' +
                         '<b>Frequency:</b> %{value}<br>' +
                         '<b>Percentage:</b> %{percent}<br>' +
                         '<extra></extra>',  # Removes trace name from hover
            marker=dict(colors=self.color_sequence[:len(filtered_data)])
        ))
        
        fig.update_layout(
            title={
                'text': 'Error Distribution by Percentage',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            height=600,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.0
            ),
            margin=dict(t=100, l=50, r=50, b=50),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )
        
        return fig
    
    def create_treemap(self, filtered_data):
        """Create an interactive treemap using Plotly"""
        fig = px.treemap(
            filtered_data,
            path=['Description'],
            values='Frequency',
            color='Frequency',
            color_continuous_scale='RdBu',
            title='Error Distribution Treemap'
        )
        
        fig.update_layout(
            height=600,
            margin=dict(t=50, l=25, r=25, b=25)
        )
        
        return fig
    
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
            with col1:
                st.metric("Total Errors", f"{total_errors:,}")
            with col2:
                st.metric("Most Common Error", max_error['Description'])
            with col3:
                st.metric("Highest Frequency", f"{max_error['Frequency']:,}")
            
            # Create and display the selected chart type
            if chart_type == "Bar Chart":
                fig = self.create_bar_chart(filtered_data)
            elif chart_type == "Pie Chart":
                fig = self.create_pie_chart(filtered_data)
            else:  # Treemap
                fig = self.create_treemap(filtered_data)
            
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
            
            # Display data table with sorting capability
            st.subheader("Detailed Data")
            st.dataframe(
                filtered_data.style.format({'Frequency': '{:,}'}),
                use_container_width=True,
                hide_index=True
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
                
                # Error checkboxes with search filter
                st.markdown("### Select Errors")
                for _, row in st.session_state.data_handler.ecl_freq_summary.iterrows():
                    error_desc = row['Description']
                    # Apply search filter
                    if search_term.lower() in error_desc.lower():
                        if st.checkbox(
                            f"{error_desc} ({row['Frequency']:,})",
                            key=f"cb_{error_desc}",
                            value=error_desc in st.session_state.selected_errors
                        ):
                            st.session_state.selected_errors.add(error_desc)
                        else:
                            st.session_state.selected_errors.discard(error_desc)
            
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