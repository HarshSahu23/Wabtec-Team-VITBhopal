import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from frontend.utils.render_section_header import render_section_header

def render_dump_log():
    render_section_header(
        "Dump Log Analysis",
        "Review and analyze system dump logs for critical events and patterns.",
        "📊"
    )
    
    if not st.session_state.data_handler or st.session_state.data_handler.dmp.empty:
        st.warning("Please upload DMP log files to begin analysis")
        return

    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Frequency Analysis")
        
        # Get the frequency summary data
        freq_summary = st.session_state.data_handler.dmp_freq_summary
        
        if not freq_summary.empty:
            # Create bar chart using Plotly
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=freq_summary.index,
                y=freq_summary.values,
                marker_color='rgba(58, 71, 180, 0.6)',
                hovertemplate='<b>Column:</b> %{x}<br>' +
                             '<b>Total Events:</b> %{y:,.0f}<extra></extra>'
            ))
            
            fig.update_layout(
                title="Event Frequency Distribution",
                xaxis_title="Event Type",
                yaxis_title="Frequency",
                xaxis_tickangle=-45,
                height=500,
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            
            # Add grid lines
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No frequency data available")
    
    with col2:
        st.subheader("Summary Statistics")
        
        if not freq_summary.empty:
            total_events, max_events, avg_events = freq_summary.sum(), freq_summary.max(), freq_summary.mean()
            
            # Create metrics
            c1, c2, c3 = st.columns(3); c1.metric("Total Events", f"{total_events:,.0f}"); c2.metric("Maximum Events", f"{max_events:,.0f}"); c3.metric("Average Events", f"{avg_events:.1f}")
            
            # Add a pie chart for distribution
            fig_pie = px.pie(
                values=freq_summary.values,
                names=freq_summary.index,
                title="Event Distribution"
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # Filtered Data Table Section
    st.subheader("Detailed Event Log")
    
    filtered_dmp = st.session_state.data_handler.filtered_dmp
    
    if not filtered_dmp.empty:
        # # Add search functionality
        # search = st.text_input("Search events", "")
        
        # # Filter based on search
        # if search:
        #     mask = filtered_dmp.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        #     filtered_dmp = filtered_dmp[mask]
        
        # Add column selector
        selected_columns = st.multiselect(
            "Select columns to display",
            options=filtered_dmp.columns.tolist(),
            default=filtered_dmp.columns.tolist()
        )
        
        # Show filtered data
        st.dataframe(filtered_dmp[selected_columns], height=400)
        
        # Add download button
        csv = filtered_dmp.to_csv(index=False)
        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name="filtered_dump_log.csv",
            mime="text/csv"
        )
        
        # Add summary statistics for filtered data
        st.subheader("Filtered Data Statistics")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.write("Numerical Columns Statistics")
            st.dataframe(filtered_dmp.describe())
            
        with col4:
            st.write("Non-Zero Events Count")
            non_zero_counts = (filtered_dmp != 0).sum()
            st.dataframe(pd.DataFrame({
                'Column': non_zero_counts.index,
                'Non-Zero Count': non_zero_counts.values
            }))
            
    else:
        st.info("No filtered data available")
    
    # Add additional analysis options
    with st.expander("Advanced Analysis Options"):
        st.write("Time Series Analysis")
        if 'Time' in filtered_dmp.columns:
            selected_column = st.selectbox(
                "Select column for time series analysis",
                options=[col for col in filtered_dmp.columns if col != 'Time']
            )
            
            # Create time series plot
            fig_time = go.Figure()
            fig_time.add_trace(go.Scatter(
                x=filtered_dmp['Time'],
                y=filtered_dmp[selected_column],
                mode='lines+markers',
                name=selected_column
            ))
            
            fig_time.update_layout(
                title=f"Time Series Analysis: {selected_column}",
                xaxis_title="Time",
                yaxis_title="Value",
                height=400
            )
            
            st.plotly_chart(fig_time, use_container_width=True)