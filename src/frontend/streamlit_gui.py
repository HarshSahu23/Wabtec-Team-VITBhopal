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
        # Create an extended color palette by combining multiple qualitative color sequences
        base_colors = (
            px.colors.qualitative.Set3 +
            px.colors.qualitative.Pastel1 +
            px.colors.qualitative.Set1 +
            px.colors.qualitative.Pastel2 +
            px.colors.qualitative.Set2
        )
        # Create a function to generate repeating colors while maintaining distinction
        self.get_color = lambda i: base_colors[i % len(base_colors)]
    
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
        if 'axes_swapped' not in st.session_state:
            st.session_state.axes_swapped = False
        if 'sort_by' not in st.session_state:
            st.session_state.sort_by = None
        if 'sort_ascending' not in st.session_state:
            st.session_state.sort_ascending = True
    
    def create_bar_chart(self, filtered_data):
        """Create an interactive bar chart using Plotly"""
        # Generate colors for each bar
        colors = [self.get_color(i) for i in range(len(filtered_data))]
        
        fig = go.Figure()
        
        if st.session_state.axes_swapped:
            fig.add_trace(go.Bar(
                y=filtered_data['Description'],
                x=filtered_data['Frequency'],
                orientation='h',
                marker_color=colors,
                hovertemplate='<b>Error:</b> %{y}<br>' +
                             '<b>Frequency:</b> %{x}<br>' +
                             '<extra></extra>'
            ))
            
            # Add percentage annotations
            total = filtered_data['Frequency'].sum()
            for i, value in enumerate(filtered_data['Frequency']):
                percentage = (value / total) * 100
                fig.add_annotation(
                    y=i,
                    x=value,
                    text=f'{percentage:.1f}%',
                    showarrow=False,
                    xshift=10
                )
        else:
            fig.add_trace(go.Bar(
                x=filtered_data['Description'],
                y=filtered_data['Frequency'],
                marker_color=colors,
                hovertemplate='<b>Error:</b> %{x}<br>' +
                             '<b>Frequency:</b> %{y}<br>' +
                             '<extra></extra>'
            ))
            
            # Add percentage annotations
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
        
        fig.update_layout(
            title={
                'text': 'Error Frequency Distribution',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Frequency' if st.session_state.axes_swapped else 'Error Description',
            yaxis_title='Error Description' if st.session_state.axes_swapped else 'Frequency',
            showlegend=False,
            xaxis_tickangle=-45 if not st.session_state.axes_swapped else 0,
            margin=dict(t=100, l=50 if not st.session_state.axes_swapped else 200, r=50, b=100),
            height=600,
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            ),
            # Improve bar appearance
            bargap=0.2,  # Adjust space between bars
            plot_bgcolor='white',  # White background
            paper_bgcolor='white'  # White surrounding
        )
        
        # Add grid lines for better readability
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
        
        return fig
    
    def create_pie_chart(self, filtered_data):
        """Create an interactive pie chart using Plotly"""
        # Generate colors for each slice
        colors = [self.get_color(i) for i in range(len(filtered_data))]
        
        fig = go.Figure()
        
        fig.add_trace(go.Pie(
            labels=filtered_data['Description'],
            values=filtered_data['Frequency'],
            textinfo='label+percent',
            textposition='outside',
            hovertemplate='<b>Error:</b> %{label}<br>' +
                         '<b>Frequency:</b> %{value}<br>' +
                         '<b>Percentage:</b> %{percent}<br>' +
                         '<extra></extra>',
            marker=dict(colors=colors)
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
        # For treemap, we'll use a continuous color scale instead of discrete colors
        fig = px.treemap(
            filtered_data,
            path=['Description'],
            values='Frequency',
            color='Frequency',
            color_continuous_scale=px.colors.sequential.Viridis,  # Changed to Viridis for better distinction
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
                st.metric("Total Errors", f"{total_errors:,}", help="Total number of errors found")
            with col2:
                st.metric("Most Common Error", max_error['Description'], help="The most frequently occurring error")
            with col3:
                st.metric("Highest Frequency", f"{max_error['Frequency']:,}", help="Frequency of the most common error")
            
            # Add custom CSS to decrease the font size of the metrics
            st.markdown("""
                <style>
                    .stMetric {
                        font-size: 0.1rem !important;
                    }
                </style>
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
            
            # Add axis swap button for bar chart
            if chart_type == "Bar Chart":
                if st.button("Swap Axes", use_container_width=True):
                    st.session_state.axes_swapped = not st.session_state.axes_swapped
            
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