import streamlit as st
import plotly.graph_objects as go
def time_series():
    st.subheader("FILL ↔ VENT Time Series", divider="gray")
    
    fill_vent_events = st.session_state.data_handler.fill_vent_events
    
    # Prepare data for time series
    time_series_data = []
    
    if fill_vent_events:
        # Process each FILL/VENT pair
        for i in range(1, 5):
            key = f'FILL_{i}_VENT_{i}'
            events = fill_vent_events.get(key, [])
            if not events:
                continue
                
            # Calculate timeline positions with duration scaling
            timeline_pos = 0
            time_positions = []
            event_durations = []
            vent_counts = []
            
            # Duration scaling factor (adjust as needed)
            DURATION_SCALE = 1.35
            
            # Process each event
            for event in events:
                duration = event['end_time'] - event['start_time']
                scaled_duration = duration * DURATION_SCALE
                
                time_positions.append(timeline_pos)
                event_durations.append(scaled_duration)
                vent_counts.append(event['vent_transition_count'])
                
                # Increment timeline position by base spacing + scaled duration
                timeline_pos += 1 + scaled_duration
            
            # Create color gradient based on event sequence
            num_points = len(events)
            colors = [
                f'rgb({int(255*idx/(num_points-1))}, 0, {int(255*(1-idx/(num_points-1)))})'
                for idx in range(num_points)
            ] if num_points > 1 else ['rgb(0, 0, 255)']
            
            fig_series = go.Scatter(
                x=time_positions,
                y=vent_counts,
                mode='lines+markers',
                name=key,
                line=dict(
                    shape='spline',
                    smoothing=0.5,
                    width=2,
                    
                    # Apply color gradient by setting individual segment colors
                ),
                marker=dict(
                    size=10,
                    color=colors,
                    line=dict(width=1, color='white')
                ),
                hovertemplate=(
                    'Event Duration: %{text:.2f}s<br>' +
                    'Vent Count: %{y}<extra></extra>'
                ),
                text=event_durations  # Add duration to hover text
            )
            time_series_data.append(fig_series)
        
        if time_series_data:
            fig = go.Figure(data=time_series_data)
            fig.update_layout(
                title='FILL/VENT Events Timeline (Event-spaced)',
                xaxis_title='Event Sequence (with scaled durations)',
                yaxis_title='Vent Transition Count',
                height=400,
                showlegend=True,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No time series data to display.")


