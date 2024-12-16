import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from frontend.utils.render_section_header import render_section_header
from frontend.utils.wsp_activity_log.summary import summary
from frontend.utils.wsp_activity_log.detailed_analysis import detailed_analysis
from frontend.utils.wsp_activity_log.time_series import time_series
from frontend.utils.wsp_activity_log.charts import charts
from frontend.utils.wsp_activity_log.analysis import analysis


def render_dump_log():
    render_section_header(
        "Dump Log Analysis",
        "Review and analyze system dump logs for critical events and patterns.",
        "📊"
    )
    
    if not st.session_state.data_handler or st.session_state.data_handler.dmp.empty:
        st.warning("Please upload DMP log files to begin analysis")
        return

    summary()

    
    # FILL/VENT Analysis 
    analysis()    
    
    # FILL/VENT Charts begin
    charts()
    
    # Time series visualization
    time_series()
    
    # Add additional analysis options
    with st.expander("Advanced Analysis Options"):
        # Filtered Data Table Section
        detailed_analysis()