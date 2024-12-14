from datetime import datetime
from frontend.compute.visualizations import get_color
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
logo_path = "wabtec-logo-red.png"
wabtec_logo = Image.open(logo_path)

# Responsible for creating the bar charts in the summary tab
def create_clubbed_horizontal_bar_chart(df,random_offset) -> go.Figure:
    """Create a clubbed horizontal bar chart from the dataframe."""
    value_columns = df.columns[1:]
    colors = [get_color(random_offset + i) for i in range(len(value_columns))]

    fig = go.Figure()
    for idx, col in enumerate(value_columns):
        values = df[col]
        values = values.replace(0, 0.1)
        fig.add_trace(go.Bar(
            y=df['Description'],
            x=values,
            name=col,
            orientation='h',
            marker_color=colors[idx],
            hovertemplate='<b>%{y}</b><br><b>' + col + ':</b> %{text}<extra></extra>',
            width=0.2,
            text=df[col]
        ))

    fig.update_layout(
        barmode='group',
        bargap=0,
        xaxis_title='Values',
        yaxis_title='Error Group',
        plot_bgcolor='white',
        showlegend=True,
        margin=dict(t=50, l=50, r=50, b=50),
        height=600,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    # Calculate the maximum length of strings in the 'Description' column
    max_description_length = df['Description'].str.len().max()
    
    # Define the scaling factor for delta (adjust as needed)
    delta_scale = 0.015

    # Calculate the delta based on the maximum length
    delta = max_description_length * delta_scale

    # Add annotations for header information
    annotations = [
        {"label": "Depot Name:", "value": st.session_state.depot_name},
        {"label": "Coach Num:", "value": st.session_state.coach_name},
        {"label": "Analysis Time:", "value": datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}
    ]

    for i, anno in enumerate(annotations):
        # Add label (title)
        fig.add_annotation(
            x=0.33 * i ,
            y=1.1,
            xref='paper',
            yref='paper',
            text=anno["label"],
            showarrow=False,
            xanchor='left',
            yanchor='bottom',
            font=dict(size=14, color='grey')
        )
        # Add value
        fig.add_annotation(
            x=0.33 * i ,
            y=1.05,
            xref='paper',
            yref='paper',
            text=anno["value"],
            showarrow=False,
            xanchor='left',
            yanchor='bottom',
            font=dict(size=14, color='indigo')
        )
    # Add wabtec logo
    fig.add_layout_image(
        dict(
            source=wabtec_logo,
            xref="paper",
            yref="paper",
            x=-0.1*delta,
            y=1.15,
            sizex=0.2,
            sizey=0.2,
            xanchor="right",
            yanchor="top",
            layer="above",
        )
    )
    # Update layout to accommodate the header
    fig.update_layout(margin=dict(t=100, l=50, r=50, b=50))

    return fig

def create_axle_grouped_bar_chart(df, random_offset) -> go.Figure:
    """Create a bar chart grouped by axles from the dataframe."""
    axle_columns = [col for col in df.columns if col.startswith('Axle')]
    colors = [get_color(random_offset + i) for i in range(len(df))]
    
    max_description_length = df['Description'].str.len().max()
    delta_scale = 0.015
    delta = max_description_length * delta_scale

    fig = go.Figure()
    for idx, row in df.iterrows():
        values = [row[col] for col in axle_columns]
        values_render = [0.05 if v == 0 else v for v in values]
        
        # Modified hover template to show description for each bar
        fig.add_trace(go.Bar(
            x=axle_columns,
            y=values_render,
            name=row['Description'],
            marker_color=colors[idx],
            hovertemplate='<b>%{x}</b><br>' + 
                         '<b>Error:</b> ' + row['Description'] + '<br>' +
                         '<b>Value:</b> %{text}<extra></extra>',
            width=0.2,
            text=values,
            textposition='auto'  # Show values on bars
        ))

    fig.update_layout(
        barmode='group',
        bargap=0,
        xaxis_title='Axles',
        yaxis_title='Values',
        plot_bgcolor='white',
        showlegend=True,
        margin=dict(t=50, l=50, r=50, b=50),
        height=600,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )

    annotations = [
        {"label": "Depot Name:", "value": st.session_state.depot_name},
        {"label": "Coach Num:", "value": st.session_state.coach_name},
        {"label": "Analysis Time:", "value": datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}
    ]

    for i, anno in enumerate(annotations):
        fig.add_annotation(
            x=0.33 * i,
            y=1.1,
            xref='paper',
            yref='paper',
            text=anno["label"],
            showarrow=False,
            xanchor='left',
            yanchor='bottom',
            font=dict(size=14, color='grey')
        )
        fig.add_annotation(
            x=0.33 * i,
            y=1.05,
            xref='paper',
            yref='paper',
            text=anno["value"],
            showarrow=False,
            xanchor='left',
            yanchor='bottom',
            font=dict(size=14, color='indigo')
        )

    fig.add_layout_image(
        dict(
            source=wabtec_logo,
            xref="paper",
            yref="paper",
            x=1 + delta/10,
            y=1.15,
            sizex=0.2,
            sizey=0.2,
            xanchor="left",
            yanchor="top",
            layer="above"
        )
    )
    
    fig.update_layout(margin=dict(t=100, l=50, r=50, b=50))
    return fig