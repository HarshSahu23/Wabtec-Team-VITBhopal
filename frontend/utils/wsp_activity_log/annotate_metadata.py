from PIL import Image
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

logo_path = "wabtec-logo-red.png"
wabtec_logo = Image.open(logo_path)

def annotate_metadata(fig: go.Figure, logo_x: float, logo_y: float, logo_sizex: float, logo_sizey: float, logo_xanchor: str, logo_yanchor: str, title_x: float, title_y: float, title_text:str, title_xanchor: str, title_yanchor: str,title_fontsize:int, title_color:str,top:int,bottom:int,left:int,right:int) -> go.Figure:
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
            x=logo_x,
            y=logo_y,
            sizex=logo_sizex,
            sizey=logo_sizey,
            xanchor=logo_xanchor,
            yanchor=logo_yanchor,
            layer="above",
        )
    )

    # Add graph title
    fig.add_annotation(
        x=title_x,
        y=title_y,
        xref='paper',
        yref='paper',
        text=f"<b>{title_text}</b>",
        showarrow=False,
        xanchor=title_xanchor,
        yanchor=title_yanchor,
        font=dict(size=title_fontsize, color=title_color)
    )
    

    # Add margins to the plot
    fig.update_layout(margin=dict(t=top or 0, l=left or 0, r=right or 0, b=bottom or 0))
    return fig
    