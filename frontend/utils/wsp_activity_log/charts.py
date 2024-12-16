import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from frontend.utils.wsp_activity_log.annotate_metadata import annotate_metadata as addFig
def charts():
    
    st.subheader("FILL ↔ VENT Charts", divider="gray")
    fill_vent_events = st.session_state.data_handler.fill_vent_events

    charts = []
    for i in range(1, 5):
        key = f'FILL_{i}_VENT_{i}'
        events = fill_vent_events.get(key, [])
        if not events:
            continue
        vent_counts = [event['vent_transition_count'] for event in events]
        fill_instances = [j + 1 for j in range(len(events))]

        df = pd.DataFrame({
            'Fill Instance': fill_instances,
            'Vent Count': vent_counts
        })

        # Define color gradient from green to red (pastel colors)
        max_count = max(vent_counts) if vent_counts else 1
        min_count = min(vent_counts) if vent_counts else 0
        colors = ['#8FBC8F', '#F0E68C', '#FA8072']  # Pastel green to red
        color_scale = [
            colors[int((vc - min_count) / (max_count - min_count) * (len(colors) - 1)) if max_count > min_count else 0]
            for vc in vent_counts
        ]

        # Transform zero values to 0.01 for display while keeping original data
        display_vent_counts = [0.01 if x == 0 else x for x in vent_counts]

        fig = go.Figure(go.Bar(
            x=display_vent_counts,
            y=fill_instances,
            orientation='h',
            text=vent_counts,  # Show original values in text
            textposition='auto',
            textfont=dict(size=18),  # Increase text font size
            marker=dict(color=color_scale),
            hovertemplate='Fill Instance: %{y}<br>Vent Count: %{x}<extra></extra>'
        ))
        fig.update_layout(
            # title=f'{key}',
            xaxis_title='Vent Count',
            yaxis_title='Fill Instance',
            yaxis=dict(autorange='reversed'),
            height=350,
            # margin=dict(l=50, r=50, t=50, b=50),
        )
        addFig(fig,0.9,-0.2,0.13,0.13,"left","bottom",0,-0.15,key,"left","top",16,"black",50,50,50,50)
        charts.append(fig)

    if charts:
        cols = st.columns(2)
        for idx, fig in enumerate(charts):
            with cols[idx % 2]:
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No FILL/VENT charts to display.")