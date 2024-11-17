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

    # [Rest of the class implementation remains the same]