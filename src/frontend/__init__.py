# src/frontend/streamlit_gui.py

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from src.backend.data_handler import DataHandler
import tempfile
import os
from pathlib import Path
from functools import lru_cache

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
        if 'show_percentage' not in st.session_state:
            st.session_state.show_percentage = True
    
    @lru_cache(maxsize=128)
    def calculate_percentages(self, total, frequencies):
        """Cache percentage calculations for better performance"""
        return [(freq / total) * 100 for freq in frequencies]
    
    def create_bar_chart(self, filtered_data):
        """Create an interactive bar chart using Plotly"""
        # Generate colors for each bar
        colors = [self.get_color(i) for i in range(len(filtered_data))]
        
        fig = go.Figure()
        
        # Calculate total for percentages
        total = filtered_data['Frequency'].sum()
        frequencies = filtered_data['Frequency'].tolist()
        
        # Get cached percentages
        percentages = self.calculate_percentages(total, tuple(frequencies))
        
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
            
            # Add annotations based on user preference
            for i, (value, percentage) in enumerate(zip(frequencies, percentages)):
                annotation_text = f'{percentage:.1f}%' if st.session_state.show_percentage else f'{value:,}'
                fig.add_annotation(
                    y=i,
                    x=value,
                    text=annotation_text,
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
            
            # Add annotations based on user preference
            for i, (value, percentage) in enumerate(zip(frequencies, percentages)):
                annotation_text = f'{percentage:.1f}%' if st.session_state.show_percentage else f'{value:,}'
                fig.add_annotation(
                    x=i,
                    y=value,
                    text=annotation_text,
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
            bargap=0.2,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        # Add grid lines for better readability
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
        
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
    
    def func():
        pass