import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from frontend.utils.wsp_activity_log.annotate_metadata import annotate_metadata as addToFig

def summary():
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
                text=freq_summary.values,  
                textposition='outside',  # Position the text outside for better visibility
                texttemplate='<b>%{y:,.0f}</b>',  # Format the text to show whole numbers and make it bold
                hovertemplate='<b>Column:</b> %{x}<br>' +
                             '<b>Total Events:</b> %{y:,.0f}<extra></extra>',
            ))
            fig.update_layout(
                font=dict(size=18)  # Increase font size
            )
            
            fig.update_layout(
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
            # Annotates metadata to the figure - Logo,Folder,ChartTitle
            addToFig(fig,0.95,-0.07,0.15,0.15,"right","top",0,1.15,"Event Frequency Distribution","left","bottom",20,'black',0,0,0,0)
            st.plotly_chart(fig, use_container_width=False)
        else:
            st.info("No frequency data available")
    
    with col2:
        st.subheader("Summary Statistics")
        if not freq_summary.empty:
            total_events, max_events, avg_events = (
                freq_summary.sum(),
                freq_summary.max(),
                freq_summary.mean(),
            )

            # --- Custom Metric Implementation (Modified) ---
            st.markdown(
                """
                <style>
                .metric-container-wsp {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 20px;
                }
                .metric-box-wsp {
                    border: 2px solid #70a8db;
                    padding: 5px;
                    border-radius: 5px;
                    text-align: center;
                    width: 30%; /* Adjust width as needed */
                    display: flex; /* Use flexbox within each metric box */
                    align-items: center; /* Vertically center label and value */
                    justify-content: center; /* Horizontally center label and value */
                }
                .metric-label-wsp {
                    font-size: 16px; /* Smaller font size for label */
                    font-weight: bold;
                    margin-right: 5px; /* Add some space between label and value */
                }
                .metric-value-wsp {
                    font-size: 18px; /* Smaller font size for value */
                    color: #2E75B6; /* Example color, adjust as desired */
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="metric-container-wsp">
                    <div class="metric-box-wsp">
                        <span class="metric-label-wsp">Total :</span>
                        <span class="metric-value-wsp">{total_events:,.0f}</span>
                    </div>
                    <div class="metric-box-wsp">
                        <span class="metric-label-wsp">Max :</span>
                        <span class="metric-value-wsp">{max_events:,.0f}</span>
                    </div>
                    <div class="metric-box-wsp">
                        <span class="metric-label-wsp">Average :</span>
                        <span class="metric-value-wsp">{avg_events:.1f}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # --- Pie Chart ---
            fig_pie = px.pie(
                values=freq_summary.values,
                names=freq_summary.index,
            )
            logox,logoy = 1,0.1
            pie_chart_title="FILL/VENT Event Distribution"
            fig_pie.update_traces(textposition="inside", textinfo="percent+label")
            # Annotates metadata to the figure - Logo,Folder,ChartTitle
            addToFig(fig_pie,logox,logoy,0.2,0.2,"right","top",0.1,-0.05,pie_chart_title,"left","top",16,'black',50,50,30,30)
            fig_pie.update_layout(height=410, width=400)  # Set chart dimensions

            st.plotly_chart(fig_pie, use_container_width=True)

            # --- Toggle to Change Annotation ---
            # TODO:
            # Add a button/toggle/checkbox that 
            # switches the pie_chart label from percent to actual value

    
    # Ensure both columns end at the same bottom line
    st.write("")  # Add an empty element to balance the columns
    st.write("")  # Add another empty element if needed