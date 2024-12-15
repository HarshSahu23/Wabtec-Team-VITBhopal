from datetime import datetime
from frontend.compute.visualizations import get_color
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
logo_path = "wabtec-logo-red.png"
wabtec_logo = Image.open(logo_path)

# Responsible for creating the bar charts in the summary tab
# Default mode, grouped by error_type, subdivision is the various axles
def create_clubbed_horizontal_bar_chart(df,table_name,random_offset, swap_axes=False) -> go.Figure:
    """Create a clubbed bar chart with optional axis swapping."""
    value_columns = df.columns[1:]
    colors = [get_color(random_offset + i) for i in range(len(value_columns))]

    if swap_axes:
        # Swap X and Y axes
        fig = go.Figure()
        for idx, col in enumerate(value_columns):
            values = df[col].replace(0, 0.1)
            fig.add_trace(go.Bar(
                x=df['Description'],  # Swapped Y -> X
                y=values,
                name=col,
                orientation='v',  # Changed orientation from 'h' to 'v'
                marker_color=colors[idx],
                hovertemplate='<b>%{x}</b><br><b>' + col + ':</b> %{text}<extra></extra>',
                width=0.15,  # Reduced from 0.2
                text=df[col].astype(str)+'    ',
                textfont=dict(size=16)  # Increased font size
            ))

        fig.update_layout(
            barmode='group',
            bargap=0.4,
            bargroupgap=0,  # Added to reduce space between groups
            xaxis_title='Error Group',  # Swapped axes titles
            yaxis_title='Values',
            plot_bgcolor='white',
            xaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            ),
            showlegend=True,
            margin=dict(t=50, l=50, r=50, b=00),
            height=600,
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )
    else:
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
                width=0.15,  # Reduced from 0.2
                text=df[col].astype(str)+'    ',
                textfont=dict(size=16)  # Increased font size
            ))

        fig.update_layout(
            barmode='group',
            bargap=0.4,
            bargroupgap=0,  # Added to reduce space between groups
            xaxis_title='Values',
            yaxis_title='Error Group',
            plot_bgcolor='white',
            xaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            ),
            showlegend=True,
            margin=dict(t=50, l=50, r=50, b=00),
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
            x=-0.01,
            y=1.15,
            sizex=0.15,
            sizey=0.15,
            xanchor="right",
            yanchor="top",
            layer="above",
        )
    )
    # Add the title of the chart
    fig.add_annotation(
        x=0,
        y=-0.18,
        xref='paper',
        yref='paper',
        text=f"<b>{table_name}</b>",
        showarrow=False,
        xanchor='left',
        yanchor='bottom',
        font=dict(size=18, color='black')
    )
    # Update layout to accommodate the header and footer
    fig.update_layout(margin=dict(t=100, l=50, r=50, b=100))

    return fig

# Bar chart in toggled mode, grouped by axle type, subdivision is the error types. 
def create_axle_grouped_bar_chart(df, table_name, random_offset, swap_axes=False) -> go.Figure:
    """Create a bar chart grouped by axles with optional axis swapping."""
    axle_columns = [col for col in df.columns if col.startswith('Axle')]
    colors = [get_color(random_offset + i) for i in range(len(df))]
    
    max_description_length = df['Description'].str.len().max()
    delta_scale = 0.015
    delta = max_description_length * delta_scale

    if swap_axes:
        # Swap X and Y axes
        fig = go.Figure()
        for idx, row in df.iterrows():
            values = [row[col] for col in axle_columns]
            values_render = [0.05 if v == 0 else v for v in values]
            fig.add_trace(go.Bar(
                x=axle_columns,  # Swapped Y -> X
                y=values_render,
                name=row['Description'],
                marker_color=colors[idx],
                orientation='v',  # Changed orientation from 'h' to 'v'
                hovertemplate='<b>%{x}</b><br>' +  # Swapped: y -> x
                             '<b>Error:</b> ' + row['Description'] + '<br>' +
                             '<b>Value:</b> %{text}<extra></extra>',
                width=0.25,
                text=values,
                textposition='auto'
            ))

        fig.update_layout(
            barmode='group',
            bargap=0.25,
            bargroupgap=0,
            xaxis_title='Axles',  # Swapped axes titles
            yaxis_title='Values',
            plot_bgcolor='white',
            xaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            ),
            showlegend=True,
            margin=dict(t=50, l=150, r=50, b=50),  # Increased left margin for axle labels
            height=600,
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )
    else:
        fig = go.Figure()
        for idx, row in df.iterrows():
            values = [row[col] for col in axle_columns]
            values_render = [0.05 if v == 0 else v for v in values]
            
            fig.add_trace(go.Bar(
                y=axle_columns,  # Swapped: x -> y
                x=values_render,  # Swapped: y -> x
                name=row['Description'],
                marker_color=colors[idx],
                orientation='h',  # Added horizontal orientation
                hovertemplate='<b>%{y}</b><br>' +  # Swapped: x -> y
                             '<b>Error:</b> ' + row['Description'] + '<br>' +
                             '<b>Value:</b> %{text}<extra></extra>',
                width=0.25,
                text=values,
                textposition='auto'
            ))

        fig.update_layout(
            barmode='group',
            bargap=0.25,
            bargroupgap=0,
            yaxis_title='Axles',  # Swapped: x -> y
            xaxis_title='Values',  # Swapped: y -> x
            plot_bgcolor='white',
            xaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            ),
            showlegend=True,
            margin=dict(t=50, l=150, r=50, b=50),  # Increased left margin for axle labels
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

    # Add wabtec logo
    fig.add_layout_image(
        dict(
            source=wabtec_logo,
            xref="paper",
            yref="paper",
            x=-0.01,
            y=1.15,
            sizex=0.15,
            sizey=0.15,
            xanchor="right",
            yanchor="top",
            layer="above",
        )
    )
    

    fig.add_annotation(
        x=0,
        y=-0.18,
        xref='paper',
        yref='paper',
        text=f"<b>{table_name}</b>",
        showarrow=False,
        xanchor='left',
        yanchor='bottom',
        font=dict(size=18, color='black')
    )
    
    fig.update_layout(margin=dict(t=100, l=150, r=50, b=100))  # Adjusted left margin again
    return fig

def create_simple_bar_chart(df, table_name, random_offset, swap_axes=False) -> go.Figure:
    """Create a simple bar chart with optional axis swapping."""
    if swap_axes:
        # Swap X and Y axes
        fig = go.Figure()
        values = df.iloc[:, 1].replace(0, 0.1)
        fig.add_trace(go.Bar(
            x=df['Description'],  # Swapped Y -> X
            y=values,
            orientation='v',  # Changed orientation from 'h' to 'v'
            marker_color=get_color(random_offset),
            hovertemplate='<b>%{x}</b><br>Value: %{text}<extra></extra>',
            text=df.iloc[:, 1].astype(str)+'    ',  # Convert values to string
            textfont=dict(size=16)
        ))

        fig.update_layout(
            xaxis_title='Error Group',  # Swapped axes titles
            yaxis_title='Values',
            plot_bgcolor='white',
            xaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            ),
            showlegend=False,
            margin=dict(t=50, l=50, r=50, b=0),
            height=600,
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            ),
            # bargap=0.1  # Reduced gap between bars #doesn't works
            bargroupgap=0
        )
    else:
        fig = go.Figure()
    
        values = df.iloc[:, 1]  # Second column contains values
        values = values.replace(0, 0.1)
        
        fig.add_trace(go.Bar(
            y=df['Description'],
            x=values,
            orientation='h',
            marker_color=get_color(random_offset),
            hovertemplate='<b>%{y}</b><br>Value: %{text}<extra></extra>',
            text=df.iloc[:, 1].astype(str)+'    ',  # Convert values to string
            textfont=dict(size=16)
        ))

        fig.update_layout(
            xaxis_title='Values',
            yaxis_title='Error Group',
            plot_bgcolor='white',
            xaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            ),
            showlegend=False,
            margin=dict(t=50, l=50, r=50, b=0),
            height=600,
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            ),
            # bargap=0.1  # Reduced gap between bars #doesn't works
            bargroupgap=0
        )

    # Add header annotations
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

    # Add wabtec logo
    fig.add_layout_image(
        dict(
            source=wabtec_logo,
            xref="paper",
            yref="paper",
            x=-0.01,
            y=1.15,
            sizex=0.15,
            sizey=0.15,
            xanchor="right",
            yanchor="top",
            layer="above",
        )
    )

    # Add title
    fig.add_annotation(
        x=0,
        y=-0.18,
        xref='paper',
        yref='paper',
        text=f"<b>{table_name}</b>",
        showarrow=False,
        xanchor='left',
        yanchor='bottom',
        font=dict(size=18, color='black')
    )

    fig.update_layout(margin=dict(t=100, l=50, r=50, b=100))
    return fig